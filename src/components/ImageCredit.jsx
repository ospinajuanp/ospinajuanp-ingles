export default function ImageCredit({ credit }) {
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
      <svg
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        className="size-3"
        aria-hidden="true"
      >
        <path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z" />
        <circle cx="12" cy="13" r="3.5" />
      </svg>
      <span className="max-w-[10rem] truncate">{credit.photographer}</span>
    </a>
  )
}