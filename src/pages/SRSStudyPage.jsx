import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { ArrowLeft, Plus, CheckCircle2, ListFilter, BookOpen } from 'lucide-react'
import AddFlashcardForm from '../components/AddFlashcardForm'
import Flashcard from '../components/Flashcard'
import DeckManager from '../components/DeckManager'
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
  const [mode, setMode] = useState('study') // 'study' | 'manage'

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
          <h1 className="text-2xl font-bold tracking-tight text-base-content sm:text-3xl">
            Repaso espaciado
          </h1>
          <p className="mt-1 text-sm text-base-content/70">
            {mode === 'study'
              ? 'Mezcla tus oraciones personalizadas con los verbos que has visitado.'
              : 'Busca, edita o elimina tarjetas del mazo.'}
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <ModeToggle mode={mode} onChange={setMode} />
          <Link
            to="/"
            className="inline-flex w-fit items-center gap-2 rounded-full border border-base-300 bg-base-100 px-4 py-2 text-sm font-medium text-base-content shadow-sm transition hover:bg-base-200 active:scale-95"
          >
            <ArrowLeft className="size-4" aria-hidden="true" />
            Volver a verbos
          </Link>
        </div>
      </div>

      {mode === 'manage' ? (
        <DeckManager />
      ) : (
        <>
          <dl className="mb-6 grid grid-cols-2 gap-3 sm:grid-cols-4">
            <Stat label="Pendientes hoy" value={srs.dueCount} accent="primary" />
            <Stat label="Total" value={srs.totalCount} />
            <Stat label="Oraciones" value={srs.customCount} />
            <Stat label="Verbos" value={srs.verbCount} />
          </dl>

          <div className="space-y-6">
            {!showForm ? (
              <button
                type="button"
                onClick={() => setShowForm(true)}
                className="inline-flex items-center gap-2 rounded-full border border-dashed border-base-300 bg-base-100 px-4 py-2 text-sm font-medium text-base-content/70 shadow-sm transition hover:border-primary hover:text-primary active:scale-95"
              >
                <Plus className="size-4" aria-hidden="true" />
                Agregar oración
              </button>
            ) : (
              <AddFlashcardForm
                onAdd={handleAdd}
                onCancel={() => setShowForm(false)}
              />
            )}

            {activeCard ? (
              <section className="rounded-3xl border border-base-300 bg-gradient-to-b from-base-100 to-base-200 p-5 shadow-sm sm:p-8">
                <div className="mb-4 flex items-center justify-between text-xs uppercase tracking-[0.18em] text-base-content/50">
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
                onSwitchToManage={() => setMode('manage')}
              />
            )}
          </div>
        </>
      )}
    </div>
  )
}

function ModeToggle({ mode, onChange }) {
  const isStudy = mode === 'study'
  return (
    <div
      role="group"
      aria-label="Modo de la página de repaso"
      className="join shadow-sm"
    >
      <button
        type="button"
        onClick={() => onChange('study')}
        aria-pressed={isStudy}
        className={
          'btn btn-sm join-item gap-2 rounded-l-full normal-case transition ' +
          (isStudy
            ? 'btn-primary text-primary-content'
            : 'btn-ghost text-base-content/70 hover:bg-base-200')
        }
      >
        <BookOpen className="size-4" aria-hidden="true" />
        Estudiar
      </button>
      <button
        type="button"
        onClick={() => onChange('manage')}
        aria-pressed={!isStudy}
        className={
          'btn btn-sm join-item gap-2 rounded-r-full normal-case transition ' +
          (!isStudy
            ? 'btn-primary text-primary-content'
            : 'btn-ghost text-base-content/70 hover:bg-base-200')
        }
      >
        <ListFilter className="size-4" aria-hidden="true" />
        Gestionar Mazo
      </button>
    </div>
  )
}

function Stat({ label, value, accent = 'slate' }) {
  const accentClass = accent === 'primary' ? 'text-primary' : 'text-base-content'
  return (
    <div className="rounded-2xl border border-base-300 bg-base-100 p-4 shadow-sm">
      <dt className="text-[0.65rem] font-semibold uppercase tracking-[0.18em] text-base-content/50">
        {label}
      </dt>
      <dd className={`mt-1 text-2xl font-bold ${accentClass}`}>{value}</dd>
    </div>
  )
}

function EmptyState({ dueCount, totalCount, onShowForm, onSwitchToManage }) {
  if (totalCount === 0) {
    return (
      <div className="rounded-2xl border border-dashed border-base-300 bg-base-100 p-10 text-center">
        <p className="text-lg font-semibold text-base-content">Tu mazo está vacío</p>
        <p className="mt-1 text-sm text-base-content/70">
          Agrega tu primera oración o visita verbos en la pantalla principal para empezar.
        </p>
        <button
          type="button"
          onClick={onShowForm}
          className="btn btn-primary mt-4 rounded-full px-5 normal-case"
        >
          Agregar primera oración
        </button>
      </div>
    )
  }
  return (
    <div className="rounded-2xl border border-success/30 bg-success/10 p-8 text-center">
      <div className="mx-auto mb-3 inline-flex size-12 items-center justify-center rounded-full bg-success/20 text-success">
        <CheckCircle2 className="size-6" aria-hidden="true" />
      </div>
      <p className="text-lg font-semibold text-base-content">¡Todo al día!</p>
      <p className="mt-1 text-sm text-base-content/70">
        {dueCount === 0
          ? 'No hay tarjetas pendientes por ahora. Vuelve más tarde o agrega más frases.'
          : 'Sesión completada.'}
      </p>
      {onSwitchToManage ? (
        <button
          type="button"
          onClick={onSwitchToManage}
          className="btn btn-outline btn-primary mt-4 rounded-full px-5 normal-case"
        >
          Abrir Gestión de Mazo
        </button>
      ) : null}
    </div>
  )
}
