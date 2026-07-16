export function selectTip(seed = 0) {
  const total = CONJUGATION_TIPS.length
  return CONJUGATION_TIPS[((seed % total) + total) % total]
}

export const CONJUGATION_TIPS = [
  {
    title: '¿Sabías que…?',
    text: 'El participio se combina con “have” para formar los tiempos perfectos.',
  },
  {
    title: '¿Sabías que…?',
    text: '“Will” expresa decisiones espontáneas; “would”, hipótesis o cortesía.',
  },
  {
    title: '¿Sabías que…?',
    text: 'El gerundio (-ing) se usa con “be” para acciones en curso.',
  },
  {
    title: '¿Sabías que…?',
    text: 'Irás notando patrones entre verbos regulares e irregulares con la práctica.',
  },
  {
    title: '¿Sabías que…?',
    text: 'Pronunciar las conjugaciones en voz alta ayuda a fijarlas en memoria.',
  },
  {
    title: '¿Sabías que…?',
    text: 'Lee cada oración en inglés antes de mirar la traducción para entrenar el oído.',
  },
  {
    title: '¿Sabías que…?',
    text: 'Con frecuencia el condicional se usa para consejos amables (I would…).',
  },
]
