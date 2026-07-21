// Deck management interface for the SRS module.
//
// Shows every card in the localStorage-backed store (both `type: 'custom'`
// user sentences and `type: 'verb'` auto-registered verbs). Provides:
//
//   - Real-time search filter (matches Español OR Inglés case-insensitive).
//   - Pagination 10/page with prev/next + numeric shortcuts.
//   - Per-row actions: edit (only custom cards) + delete (both types).
//   - DaisyUI native <dialog className="modal"> for the edit form AND
//     the delete confirmation (custom in-app confirmation instead of
//     `window.confirm` so it matches the theme + is styleable).
//
// Hook contract: the parent supplies the SRS context value (which already
// exposes `cards`, `removeCard`, `editCustomCard`). We don't call the
// hook directly here so this component can render even when SRSProvider
// is the only ancestor.

import { useEffect, useId, useMemo, useRef, useState } from 'react'
import {
  Search,
  Pencil,
  Trash2,
  ChevronLeft,
  ChevronRight,
  ChevronsLeft,
  ChevronsRight,
  X,
  Save,
  Layers,
  AlertTriangle,
} from 'lucide-react'
import { useSRSContext } from '../contexts/SRSContext'

const PAGE_SIZE = 10

function cardEs(card) {
  return card.type === 'custom' ? card.front?.es ?? '' : card.infinitivo?.esp ?? ''
}

function cardEn(card) {
  return card.type === 'custom' ? card.front?.en ?? '' : card.infinitivo?.ing ?? ''
}

function formatInterval(card) {
  if (!card.srs) return '—'
  if (card.srs.interval === 0) return 'nuevo'
  const n = card.srs.interval
  return `${n} ${n === 1 ? 'día' : 'días'}`
}

export default function DeckManager() {
  const srs = useSRSContext()
  const cards = useMemo(() => srs?.cards ?? [], [srs?.cards])

  const [searchTerm, setSearchTerm] = useState('')
  const [page, setPage] = useState(1)
  const [trackedSearch, setTrackedSearch] = useState(searchTerm)
  const [editingId, setEditingId] = useState(null)
  const [deletingCard, setDeletingCard] = useState(null)

  const editingCard = useMemo(
    () => (editingId ? cards.find((c) => c.id === editingId) ?? null : null),
    [editingId, cards],
  )

  // Derived-state reset: when the search term changes, jump back to page 1.
  if (trackedSearch !== searchTerm) {
    setTrackedSearch(searchTerm)
    setPage(1)
  }

  const filtered = useMemo(() => {
    const q = searchTerm.trim().toLowerCase()
    if (!q) return cards
    return cards.filter((card) => {
      const es = cardEs(card).toLowerCase()
      const en = cardEn(card).toLowerCase()
      return es.includes(q) || en.includes(q)
    })
  }, [cards, searchTerm])

  const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE))
  const safePage = Math.min(page, totalPages)
  const startIdx = (safePage - 1) * PAGE_SIZE
  const pageCards = filtered.slice(startIdx, startIdx + PAGE_SIZE)

  return (
    <section className="space-y-5">
      <header className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-base-content sm:text-3xl">
            Gestión de Mazo
          </h2>
          <p className="mt-1 text-sm text-base-content/70">
            Edita tus oraciones personalizadas o elimina tarjetas del mazo.
            Los verbos del dataset oficial solo se pueden eliminar.
          </p>
        </div>
        <div className="flex items-center gap-2 self-start rounded-full border border-base-300 bg-base-100 px-3 py-1.5 text-xs font-semibold text-base-content/70 shadow-sm">
          <Layers className="size-3.5" aria-hidden="true" />
          <span>
            {filtered.length} de {cards.length} tarjetas
          </span>
        </div>
      </header>

      <div className="relative">
        <Search
          className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 size-4 text-base-content/50"
          aria-hidden="true"
        />
        <input
          type="search"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Buscar en español o inglés…"
          aria-label="Buscar tarjetas"
          className="input input-bordered w-full rounded-full border-base-300 bg-base-100 pl-10 pr-10 text-base text-base-content placeholder:text-base-content/50 shadow-sm focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/30"
        />
        {searchTerm && (
          <button
            type="button"
            onClick={() => setSearchTerm('')}
            aria-label="Limpiar búsqueda"
            className="absolute right-3 top-1/2 -translate-y-1/2 inline-flex size-7 items-center justify-center rounded-full text-base-content/50 transition hover:bg-base-200 hover:text-base-content"
          >
            <X className="size-4" aria-hidden="true" />
          </button>
        )}
      </div>

      <div className="overflow-hidden rounded-2xl border border-base-300 bg-base-100 shadow-sm">
        <div className="overflow-x-auto">
          <table className="table">
            <thead className="bg-base-200 text-base-content/70">
              <tr>
                <th className="text-[0.65rem] font-bold uppercase tracking-[0.14em]">Tipo</th>
                <th className="text-[0.65rem] font-bold uppercase tracking-[0.14em]">Español</th>
                <th className="text-[0.65rem] font-bold uppercase tracking-[0.14em]">Inglés</th>
                <th className="text-[0.65rem] font-bold uppercase tracking-[0.14em]">Estado SRS</th>
                <th className="text-right text-[0.65rem] font-bold uppercase tracking-[0.14em]">
                  Acciones
                </th>
              </tr>
            </thead>
            <tbody>
              {pageCards.length === 0 ? (
                <tr>
                  <td colSpan={5} className="py-10 text-center text-sm text-base-content/60">
                    {cards.length === 0
                      ? 'Tu mazo está vacío. Agrega oraciones o visita verbos para empezar.'
                      : `Sin resultados para "${searchTerm}".`}
                  </td>
                </tr>
              ) : (
                pageCards.map((card) => {
                  const isCustom = card.type === 'custom'
                  return (
                    <tr key={card.id} className="hover:bg-base-200/50">
                      <td>
                        {isCustom ? (
                          <span className="badge badge-primary badge-outline text-[0.65rem] font-bold uppercase tracking-[0.12em]">
                            Custom
                          </span>
                        ) : (
                          <span className="badge badge-ghost text-[0.65rem] font-bold uppercase tracking-[0.12em]">
                            Verbo
                          </span>
                        )}
                      </td>
                      <td className="font-medium text-base-content">{cardEs(card)}</td>
                      <td className="text-base-content/80">{cardEn(card)}</td>
                      <td>
                        <div className="flex flex-col gap-0.5">
                          <span className="text-xs font-semibold text-base-content">
                            {formatInterval(card)}
                          </span>
                          <span className="text-[0.7rem] text-base-content/60 tabular-nums">
                            EF {card.srs?.ef?.toFixed(2) ?? '2.50'}
                          </span>
                        </div>
                      </td>
                      <td>
                        <div className="flex items-center justify-end gap-1.5">
                          {isCustom ? (
                            <button
                              type="button"
                              onClick={() => setEditingId(card.id)}
                              aria-label={`Editar tarjeta: ${cardEs(card)}`}
                              className="inline-flex size-9 items-center justify-center rounded-full border border-base-300 bg-base-100 text-base-content/70 transition hover:border-primary/40 hover:bg-primary/10 hover:text-primary active:scale-95"
                            >
                              <Pencil className="size-4" aria-hidden="true" />
                            </button>
                          ) : (
                            <span
                              className="inline-flex size-9 items-center justify-center text-base-content/30"
                              title="Los verbos del dataset no se pueden editar"
                            >
                              <Pencil className="size-4" aria-hidden="true" />
                            </span>
                          )}
                          <button
                            type="button"
                            onClick={() => setDeletingCard(card)}
                            aria-label={`Eliminar tarjeta: ${cardEs(card)}`}
                            className="inline-flex size-9 items-center justify-center rounded-full border border-base-300 bg-base-100 text-error/70 transition hover:border-error/40 hover:bg-error/10 hover:text-error active:scale-95"
                          >
                            <Trash2 className="size-4" aria-hidden="true" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  )
                })
              )}
            </tbody>
          </table>
        </div>

        {filtered.length > 0 ? (
          <Pagination
            page={safePage}
            totalPages={totalPages}
            onChange={setPage}
          />
        ) : null}
      </div>

      <EditDialog
        card={editingCard}
        onClose={() => setEditingId(null)}
        onSave={(payload) => {
          if (!editingCard) return
          const result = srs?.editCustomCard?.(editingCard.id, payload)
          if (result) setEditingId(null)
        }}
      />

      <ConfirmDialog
        card={deletingCard}
        onCancel={() => setDeletingCard(null)}
        onConfirm={() => {
          if (deletingCard) srs?.removeCard?.(deletingCard.id)
          setDeletingCard(null)
        }}
      />
    </section>
  )
}

function Pagination({ page, totalPages, onChange }) {
  const pages = useMemo(() => buildPageList(page, totalPages), [page, totalPages])

  return (
    <div className="flex flex-col items-center justify-between gap-3 border-t border-base-300 px-4 py-3 text-sm sm:flex-row">
      <span className="text-base-content/60">
        Página <span className="font-semibold text-base-content">{page}</span> de{' '}
        <span className="font-semibold text-base-content">{totalPages}</span>
      </span>
      <div className="join shadow-sm" role="group" aria-label="Paginación">
        <button
          type="button"
          onClick={() => onChange(1)}
          disabled={page === 1}
          aria-label="Primera página"
          className="btn btn-sm join-item bg-base-100 text-base-content/70 hover:bg-base-200 disabled:bg-base-100 disabled:text-base-content/30"
        >
          <ChevronsLeft className="size-4" aria-hidden="true" />
        </button>
        <button
          type="button"
          onClick={() => onChange(page - 1)}
          disabled={page === 1}
          aria-label="Página anterior"
          className="btn btn-sm join-item bg-base-100 text-base-content/70 hover:bg-base-200 disabled:bg-base-100 disabled:text-base-content/30"
        >
          <ChevronLeft className="size-4" aria-hidden="true" />
        </button>
        {pages.map((p, i) =>
          p === '…' ? (
            <span
              key={`gap-${i}`}
              className="btn btn-sm btn-disabled join-item bg-base-100 text-base-content/40"
              aria-hidden="true"
            >
              …
            </span>
          ) : (
            <button
              key={p}
              type="button"
              onClick={() => onChange(p)}
              aria-current={p === page ? 'page' : undefined}
              aria-label={`Página ${p}`}
              className={
                'btn btn-sm join-item ' +
                (p === page
                  ? 'btn-primary text-primary-content'
                  : 'bg-base-100 text-base-content/70 hover:bg-base-200')
              }
            >
              {p}
            </button>
          ),
        )}
        <button
          type="button"
          onClick={() => onChange(page + 1)}
          disabled={page === totalPages}
          aria-label="Página siguiente"
          className="btn btn-sm join-item bg-base-100 text-base-content/70 hover:bg-base-200 disabled:bg-base-100 disabled:text-base-content/30"
        >
          <ChevronRight className="size-4" aria-hidden="true" />
        </button>
        <button
          type="button"
          onClick={() => onChange(totalPages)}
          disabled={page === totalPages}
          aria-label="Última página"
          className="btn btn-sm join-item bg-base-100 text-base-content/70 hover:bg-base-200 disabled:bg-base-100 disabled:text-base-content/30"
        >
          <ChevronsRight className="size-4" aria-hidden="true" />
        </button>
      </div>
    </div>
  )
}

function buildPageList(page, total) {
  if (total <= 7) return Array.from({ length: total }, (_, i) => i + 1)
  const out = new Set([1, total, page - 1, page, page + 1])
  const list = [...out].filter((n) => n >= 1 && n <= total).sort((a, b) => a - b)
  const withGaps = []
  for (let i = 0; i < list.length; i++) {
    withGaps.push(list[i])
    if (i < list.length - 1 && list[i + 1] - list[i] > 1) withGaps.push('…')
  }
  return withGaps
}

function EditDialog({ card, onClose, onSave }) {
  const dialogRef = useRef(null)
  const formId = useId()
  const [es, setEs] = useState('')
  const [en, setEn] = useState('')
  const [error, setError] = useState(null)
  const [trackedId, setTrackedId] = useState(card?.id ?? null)

  // Derived-state pattern: when the parent swaps in a different card,
  // reset the form fields during render (no setState in useEffect).
  if (trackedId !== (card?.id ?? null)) {
    setTrackedId(card?.id ?? null)
    setEs(card?.front?.es ?? '')
    setEn(card?.front?.en ?? '')
    setError(null)
  }

  // Imperative side effect on the <dialog> element (DOM API). This is
  // a legitimate use of useEffect: we're synchronizing an external
  // (non-React) DOM property.
  useEffect(() => {
    const dialog = dialogRef.current
    if (!dialog) return
    if (card && !dialog.open) dialog.showModal()
    else if (!card && dialog.open) dialog.close()
  }, [card])

  useEffect(() => {
    const dialog = dialogRef.current
    if (!dialog) return
    function handleCancel(e) {
      e.preventDefault()
      onClose?.()
    }
    dialog.addEventListener('cancel', handleCancel)
    return () => dialog.removeEventListener('cancel', handleCancel)
  }, [onClose])

  function handleSubmit(e) {
    e.preventDefault()
    const trimmedEs = es.trim()
    const trimmedEn = en.trim()
    if (!trimmedEs || !trimmedEn) {
      setError('Completa ambos campos.')
      return
    }
    onSave?.({ es: trimmedEs, en: trimmedEn })
  }

  return (
    <dialog ref={dialogRef} className="modal" onClose={onClose}>
      <div className="modal-box rounded-2xl border border-base-300 bg-base-100">
        <div className="flex items-start justify-between gap-4">
          <div>
            <h3 className="text-base font-bold uppercase tracking-[0.18em] text-base-content">
              Editar tarjeta
            </h3>
            <p className="mt-1 text-xs text-base-content/70">
              Actualiza el frente (Español / Inglés). El estado SRS se preserva.
            </p>
          </div>
          <button
            type="button"
            onClick={onClose}
            aria-label="Cerrar"
            className="inline-flex size-8 shrink-0 items-center justify-center rounded-full text-base-content/50 transition hover:bg-base-200 hover:text-base-content"
          >
            <X className="size-4" aria-hidden="true" />
          </button>
        </div>

        <form id={formId} onSubmit={handleSubmit} className="mt-4 space-y-3">
          <div>
            <label
              htmlFor={`${formId}-es`}
              className="mb-1 block text-xs font-semibold uppercase tracking-wider text-base-content/70"
            >
              Español
            </label>
            <textarea
              id={`${formId}-es`}
              value={es}
              onChange={(e) => setEs(e.target.value)}
              rows={2}
              className="textarea textarea-bordered w-full resize-none rounded-xl border-base-300 bg-base-200 px-4 py-3 text-base text-base-content placeholder:text-base-content/50 outline-none transition focus:border-primary focus:bg-base-100 focus:ring-2 focus:ring-primary/30"
            />
          </div>
          <div>
            <label
              htmlFor={`${formId}-en`}
              className="mb-1 block text-xs font-semibold uppercase tracking-wider text-base-content/70"
            >
              Inglés
            </label>
            <textarea
              id={`${formId}-en`}
              value={en}
              onChange={(e) => setEn(e.target.value)}
              rows={2}
              className="textarea textarea-bordered w-full resize-none rounded-xl border-base-300 bg-base-200 px-4 py-3 text-base text-base-content placeholder:text-base-content/50 outline-none transition focus:border-primary focus:bg-base-100 focus:ring-2 focus:ring-primary/30"
            />
          </div>
          {error ? (
            <p className="text-sm text-error" role="alert">
              {error}
            </p>
          ) : null}
        </form>

        <div className="modal-action">
          <button
            type="button"
            onClick={onClose}
            className="btn btn-ghost rounded-full normal-case"
          >
            Cancelar
          </button>
          <button
            type="submit"
            form={formId}
            className="btn btn-primary gap-2 rounded-full normal-case"
          >
            <Save className="size-4" aria-hidden="true" />
            Guardar
          </button>
        </div>
      </div>
      <form method="dialog" className="modal-backdrop">
        <button type="submit" aria-label="Cerrar modal" onClick={onClose}>
          close
        </button>
      </form>
    </dialog>
  )
}

function ConfirmDialog({ card, onConfirm, onCancel }) {
  const dialogRef = useRef(null)
  const [trackedId, setTrackedId] = useState(card?.id ?? null)

  // Derived-state pattern: when the parent swaps in a different card,
  // mark it tracked so the dialog can re-open cleanly if re-triggered.
  if (trackedId !== (card?.id ?? null)) {
    setTrackedId(card?.id ?? null)
  }

  // Imperative side effect on the <dialog> element (DOM API). Legitimate
  // useEffect usage — we're synchronizing an external (non-React) DOM
  // property (the open/closed attribute of the native dialog element).
  useEffect(() => {
    const dialog = dialogRef.current
    if (!dialog) return
    if (card && !dialog.open) dialog.showModal()
    else if (!card && dialog.open) dialog.close()
  }, [card])

  useEffect(() => {
    const dialog = dialogRef.current
    if (!dialog) return
    function handleCancel(e) {
      e.preventDefault()
      onCancel?.()
    }
    dialog.addEventListener('cancel', handleCancel)
    return () => dialog.removeEventListener('cancel', handleCancel)
  }, [onCancel])

  const isCustom = card?.type === 'custom'
  const es = card ? cardEs(card) : ''
  const en = card ? cardEn(card) : ''

  return (
    <dialog ref={dialogRef} className="modal" onClose={onCancel}>
      <div className="modal-box rounded-2xl border border-base-300 bg-base-100">
        <div className="flex items-start gap-4">
          <div className="flex size-11 shrink-0 items-center justify-center rounded-full border border-error/30 bg-error/10 text-error">
            <AlertTriangle className="size-5" aria-hidden="true" />
          </div>
          <div className="flex-1 pt-0.5">
            <h3 className="text-base font-bold uppercase tracking-[0.18em] text-base-content">
              Eliminar tarjeta
            </h3>
            <p className="mt-1 text-xs text-base-content/70">
              Esta acción no se puede deshacer. La tarjeta se quitará del mazo
              y su estado SRS se perderá.
            </p>
          </div>
        </div>

        <div className="mt-5 rounded-xl border border-base-300 bg-base-200 p-4">
          <div className="mb-2">
            {isCustom ? (
              <span className="badge badge-primary badge-outline text-[0.65rem] font-bold uppercase tracking-[0.12em]">
                Custom
              </span>
            ) : (
              <span className="badge badge-ghost text-[0.65rem] font-bold uppercase tracking-[0.12em]">
                Verbo
              </span>
            )}
          </div>
          <p className="text-sm font-semibold text-base-content">{es}</p>
          <p className="mt-0.5 text-sm text-base-content/70">{en}</p>
        </div>

        <div className="modal-action">
          <button
            type="button"
            onClick={onCancel}
            className="btn btn-ghost rounded-full normal-case"
          >
            Cancelar
          </button>
          <button
            type="button"
            onClick={onConfirm}
            className="btn gap-2 rounded-full border-none bg-error normal-case text-error-content hover:bg-error/90"
          >
            <Trash2 className="size-4" aria-hidden="true" />
            Eliminar
          </button>
        </div>
      </div>
      <form method="dialog" className="modal-backdrop">
        <button type="submit" aria-label="Cerrar modal" onClick={onCancel}>
          close
        </button>
      </form>
    </dialog>
  )
}
