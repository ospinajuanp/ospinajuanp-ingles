import type { Metadata, Viewport } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Providers } from './providers'
import Footer from '@/components/Footer'

const inter = Inter({
  subsets: ['latin'],
  weight: ['400', '500', '600', '700', '800'],
  display: 'swap',
  variable: '--font-inter',
})

const SITE_URL = 'https://ospinajuanp-ingles.vercel.app'

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: 'Verbos Inglés — Aprende conjugando',
    template: '%s · Verbos Inglés',
  },
  description:
    'Aprende verbos en inglés con oraciones contextualizadas, conjugaciones y revelación progresiva.',
  applicationName: 'Verbos Inglés',
  keywords: [
    'inglés',
    'verbos',
    'conjugaciones',
    'aprendizaje',
    'repaso espaciado',
  ],
  openGraph: {
    title: 'Verbos Inglés — Aprende conjugando',
    description:
      'Aprende verbos en inglés con oraciones contextualizadas, conjugaciones y revelación progresiva.',
    type: 'website',
    locale: 'es_ES',
    siteName: 'Verbos Inglés',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Verbos Inglés — Aprende conjugando',
    description:
      'Aprende verbos en inglés con oraciones contextualizadas y repetición espaciada.',
  },
  alternates: {
    canonical: '/',
  },
  icons: {
    icon: '/icon.ico',
    shortcut: '/icon.ico',
    apple: '/icon.ico',
  },
}

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  viewportFit: 'cover',
  themeColor: '#f8fafc',
}

const themeScript = `
(function () {
  try {
    var t = localStorage.getItem('ospinajuanp-ingles:theme');
    if (t) document.documentElement.setAttribute('data-theme', t);
  } catch (e) {}
})();
`

const websiteJsonLd = {
  '@context': 'https://schema.org',
  '@type': 'WebSite',
  name: 'Verbos Inglés',
  url: SITE_URL,
  description:
    'Aprende verbos en inglés con oraciones contextualizadas, conjugaciones y repetición espaciada.',
  inLanguage: 'es-ES',
  potentialAction: {
    '@type': 'SearchAction',
    target: `${SITE_URL}/v1/verbs/{search_term_string}`,
    'query-input': 'required name=search_term_string',
  },
}

const organizationJsonLd = {
  '@context': 'https://schema.org',
  '@type': 'Organization',
  name: 'Verbos Inglés',
  url: SITE_URL,
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es" className={inter.variable} suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: themeScript }} />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(websiteJsonLd) }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(organizationJsonLd) }}
        />
      </head>
      <body className={`${inter.className} flex min-h-screen flex-col bg-base-200 text-base-content`}>
        <Providers>
          <div className="flex-1">{children}</div>
          <Footer />
        </Providers>
      </body>
    </html>
  )
}
