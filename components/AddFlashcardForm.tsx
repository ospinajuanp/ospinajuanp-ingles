'use client'
import { useState } from 'react'
import { X, Plus } from 'lucide-react'

interface AddFlashcardFormProps {
  onAdd?: (payload: { es: string; en: string }) => void
  onCancel?: () => void
}

export default function AddFlashcardForm({ onAdd, onCancel }: AddFlashcardFormProps) {
  const [es, setEs] = useState('')
  const [en, setEn] = useState('')
  const [error, setError] = useState<string | null>(null)

  function handleSubmit(e: React.FormEvent<HTMLFormElement>): void {
    e.preventDefault()
    setError(null)
    const trimmedEs = es.trim()
    const trimmedEn = en.trim()
    if (!trimmedEs || !trimmedEn) {
      setError('Completa ambos campos.')
      return
    }
    onAdd?.({ es: trimmedEs, en: trimmedEn })
    setEs('')
    setEn('')
  }

  const canSubmit = Boolean(es.trim() && en.trim())

  return (
    <form
      onSubmit={handleSubmit}
      className="rounded-2xl border border-base-300 bg-base-100 p-5 shadow-sm sm:p-6"
    >
      <div className="mb-4 flex items-start justify-between gap-4">
        <div>
          <h2 className="text-sm font-bold uppercase tracking-[0.18em] text-base-content sm:text-base">
            Nueva oración
          </h2>
          <p className="mt-1 text-xs text-base-content/70">
            Agrega frases propias para repasarlas con repetición espaciada.
          </p>
        </div>
        {onCancel ? (
          <button
            type="button"
            onClick={onCancel}
            aria-label="Cerrar formulario"
            className="inline-flex size-8 shrink-0 items-center justify-center rounded-full text-base-content/50 transition hover:bg-base-200 hover:text-base-content active:scale-95"
          >
            <X className="size-4" aria-hidden="true" />
          </button>
        ) : null}
      </div>

      <div className="space-y-3">
        <div>
          <label
            htmlFor="srs-es"
            className="mb-1 block text-xs font-semibold uppercase tracking-wider text-base-content/70"
          >
            Español
          </label>
          <textarea
            id="srs-es"
            value={es}
            onChange={(e) => setEs(e.target.value)}
            placeholder="Ej: Yo como manzanas todos los días."
            rows={2}
            className="textarea textarea-bordered w-full resize-none rounded-xl border-base-300 bg-base-200 px-4 py-3 text-base text-base-content placeholder:text-base-content/50 outline-none transition focus:border-primary focus:bg-base-100 focus:ring-2 focus:ring-primary/30"
          />
        </div>
        <div>
          <label
            htmlFor="srs-en"
            className="mb-1 block text-xs font-semibold uppercase tracking-wider text-base-content/70"
          >
            Inglés
          </label>
          <textarea
            id="srs-en"
            value={en}
            onChange={(e) => setEn(e.target.value)}
            placeholder="Ex: I eat apples every day."
            rows={2}
            className="textarea textarea-bordered w-full resize-none rounded-xl border-base-300 bg-base-200 px-4 py-3 text-base text-base-content placeholder:text-base-content/50 outline-none transition focus:border-primary focus:bg-base-100 focus:ring-2 focus:ring-primary/30"
          />
        </div>
      </div>

      {error ? (
        <p className="mt-3 text-sm text-error" role="alert">
          {error}
        </p>
      ) : null}

      <div className="mt-4 flex items-center justify-end gap-3">
        <button
          type="submit"
          disabled={!canSubmit}
          className="btn btn-primary gap-2 rounded-full px-5 normal-case shadow-sm disabled:bg-base-300 disabled:text-base-content/40"
        >
          <Plus className="size-4" aria-hidden="true" />
          Agregar tarjeta
        </button>
      </div>
    </form>
  )
}
