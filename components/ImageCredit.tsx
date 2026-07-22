'use client'
import { Camera } from 'lucide-react'

export interface ImageCreditInfo {
  photographer?: string
  photographerUrl?: string
  pexelsUrl?: string
  source?: 'pexels' | 'picsum'
}

interface ImageCreditProps {
  credit?: ImageCreditInfo | null
}

export default function ImageCredit({ credit }: ImageCreditProps) {
  if (credit?.source === 'picsum') {
    return (
      <a
        href="https://picsum.photos"
        target="_blank"
        rel="noopener noreferrer"
        onClick={(e) => e.stopPropagation()}
        className="absolute bottom-2 right-2 z-30 inline-flex items-center gap-1 rounded-full bg-slate-900/60 px-2.5 py-1 text-[0.65rem] font-medium text-white backdrop-blur-sm transition hover:bg-slate-900/80"
        aria-label="Foto vía Lorem Picsum (Unsplash)"
      >
        <Camera className="size-3" aria-hidden="true" />
        <span className="max-w-[10rem] truncate">Lorem Picsum</span>
      </a>
    )
  }

  if (!credit?.photographer) return null

  const href = credit.photographerUrl || credit.pexelsUrl

  return (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      onClick={(e) => e.stopPropagation()}
      className="absolute bottom-2 right-2 z-30 inline-flex items-center gap-1 rounded-full bg-slate-900/60 px-2.5 py-1 text-[0.65rem] font-medium text-white backdrop-blur-sm transition hover:bg-slate-900/80"
      aria-label={`Foto por ${credit.photographer} en Pexels`}
    >
      <Camera className="size-3" aria-hidden="true" />
      <span className="max-w-[10rem] truncate">{credit.photographer}</span>
    </a>
  )
}
