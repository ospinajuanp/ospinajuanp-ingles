export type Grade = 'fail' | 'hard' | 'good' | 'easy'

export interface SrsCardSrs {
  interval: number
  ef: number
  repetitions?: number
  nextReview?: number
  lastReviewed?: number
  due?: number
  lastReviewedAt?: number
}

export interface SrsVerbCard {
  type: 'verb'
  id: string
  verbKey: string
  infinitivo: { ing: string; esp: string }
  verbId?: number | null
  createdAt?: number
  srs?: SrsCardSrs
}

export interface SrsCustomCard {
  type: 'custom'
  id: string
  front: { es: string; en: string }
  createdAt?: number
  srs?: SrsCardSrs
}

export type SrsCard = SrsVerbCard | SrsCustomCard

export interface SrsStore {
  version: 1
  cards: Record<string, SrsCard>
  order: string[]
}

export interface SrsApi {
  cards: SrsCard[]
  cardsById: SrsStore['cards']
  dueCards: SrsCard[]
  dueCount: number
  totalCount: number
  customCount: number
  verbCount: number
  revision: number
  registerVerb: (verb: { id: number; infinitivo: { ing: string; esp: string } }) => SrsVerbCard | null
  addCustomSentence: (payload: { es: string; en: string }) => SrsCustomCard | null
  gradeCard: (cardId: string, grade: Grade) => void
  removeCard: (cardId: string) => void
  editCustomCard: (cardId: string, payload: { es: string; en: string }) => SrsCustomCard | null
  replaceStore: (incoming: SrsStore | null | undefined) => boolean
}
