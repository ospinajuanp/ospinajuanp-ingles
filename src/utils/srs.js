// SM-2 Spaced Repetition Algorithm.
//
// Pure functions only — no I/O, no React, no localStorage. Given the
// current interval (in days) and the current Ease Factor (EF), return
// the next state after the user grades the card.
//
// References:
//   - https://super-memory.com/english/ol/sm2.htm
//   - Piotr Wozniak (1985-1990)
//
// Conventions of this codebase:
//   - Interval is always expressed in WHOLE DAYS (integer, ≥ 0).
//   - `nextReview` is a millisecond epoch timestamp.
//   - Never mutate input objects — return a new SRS state.

export const SRS_MIN_EF = 1.3
export const SRS_INITIAL_EF = 2.5
export const SRS_GRADES = ['fail', 'hard', 'good', 'easy']

// EF delta applied per grade. fail = blackout, hard = success-but-struggled,
// good = clean recall, easy = instant recall.
const GRADE_EF_DELTA = {
  fail: -0.2,
  hard: -0.1,
  good: 0,
  easy: 0.15,
}

const MS_PER_DAY = 24 * 60 * 60 * 1000

/**
 * Build the initial SRS state for a brand-new card.
 * First review is scheduled `initialIntervalDays` from now (default 0 → today).
 */
export function createInitialSRSState(initialIntervalDays = 0) {
  return {
    interval: initialIntervalDays,
    ef: SRS_INITIAL_EF,
    repetitions: 0,
    lastReviewed: null,
    nextReview: Date.now() + initialIntervalDays * MS_PER_DAY,
  }
}

/**
 * Pure SM-2 step (4-level grading).
 *
 * Fail path: interval resets to 1 day, EF drops by 0.20 (floor 1.3),
 *   repetitions counter resets to 0.
 * Success path (hard / good / easy): interval grows by *EF (1d → 3d
 *   ramp on first two reviews, then `round(prev * EF)` thereafter),
 *   repetitions increments, EF adjusts by the grade delta (hard -0.10,
 *   good 0, easy +0.15) with the same 1.3 floor.
 *
 * @param {number} currentInterval  Interval in days used for the LAST review.
 * @param {number} currentEF        Ease Factor BEFORE grading this review.
 * @param {'fail'|'hard'|'good'|'easy'} grade  Quality of this review.
 * @returns {{ interval: number, ef: number, repetitions: number,
 *             nextReview: number, lastReviewed: number }}
 */
export function calculateNextReview(currentInterval, currentEF, grade) {
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

  // Success path (hard / good / easy): same interval formula for all,
  // different EF delta. Keeps the recovery slope predictable across grades.
  let nextInterval
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

function roundEF(ef) {
  return Math.round(ef * 100) / 100
}

/**
 * A card is due when its `nextReview` is in the past (or right now).
 */
export function isDue(state, now = Date.now()) {
  if (!state || typeof state.nextReview !== 'number') return false
  return state.nextReview <= now
}
