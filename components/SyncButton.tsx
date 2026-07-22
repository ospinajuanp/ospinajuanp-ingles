'use client'
// Header button that opens the SyncModal. DaisyUI v5 button primitives
// only — no custom colors. Renders a single icon button with a status
// dot (DaisyUI badge) when there is pending sync activity.

import { RefreshCw } from 'lucide-react'
import { useSyncContext } from '@/components/providers/SyncContext'

export default function SyncButton({ onClick, className = '' }: { onClick?: () => void; className?: string }) {
  const sync = useSyncContext()
  const status = sync?.status ?? 'idle'
  const pending = sync?.pendingPush ?? false
  const isError = status === 'error'
  const isBusy = status === 'pulling' || status === 'pushing' || pending

  const dotClass = isError
    ? 'bg-error'
    : isBusy
      ? 'bg-warning animate-pulse'
      : 'bg-success'

  return (
    <button
      type="button"
      onClick={onClick}
      aria-label={
        isError
          ? 'Sincronización: error. Abre para ver detalles.'
          : isBusy
            ? 'Sincronización en curso'
            : 'Sincronización multi-dispositivo'
      }
      className={`relative inline-flex size-10 items-center justify-center rounded-full border border-base-300 bg-base-100 text-base-content shadow-sm transition hover:border-primary/40 hover:text-primary hover:shadow-md active:scale-95 ${className}`.trim()}
      title="Sincronizar entre dispositivos"
    >
      <RefreshCw className="size-5" aria-hidden="true" />
      <span
        aria-hidden="true"
        className={`absolute right-1 top-1 inline-block size-2 rounded-full ring-2 ring-base-100 ${dotClass}`}
      />
    </button>
  )
}