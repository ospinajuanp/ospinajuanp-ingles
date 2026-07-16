# Guía de Estilo — Generación de Verbos

## Reglas obligatorias

### 1. Pronombre `eso` (slot condicional)
Solo usar `eso / It / That` cuando el verbo lo acepte de forma **natural**. Para verbos incompatibles, usar un sujeto concreto variable:
- ✅ Verbos compatibles con `It/eso`: `work, change, happen, exist, depend, matter, count, affect, add (complexity), appear, charge (interés)`
- ❌ Verbos incompatibles: usar sujetos como `That, The system, The app, This approach, The user, The team`

### 2. Un significado por verbo
Elegir **UN solo significado principal** y mantenerlo consistente en las 6 oraciones.
- ❌ Mezclar `preguntar` y `pedir` para `ask`
- ❌ Mezclar `importar` y `preocuparse` para `care`
- ✅ Decidir uno y aplicar en infinitivo + conjugaciones + oraciones

### 3. Conjugación español coherente
- El infinitivo debe **concordar** con las conjugaciones generadas (futuro/condicional mecánico)
- Verificar: si infinitivo es X, futuro debe ser `Xá` (ar) o `Xerá` (er/ir); condicional `Xría` o `Xería`
- Si el infinitivo tiene forma compuesta (`pedir prestado`), ajustar manualmente

### 4. Variedad de contextos
- No usar siempre `I [verb] the [noun]`
- Variar: adverbios (`often, carefully`), frases preposicionales (`in the morning, after lunch`), escenarios reales
- Distribuir 6 oraciones en al menos 3-4 contextos distintos

### 5. Inglés natural
- Usar `That` cuando `It` suene artificial
- Frases hechas / modismos cuando aplique (`bounce an idea`, `carry forward`)
- No abusar de "We will..." o "I [verb]..."

### 6. Traducción español natural (NO literal)
- Equivalencias culturales, no calcos
- Ej: `carry forward` ≠ `llevar adelante` → `continuar` o `seguir`
- Ej: `bounce an idea` ≠ `considerar` → `intercambiar ideas` o `debatir`

### 7. Errores a evitar (lecciones aprendidas)
| Error | Corrección |
|---|---|
| `I care about you` / `Yo importo por ti` | `Me preocupo por ti` |
| `ask` mezclando pedir/preguntar | Elegir uno (preferir `pedir`) |
| `bounce the idea` / `considerar la idea` | `debatir la idea` o cambiar contexto |
| `carry forward` / `seguiremos adelante` | Mantener sentido: `continuaremos` |
| `It would attack the weakness` | `That would exploit the weakness` |
| `belong` futuro `pertenecemos` | `perteneceremos` |

## Plantilla de oración por slot

| Slot | Pronombre | Tiempo en inglés | Tiempo en español |
|---|---|---|---|
| `infinitivo` | yo | Presente simple | Presente simple |
| `pasadoSimple` | tu | Pasado simple | Pretérito |
| `participio` | el_ella | Presente perfecto (`have + pp`) | Pretérito perfecto (`ha + pp`) |
| `gerundio` | ellos | Presente continuo (`are + -ing`) | Gerundio (`están + -ando/-iendo`) |
| `futuro` | nosotros | `will + verb` | Futuro simple |
| `condicional` | eso/that | `would + verb` | Condicional simple |