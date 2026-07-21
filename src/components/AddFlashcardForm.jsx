import { useState } from 'react'

export default function AddFlashcardForm({ onAdd, onCancel }) {
  const [es, setEs] = useState('')
  const [en, setEn] = useState('')
  const [error, setError] = useState(null)

  function handleSubmit(e) {
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

  const canSubmit = es.trim() && en.trim()

  return (
    <form
      onSubmit={handleSubmit}
      className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6"
    >
      <div className="mb-4 flex items-start justify-between gap-4">
        <div>
          <h2 className="text-sm font-bold uppercase tracking-[0.18em] text-slate-900 sm:text-base">
            Nueva oración
          </h2>
          <p className="mt-1 text-xs text-slate-500">
            Agrega frases propias para repasarlas con repetición espaciada.
          </p>
        </div>
        {onCancel ? (
          <button
            type="button"
            onClick={onCancel}
            aria-label="Cerrar formulario"
            className="inline-flex size-8 shrink-0 items-center justify-center rounded-full text-slate-400 transition hover:bg-slate-100 hover:text-slate-600 active:scale-95"
          >
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="size-4"
              aria-hidden="true"
            >
              <path d="M18 6 6 18M6 6l12 12" />
            </svg>
          </button>
        ) : null}
      </div>

      <div className="space-y-3">
        <div>
          <label
            htmlFor="srs-es"
            className="mb-1 block text-xs font-semibold uppercase tracking-wider text-slate-500"
          >
            Español
          </label>
          <textarea
            id="srs-es"
            value={es}
            onChange={(e) => setEs(e.target.value)}
            placeholder="Ej: Yo como manzanas todos los días."
            rows={2}
            className="w-full resize-none rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-base text-slate-800 placeholder:text-slate-400 outline-none transition focus:border-indigo-500 focus:bg-white focus:ring-2 focus:ring-indigo-100"
          />
        </div>
        <div>
          <label
            htmlFor="srs-en"
            className="mb-1 block text-xs font-semibold uppercase tracking-wider text-slate-500"
          >
            Inglés
          </label>
          <textarea
            id="srs-en"
            value={en}
            onChange={(e) => setEn(e.target.value)}
            placeholder="Ex: I eat apples every day."
            rows={2}
            className="w-full resize-none rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-base text-slate-800 placeholder:text-slate-400 outline-none transition focus:border-indigo-500 focus:bg-white focus:ring-2 focus:ring-indigo-100"
          />
        </div>
      </div>

      {error ? (
        <p className="mt-3 text-sm text-red-500" role="alert">
          {error}
        </p>
      ) : null}

      <div className="mt-4 flex items-center justify-end gap-3">
        <button
          type="submit"
          disabled={!canSubmit}
          className="inline-flex items-center gap-2 rounded-full bg-indigo-600 px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-indigo-500 active:scale-95 disabled:cursor-not-allowed disabled:bg-slate-300"
        >
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            className="size-4"
            aria-hidden="true"
          >
            <path d="M12 5v14M5 12h14" />
          </svg>
          Agregar tarjeta
        </button>
      </div>
    </form>
  )
}
