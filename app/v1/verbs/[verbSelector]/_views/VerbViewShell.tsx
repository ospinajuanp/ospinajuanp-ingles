'use client'

import { useVerbosContext } from '@/components/providers/VerbContext'
import VerbCard from '@/components/VerbCard'
import type { ConjugationGridEntry, FlatVerb, OracionFillable, Verb } from '@/lib/types/verbs'

interface VerbViewShellProps {
  initialVerb: FlatVerb
}

function asSentencePillData(oraciones: readonly OracionFillable[]) {
  return oraciones.map((o) => ({
    timeKey: o.timeKey,
    data: { ing: o.data.ing, esp: o.data.esp },
  }))
}

export function VerbViewShell({ initialVerb }: VerbViewShellProps) {
  const verbos = useVerbosContext()

  const showSkeleton = verbos?.loading && !verbos?.currentVerb
  const effectiveVerb: Verb | null = verbos?.currentVerb ?? initialVerb.verb
  const effectiveCurrent: FlatVerb | null = verbos?.current ?? initialVerb
  const effectiveOraciones = (verbos?.oraciones ?? []) as readonly OracionFillable[]
  const effectiveEntries = verbos?.conjugationEntries ?? []

  if (showSkeleton) return <LoadingSkeleton />

  return (
    <main className="mx-auto max-w-4xl px-4 py-6 sm:px-6 sm:py-8">
      <VerbCard
        current={effectiveCurrent}
        currentVerb={effectiveVerb}
        oraciones={asSentencePillData(effectiveOraciones)}
        conjugationEntries={effectiveEntries as readonly ConjugationGridEntry[]}
        currentIndex={verbos?.currentIndex ?? -1}
        total={verbos?.total ?? 0}
        onPrev={verbos?.prev}
        onNext={verbos?.next}
        onShuffle={verbos?.shuffle}
        onEnriched={verbos?.reportEnrichment}
      />
    </main>
  )
}

function LoadingSkeleton() {
  return (
    <main className="mx-auto max-w-4xl px-4 py-6 sm:px-6 sm:py-8">
      <div className="overflow-hidden rounded-2xl border border-base-300 bg-base-100 shadow-sm">
        <div className="h-44 w-full animate-pulse bg-base-300 motion-reduce:animate-none sm:h-52 md:h-56" />
        <div className="space-y-8 p-5 sm:p-7 md:p-8">
          <div className="space-y-3 text-center">
            <div className="mx-auto h-12 w-40 animate-pulse rounded-lg bg-base-300 motion-reduce:animate-none" />
            <div className="mx-auto h-6 w-32 animate-pulse rounded-lg bg-base-300 motion-reduce:animate-none" />
          </div>
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
            {Array.from({ length: 6 }).map((_, i) => (
              <div
                key={i}
                className="h-16 animate-pulse rounded-xl bg-base-300 motion-reduce:animate-none"
              />
            ))}
          </div>
          <div className="space-y-2.5">
            {Array.from({ length: 3 }).map((_, i) => (
              <div
                key={i}
                className="h-24 animate-pulse rounded-xl bg-base-300 motion-reduce:animate-none"
              />
            ))}
          </div>
          <div className="flex justify-center">
            <div className="h-12 w-64 animate-pulse rounded-full bg-base-300 motion-reduce:animate-none" />
          </div>
        </div>
      </div>
    </main>
  )
}
