// Sync modal — DaisyUI v5 <dialog> with QR, copyable token, and
// "link another device" input. All copy is in Spanish to match the
// rest of the UI; the layout uses DaisyUI primitives (`card`, `btn`,
// `input`, `badge`) so it inherits the active theme automatically.
//
// The QR is generated server-side by qrserver.com — a free public
// service with no API key. We never block on it: if the network is
// down the <img> simply fails to load and we fall back to a copyable
// URL chunk the user can paste manually into their second device.

import { useEffect, useMemo, useRef, useState } from 'react'
import {
  Copy,
  Check,
  Link2,
  RefreshCw,
  Unplug,
  X,
  Smartphone,
} from 'lucide-react'
import { useSyncContext } from '../contexts/SyncContext'
import { buildLinkUrl } from '../hooks/useSyncEngine'

const QR_API = 'https://api.qrserver.com/v1/create-qr-code/'

function formatToken(token) {
  if (!token) return ''
  // Insert a soft break every 4 chars for readability on narrow screens.
  return token.match(/.{1,4}/g)?.join(' ') ?? token
}

function StatusBadge({ status, lastError, lastSyncedAt, pending }) {
  // `now` ticks every 30s via an effect below — keeps the "hace Xs/min"
  // label fresh without calling Date.now() during render (forbidden by
  // react-hooks/purity in React 19).
  const [now, setNow] = useState(() => Date.now())
  useEffect(() => {
    if (status !== 'synced' || !lastSyncedAt) return
    const id = setInterval(() => setNow(Date.now()), 30_000)
    return () => clearInterval(id)
  }, [status, lastSyncedAt])

  const label = useMemo(() => {
    if (status === 'pulling') return 'Obteniendo…'
    if (status === 'pushing') return 'Enviando…'
    if (pending && status !== 'pushing') return 'Cambios pendientes'
    if (status === 'error') return lastError ? `Error: ${lastError}` : 'Error'
    if (status === 'synced') {
      if (lastSyncedAt) {
        const ago = Math.max(0, Math.round((now - lastSyncedAt) / 1000))
        if (ago < 5) return 'Sincronizado'
        if (ago < 60) return `Sincronizado hace ${ago}s`
        return `Sincronizado hace ${Math.round(ago / 60)} min`
      }
      return 'Sincronizado'
    }
    return 'En espera'
  }, [status, lastError, lastSyncedAt, pending, now])

  const tone =
    status === 'error'
      ? 'badge-error'
      : status === 'synced' && !pending
        ? 'badge-success'
        : 'badge-warning'

  return (
    <span
      className={`badge ${tone} badge-soft gap-2 rounded-full px-3 py-3 text-xs font-semibold normal-case`}
      role="status"
      aria-live="polite"
    >
      <span
        aria-hidden="true"
        className={`inline-block size-1.5 rounded-full ${
          status === 'error'
            ? 'bg-error'
            : status === 'synced' && !pending
              ? 'bg-success'
              : 'bg-warning animate-pulse'
        }`}
      />
      {label}
    </span>
  )
}

export default function SyncModal({ open, onClose }) {
  const sync = useSyncContext()
  const dialogRef = useRef(null)

  // DaisyUI v5 <dialog> pattern: control via .showModal() / .close().
  // We mirror `open` into the imperative API so screen readers + Esc
  // work without any extra wiring.
  useEffect(() => {
    const el = dialogRef.current
    if (!el) return
    if (open && !el.open) el.showModal()
    if (!open && el.open) el.close()
  }, [open])

  const [copied, setCopied] = useState(false)
  const [linkInput, setLinkInput] = useState('')
  const [linkError, setLinkError] = useState(null)
  const [linkSuccess, setLinkSuccess] = useState(null)
  const [prevOpen, setPrevOpen] = useState(open)

  // Reset transient UI bits on the open→true transition. Using the
  // "adjusting state during render" pattern (React docs) instead of a
  // useEffect — sidesteps `react-hooks/set-state-in-effect`.
  if (open !== prevOpen) {
    setPrevOpen(open)
    if (open) {
      setCopied(false)
      setLinkInput('')
      setLinkError(null)
      setLinkSuccess(null)
    }
  }

  const syncToken = sync?.syncToken ?? ''
  const linkUrl = useMemo(() => buildLinkUrl(syncToken), [syncToken])
  const qrSrc = useMemo(() => {
    if (!linkUrl) return null
    return `${QR_API}?size=240x240&margin=1&data=${encodeURIComponent(linkUrl)}`
  }, [linkUrl])

  async function copyToken() {
    if (!syncToken) return
    try {
      await navigator.clipboard.writeText(syncToken)
      setCopied(true)
      setTimeout(() => setCopied(false), 1500)
    } catch {
      // Clipboard blocked (e.g. insecure context). User can copy by hand.
      setCopied(false)
    }
  }

  async function copyLinkUrl() {
    if (!linkUrl) return
    try {
      await navigator.clipboard.writeText(linkUrl)
      setCopied(true)
      setTimeout(() => setCopied(false), 1500)
    } catch {
      // ignore
    }
  }

  function handleLink(e) {
    e.preventDefault()
    setLinkError(null)
    setLinkSuccess(null)
    const raw = linkInput.trim()
    if (!raw) {
      setLinkError('Pega un token primero.')
      return
    }
    // Tolerate the user pasting the full URL instead of just the token.
    let candidate = raw
    try {
      const u = new URL(raw)
      const fromUrl = u.searchParams.get('syncToken')
      if (fromUrl) candidate = fromUrl
    } catch {
      // not a URL — assume it's the bare token
    }
    const ok = sync?.linkNewToken(candidate)
    if (!ok) {
      setLinkError('Token inválido o ya vinculado a este dispositivo.')
      return
    }
    setLinkSuccess('Vinculado. Obteniendo datos del otro dispositivo…')
    setLinkInput('')
  }

  function handleUnlink() {
    if (typeof window !== 'undefined') {
      const ok = window.confirm(
        'Esto generará un nuevo token. Tu progreso local no se borra, pero este dispositivo dejará de estar sincronizado con el anterior. ¿Continuar?',
      )
      if (!ok) return
    }
    sync?.unlink()
  }

  return (
    <dialog
      ref={dialogRef}
      className="modal"
      onClose={onClose}
      aria-labelledby="sync-modal-title"
    >
      <div className="modal-box w-11/12 max-w-md rounded-3xl border border-base-300 bg-base-100 p-0 shadow-xl">
        {/* Header */}
        <header className="flex items-start justify-between gap-3 border-b border-base-300 px-5 py-4 sm:px-6">
          <div className="min-w-0">
            <h2
              id="sync-modal-title"
              className="text-lg font-bold text-base-content"
            >
              Sincronización
            </h2>
            <p className="mt-0.5 text-xs text-base-content/60">
              Multi-dispositivo sin cuenta. Identidad anónima con un token local.
            </p>
          </div>
          <button
            type="button"
            onClick={onClose}
            aria-label="Cerrar"
            className="btn btn-circle btn-ghost btn-sm shrink-0"
          >
            <X className="size-4" aria-hidden="true" />
          </button>
        </header>

        <div className="space-y-5 px-5 py-5 sm:px-6">
          {/* Status */}
          <div className="flex items-center justify-between gap-3">
            <StatusBadge
              status={sync?.status}
              lastError={sync?.lastError}
              lastSyncedAt={sync?.lastSyncedAt}
              pending={sync?.pendingPush}
            />
            <div className="flex items-center gap-1">
              <button
                type="button"
                onClick={() => sync?.forcePullNow?.()}
                aria-label="Obtener ahora"
                className="btn btn-ghost btn-xs gap-1 normal-case"
                title="Obtener datos del servidor"
              >
                <RefreshCw className="size-3.5" aria-hidden="true" />
                Obtener
              </button>
              <button
                type="button"
                onClick={() => sync?.forcePushNow?.()}
                aria-label="Enviar ahora"
                className="btn btn-ghost btn-xs gap-1 normal-case"
                title="Enviar datos al servidor"
              >
                <RefreshCw className="size-3.5" aria-hidden="true" />
                Enviar
              </button>
            </div>
          </div>

          {/* QR + Token */}
          <section className="rounded-2xl border border-base-300 bg-base-200/40 p-4">
            <div className="flex flex-col items-center gap-4 sm:flex-row">
              <div className="shrink-0">
                {qrSrc ? (
                  <img
                    src={qrSrc}
                    width="144"
                    height="144"
                    alt={`Código QR que vincula este dispositivo a la URL ${linkUrl}`}
                    className="size-36 rounded-xl border border-base-300 bg-base-100 p-2 shadow-sm"
                    loading="lazy"
                    onError={(e) => {
                      // If the QR service is blocked, swap the img for a
                      // plain "open this URL" hint so the feature still
                      // works offline / behind firewalls.
                      e.currentTarget.style.display = 'none'
                    }}
                  />
                ) : null}
              </div>

              <div className="min-w-0 flex-1 space-y-2">
                <p className="flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.16em] text-base-content/60">
                  <Smartphone className="size-3.5" aria-hidden="true" />
                  Tu token
                </p>
                <code
                  className="block select-all break-all rounded-xl border border-base-300 bg-base-100 px-3 py-2 font-mono text-xs leading-relaxed text-base-content"
                  title={syncToken}
                >
                  {formatToken(syncToken)}
                </code>
                <div className="flex flex-wrap gap-2">
                  <button
                    type="button"
                    onClick={copyToken}
                    className="btn btn-sm btn-primary gap-2 rounded-full normal-case"
                  >
                    {copied ? (
                      <>
                        <Check className="size-3.5" aria-hidden="true" />
                        Copiado
                      </>
                    ) : (
                      <>
                        <Copy className="size-3.5" aria-hidden="true" />
                        Copiar token
                      </>
                    )}
                  </button>
                  <button
                    type="button"
                    onClick={copyLinkUrl}
                    className="btn btn-sm btn-ghost gap-2 rounded-full normal-case"
                  >
                    <Link2 className="size-3.5" aria-hidden="true" />
                    Copiar link
                  </button>
                </div>
              </div>
            </div>

            <p className="mt-3 text-xs leading-relaxed text-base-content/60">
              Escanea el QR desde tu otro dispositivo o pega el token en él. Se
              abrirá esta misma página con <code>?syncToken=…</code> y tus
              tarjetas se sincronizarán solas.
            </p>
          </section>

          {/* Vincular otro dispositivo */}
          <section>
            <label
              htmlFor="sync-link-input"
              className="mb-2 block text-xs font-semibold uppercase tracking-[0.16em] text-base-content/60"
            >
              Vincular otro dispositivo
            </label>
            <form onSubmit={handleLink} className="flex flex-col gap-2 sm:flex-row">
              <input
                id="sync-link-input"
                type="text"
                inputMode="text"
                autoComplete="off"
                spellCheck={false}
                value={linkInput}
                onChange={(e) => {
                  setLinkInput(e.target.value)
                  setLinkError(null)
                  setLinkSuccess(null)
                }}
                placeholder="Pega aquí el token o la URL del otro dispositivo"
                className="input input-bordered input-sm w-full rounded-full font-mono text-xs"
                aria-invalid={!!linkError}
                aria-describedby="sync-link-msg"
              />
              <button
                type="submit"
                className="btn btn-sm btn-primary rounded-full normal-case"
              >
                Vincular
              </button>
            </form>
            <div id="sync-link-msg" className="mt-2 min-h-[1rem] text-xs">
              {linkError ? (
                <span className="text-error">{linkError}</span>
              ) : linkSuccess ? (
                <span className="text-success">{linkSuccess}</span>
              ) : (
                <span className="text-base-content/50">
                  También puedes abrir directamente
                  <code className="mx-1 rounded bg-base-200 px-1 py-0.5 text-[0.7rem]">
                    ?syncToken=…
                  </code>
                  en el otro dispositivo.
                </span>
              )}
            </div>
          </section>

          {/* Danger zone */}
          <section className="border-t border-base-300 pt-4">
            <button
              type="button"
              onClick={handleUnlink}
              className="btn btn-ghost btn-xs gap-2 normal-case text-base-content/60 hover:text-error"
            >
              <Unplug className="size-3.5" aria-hidden="true" />
              Generar token nuevo (desvincular este dispositivo)
            </button>
          </section>
        </div>
      </div>

      {/* Click-outside backdrop closes the modal */}
      <form method="dialog" className="modal-backdrop">
        <button type="submit" aria-label="Cerrar">
          cerrar
        </button>
      </form>
    </dialog>
  )
}