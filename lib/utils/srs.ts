import type { Grade, SrsCard, SrsCardSrs, SrsStore } from '@/lib/types/srs'

export const SRS_MIN_EF = 1.3
export const SRS_INITIAL_EF = 2.5

export const SRS_GRADES: readonly Grade[] = ['fail', 'hard', 'good', 'easy'] as const

const GRADE_EF_DELTA: Record<Grade, number> = {
  fail: -0.2,
  hard: -0.1,
  good: 0,
  easy: 0.15,
}

const MS_PER_DAY = 24 * 60 * 60 * 1000

export interface SrsState {
  interval: number
  ef: number
  repetitions: number
  lastReviewed: number | null
  nextReview: number
}

export function createInitialSRSState(initialIntervalDays: number = 0): SrsState {
  return {
    interval: initialIntervalDays,
    ef: SRS_INITIAL_EF,
    repetitions: 0,
    lastReviewed: null,
    nextReview: Date.now() + initialIntervalDays * MS_PER_DAY,
  }
}

export function calculateNextReview(
  currentInterval: number,
  currentEF: number,
  grade: Grade,
): SrsState {
  if (!SRS_GRADES.includes(grade)) {
    throw new Error(`Invalid SRS grade: ${String(grade)}`)
  }

  const now = Date.now()
  const safeInterval = Number.isFinite(currentInterval) ? Math.max(0, currentInterval) : 0
  const safeEF = Number.isFinite(currentEF) ? currentEF : SRS_INITIAL_EF

  if (grade === 'fail') {
    const nextEF = Math.max(SRS_MIN_EF, safeEF + GRADE_EF_DELTA.fail)
    return {
      interval: 1,
      ef: roundEF(nextEF),
      repetitions: 0,
      nextReview: now + MS_PER_DAY,
      lastReviewed: now,
    }
  }

  let nextInterval: number
  if (safeInterval <= 0) nextInterval = 1
  else if (safeInterval < 3) nextInterval = 3
  else nextInterval = Math.round(safeInterval * safeEF)

  const nextEF = Math.max(SRS_MIN_EF, safeEF + GRADE_EF_DELTA[grade])

  return {
    interval: nextInterval,
    ef: roundEF(nextEF),
    repetitions: Math.max(0, Math.floor(safeInterval)) + 1,
    nextReview: now + nextInterval * MS_PER_DAY,
    lastReviewed: now,
  }
}

function roundEF(ef: number): number {
  return Math.round(ef * 100) / 100
}

interface SrsWithDue {
  nextReview?: number
}

export function isDue(state: SrsWithDue | SrsCardSrs | null | undefined, now: number = Date.now()): boolean {
  if (!state || typeof state.nextReview !== 'number') return false
  return state.nextReview <= now
}

export interface CardSrsView {
  srs?: SrsCardSrs
}

export function isCardDue(card: CardSrsView, now: number = Date.now()): boolean {
  return isDue(card.srs, now)
}

export type { Grade, SrsCard, SrsCardSrs, SrsStore }
