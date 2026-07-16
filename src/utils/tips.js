export function selectTip(seed = 0) {
  const total = TIPS.length
  return TIPS[((seed % total) + total) % total]
}

export const TIPS = [
  // Tiempos verbales
  {
    title: 'Presente simple',
    text: 'Hábitos, rutinas y verdades: “I work every day”, “Water boils at 100°C”.',
  },
  {
    title: 'Presente continuo',
    text: 'Acciones que pasan ahora mismo: “I am learning English right now”.',
  },
  {
    title: 'Pasado simple',
    text: 'Cosas terminadas en el pasado: “I visited Paris last year”.',
  },
  {
    title: 'Pasado continuo',
    text: 'Algo que estaba pasando en un momento del pasado: “I was cooking when you called”.',
  },
  {
    title: 'Presente perfecto',
    text: 'Pasado con conexión al presente: “I have lived here for 5 years”.',
  },
  {
    title: 'Will vs. going to',
    text: '“Will” = decisión espontánea. “Going to” = plan hecho antes.',
  },
  {
    title: '“Would”',
    text: 'Hipótesis, cortesía y hábitos del pasado: “I would like a coffee”.',
  },
  {
    title: '“Used to”',
    text: 'Cosas que hacías antes pero ya no: “I used to play soccer”.',
  },
  // Verbos auxiliares básicos
  {
    title: 'Do / does',
    text: 'Para preguntas y negaciones en presente: “Do you speak English?”',
  },
  {
    title: 'Did',
    text: 'Para preguntas y negaciones en pasado: “I didn’t go”.',
  },
  {
    title: 'Can',
    text: 'Habilidad o permiso informal: “I can swim”, “Can I sit here?”.',
  },
  {
    title: 'Should',
    text: 'Consejo o sugerencia suave: “You should rest”.',
  },
  {
    title: 'Must',
    text: 'Obligación fuerte: “You must wear a seatbelt”.',
  },
  {
    title: 'Have to',
    text: 'Obligación externa (no necesariamente tuya): “I have to work tomorrow”.',
  },
  // Preposiciones
  {
    title: '“In”, “on”, “at”',
    text: 'In = dentro. On = sobre. At = punto exacto (hora, lugar preciso).',
  },
  {
    title: '“By” vs. “until”',
    text: '“By” = no más tarde de. “Until” = desde ahora hasta ese momento.',
  },
  {
    title: '“For” vs. “since”',
    text: '“For” = duración (“for 3 years”). “Since” = punto de inicio (“since 2020”).',
  },
  {
    title: '“In”, “on”, “at” (tiempo)',
    text: 'In = meses/años. On = días. At = hora exacta.',
  },
  // Artículos y plurales
  {
    title: 'A vs. an',
    text: '“An” antes de sonido de vocal: “an apple”, “an hour” (h muda).',
  },
  {
    title: 'The',
    text: 'Se usa cuando el oyente sabe a qué nos referimos: “the book I bought”.',
  },
  {
    title: 'Plural regular',
    text: 'Añade -s: book → books. Termina en -s, -sh, -ch, -x, -z → -es: bus → buses.',
  },
  {
    title: 'Plural irregular',
    text: 'Los más comunes: child → children, person → people, foot → feet, tooth → teeth.',
  },
  // Errores frecuentes de hispanohablantes
  {
    title: '“Hacer” no siempre es “do”',
    text: '“Do” = hacer genérico. “Make” = construir/crear. “I made a cake”, no “I did a cake”.',
  },
  {
    title: '“Ser” vs. “estar”',
    text: '“To be” cubre los dos. “I am tired” (estado) vs. “I am a doctor” (identidad).',
  },
  {
    title: '“Tener” ≠ “have”',
    text: '“I am 25 years old”, NO “I have 25 years”. La edad usa “to be”.',
  },
  {
    title: '“Hace frío”',
    text: 'Se dice “It is cold”, NO “It makes cold”. El inglés usa el verbo “to be” para el clima.',
  },
  {
    title: '“Tengo hambre”',
    text: 'Se dice “I am hungry”, NO “I have hungry”. Adjetivos, no verbo.',
  },
  {
    title: '“Desde hace”',
    text: 'Se construye con presente perfecto: “I have lived here for 3 years”.',
  },
  // Phrasal verbs más comunes
  {
    title: '“Get up”',
    text: 'Levantarse. “I get up at 7 a.m.”',
  },
  {
    title: '“Wake up”',
    text: 'Despertarse. Mismo uso que “get up”, pero más enfático.',
  },
  {
    title: '“Look for”',
    text: 'Buscar. “I’m looking for my keys”.',
  },
  {
    title: '“Find out”',
    text: 'Averiguar / descubrir. “I found out she moved to Madrid”.',
  },
  {
    title: '“Give up”',
    text: 'Rendirse. “Don’t give up!”.',
  },
  {
    title: '“Run out of”',
    text: 'Quedarse sin algo. “We ran out of milk”.',
  },
  // Orden y estructura
  {
    title: 'Orden adjetivos',
    text: 'Opinion-size-age-shape-color-origin-material-purpose. En la práctica: “a beautiful small old red car”.',
  },
  {
    title: 'Pregunta en inglés',
    text: 'Estructura: auxiliary + subject + verb? “Do you like coffee?”',
  },
  {
    title: 'Negación',
    text: '“not” después del auxiliar: “I do not know” → “I don’t know”.',
  },
  {
    title: 'Yes / No',
    text: 'Yes + sujeto + auxiliar: “Yes, I do”. NO “Yes, I know”.',
  },
  // Pronunciación y ortografía
  {
    title: 'Pronunciación: “th”',
    text: '“Think”, “three”. Lengua entre los dientes, sopla aire. Suena distinto a “s” o “t”.',
  },
  {
    title: 'Letra muda',
    text: '“K” en knife, “W” en write, “B” en doubt. La letra está pero no se pronuncia.',
  },
  {
    title: '“-ed” no siempre es “-ed”',
    text: '“Worked” = /t/, “Played” = /d/, “Wanted” = /ɪd/. La terminación cambia según el sonido anterior.',
  },
  {
    title: '“ough”',
    text: 'Una de las combinaciones más raras: “though”, “through”, “thought”, “tough” — todas se pronuncian distinto.',
  },
  // Vocabulario útil
  {
    title: '“Actually”',
    text: 'Significa “de hecho” o “en realidad”, NO “actualmente”. Para eso es “currently”.',
  },
  {
    title: '“Eventually”',
    text: '“Finalmente” o “al final”, NO “eventualmente” en sentido de “ocasionalmente”.',
  },
  {
    title: '“Realize”',
    text: 'Darse cuenta de algo. NO “realizar” (que sería “carry out”). “I realized I was wrong”.',
  },
  {
    title: '“Succeed”',
    text: 'Tener éxito. NO “suceder” (que es “to happen”). “I succeeded in passing the exam”.',
  },
  {
    title: '“Attend”',
    text: 'Asistir a un evento. NO “atender” (que es “to assist/help a customer”).',
  },
  {
    title: 'Sensación + -ing',
    text: '“I enjoy cooking”, “I avoid eating sugar”, “I keep practicing”. Verbo + gerundio.',
  },
  {
    title: '“Want to” vs. “want”',
    text: '“I want a coffee” (quiero un café, objeto). “I want to study” (quiero estudiar, acción).',
  },
  // Cultura y práctica
  {
    title: 'Series con subtítulos',
    text: 'Mira con subtítulos en inglés. Al principio交替 inglés/español, después solo inglés.',
  },
  {
    title: 'Habla contigo mismo',
    text: 'Describe lo que ves en inglés mientras caminas: “I see a red car, a tall building…”.',
  },
  {
    title: 'Canciones y letras',
    text: 'Busca la letra (lyrics) y canta siguiendo. Trabaja vocabulario, ritmo y pronunciación a la vez.',
  },
  {
    title: 'Aprende chunks',
    text: 'Memoriza frases hechas, no palabras sueltas. “How’s it going?”, “What’s up?” — no las analiza palabra por palabra.',
  },
]