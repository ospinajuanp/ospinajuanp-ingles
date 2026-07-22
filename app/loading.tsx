export default function Loading() {
  return (
    <section className="mx-auto max-w-4xl px-4 py-6 sm:px-6 sm:py-8">
      <div className="rounded-3xl border border-base-300 bg-base-100 p-8 shadow-sm sm:p-12">
        <div className="space-y-8 text-center">
          <div className="mx-auto h-6 w-32 animate-pulse rounded-full bg-base-300 motion-reduce:animate-none" />
          <div className="space-y-3">
            <div className="mx-auto h-12 w-3/4 animate-pulse rounded-lg bg-base-300 motion-reduce:animate-none sm:w-1/2" />
            <div className="mx-auto h-6 w-1/2 animate-pulse rounded-lg bg-base-300 motion-reduce:animate-none" />
          </div>
          <div className="grid w-full grid-cols-1 gap-5 sm:grid-cols-2">
            {Array.from({ length: 2 }).map((_, i) => (
              <div
                key={i}
                className="h-48 animate-pulse rounded-2xl bg-base-200 motion-reduce:animate-none"
              />
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
