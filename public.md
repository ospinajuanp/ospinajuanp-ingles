# ospinajuanp-ingles — Aprende verbos en inglés con repetición espaciada

## Serie: Construyendo ospinajuanp-ingles

### POST #1 —
Yo todavía estoy aprendiendo inglés. No soy nativo, no soy fluido, y probablemente nunca voy a escribir un post técnico en inglés sin revisar tres veces antes de publicar.

Lo que sí sé es lo que me cuesta: documentación que me toma el doble leer, tickets de issues que entiendo a medias, posts en foros donde la respuesta buena está en inglés y la traducción automática me deforma el sentido. Cada vez que peleo con un párrafo técnico en español que no encuentro bien explicado, termino cayendo en la versión inglesa y entendiendo en cinco minutos lo que en español me costó una hora.

Ahí entendí algo: el cuello de botella más persistente de mi carrera técnica no es una tecnología, es el idioma. Y es un cuello de botella que puedo atacar yo, sin esperar a terminar un curso caro o a tener más tiempo libre.

Por eso empecé `ospinajuanp-ingles`: una aplicación web para practicar **verbos en inglés** desde el español. No es un curso. Es la herramienta que yo mismo quería tener para mis ratos muertos: práctica diaria, repetición espaciada, verbos con contexto real y audio para entrenar pronunciación.

Decidí construirla con stack moderno, todo client-side:

- **React 19** con strict mode y concurrent rendering
- **Vite 8** como dev server y bundler
- **Tailwind CSS v4** + **DaisyUI 5** (configuración CSS-first, sin archivo de config)
- **React Router 7** con rutas namespaced bajo `/v1` y redirects legacy
- **MongoDB Atlas** para sync perezoso de visitas, no como almacén crítico
- **lucide-react** para iconos

El proyecto es totalmente **local-first**: el mazo de repetición espaciada vive en `localStorage` del navegador. Funciona offline, sin cuentas, sin login, sin email. El código es abierto y se puede auditar línea por línea.

Está desplegada y abierta para quien quiera probarla:

👉 Live: https://ospinajuanp-ingles.vercel.app/
👉 Repo: https://github.com/ospinajuanp/ospinajuanp-ingles

La construyo como proyecto de práctica real para profundizar en arquitectura frontend, mientras resuelvo un problema que yo mismo tengo. Estoy activamente disponible para nuevos retos profesionales como Software Developer.

#Inglés #SoftwareEngineering #Frontend #ReactJS #Vite #EnProceso #JobSearch

### POST #2 —
Antes de escribir una sola línea de React, el reto más grande del proyecto estaba en los **datos**.

Una aplicación de práctica de verbos sólo sirve si los verbos están bien conjugados, bien traducidos y bien contextualizados. Construí un dataset de **1000 verbos** en `verbos_estructura.json`, donde cada uno tiene:

- **6 formas conjugadas** en inglés y español: infinitivo, pasado simple, participio, gerundio, futuro, condicional
- **6 oraciones contextualizadas**, una por cada tiempo, en ambos idiomas

La parte difícil no fue generar las oraciones. Fue garantizar consistencia entre todas. Por eso escribí `GUIA_ESTILO.md`, una guía de estilo con reglas obligatorias:

1. **Un significado por verbo**: si `ask` significa `pedir`, no se mezcla con `preguntar` en otras conjugaciones
2. **Pronombre fijo por slot**: `yo` para infinitivo, `tu` para pasado, `el/ella` para participio, `ellos` para gerundio, `nosotros` para futuro, `eso` (solo cuando suene natural) para condicional
3. **Conjugación coherente**: si el infinitivo es X, el futuro debe ser `Xá` o `Xerá` mecánicamente
4. **Traducción cultural, no literal**: `bounce an idea` no se traduce como `considerar la idea`, sino como `debatir la idea`
5. **Variedad de contextos**: no repetir `I [verb] the [noun]` en las 6 oraciones

El script `llenar_verbos.py` genera el JSON a partir de una lista base de infinitivos. La guía de estilo atrapa los errores antes de que lleguen al dataset. El resultado: 1000 verbos con 36 datos cada uno (60.000 piezas de contenido) que se mantienen coherentes en toda la app.

Si quieres auditar cómo estructuré el dataset o ver la guía de estilo completa, te invito a explorar el repositorio:

👉 Live: https://ospinajuanp-ingles.vercel.app/
👉 Repo: https://github.com/ospinajuanp/ospinajuanp-ingles

Estoy buscando activamente mi próxima oportunidad como Software Developer. Si tu equipo necesita a alguien obsesionado con la calidad del dato y la consistencia de contenido, hablemos.

#Inglés #DataModeling #ContentDesign #Python #ReactJS #SoftwareEngineering #JobSearch

### POST #3 —
Cuando tienes 1000 verbos, ¿cuál le muestras primero al usuario?

Si eliges uno al azar, el usuario va a caer la mitad del tiempo en verbos raros como `befuddle` o `abnegate`. Si eliges siempre el más común, el usuario se aburre del mismo top 20. Para resolver esto, implementé un sistema de **selección aleatoria ponderada** con tres baldes:

| Balde | Rango de frecuencia | Probabilidad |
|---|---|---|
| **A** | ≤ 10 (verbos muy frecuentes) | 50 % |
| **B** | 10.1 – 500 (verbos comunes) | 30 % |
| **C** | 500.1 – 1000 (verbos raros) | 20 % |

La lógica vive en `src/utils/weightedRandom.js`:

1. Primero se elige el balde por probabilidad acumulada
2. Luego se selecciona un verbo uniforme dentro del balde ganador
3. Si el balde está vacío, cae al siguiente no vacío

Validé empíricamente la distribución con 5.000 picks: 61 / 24.5 / 14.5 % sobre los valores teóricos de 50 / 30 / 20. Sesgo estadísticamente aceptable para una herramienta de práctica.

El botón de dado en la cabecera y el CTA de "Empezar" en la landing disparan exactamente este mismo cálculo. Cuando el usuario lo presiona 10 veces seguidas, no necesariamente verá 10 verbos distintos del balde A: verá una muestra que prioriza los útiles sin sentirse repetitiva.

Si quieres auditar la implementación o ver los buckets, te invito al repo:

👉 Live: https://ospinajuanp-ingles.vercel.app/
👉 Repo: https://github.com/ospinajuanp/ospinajuanp-ingles

Disponible como Software Developer para aportar implementaciones cuidadosas en frontend y producto.

#Inglés #JavaScript #Algorithms #UXDesign #Frontend #ReactJS #JobSearch

### POST #4 —
La mejor forma de aprender no es mostrando la respuesta, es **obligando al cerebro a producirla**.

Diseñé la app con un patrón de **progressive disclosure**: la traducción al español aparece borrosa por defecto, y se revela sólo cuando el usuario pasa el mouse (escritorio) o toca la pantalla (móvil). Esto fuerza al estudiante a intentar traducir mentalmente antes de ver la respuesta.

La implementación:

- **Conjugaciones (`ConjugationGrid`)**: cada celda tiene la conjugación en inglés siempre visible; al lado, la traducción en español aparece difuminada con `filter: blur(4px)` y un ícono de ojo. El usuario debe adivinar primero.
- **Oraciones (`SentencePill`)**: cada oración muestra el inglés sin restricción; la traducción al español está bloqueada detrás del mismo blur. La oración se renderiza con `whitespace-pre-line` para preservar formato en tipografía monoespaciada cuando aplica.
- **Cursor**: cambia a `cursor-pointer` sobre el blur para sugerir que es interactivo.
- **Mobile**: en pantallas táctiles no hay hover, así que un tap sencillo revela la traducción. Otro tap la vuelve a ocultar.

El patrón funciona porque convierte la lectura pasiva en un mini-ejercicio de recuperación activa (active recall), que es la técnica con mayor respaldo en investigación de aprendizaje. El estudiante ya no consume contenido: lo reconstruye.

El grid completo está disponible en `/v1/verbs/:verbSelector` con 6 conjugaciones + 6 oraciones, todas con reveal por interacción.

Disponible para nuevos retos como Software Developer, llevando rigor pedagógico al producto digital.

👉 Live: https://ospinajuanp-ingles.vercel.app/
👉 Repo: https://github.com/ospinajuanp/ospinajuanp-ingles

#Inglés #ActiveRecall #LearningScience #UXDesign #Frontend #MobileFirst #JobSearch

### POST #5 —
Una app educativa sin contexto visual y auditivo se siente como un libro de texto. Yo quería verbos **vivos**.

Construí dos pipelines multimedia asíncronos que se ejecutan on-demand al visitar cada verbo:

**Imágenes con Pexels** (`src/utils/pexels.js`):
- El header del verbo muestra una foto curada de PexelsAPI relacionada semánticamente con la palabra
- Implementé **rotación automática entre dos API keys** (`VITE_PEXELS_API_KEY` + `VITE_PEXELS_API_KEY_2`): si la primera responde 401/403/429/5xx o falla por red, el sistema conmuta a la segunda sin que el usuario lo note
- Las fotos se persisten en `localStorage` bajo `verbos:pexelsCache` (~100 KB para ~700 verbos)
- Sin ninguna key configurada, el sistema cae en cascada: Pexels → **Picsum** (placeholders deterministas por palabra) → SVG inline de un camino en el bosque

**Audio con Dictionary API + SpeechSynthesis fallback** (`src/components/AudioButton.jsx`):
- El botón de play central sobre la imagen consulta `dictionaryapi.dev` y reproduce la primera URL de audio disponible del verbo
- Si la API no devuelve fonética (verbos como `draw`, `set`, `run` a veces no tienen audio), el sistema conmuta a `Web Speech API` (`speechSynthesis`) con `lang: 'en-US'`, `rate: 0.9`
- El audio se cachea en memoria, así que la segunda reproducción es instantánea
- El wrapper completo de la imagen es el touch target, no sólo el botón, así un tap en cualquier parte del hero reproduce la pronunciación

Toda esta infraestructura corre sin backend propio: Vite sirve los assets, las APIs externas son gratuitas con límites generosos, y el caché se queda en el navegador. Cero costos operacionales.

Disponible como Software Developer para integrar servicios externos con degradación elegante.

👉 Live: https://ospinajuanp-ingles.vercel.app/
👉 Repo: https://github.com/ospinajuanp/ospinajuanp-ingles

#Inglés #APIIntegration #WebAudio #Fallback #Frontend #ReactJS #JobSearch

### POST #6 —
Practicar verbos al azar es como estudiar leyendo en diagonal. Lo que funciona de verdad es la **repetición espaciada**.

Implementé el algoritmo **SM-2** (SuperMemo 2, la base científica de Anki) en `src/utils/srs.js` como funciones puras, sin red, sin base de datos:

```text
SRS_MIN_EF = 1.3      // suelo del factor de facilidad
SRS_INITIAL_EF = 2.5  // factor inicial de una tarjeta nueva

calculateNextReview(interval, ef, grade)
  fail → interval = 1, repetitions = 0, ef = max(1.3, ef - 0.20)
  hard → interval crece por EF,         ef = max(1.3, ef - 0.10)
  good → interval crece por EF,         ef sin cambio
  easy → interval crece por EF,         ef += 0.15
  (éxitos comparten fórmula: 0 → 1, 1 → 3, luego round(prev × ef))
```

Cada verbo visitado se auto-registra en el mazo `Mazo de Verbos Vistos`. El usuario también puede crear su propio **Mazo Personalizado** desde `/v1/test` con tarjetas ES/EN escritas a mano. Ambos mazos conviven en una sola cola mezclada y barajada.

La UI usa **flashcards 3D con flip real** (no fade):

- Perspectiva CSS: `[perspective:1200px]` en el contenedor
- Transformación: `[transform-style:preserve-3d]` + `[transform:rotateY(180deg)]` en la cara trasera
- Visibilidad: `[backface-visibility:hidden]` en ambas caras
- Transición: 600 ms con `transition: transform`

Cuatro botones de calificación: **Otra vez** (fail/rojo), **Difícil** (hard/amber), **Bien** (good/esmeralda), **Fácil** (easy/celeste). Las cuatro tarjetas graduadas actualizan `localStorage` sincrónicamente y la cabecera muestra un contador en tiempo real con la cantidad de tarjetas pendientes hoy.

Todo el SRS vive en `localStorage['ospinajuanp-ingles:srs:v1']` con versionado de esquema. Funciona sin conexión. Sin backend. Sin cuentas.

Si quieres auditar el algoritmo o ver la implementación del flip 3D, te invito al repo:

👉 Live: https://ospinajuanp-ingles.vercel.app/
👉 Repo: https://github.com/ospinajuanp/ospinajuanp-ingles

Disponible como Software Developer para construir features complejas que se sientan simples para el usuario final.

#Inglés #SpacedRepetition #SM2 #LocalStorage #OfflineFirst #Frontend #ReactJS #JobSearch

### POST #7 —
Un sistema de repetición espaciada sin gestor de mazos termina lleno de tarjetas obsoletas.

Construí un **Deck Manager** completo dentro de `/v1/test`, accesible con un `ModeToggle` (join group de DaisyUI) en la cabecera de la página de repaso. Cambiar entre "Estudiar" y "Gestionar Mazo" no recarga la página.

La tabla muestra todas las tarjetas (personalizadas + verbos vistos) con columnas:

- **Tipo** — badge DaisyUI (`custom` vs `verb`)
- **Español** + **Inglés** — el contenido de la tarjeta
- **Estado SRS** — próxima revisión calculada
- **Acciones** — editar (sólo personalizadas) / eliminar (todas)

Implementé búsqueda en tiempo real que filtra sobre ambos idiomas con un `useState` local y patrón de **estado derivado**: el cambio de `searchTerm` resetea la página a 1 automáticamente sin disparar un `useEffect`. La paginación es 10 por página con números directos, primera/última, y huecos con elipsis cuando hay más de 7 páginas.

Las acciones usan `<dialog className="modal">` nativo de HTML5, gestionado por `useEffect` que llama imperativamente a `dialog.showModal()` / `dialog.close()`. Esto reemplaza el horrible `window.confirm` con un modal DaisyUI con backdrop, atajo de teclado ESC, y cierre por click fuera.

El modal de eliminación muestra un preview de la tarjeta antes de pedir confirmación, con un botón destructivo `btn bg-error text-error-content` claramente diferenciado. El de edición usa el mismo lifecycle pero mantiene el schedule SRS al guardar (sólo cambia el texto del prompt, no el intervalo ni el factor de facilidad).

Disponible como Software Developer para construir interfaces densas en datos que no se sientan densas.

👉 Live: https://ospinajuanp-ingles.vercel.app/
👉 Repo: https://github.com/ospinajuanp/ospinajuanp-ingles

#Inglés #UXDesign #Accessibility #ReactJS #DaisyUI #Frontend #Dialogs #JobSearch

### POST #8 —
Una app educativa no tiene por qué verse triste. Construí un sistema multi-tema completo con 4 variantes visuales:

- **Light** (default, alto contraste para lectura diurna)
- **Dark** (modo nocturno para estudio prolongado)
- **Dracula** (paleta vibrante de bajo fatiga visual)
- **Cupcake** (tonos pastel cálidos para sesiones largas)

Todo el sistema usa **DaisyUI 5** registrado como plugin CSS dentro de `src/index.css`:

```css
@import "tailwindcss";
@plugin "daisyui" { themes: light --default, dark, dracula, cupcake; }
```

No hay archivo `tailwind.config.js`. La configuración es CSS-first, aprovechando Tailwind v4 con la directiva `@theme`. Cada referencia a `bg-slate-900` o `text-indigo-600` del código viejo se reemplazó por tokens semánticos de DaisyUI (`bg-base-100`, `text-base-content`, `text-primary`, `border-base-300`). Esto permite que cambiar de tema re-pinte **toda la app** sin overrides manuales.

El reto técnico fue **evitar el flash de tema incorrecto** al recargar en modo oscuro. La solución:

1. `useTheme()` persiste en `localStorage['ospinajuanp-ingles:theme']`
2. Un `<script>` inline en `index.html` (antes de que React monte) lee esa misma key y aplica `data-theme` a `<html>` directamente
3. Cuando React monta y `useEffect` corre, el tema ya está en su lugar

Resultado: el usuario que usa Dracula nunca ve un flash blanco al refrescar.

El `ThemeSwitcher` en la cabecera es un dropdown DaisyUI con ícono lucide-react y checkmark sobre el tema activo. Todo el cambio de tema se aplica en menos de 16ms.

Disponible como Software Developer para construir productos que se ven bien sin sacrificar mantenibilidad.

👉 Live: https://ospinajuanp-ingles.vercel.app/
👉 Repo: https://github.com/ospinajuanp/ospinajuanp-ingles

#Inglés #ThemeDesign #UXDesign #TailwindCSS #DaisyUI #Frontend #ReactJS #JobSearch

### POST #9 —
El santo grial de las apps local-first es: **tus datos te siguen sin pedirte permiso**.

Construí un motor de sincronización silenciosa entre dispositivos, sin cuentas, sin login, sin email. La identidad es un UUIDv4 anónimo auto-generado en el primer mount con `crypto.randomUUID()`, persistido en `localStorage['ospinajuanp-ingles:syncToken']`. Listo: ese es tu "usuario".

El flujo de emparejamiento entre dispositivos es ridículamente simple:

1. **Dispositivo A** abre el modal de Sync → ve un QR con la URL `?syncToken=<uuid>`
2. **Dispositivo B** escanea el QR → adopta ese token como propio
3. A partir de ese momento, ambos dispositivos comparten el mismo mazo

El merge usa **Last-Write-Wins por timestamp de última revisión** (`srs.lastReviewed`, con fallback a `nextReview` y `createdAt`). Para empatar, gana el servidor (Atlas). El algoritmo vive en `src/utils/syncMerge.js` como función pura, testeable con Node directamente.

Las garantías operativas:

- **Push debounced de 2 segundos**: cada cambio en SRS dispara un POST al endpoint `/api/sync/user` con `keepalive: true`
- **Pull al montar** y al cambiar de token: el nuevo dispositivo se hidrata con el mazo existente en Atlas
- **Bootstrap push silencioso**: si el dispositivo A tenía mazo local y el remoto está vacío, se sube automáticamente sin "Upload" button
- **Pagehide flush**: al cerrar la pestaña, un POST final se dispara para no perder los últimos 2s de cambios
- **Safety-net cada 5 minutos**: por si el pagehide no alcanzó a ejecutarse
- **Anti-loop por hash FNV-1a**: si el estado remoto es idéntico al local, no se aplica merge, no se bumpea revisión, no se hace ningún render. Cero parpadeo, cero ciclos desperdiciados

El `SyncButton` en la cabecera muestra un dot discreto (success/warning/error) y el modal revela el QR + token + historial. Sin spinner invasivo. Sin "Conectando…" que asuste.

Disponible como Software Developer para construir infraestructura invisible que mejora la vida del usuario sin pedirle atención.

👉 Live: https://ospinajuanp-ingles.vercel.app/
👉 Repo: https://github.com/ospinajuanp/ospinajuanp-ingles

#Inglés #Sync #LocalFirst #MongoDB #UUID #QRCode #ReactJS #JobSearch

### POST #10 —
Yo sigo estudiando. Esta herramienta es lo que estoy usando para no abandonar.

Quiero ser honesto antes de cerrar esta serie: **yo todavía no domino el inglés**. Estoy en el camino, no al final. Uso esta aplicación todos los días para practicar verbos, y la construí precisamente porque estaba cansado de esperar a "tener el nivel" para empezar a leer documentación real, escribir en foros o aplicar a ofertas internacionales.

Lo que me pasó al construirla fue inesperado: pasé de verme como "alguien que necesita aprender inglés" a convertirme en "alguien que construyó la herramienta que necesitaba para aprender inglés". Y esa diferencia psicológica importa mucho. Tener un dashboard propio, ver tu mazo crecer, sincronizarse entre el computador y el celular, te hace volver al día siguiente.

Hay partes de esta app que probablemente un nativo jamás construiría así. Por ejemplo: el orden de las conjugaciones (infinitivo, pasado, participio, gerundio, futuro, condicional) está pensado para que **yo** entienda cómo se transforma un verbo en cada tiempo, no para optimizar la memorización rápida de un angloparlante. El blur en las traducciones al español es porque sé que si se las pongo a un click, voy a leerlas en lugar de intentar traducir primero. La SRS está afinada para verbos que **me** cuestan a mí, no para verbos que ya sé.

Si me funciona a mí como estudiante, ojalá le funcione a alguien más que esté en la misma.

**Si estás aprendiendo inglés**, te la presto. Tiene 1000 verbos, 6000 oraciones, repetición espaciada con SM-2, mazos personalizados, sincronización silenciosa entre dispositivos, modo oscuro, audio nativo y modo móvil. Y todo es gratis, sin anuncios, sin rastreo, sin pedirte email. No prometo que te va a hacer fluido, porque nada me hizo eso a mí tampoco. Pero sí te va a dar un lugar donde practicar 10 minutos al día sin excusas.

**Si eres desarrollador**, el repo está abierto. Hay patrones interesantes: un algoritmo SM-2 puro, una sincronización LWW por hash, un dataset de 1000 verbos con guía de estilo, un sistema multi-tema con anti-flicker, y un motor de sincronización silenciosa con QR. Todo el código se puede leer en una tarde.

**Si tu equipo necesita a alguien** que combine rigor técnico, obsesión por la calidad del dato y cariño por el detalle en el frontend, estoy abiertamente disponible para conversar. Construí este proyecto pensando en mi portfolio tanto como en mi propio aprendizaje.

No sé si esta herramienta es la diferencia entre alguien que aprende inglés y alguien que no. Pero a mí me mantiene en la silla, todos los días, sin que se me olvide. Si te mantiene a ti también, ya vale la pena.

Gracias por seguir la serie. El código sigue corriendo.

👉 Live: https://ospinajuanp-ingles.vercel.app/
👉 Repo: https://github.com/ospinajuanp/ospinajuanp-ingles

#Inglés #SoftwareEngineering #Frontend #ReactJS #JobSearch #OpenSource #ConstruyendoEnPúblico #AprendizajeContinuo #AprendizDeInglés

## Próximos Pasos

Para seguir la evolución del proyecto:
- [Live Demo](https://ospinajuanp-ingles.vercel.app/)
- [Repositorio GitHub](https://github.com/ospinajuanp/ospinajuanp-ingles)
- [Documentación](./README.md)
