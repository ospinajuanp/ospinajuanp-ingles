import { useCallback, useEffect, useRef, useState } from 'react'
import {
  getCachedAudio,
  isUnavailable,
  setCachedAudio,
  setUnavailable,
} from '../utils/audioCache'

const API_BASE = 'https://api.dictionaryapi.dev/api/v2/entries/en/'

function pickFirstAudio(entry) {
  const phonetics = entry?.phonetics
  if (!Array.isArray(phonetics)) return null
  for (const p of phonetics) {
    if (p?.audio) return p.audio
  }
  return null
}

async function fetchAudioUrl(word) {
  const res = await fetch(`${API_BASE}${encodeURIComponent(word)}`)
  if (!res.ok) {
    if (res.status === 404) return { url: null, reason: 'missing' }
    throw new Error(`HTTP ${res.status}`)
  }
  const data = await res.json()
  const entry = Array.isArray(data) ? data[0] : null
  const url = pickFirstAudio(entry)
  return { url, reason: url ? null : 'no-audio' }
}

export default function AudioButton({ word }) {
  const audioRef = useRef(null)
  const isMountedRef = useRef(true)
  const [state, setState] = useState(() => {
    if (!word) return 'unavailable'
    if (isUnavailable(word)) return 'unavailable'
    return 'idle'
  })

  useEffect(() => {
    isMountedRef.current = true
    return () => {
      isMountedRef.current = false
      const audio = audioRef.current
      if (audio) {
        audio.pause()
        audio.removeAttribute('src')
      }
    }
  }, [])

  const playUrl = useCallback((url) => {
    if (!url) return
    if (!audioRef.current) {
      const a = new Audio()
      a.preload = 'none'
      a.onended = () => {
        if (isMountedRef.current) setState('idle')
      }
      a.onerror = () => {
        if (isMountedRef.current) setState('error')
      }
      // eslint-disable-next-line react-hooks/immutability
      audioRef.current = a
      a.src = url
      a.currentTime = 0
      const p = a.play()
      if (p && typeof p.then === 'function') {
        p.then(() => {
          if (isMountedRef.current) setState('playing')
        }).catch(() => {
          if (isMountedRef.current) setState('error')
        })
      } else {
        setState('playing')
      }
      return
    }
    audioRef.current.src = url
    audioRef.current.currentTime = 0
    const p = audioRef.current.play()
    if (p && typeof p.then === 'function') {
      p.then(() => {
        if (isMountedRef.current) setState('playing')
      }).catch(() => {
        if (isMountedRef.current) setState('error')
      })
    } else {
      setState('playing')
    }
  }, [])

  const handleClick = useCallback(async () => {
    if (!word) return

    if (state === 'playing') {
      audioRef.current?.pause()
      setState('idle')
      return
    }
    if (state === 'loading') return
    if (state === 'unavailable') return

    const cached = getCachedAudio(word)
    if (cached) {
      playUrl(cached)
      return
    }

    setState('loading')
    try {
      const { url, reason } = await fetchAudioUrl(word)
      if (!isMountedRef.current) {
        if (url) setCachedAudio(word, url)
        else if (reason) setUnavailable(word)
        return
      }
      if (reason) {
        setUnavailable(word)
        setState('unavailable')
        return
      }
      setCachedAudio(word, url)
      playUrl(url)
    } catch {
      if (isMountedRef.current) setState('error')
    }
  }, [word, state, playUrl])

  const baseClass =
    'group/audio inline-flex size-12 items-center justify-center rounded-full bg-white/95 text-indigo-600 shadow-lg ring-1 ring-black/5 backdrop-blur-sm transition hover:scale-105 hover:bg-white hover:shadow-xl active:scale-95 disabled:opacity-50 disabled:hover:scale-100 disabled:hover:bg-white/95 motion-reduce:animate-none'

  const ariaLabel =
    state === 'unavailable'
      ? `Sin audio disponible para ${word}`
      : state === 'playing'
        ? `Pausar pronunciación de ${word}`
        : `Escuchar pronunciación de ${word}`

  let icon
  if (state === 'loading') {
    icon = (
      <svg
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        className="size-5 animate-spin motion-reduce:animate-none"
        aria-hidden="true"
      >
        <path d="M21 12a9 9 0 1 1-6.219-8.56" />
      </svg>
    )
  } else if (state === 'playing') {
    icon = (
      <svg
        viewBox="0 0 24 24"
        fill="currentColor"
        className="size-5"
        aria-hidden="true"
      >
        <rect x="6" y="5" width="4" height="14" rx="1" />
        <rect x="14" y="5" width="4" height="14" rx="1" />
      </svg>
    )
  } else if (state === 'unavailable') {
    icon = (
      <svg
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        className="size-5"
        aria-hidden="true"
      >
        <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5" />
        <line x1="23" y1="9" x2="17" y2="15" />
        <line x1="17" y1="9" x2="23" y2="15" />
      </svg>
    )
  } else if (state === 'error') {
    icon = (
      <svg
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        className="size-5"
        aria-hidden="true"
      >
        <circle cx="12" cy="12" r="10" />
        <line x1="12" y1="8" x2="12" y2="12" />
        <line x1="12" y1="16" x2="12.01" y2="16" />
      </svg>
    )
  } else {
    icon = (
      <svg
        viewBox="0 0 24 24"
        fill="currentColor"
        className="size-5 translate-x-[1px] transition group-hover/audio:scale-110"
        aria-hidden="true"
      >
        <path d="M8 5v14l11-7z" />
      </svg>
    )
  }

  return (
    <button
      type="button"
      onClick={handleClick}
      disabled={!word || state === 'unavailable' || state === 'loading'}
      aria-label={ariaLabel}
      title={
        state === 'unavailable'
          ? 'Sin pronunciación disponible'
          : state === 'error'
            ? 'Error al cargar, reintentar'
            : 'Escuchar'
      }
      className={
        baseClass +
        (state === 'playing'
          ? ' animate-pulse motion-reduce:animate-none ring-2 ring-indigo-300'
          : '')
      }
    >
      {icon}
    </button>
  )
}