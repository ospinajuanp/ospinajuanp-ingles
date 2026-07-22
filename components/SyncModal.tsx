'use client'
import { useEffect, useMemo, useRef, useState } from 'react'
import {
  Copy,
  Check,
  Link2,
  RefreshCw,
  Unplug,
  X,
  Smartphone,
  AlertTriangle,
} from 'lucide-react'
import { useSyncContext } from '@/components/providers/SyncContext'
import { buildLinkUrl } from '@/lib/hooks/useSyncEngine'
import type { SyncStatus } from '@/lib/types/sync'

const QR_API = 'https://api.qrserver.com/v1/create-qr-code/'

function formatToken(token: string): string {
  if (!token) return ''
  return token.match(/.{1,4}/g)?.join(' ') ?? token
}

function StatusBadge({
  status,
  lastError,
  lastSyncedAt,
  pending,
}: {
  status: SyncStatus
  lastError: string | null
  lastSyncedAt: number | null
  pending: boolean
}) {
  const [now, setNow] = useState<number>(() => Date.now())
  useEffect(() => {
    if (status !== 'synced' || !lastSyncedAt) return
    const id = setInterval(() => setNow(Date.now()), 30_000)
    return () => clearInterval(id)
  }, [status, lastSyncedAt])

  const label = useMemo<string>(() => {
    const s: SyncStatus = status
    if (s === ('pulling' as SyncStatus)) return 'Obteniendo…'
    if (s === ('pushing' as SyncStatus)) return 'Enviando…'
    if (pending && s !== ('pushing' as SyncStatus)) return 'Cambios pendientes'
    if (s === ('error' as SyncStatus)) return lastError ? `Error: ${lastError}` : 'Error'
    if (s === ('synced' as SyncStatus)) {
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
              : 'bg-warning motion-safe:animate-pulse'
        }`}
      />
      {label}
    </span>
  )
}

export default function SyncModal({
  open,
  onClose,
}: {
  open: boolean
  onClose: () => void
}) {
  const [mounted, setMounted] = useState(false)
  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) {
    return <dialog className="modal" aria-hidden="true" />
  }

  return <SyncModalClient open={open} onClose={onClose} />
}

function SyncModalClient({
  open,
  onClose,
}: {
  open: boolean
  onClose: () => void
}) {
  const sync = useSyncContext()
  const dialogRef = useRef<HTMLDialogElement | null>(null)
  const confirmRef = useRef<HTMLDialogElement | null>(null)

  const [copied, setCopied] = useState(false)
  const [copiedAnnounce, setCopiedAnnounce] = useState('')
  const [linkInput, setLinkInput] = useState('')
  const [linkError, setLinkError] = useState<string | null>(null)
  const [linkSuccess, setLinkSuccess] = useState<string | null>(null)
  const [showUnlinkConfirm, setShowUnlinkConfirm] = useState(false)
  const [prevOpen, setPrevOpen] = useState(open)

  useEffect(() => {
    const el = dialogRef.current
    if (!el) return
    if (open && !el.open) el.showModal()
    if (!open && el.open) el.close()
  }, [open])

  useEffect(() => {
    const el = confirmRef.current
    if (!el) return
    if (showUnlinkConfirm && !el.open) el.showModal()
    if (!showUnlinkConfirm && el.open) el.close()
  }, [showUnlinkConfirm])

  if (open !== prevOpen) {
    setPrevOpen(open)
    if (open) {
      setCopied(false)
      setCopiedAnnounce('')
      setLinkInput('')
      setLinkError(null)
      setLinkSuccess(null)
    }
  }

  const syncToken = sync?.syncToken ?? ''
  const linkUrl = useMemo<string>(() => buildLinkUrl(syncToken), [syncToken])
  const qrSrc = useMemo<string | null>(() => {
    if (!linkUrl) return null
    return `${QR_API}?size=240x240&margin=1&data=${encodeURIComponent(linkUrl)}`
  }, [linkUrl])

  async function copyToken(): Promise<void> {
    if (!syncToken) return
    try {
      await navigator.clipboard.writeText(syncToken)
      setCopied(true)
      setCopiedAnnounce('Token copiado al portapapeles')
      setTimeout(() => {
        setCopied(false)
        setCopiedAnnounce('')
      }, 1500)
    } catch {
      setCopiedAnnounce('No se pudo copiar. Copialo manualmente.')
    }
  }

  async function copyLinkUrl(): Promise<void> {
    if (!linkUrl) return
    try {
      await navigator.clipboard.writeText(linkUrl)
      setCopied(true)
      setCopiedAnnounce('Link copiado al portapapeles')
      setTimeout(() => {
        setCopied(false)
        setCopiedAnnounce('')
      }, 1500)
    } catch {
      setCopiedAnnounce('No se pudo copiar. Copialo manualmente.')
    }
  }

  function handleLink(e: React.FormEvent<HTMLFormElement>): void {
    e.preventDefault()
    setLinkError(null)
    setLinkSuccess(null)
    const raw = linkInput.trim()
    if (!raw) {
      setLinkError('Pegá un token primero.')
      return
    }
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

  function handleAskUnlink(): void {
    setShowUnlinkConfirm(true)
  }

  function handleConfirmUnlink(): void {
    setShowUnlinkConfirm(false)
    sync?.unlink()
  }

  return (
    <>
      <dialog
        ref={dialogRef}
        className="modal"
        onClose={onClose}
        aria-labelledby="sync-modal-title"
      >
        <div className="modal-box w-11/12 max-w-md rounded-3xl border border-base-300 bg-base-100 p-0 shadow-xl">
          <header className="flex items-start justify-between gap-3 border-b border-base-300 px-5 py-4 sm:px-6">
            <div className="min-w-0">
              <h2
                id="sync-modal-title"
                className="text-lg font-bold text-base-content"
              >
                Sincronización
              </h2>
              <p className="mt-0.5 text-xs text-base-content/70">
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
            <div className="flex items-center justify-between gap-3">
              <StatusBadge
                status={sync?.status ?? 'idle'}
                lastError={sync?.lastError ?? null}
                lastSyncedAt={sync?.lastSyncedAt ?? null}
                pending={sync?.pendingPush ?? false}
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
                        const img = e.currentTarget as HTMLImageElement
                        img.style.display = 'none'
                      }}
                    />
                  ) : null}
                </div>

                <div className="min-w-0 flex-1 space-y-2">
                  <p className="flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.16em] text-base-content/70">
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
                      onClick={() => void copyToken()}
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
                      onClick={() => void copyLinkUrl()}
                      className="btn btn-sm btn-ghost gap-2 rounded-full normal-case"
                    >
                      <Link2 className="size-3.5" aria-hidden="true" />
                      Copiar link
                    </button>
                  </div>
                  <span className="sr-only" role="status" aria-live="polite">
                    {copiedAnnounce}
                  </span>
                </div>
              </div>

              <p className="mt-3 text-xs leading-relaxed text-base-content/70">
                Escaneá el QR desde tu otro dispositivo o pegá el token en él.
                Se abrirá esta misma página con <code>?syncToken=…</code> y tus
                tarjetas se sincronizarán solas.
              </p>
            </section>

            <section>
              <label
                htmlFor="sync-link-input"
                className="mb-2 block text-xs font-semibold uppercase tracking-[0.16em] text-base-content/70"
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
                  placeholder="Pegá acá el token o la URL del otro dispositivo"
                  className="input input-bordered input-sm w-full rounded-full font-mono text-xs"
                  aria-invalid={Boolean(linkError)}
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
                  <span className="text-base-content/70">
                    También podés abrir directamente
                    <code className="mx-1 rounded bg-base-200 px-1 py-0.5 text-[0.7rem]">
                      ?syncToken=…
                    </code>
                    en el otro dispositivo.
                  </span>
                )}
              </div>
            </section>

            <section className="border-t border-base-300 pt-4">
              <button
                type="button"
                onClick={handleAskUnlink}
                className="btn btn-ghost btn-xs gap-2 normal-case text-base-content/70 hover:text-error"
              >
                <Unplug className="size-3.5" aria-hidden="true" />
                Generar token nuevo (desvincular este dispositivo)
              </button>
            </section>
          </div>
        </div>

        <form method="dialog" className="modal-backdrop">
          <button type="submit" aria-label="Cerrar">
            cerrar
          </button>
        </form>
      </dialog>

      <dialog
        ref={confirmRef}
        className="modal"
        aria-labelledby="unlink-confirm-title"
        onClose={() => setShowUnlinkConfirm(false)}
      >
        <div className="modal-box rounded-2xl border border-base-300 bg-base-100">
          <div className="flex items-start gap-4">
            <div className="flex size-11 shrink-0 items-center justify-center rounded-full border border-error/30 bg-error/10 text-error">
              <AlertTriangle className="size-5" aria-hidden="true" />
            </div>
            <div className="flex-1">
              <h3
                id="unlink-confirm-title"
                className="text-base font-bold uppercase tracking-[0.18em] text-base-content"
              >
                ¿Desvincular este dispositivo?
              </h3>
              <p className="mt-2 text-sm text-base-content/80">
                Se generará un nuevo token. Tu progreso local no se borra, pero
                este dispositivo dejará de estar sincronizado con el anterior.
              </p>
            </div>
          </div>

          <div className="modal-action">
            <form method="dialog">
              <button
                type="submit"
                className="btn btn-ghost rounded-full normal-case"
              >
                Cancelar
              </button>
            </form>
            <button
              type="button"
              onClick={handleConfirmUnlink}
              className="btn gap-2 rounded-full border-none bg-error text-base-100 normal-case hover:bg-error/90"
            >
              <Unplug className="size-4" aria-hidden="true" />
              Sí, desvincular
            </button>
          </div>
        </div>
      </dialog>
    </>
  )
}
