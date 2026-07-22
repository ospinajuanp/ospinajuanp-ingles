export default function Loading() {
  return (
    <div className="mx-auto max-w-4xl px-4 py-6 sm:px-6 sm:py-8">
      <div className="mb-6 h-9 w-24 animate-pulse rounded-full bg-base-200 motion-reduce:animate-none" />
      <div className="mb-6 space-y-2">
        <div className="h-9 w-1/3 animate-pulse rounded-lg bg-base-200 motion-reduce:animate-none" />
        <div className="h-5 w-1/2 animate-pulse rounded bg-base-200 motion-reduce:animate-none" />
      </div>
      <div className="mb-6 grid grid-cols-2 gap-3 sm:grid-cols-4">
        {Array.from({ length: 4 }).map((_, i) => (
          <div
            key={i}
            className="h-20 animate-pulse rounded-2xl bg-base-200 motion-reduce:animate-none"
          />
        ))}
      </div>
      <div className="h-72 animate-pulse rounded-3xl bg-base-200 motion-reduce:animate-none" />
    </div>
  )
}
