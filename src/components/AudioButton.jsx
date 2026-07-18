import { forwardRef, useCallback, useEffect, useRef, useState } from 'react'
import {
  getCachedAudio,
  isTTSSupported,
  isUnavailable,
  markTTSSupported,
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

function speakWithSpeechSynthesis(word) {
  return new Promise((resolve, reject) => {
    if (typeof window === 'undefined' || !('speechSynthesis' in window)) {
      reject(new Error('SpeechSynthesis not available'))
      return
    }
    const synth = window.speechSynthesis
    try {
      synth.cancel()
    } catch {
      // ignore cancel errors
    }

    const utterance = new SpeechSynthesisUtterance(word)
    utterance.lang = 'en-US'
    utterance.rate = 0.9
    utterance.pitch = 1

    let settled = false
    const settle = (fn, value) => {
      if (settled) return
      settled = true
      fn(value)
    }

    utterance.onend = () => settle(resolve)
    utterance.onerror = (e) => settle(reject, new Error(e?.error || 'TTS error'))

    try {
      synth.speak(utterance)
    } catch (err) {
      settle(reject, err)
    }
  })
}

export default forwardRef(function AudioButton({ word, onResolved }, ref) {
  const audioRef = useRef(null)
  const isMountedRef = useRef(true)
  const ttsActiveRef = useRef(false)
  const [state, setState] = useState(() => {
    if (!word) return 'unavailable'
    if (isUnavailable(word)) return 'unavailable'
    return 'idle'
  })

  const reportResolution = useCallback(() => {
    if (!word || !onResolved) return
    const cached = getCachedAudio(word)
    if (cached) onResolved({ audio_url: cached, audio_source: 'dictionaryapi.dev' })
    else if (isUnavailable(word)) onResolved({ audio_url: null, audio_source: 'none' })
    else if (isTTSSupported(word)) onResolved({ audio_url: null, audio_source: 'tts' })
    else onResolved(null)
  }, [word, onResolved])

  // Eager resolution on mount: fires onResolved as soon as audio state
  // is known (cache hit, known unsupported, known TTS-only) OR after
  // a one-shot fetch from dictionaryapi.dev. Without this, onResolved
  // never fires until the user clicks the button, and VerbCard's
  // `onEnriched` (which triggers the MongoDB lazy sync) stays idle.
  useEffect(() => {
    if (!word || !onResolved) return

    console.info('[audio-eager] mount word=', word)
    let cancelled = false
    const fire = (info) => {
      if (cancelled) return
      if (info) onResolved(info)
    }

    const cached = getCachedAudio(word)
    if (cached) {
      console.info('[audio-eager] cache hit for', word)
      fire({ audio_url: cached, audio_source: 'dictionaryapi.dev' })
      return
    }
    if (isUnavailable(word)) {
      console.info('[audio-eager] known unavailable for', word)
      fire({ audio_url: null, audio_source: 'none' })
      return
    }
    if (isTTSSupported(word)) {
      console.info('[audio-eager] known tts for', word)
      fire({ audio_url: null, audio_source: 'tts' })
      return
    }

    console.info('[audio-eager] fetching dictionaryapi for', word)
    fetchAudioUrl(word)
      .then(({ url, reason }) => {
        if (cancelled) return
        console.info('[audio-eager] dict result', word, { url, reason })
        if (url) {
          setCachedAudio(word, url)
          fire({ audio_url: url, audio_source: 'dictionaryapi.dev' })
        } else if (reason === 'no-audio') {
          markTTSSupported(word)
          fire({ audio_url: null, audio_source: 'tts' })
        } else if (reason === 'missing') {
          setUnavailable(word)
          fire({ audio_url: null, audio_source: 'none' })
        }
      })
      .catch((err) => {
        console.warn('[audio-eager] fetch failed for', word, err?.message ?? err)
      })

    return () => {
      cancelled = true
    }
  }, [word, onResolved])

  useEffect(() => {
    isMountedRef.current = true
    return () => {
      isMountedRef.current = false
      const audio = audioRef.current
      if (audio) {
        audio.pause()
        audio.removeAttribute('src')
      }
      if (ttsActiveRef.current && typeof window !== 'undefined' && 'speechSynthesis' in window) {
        try {
          window.speechSynthesis.cancel()
        } catch {
          // ignore
        }
      }
    }
  }, [])

  const stopPlayback = useCallback(() => {
    const audio = audioRef.current
    if (audio) {
      audio.pause()
      audio.currentTime = 0
    }
    if (ttsActiveRef.current && typeof window !== 'undefined' && 'speechSynthesis' in window) {
      try {
        window.speechSynthesis.cancel()
      } catch {
        // ignore
      }
    }
    ttsActiveRef.current = false
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
      audioRef.current = a
    }
    const audio = audioRef.current
    audio.src = url
    audio.currentTime = 0
    const p = audio.play()
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

  const playTTS = useCallback(async () => {
    setState('playing')
    ttsActiveRef.current = true
    try {
      await speakWithSpeechSynthesis(word)
      if (isMountedRef.current) {
        ttsActiveRef.current = false
        setState('idle')
      }
    } catch {
      if (isMountedRef.current) {
        ttsActiveRef.current = false
        setState('error')
      }
    }
  }, [word])

  const handleClick = useCallback(async () => {
    if (!word) return

    if (state === 'playing') {
      stopPlayback()
      setState('idle')
      return
    }
    if (state === 'loading') return
    if (state === 'unavailable') return

    const cached = getCachedAudio(word)
    if (cached) {
      playUrl(cached)
      reportResolution()
      return
    }

    if (isTTSSupported(word)) {
      playTTS()
      reportResolution()
      return
    }

    setState('loading')
    try {
      const { url, reason } = await fetchAudioUrl(word)
      if (!isMountedRef.current) {
        if (url) setCachedAudio(word, url)
        else if (reason === 'missing') setUnavailable(word)
        else if (reason === 'no-audio') markTTSSupported(word)
        return
      }

      if (url) {
        setCachedAudio(word, url)
        playUrl(url)
        reportResolution()
        return
      }

      if (reason === 'no-audio') {
        try {
          await speakWithSpeechSynthesis(word)
          markTTSSupported(word)
          if (isMountedRef.current) setState('idle')
          reportResolution()
        } catch {
          setUnavailable(word)
          if (isMountedRef.current) setState('unavailable')
          reportResolution()
        }
        return
      }

      if (reason === 'missing') {
        setUnavailable(word)
        setState('unavailable')
        reportResolution()
      }
    } catch {
      if (isMountedRef.current) setState('error')
    }
  }, [word, state, playUrl, playTTS, stopPlayback, reportResolution])

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
      ref={ref}
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
})