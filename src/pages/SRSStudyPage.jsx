import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import AddFlashcardForm from '../components/AddFlashcardForm'
import Flashcard from '../components/Flashcard'
import { useSRSContext } from '../contexts/SRSContext'

function shuffle(arr) {
  const out = arr.slice()
  for (let i = out.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[out[i], out[j]] = [out[j], out[i]]
  }
  return out
}

export default function SRSStudyPage() {
  const srs = useSRSContext()
  const [showForm, setShowForm] = useState(false)

  // Mix both decks + shuffle once per store change. Derives naturally
  // (no setState-in-useEffect): when the user grades or adds a card, the
  // queue updates and we re-render with the fresh data.
  const queue = useMemo(() => shuffle(srs.dueCards), [srs.dueCards])
  const [cursor, setCursor] = useState(0)

  const activeCard = cursor < queue.length ? queue[cursor] : null

  function handleAdd(payload) {
    const created = srs.addCustomSentence(payload)
    if (created) setShowForm(false)
  }

  function handleGrade(cardId, grade) {
    srs.gradeCard(cardId, grade)
    setCursor((c) => c + 1)
  }

  return (
    <div className="mx-auto max-w-4xl px-4 py-6 sm:px-6 sm:py-8">
      <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900 sm:text-3xl">
            Repaso espaciado
          </h1>
          <p className="mt-1 text-sm text-slate-500">
            Mezcla tus oraciones personalizadas con los verbos que has visitado.
          </p>
        </div>
        <Link
          to="/"
          className="inline-flex w-fit items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-700 shadow-sm transition hover:bg-slate-50 active:scale-95"
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
            <path d="m15 18-6-6 6-6" />
          </svg>
          Volver a verbos
        </Link>
      </div>

      <dl className="mb-6 grid grid-cols-2 gap-3 sm:grid-cols-4">
        <Stat label="Pendientes hoy" value={srs.dueCount} accent="indigo" />
        <Stat label="Total" value={srs.totalCount} />
        <Stat label="Oraciones" value={srs.customCount} />
        <Stat label="Verbos" value={srs.verbCount} />
      </dl>

      <div className="space-y-6">
        {!showForm ? (
          <button
            type="button"
            onClick={() => setShowForm(true)}
            className="inline-flex items-center gap-2 rounded-full border border-dashed border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-600 shadow-sm transition hover:border-indigo-400 hover:text-indigo-600 active:scale-95"
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
            Agregar oración
          </button>
        ) : (
          <AddFlashcardForm
            onAdd={handleAdd}
            onCancel={() => setShowForm(false)}
          />
        )}

        {activeCard ? (
          <section className="rounded-3xl border border-slate-200 bg-gradient-to-b from-white to-slate-50 p-5 shadow-sm sm:p-8">
            <div className="mb-4 flex items-center justify-between text-xs uppercase tracking-[0.18em] text-slate-400">
              <span>
                Tarjeta {Math.min(cursor + 1, queue.length)} de {queue.length}
              </span>
              <span>
                {activeCard.type === 'custom' ? 'Personalizada' : 'Verbo visto'}
              </span>
            </div>
            <Flashcard
              key={activeCard.id}
              card={activeCard}
              onGrade={handleGrade}
            />
          </section>
        ) : (
          <EmptyState
            dueCount={srs.dueCount}
            totalCount={srs.totalCount}
            onShowForm={() => setShowForm(true)}
          />
        )}
      </div>
    </div>
  )
}

function Stat({ label, value, accent = 'slate' }) {
  const accentClass = accent === 'indigo' ? 'text-indigo-600' : 'text-slate-900'
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
      <dt className="text-[0.65rem] font-semibold uppercase tracking-[0.18em] text-slate-400">
        {label}
      </dt>
      <dd className={`mt-1 text-2xl font-bold ${accentClass}`}>{value}</dd>
    </div>
  )
}

function EmptyState({ dueCount, totalCount, onShowForm }) {
  if (totalCount === 0) {
    return (
      <div className="rounded-2xl border border-dashed border-slate-300 bg-white p-10 text-center">
        <p className="text-lg font-semibold text-slate-800">Tu mazo está vacío</p>
        <p className="mt-1 text-sm text-slate-500">
          Agrega tu primera oración o visita verbos en la pantalla principal para empezar.
        </p>
        <button
          type="button"
          onClick={onShowForm}
          className="mt-4 inline-flex items-center gap-2 rounded-full bg-indigo-600 px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-indigo-500 active:scale-95"
        >
          Agregar primera oración
        </button>
      </div>
    )
  }
  return (
    <div className="rounded-2xl border border-emerald-100 bg-emerald-50/60 p-8 text-center">
      <div className="mx-auto mb-3 inline-flex size-12 items-center justify-center rounded-full bg-emerald-100 text-emerald-600">
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="size-6"
          aria-hidden="true"
        >
          <path d="M20 6 9 17l-5-5" />
        </svg>
      </div>
      <p className="text-lg font-semibold text-slate-800">¡Todo al día!</p>
      <p className="mt-1 text-sm text-slate-500">
        {dueCount === 0
          ? 'No hay tarjetas pendientes por ahora. Vuelve más tarde o agrega más frases.'
          : 'Sesión completada.'}
      </p>
    </div>
  )
}
