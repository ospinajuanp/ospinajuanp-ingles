export default function HeroIllustration({ className = '' }) {
  return (
    <svg
      viewBox="0 0 1200 320"
      preserveAspectRatio="xMidYMid slice"
      xmlns="http://www.w3.org/2000/svg"
      role="img"
      aria-label="Camino forestal con luz solar suave"
      className={className}
    >
      <defs>
        <linearGradient id="hero-sky" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#fff7ed" />
          <stop offset="55%" stopColor="#fef3c7" />
          <stop offset="100%" stopColor="#fcd9a5" />
        </linearGradient>
        <radialGradient id="hero-glow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#fffbeb" stopOpacity="0.95" />
          <stop offset="55%" stopColor="#fef3c7" stopOpacity="0.55" />
          <stop offset="100%" stopColor="#fef3c7" stopOpacity="0" />
        </radialGradient>
        <linearGradient id="hero-ridge-far" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#cbd5e1" />
          <stop offset="100%" stopColor="#94a3b8" />
        </linearGradient>
        <linearGradient id="hero-ridge-near" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#94a3b8" />
          <stop offset="100%" stopColor="#475569" />
        </linearGradient>
        <linearGradient id="hero-path" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#fef3c7" />
          <stop offset="100%" stopColor="#fde68a" />
        </linearGradient>
      </defs>

      <rect width="1200" height="320" fill="url(#hero-sky)" />

      <circle cx="980" cy="100" r="210" fill="url(#hero-glow)" />
      <circle cx="980" cy="100" r="44" fill="#fffbeb" />

      <g opacity="0.32" fill="#ffffff">
        <polygon points="980,100 1200,320 1200,120" />
        <polygon points="980,100 600,320 0,260 0,180" />
      </g>

      <path
        d="M0 198 Q160 168 320 184 T640 178 T960 174 T1200 178 L1200 320 L0 320 Z"
        fill="url(#hero-ridge-far)"
        opacity="0.55"
      />
      <path
        d="M0 248 Q200 228 420 240 T840 234 T1200 240 L1200 320 L0 320 Z"
        fill="url(#hero-ridge-near)"
        opacity="0.7"
      />

      <g fill="#475569" opacity="0.6">
        <polygon points="120,238 108,200 132,200" />
        <polygon points="160,242 150,206 170,206" />
        <polygon points="200,234 188,194 212,194" />
        <polygon points="240,240 230,206 250,206" />
        <polygon points="900,236 885,196 915,196" />
        <polygon points="980,240 970,202 990,202" />
        <polygon points="1050,234 1038,192 1062,192" />
      </g>

      <path
        d="M510 320 L582 208 L618 208 L690 320 Z"
        fill="url(#hero-path)"
      />
      <path
        d="M536 320 L585 213 L615 213 L664 320 Z"
        fill="#fffbeb"
        opacity="0.7"
      />

      <g fill="#0f172a">
        <polygon points="40,320 80,160 0,160" />
        <rect x="32" y="270" width="16" height="50" fill="#27272a" />
        <polygon points="40,250 80,160 0,160 40,180 0,180 80,250" opacity="0.6" />
      </g>

      <g fill="#1e293b">
        <polygon points="180,320 218,170 142,170" />
        <rect x="172" y="270" width="16" height="50" fill="#3f3f46" />
      </g>

      <g fill="#1e293b">
        <polygon points="1010,320 1052,150 968,150" />
        <rect x="1000" y="270" width="16" height="50" fill="#3f3f46" />
      </g>

      <g fill="#0f172a">
        <polygon points="1140,320 1180,170 1100,170" />
      </g>

      <g fill="none" stroke="#64748b" strokeWidth="1.5" opacity="0.45" strokeLinecap="round">
        <path d="M430 70 q5 -7 10 0 q5 -7 10 0" />
        <path d="M480 50 q4 -6 8 0 q4 -6 8 0" />
        <path d="M520 78 q5 -7 10 0 q5 -7 10 0" />
      </g>
    </svg>
  )
}
