export interface TipDescriptor {
  title: string
  text: string
}

export const TIPS: readonly TipDescriptor[] = [
  {
    title: 'Presente simple',
    text: 'Para hábitos (cada día, cada semana) y verdades generales.\nEj: "I work every day" = Trabajo cada día. "Every day" = cada día. "Work" = trabajar.',
  },
  {
    title: 'Presente continuo',
    text: 'Algo que está pasando AHORA, en este momento.\nEj: "I am learning English right now" = Estoy aprendiendo inglés ahora mismo. "Right now" = ahora mismo.',
  },
  {
    title: 'Pasado simple',
    text: 'Cosas terminadas en el pasado. La palabra clave suele ser "yesterday" (ayer) o un año.\nEj: "I visited Paris last year" = Visité París el año pasado. "Visited" = visité. "Last year" = el año pasado.',
  },
  {
    title: 'Pasado continuo',
    text: 'Algo que ESTABA pasando en un momento del pasado (cuando pasó otra cosa).\nEj: "I was cooking when you called" = Estaba cocinando cuando llamaste. "Was cooking" = estaba cocinando. "Called" = llamaste.',
  },
  {
    title: 'Presente perfecto',
    text: 'Pasado con conexión al presente: "I have lived here for 5 years" = Vivo aquí desde hace 5 años (y sigo viviendo).\n"For" = durante. "Years" = años.',
  },
  {
    title: '"Will" vs. "going to"',
    text: '"Will" = decisión espontánea del momento. "Going to" = plan pensado antes.\nEj1: "I\'ll help you" = Te ayudo (recién decidí). \nEj2: "I\'m going to study tonight" = Voy a estudiar esta noche (ya lo tenía planeado).',
  },
  {
    title: '"Would"',
    text: 'Tres usos: hipótesis, pedidos corteses, y hábitos del pasado.\nEj1: "I would like a coffee" = Me gustaría un café (pedido cortés).\nEj2: "When I was a kid, I would play outside" = Cuando era chico, jugaba afuera. "Would" = solía.',
  },
  {
    title: '"Used to"',
    text: 'Cosas que hacías antes pero YA NO haces.\nEj: "I used to play soccer" = Antes jugaba fútbol (ya no). "Used to" = antes solía.',
  },
  {
    title: '"Do / does"',
    text: 'Para preguntas y negaciones en presente.\nEj: "Do you speak English?" = ¿Hablas inglés? "Speak" = hablar.',
  },
  {
    title: '"Did"',
    text: 'Para preguntas y negaciones en pasado.\nEj: "I didn\'t go" = No fui. "Didn\'t" = no (pasado). "Go" = ir.',
  },
  {
    title: '"Can"',
    text: 'Habilidad (saber hacer algo) o permiso informal.\nEj1: "I can swim" = Sé nadar (habilidad). \nEj2: "Can I sit here?" = ¿Puedo sentarme aquí? (permiso).',
  },
  {
    title: '"Should"',
    text: 'Consejo o sugerencia suave. Equivale a "deberías".\nEj: "You should rest" = Deberías descansar.\n"Should" = deberías. "Rest" = descansar.',
  },
  {
    title: '"Must"',
    text: 'Obligación FUERTE (norma, ley, algo muy importante).\nEj: "You must wear a seatbelt" = Debes usar cinturón (es obligatorio). "Must" = debes. "Seatbelt" = cinturón de seguridad.',
  },
  {
    title: '"Have to"',
    text: 'Obligación externa, no necesariamente tuya (la empresa, la escuela, etc.).\nEj: "I have to work tomorrow" = Tengo que trabajar mañana (mi jefe me obliga).',
  },
  {
    title: '"In", "on", "at" (lugar)',
    text: '"In" = dentro de un espacio. "On" = sobre una superficie. "At" = punto exacto.\nEj1: "in the room" = en la habitación.\nEj2: "on the table" = sobre la mesa.\nEj3: "at the door" = en la puerta.',
  },
  {
    title: '"By" vs. "until"',
    text: '"By" = NO MÁS TARDE de (fecha límite). "Until" = DESDE AHORA HASTA ese momento.\nEj1: "Finish by Friday" = Termina antes del viernes.\nEj2: "Wait until 5 PM" = Espera hasta las 5.',
  },
  {
    title: '"For" vs. "since"',
    text: '"For" = DURACIÓN (cuánto). "Since" = PUNTO DE INICIO (desde cuándo).\nEj1: "for 3 years" = durante 3 años.\nEj2: "since 2020" = desde 2020.',
  },
  {
    title: '"In", "on", "at" (tiempo)',
    text: '"In" = meses, años, estaciones. "On" = días. "At" = hora exacta.\nEj1: "in March" = en marzo.\nEj2: "on Monday" = el lunes.\nEj3: "at 3 PM" = a las 3 PM.',
  },
  {
    title: '"A" vs. "an"',
    text: '"An" antes de sonido de VOCAL. "A" en los demás casos.\nEj1: "an apple" = una manzana (empieza con vocal). \nEj2: "an hour" = una hora (la "h" es muda, suena vocal). \nEj3: "a book" = un libro.',
  },
  {
    title: '"The"',
    text: 'Se usa cuando AMBOS saben a qué nos referimos (ya se mencionó, o es único).\nEj1: "the book I bought" = el libro que compré (ambos saben cuál).\nEj2: "the sun" = el sol (hay uno solo).',
  },
  {
    title: 'Plural regular',
    text: 'Casi siempre se añade "-s".\nSi termina en -s, -sh, -ch, -x o -z, se añade "-es".\nEj1: "book → books". \nEj2: "bus → buses" (autobús → autobuses).',
  },
  {
    title: 'Plural irregular',
    text: 'Hay que memorizarlos, no siguen regla.\nLos más comunes:\n• child → children (niño → niños)\n• person → people (persona → personas)\n• foot → feet (pie → pies)\n• tooth → teeth (diente → dientes)\n• mouse → mice (ratón → ratones)',
  },
  {
    title: '"Hacer" no siempre es "do"',
    text: '"Do" = hacer en general. "Make" = construir, crear, producir.\nEj: "I made a cake" = Hice un pastel (lo creé). NO se dice "I did a cake".\nTruco: "make food, make a plan, make a mistake".',
  },
  {
    title: '"Ser" vs. "estar"',
    text: 'En inglés "to be" cubre los dos casos.\n• Identidad/profesión: "I am a doctor" = Soy médico.\n• Estado/animo: "I am tired" = Estoy cansado.',
  },
  {
    title: '"Tener" ≠ "have"',
    text: 'La edad NO usa "tener", usa "to be".\nEj: "I am 25 years old" = Tengo 25 años. NO "I have 25 years".\n"Age" = edad. "Years old" = años (de edad).',
  },
  {
    title: '"Hace frío"',
    text: 'En inglés se usa "to be" para el clima, no "to make".\nEj: "It is cold" = Hace frío. NO "It makes cold".\n"It is hot" = Hace calor. "It is sunny" = Hace sol.',
  },
  {
    title: '"Tengo hambre / sed"',
    text: 'En inglés se usan adjetivos, no el verbo "tener".\n• "I am hungry" = Tengo hambre (hambriento).\n• "I am thirsty" = Tengo sed (sediento).\nNO "I have hungry".',
  },
  {
    title: '"Desde hace"',
    text: 'Se construye con presente perfecto, NO con "hacer".\nEj: "I have lived here for 3 years" = Vivo aquí desde hace 3 años.\n"Aquí NO se traduce "for" como "por".',
  },
  {
    title: '"Get up"',
    text: 'Levantarse de la cama por la mañana.\nEj: "I get up at 7 AM" = Me levanto a las 7 AM.\n"Get up" = levantarse. "At 7 AM" = a las 7 de la mañana.',
  },
  {
    title: '"Wake up"',
    text: 'Despertarse. Es la acción de abrir los ojos; "get up" es levantarte.\nEj: "I wake up at 6:30 and get up at 7" = Me despierto a las 6:30 y me levanto a las 7.',
  },
  {
    title: '"Look for"',
    text: 'Buscar algo (intentar encontrarlo).\nEj: "I\'m looking for my keys" = Estoy buscando mis llaves. "Keys" = llaves.',
  },
  {
    title: '"Find out"',
    text: 'Averiguar / descubrir algo (por investigación o casualidad).\nEj: "I found out she moved to Madrid" = Descubrí que se mudó a Madrid. "Moved" = se mudó.',
  },
  {
    title: '"Give up"',
    text: 'Rendirse.\nEj: "Don\'t give up!" = ¡No te rindas!\nSimilar a un conocido meme: "never give up" = nunca te rindas.',
  },
  {
    title: '"Run out of"',
    text: 'Quedarse sin algo (se acabó).\nEj: "We ran out of milk" = Se nos acabó la leche. "Milk" = leche.',
  },
  {
    title: 'Orden de adjetivos',
    text: 'En inglés los adjetivos van en un orden fijo (si hay varios):\nopinión + tamaño + edad + forma + color + origen + material + uso.\nEj: "a beautiful small old red car" = un auto rojo viejo pequeño hermoso.\nEn la práctica: máximo 2-3 adjetivos, sino suena raro.',
  },
  {
    title: 'Cómo hacer una pregunta',
    text: 'Estructura: auxiliar + sujeto + verbo?\nSi no hay auxiliar (presente/pasado simple), se añade "do" / "did".\nEj: "Do you like coffee?" = ¿Te gusta el café? "Like" = gustar.',
  },
  {
    title: 'Negación',
    text: 'Se pone "not" DESPUÉS del primer auxiliar.\nEj: "I do not know" = No sé. → Contraído: "I don\'t know".\n"Do not / don\'t" = no (auxiliar).',
  },
  {
    title: 'Respuestas cortas',
    text: 'Se responde con "Yes/No" + sujeto + MISMO AUXILIAR de la pregunta. NO repetir el verbo principal.\n• "Do you like coffee?" → "Yes, I do" (sí) / "No, I don\'t" (no).\n• "Can you swim?" → "Yes, I can".',
  },
  {
    title: 'Pronunciación: "th"',
    text: 'No suena como "s" ni como "t". Lengua entre los dientes y sopla aire.\nEj: "think" (piensa, /θɪŋk/). "three" (tres, /θriː/).\nPractica con la frase: "three thin thieves" (tres ladrones flacos).',
  },
  {
    title: 'Letras mudas',
    text: 'Algunas letras se escriben pero NO se pronuncian.\n• "K" en "knife" (cuchillo).\n• "W" en "write" (escribir).\n• "B" en "doubt" (duda).\n• "H" en "hour" (hora), "honest" (honesto).',
  },
  {
    title: '"-ed" no siempre es "-ed"',
    text: 'La terminación de pasado cambia según el sonido anterior:\n• después de sonido sordo: /t/ → "worked" = /wɜːrkt/.\n• después de sonido sonoro: /d/ → "played" = /pleɪd/.\n• después de /t/ o /d/: /ɪd/ → "wanted" = /ˈwɑːntɪd/.',
  },
  {
    title: '"-ough"',
    text: 'Una de las combinaciones más raras del inglés: SIEMPRE se pronuncia distinto.\n• "though" (aunque) = /ðoʊ/.\n• "through" (a través de) = /θruː/.\n• "thought" (pensé) = /θɔːt/.\n• "tough" (difícil) = /tʌf/.\nNo hay regla, hay que memorizar.',
  },
  {
    title: '"Actually"',
    text: 'Significa "de hecho" o "en realidad", NO "actualmente".\nPara "actualmente" se usa "currently".\nEj: "I actually live in Spain" = De hecho vivo en España.\n"Currently" = actualmente (ahora).',
  },
  {
    title: '"Eventually"',
    text: 'Significa "al final" o "finalmente", NO "eventualmente".\nPara "eventualmente" (a veces) se usa "sometimes" / "occasionally".\nEj: "Eventually I passed the exam" = Al final aprobé el examen.',
  },
  {
    title: '"Realize"',
    text: 'Significa "darse cuenta de algo", NO "realizar" (que en inglés es "carry out").\nEj: "I realized I was wrong" = Me di cuenta de que estaba equivocado.\n"Carry out" = llevar a cabo, ejecutar.',
  },
  {
    title: '"Succeed"',
    text: 'Significa "tener éxito", NO "suceder" (que es "to happen").\nEj: "I succeeded in passing the exam" = Logré aprobar el examen.\n"Happen" = suceder, ocurrir.',
  },
  {
    title: '"Attend"',
    text: 'Significa "asistir a un evento" (ir a una boda, clase, reunión).\nNO es "atender" (que sería "assist / help" a un cliente).\nEj: "I attended the meeting" = Asistí a la reunión.\n"Assist" = ayudar a alguien.',
  },
  {
    title: 'Sensación + -ing',
    text: 'Verbos como "enjoy", "avoid" y "keep" van seguidos del gerundio (-ing), no del infinitivo.\n• "I enjoy cooking" = Disfruto cocinar.\n• "I avoid eating sugar" = Evito comer azúcar.\n• "I keep practicing" = Sigo practicando.\n"Keep" = seguir / continuar.',
  },
  {
    title: '"Want" vs. "want to"',
    text: '"Want" + OBJETO (cosa). "Want to" + ACCIÓN (verbo).\n• "I want a coffee" = Quiero un café (objeto).\n• "I want to study" = Quiero estudiar (acción).\nSi pones "to study" = estudiar.',
  },
  {
    title: 'Series con subtítulos',
    text: 'Mira series con subtítulos en INGLÉS.\nAl principio alternando inglés/español; cuando te canses del español, déjalos solo en inglés. Te acostumbras al oído rápido.',
  },
  {
    title: 'Habla contigo mismo',
    text: 'Describe en voz alta lo que ves mientras caminas.\nEj: "I see a red car, a tall building, two dogs…" = Veo un auto rojo, un edificio alto, dos perros…\nNo te juzgues, nadie te escucha.',
  },
  {
    title: 'Canciones y letras',
    text: 'Busca la letra ("lyrics") y canta siguiendo. Trabajas vocabulario, ritmo y pronunciación a la vez.\nPractica primero leyendo, después canta. "Lyrics" = letra (de canción).',
  },
  {
    title: 'Aprende frases hechas',
    text: 'Memoriza frases completas ("chunks"), NO palabra por palabra.\n• "How\'s it going?" = ¿Qué tal? (saludo informal).\n• "What\'s up?" = ¿Qué hay? (más informal aún).\nSuenan naturales porque así hablan los nativos.',
  },
]

export function selectTip(seed: number = 0): TipDescriptor {
  const total = TIPS.length
  const idx = ((seed % total) + total) % total
  return TIPS[idx] as TipDescriptor
}
