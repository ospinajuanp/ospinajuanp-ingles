import json

RUTA_JSON = "/home/ospinajuanp/proyectos/ospinajuanp-ingles/verbos_estructura.json"

CATEGORIAS = ["simples", "irregulares", "compuestos"]
BASE_IDX = {"simples": 0, "irregulares": 400, "compuestos": 700, "tecnologia": 850}


def cargar():
    with open(RUTA_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar(data):
    with open(RUTA_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def idx_global(cat, idx):
    return BASE_IDX[cat] + idx


def llenar_verbo(data, categoria, posicion, verbo):
    if categoria == "tecnologia":
        entry = data["tecnologia"][posicion]
    else:
        entry = data["generales"][categoria][posicion]

    entry["id"] = idx_global(categoria, posicion)
    entry["imagen"] = ""
    entry["infinitivo"]   = {"esp": verbo["esp_inf"],        "ing": verbo["ing_inf"]}
    entry["pasadoSimple"] = {"esp": verbo["pasado_esp"],     "ing": verbo["pasado_ing"]}
    entry["participio"]   = {"esp": verbo["participio_esp"], "ing": verbo["participio_ing"]}
    entry["gerundio"]     = {"esp": verbo["gerundio_esp"],   "ing": verbo["gerundio_ing"]}
    entry["futuro"]       = {"esp": verbo.get("futuro_esp", f"{verbo['esp_inf']}á"),  "ing": f"will {verbo['ing_inf']}"}
    entry["condicional"]  = {"esp": verbo.get("cond_esp",  f"{verbo['esp_inf']}ía"), "ing": f"would {verbo['ing_inf']}"}

    for tiempo_key, vals in verbo["oraciones"].items():
        entry["oraciones"][tiempo_key]["ing"] = vals["ing"]
        entry["oraciones"][tiempo_key]["esp"] = vals["esp"]

    return entry["id"]


def procesar_bloque(verbos, categoria, posicion_inicio):
    """
    verbos: lista de diccionarios con la estructura de verbo.
    categoria: 'simples' | 'irregulares' | 'compuestos' | 'tecnologia'
    posicion_inicio: índice dentro del array de la categoría.
    Llena 10 verbos consecutivos a partir de posicion_inicio.
    """
    data = cargar()
    for i, verbo in enumerate(verbos):
        vid = llenar_verbo(data, categoria, posicion_inicio + i, verbo)
        print(f"  [#{vid}] {verbo['ing_inf']:12s} -> {verbo['esp_inf']}")
    guardar(data)
    print(f"\nBloque guardado: {len(verbos)} verbos en {categoria}[{posicion_inicio}..{posicion_inicio+len(verbos)-1}]")
    return data


def aplicar_correcciones(correcciones, categoria):
    """Sobrescribe verbos específicos (por índice) con datos corregidos."""
    data = cargar()
    for idx, verbo in correcciones.items():
        vid = llenar_verbo(data, categoria, idx, verbo)
        print(f"  [#{vid}] {verbo['ing_inf']:12s} -> {verbo['esp_inf']}  (corregido)")
    guardar(data)
    print(f"\nCorrecciones aplicadas: {len(correcciones)} verbos actualizados en {categoria}")


BLOQUE_1 = [
    {
        "ing_inf": "accept", "esp_inf": "aceptar",
        "pasado_ing": "accepted", "pasado_esp": "aceptó",
        "participio_ing": "accepted", "participio_esp": "aceptado",
        "gerundio_ing": "accepting", "gerundio_esp": "aceptando",
        "oraciones": {
            "infinitivo":   {"ing": "I accept the proposal.",            "esp": "Yo acepto la propuesta."},
            "pasadoSimple": {"ing": "You accepted the challenge.",        "esp": "Tú aceptaste el desafío."},
            "participio":   {"ing": "She has accepted the invitation.",   "esp": "Ella ha aceptado la invitación."},
            "gerundio":     {"ing": "They are accepting the terms.",      "esp": "Ellos están aceptando los términos."},
            "futuro":       {"ing": "We will accept the decision.",       "esp": "Nosotros aceptaremos la decisión."},
            "condicional":  {"ing": "It would accept the configuration.", "esp": "Eso aceptaría la configuración."}
        }
    },
    {
        "ing_inf": "add", "esp_inf": "añadir",
        "pasado_ing": "added", "pasado_esp": "añadió",
        "participio_ing": "added", "participio_esp": "añadido",
        "gerundio_ing": "adding", "gerundio_esp": "añadiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I add sugar to my coffee.",        "esp": "Yo añado azúcar a mi café."},
            "pasadoSimple": {"ing": "You added too much salt.",          "esp": "Tú añadiste demasiada sal."},
            "participio":   {"ing": "He has added the files.",           "esp": "Él ha añadido los archivos."},
            "gerundio":     {"ing": "They are adding new features.",     "esp": "Ellos están añadiendo nuevas funciones."},
            "futuro":       {"ing": "We will add more details.",         "esp": "Nosotros añadiremos más detalles."},
            "condicional":  {"ing": "It would add complexity.",          "esp": "Eso añadiría complejidad."}
        }
    },
    {
        "ing_inf": "admire", "esp_inf": "admirar",
        "pasado_ing": "admired", "pasado_esp": "admiró",
        "participio_ing": "admired", "participio_esp": "admirado",
        "gerundio_ing": "admiring", "gerundio_esp": "admirando",
        "oraciones": {
            "infinitivo":   {"ing": "I admire his courage.",            "esp": "Yo admiro su valentía."},
            "pasadoSimple": {"ing": "You admired the painting.",        "esp": "Tú admiraste la pintura."},
            "participio":   {"ing": "She has admired the view.",        "esp": "Ella ha admirado la vista."},
            "gerundio":     {"ing": "They are admiring the sunset.",    "esp": "Ellos están admirando el atardecer."},
            "futuro":       {"ing": "We will admire the artwork.",      "esp": "Nosotros admiraremos la obra."},
            "condicional":  {"ing": "It would admire the work.",        "esp": "Eso admiraría el trabajo."}
        }
    },
    {
        "ing_inf": "admit", "esp_inf": "admitir",
        "pasado_ing": "admitted", "pasado_esp": "admitió",
        "participio_ing": "admitted", "participio_esp": "admitido",
        "gerundio_ing": "admitting", "gerundio_esp": "admitiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I admit my mistake.",              "esp": "Yo admito mi error."},
            "pasadoSimple": {"ing": "You admitted the truth.",          "esp": "Tú admitiste la verdad."},
            "participio":   {"ing": "He has admitted his fault.",        "esp": "Él ha admitido su culpa."},
            "gerundio":     {"ing": "They are admitting the problem.",  "esp": "Ellos están admitiendo el problema."},
            "futuro":       {"ing": "We will admit the error.",         "esp": "Nosotros admitiremos el error."},
            "condicional":  {"ing": "It would admit the issue.",        "esp": "Eso admitiría el problema."}
        }
    },
    {
        "ing_inf": "advise", "esp_inf": "aconsejar",
        "pasado_ing": "advised", "pasado_esp": "aconsejó",
        "participio_ing": "advised", "participio_esp": "aconsejado",
        "gerundio_ing": "advising", "gerundio_esp": "aconsejando",
        "oraciones": {
            "infinitivo":   {"ing": "I advise caution.",                "esp": "Yo aconsejo precaución."},
            "pasadoSimple": {"ing": "You advised him well.",            "esp": "Tú le aconsejaste bien."},
            "participio":   {"ing": "She has advised the client.",      "esp": "Ella ha aconsejado al cliente."},
            "gerundio":     {"ing": "They are advising the team.",      "esp": "Ellos están aconsejando al equipo."},
            "futuro":       {"ing": "We will advise the manager.",      "esp": "Nosotros aconsejaremos al gerente."},
            "condicional":  {"ing": "It would advise the user.",        "esp": "Eso aconsejaría al usuario."}
        }
    },
    {
        "ing_inf": "allow", "esp_inf": "permitir",
        "pasado_ing": "allowed", "pasado_esp": "permitió",
        "participio_ing": "allowed", "participio_esp": "permitido",
        "gerundio_ing": "allowing", "gerundio_esp": "permitiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I allow my kids to play.",         "esp": "Yo permito que mis hijos jueguen."},
            "pasadoSimple": {"ing": "You allowed access.",              "esp": "Tú permitiste el acceso."},
            "participio":   {"ing": "He has allowed the change.",       "esp": "Él ha permitido el cambio."},
            "gerundio":     {"ing": "They are allowing comments.",      "esp": "Ellos están permitiendo comentarios."},
            "futuro":       {"ing": "We will allow exceptions.",        "esp": "Nosotros permitiremos excepciones."},
            "condicional":  {"ing": "It would allow modifications.",    "esp": "Eso permitiría modificaciones."}
        }
    },
    {
        "ing_inf": "analyze", "esp_inf": "analizar",
        "pasado_ing": "analyzed", "pasado_esp": "analizó",
        "participio_ing": "analyzed", "participio_esp": "analizado",
        "gerundio_ing": "analyzing", "gerundio_esp": "analizando",
        "oraciones": {
            "infinitivo":   {"ing": "I analyze the data daily.",        "esp": "Yo analizo los datos a diario."},
            "pasadoSimple": {"ing": "You analyzed the report.",         "esp": "Tú analizaste el informe."},
            "participio":   {"ing": "She has analyzed the results.",    "esp": "Ella ha analizado los resultados."},
            "gerundio":     {"ing": "They are analyzing trends.",       "esp": "Ellos están analizando tendencias."},
            "futuro":       {"ing": "We will analyze the problem.",     "esp": "Nosotros analizaremos el problema."},
            "condicional":  {"ing": "It would analyze the input.",      "esp": "Eso analizaría la entrada."}
        }
    },
    {
        "ing_inf": "announce", "esp_inf": "anunciar",
        "pasado_ing": "announced", "pasado_esp": "anunció",
        "participio_ing": "announced", "participio_esp": "anunciado",
        "gerundio_ing": "announcing", "gerundio_esp": "anunciando",
        "oraciones": {
            "infinitivo":   {"ing": "I announce the winners.",          "esp": "Yo anuncio a los ganadores."},
            "pasadoSimple": {"ing": "You announced the news.",          "esp": "Tú anunciaste la noticia."},
            "participio":   {"ing": "She has announced the launch.",    "esp": "Ella ha anunciado el lanzamiento."},
            "gerundio":     {"ing": "They are announcing the merger.",  "esp": "Ellos están anunciando la fusión."},
            "futuro":       {"ing": "We will announce the decision.",   "esp": "Nosotros anunciaremos la decisión."},
            "condicional":  {"ing": "It would announce the result.",    "esp": "Eso anunciaría el resultado."}
        }
    },
    {
        "ing_inf": "answer", "esp_inf": "responder",
        "pasado_ing": "answered", "pasado_esp": "respondió",
        "participio_ing": "answered", "participio_esp": "respondido",
        "gerundio_ing": "answering", "gerundio_esp": "respondiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I answer the phone.",              "esp": "Yo respondo el teléfono."},
            "pasadoSimple": {"ing": "You answered the question.",       "esp": "Tú respondiste la pregunta."},
            "participio":   {"ing": "He has answered the email.",       "esp": "Él ha respondido el correo."},
            "gerundio":     {"ing": "They are answering calls.",        "esp": "Ellos están respondiendo llamadas."},
            "futuro":       {"ing": "We will answer shortly.",          "esp": "Nosotros responderemos pronto."},
            "condicional":  {"ing": "It would answer automatically.",   "esp": "Eso respondería automáticamente."}
        }
    },
    {
        "ing_inf": "apologize", "esp_inf": "disculparse",
        "pasado_ing": "apologized", "pasado_esp": "se disculpó",
        "participio_ing": "apologized", "participio_esp": "disculpado",
        "gerundio_ing": "apologizing", "gerundio_esp": "disculpándose",
        "oraciones": {
            "infinitivo":   {"ing": "I apologize for the delay.",       "esp": "Yo me disculpo por el retraso."},
            "pasadoSimple": {"ing": "You apologized sincerely.",       "esp": "Tú te disculpaste sinceramente."},
            "participio":   {"ing": "She has apologized to them.",      "esp": "Ella se ha disculpado con ellos."},
            "gerundio":     {"ing": "They are apologizing now.",        "esp": "Ellos se están disculpando ahora."},
            "futuro":       {"ing": "We will apologize later.",         "esp": "Nosotros nos disculparemos después."},
            "condicional":  {"ing": "It would apologize automatically.","esp": "Eso se disculparía automáticamente."}
        }
    }
]


BLOQUE_2 = [
    {
        "ing_inf": "appear", "esp_inf": "aparecer",
        "pasado_ing": "appeared", "pasado_esp": "apareció",
        "participio_ing": "appeared", "participio_esp": "aparecido",
        "gerundio_ing": "appearing", "gerundio_esp": "apareciendo",
        "oraciones": {
            "infinitivo":   {"ing": "I appear on TV sometimes.",       "esp": "Yo aparezco en la tele a veces."},
            "pasadoSimple": {"ing": "You appeared suddenly.",          "esp": "Tú apareciste de repente."},
            "participio":   {"ing": "He has appeared in films.",       "esp": "Él ha aparecido en películas."},
            "gerundio":     {"ing": "They are appearing together.",    "esp": "Ellos están apareciendo juntos."},
            "futuro":       {"ing": "We will appear in court.",        "esp": "Nosotros apareceremos en el juzgado."},
            "condicional":  {"ing": "It would appear on screen.",      "esp": "Eso aparecería en pantalla."}
        }
    },
    {
        "ing_inf": "approve", "esp_inf": "aprobar",
        "pasado_ing": "approved", "pasado_esp": "aprobó",
        "participio_ing": "approved", "participio_esp": "aprobado",
        "gerundio_ing": "approving", "gerundio_esp": "aprobando",
        "oraciones": {
            "infinitivo":   {"ing": "I approve your proposal.",        "esp": "Yo apruebo tu propuesta."},
            "pasadoSimple": {"ing": "You approved the budget.",        "esp": "Tú aprobaste el presupuesto."},
            "participio":   {"ing": "She has approved the plan.",      "esp": "Ella ha aprobado el plan."},
            "gerundio":     {"ing": "They are approving the rules.",   "esp": "Ellos están aprobando las reglas."},
            "futuro":       {"ing": "We will approve the project.",    "esp": "Nosotros aprobaremos el proyecto."},
            "condicional":  {"ing": "It would approve the request.",   "esp": "Eso aprobaría la solicitud."}
        }
    },
    {
        "ing_inf": "argue", "esp_inf": "discutir",
        "pasado_ing": "argued", "pasado_esp": "discutió",
        "participio_ing": "argued", "participio_esp": "discutido",
        "gerundio_ing": "arguing", "gerundio_esp": "discutiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I argue with my brother.",        "esp": "Yo discuto con mi hermano."},
            "pasadoSimple": {"ing": "You argued with the teacher.",    "esp": "Tú discutiste con el profesor."},
            "participio":   {"ing": "She has argued her point.",       "esp": "Ella ha discutido su punto."},
            "gerundio":     {"ing": "They are arguing about money.",   "esp": "Ellos están discutiendo por dinero."},
            "futuro":       {"ing": "We will argue in court.",         "esp": "Nosotros discutiremos en el juzgado."},
            "condicional":  {"ing": "It would argue against it.",      "esp": "Eso argumentaría en contra."}
        }
    },
    {
        "ing_inf": "arrange", "esp_inf": "organizar",
        "pasado_ing": "arranged", "pasado_esp": "organizó",
        "participio_ing": "arranged", "participio_esp": "organizado",
        "gerundio_ing": "arranging", "gerundio_esp": "organizando",
        "oraciones": {
            "infinitivo":   {"ing": "I arrange the books.",            "esp": "Yo organizo los libros."},
            "pasadoSimple": {"ing": "You arranged the meeting.",       "esp": "Tú organizaste la reunión."},
            "participio":   {"ing": "He has arranged the trip.",       "esp": "Él ha organizado el viaje."},
            "gerundio":     {"ing": "They are arranging the party.",   "esp": "Ellos están organizando la fiesta."},
            "futuro":       {"ing": "We will arrange the details.",    "esp": "Nosotros organizaremos los detalles."},
            "condicional":  {"ing": "It would arrange the files.",     "esp": "Eso organizaría los archivos."}
        }
    },
    {
        "ing_inf": "arrive", "esp_inf": "llegar",
        "pasado_ing": "arrived", "pasado_esp": "llegó",
        "participio_ing": "arrived", "participio_esp": "llegado",
        "gerundio_ing": "arriving", "gerundio_esp": "llegando",
        "oraciones": {
            "infinitivo":   {"ing": "I arrive at eight.",              "esp": "Yo llego a las ocho."},
            "pasadoSimple": {"ing": "You arrived late.",               "esp": "Tú llegaste tarde."},
            "participio":   {"ing": "She has arrived already.",        "esp": "Ella ya ha llegado."},
            "gerundio":     {"ing": "They are arriving now.",          "esp": "Ellos están llegando ahora."},
            "futuro":       {"ing": "We will arrive tomorrow.",        "esp": "Nosotros llegaremos mañana."},
            "condicional":  {"ing": "It would arrive on time.",        "esp": "Eso llegaría a tiempo."}
        }
    },
    {
        "ing_inf": "ask", "esp_inf": "preguntar",
        "pasado_ing": "asked", "pasado_esp": "preguntó",
        "participio_ing": "asked", "participio_esp": "preguntado",
        "gerundio_ing": "asking", "gerundio_esp": "preguntando",
        "oraciones": {
            "infinitivo":   {"ing": "I ask for help.",                 "esp": "Yo pido ayuda."},
            "pasadoSimple": {"ing": "You asked a question.",           "esp": "Tú hiciste una pregunta."},
            "participio":   {"ing": "He has asked for it.",            "esp": "Él lo ha pedido."},
            "gerundio":     {"ing": "They are asking about us.",       "esp": "Ellos están preguntando por nosotros."},
            "futuro":       {"ing": "We will ask permission.",         "esp": "Nosotros pediremos permiso."},
            "condicional":  {"ing": "It would ask again.",             "esp": "Eso preguntaría de nuevo."}
        }
    },
    {
        "ing_inf": "attack", "esp_inf": "atacar",
        "pasado_ing": "attacked", "pasado_esp": "atacó",
        "participio_ing": "attacked", "participio_esp": "atacado",
        "gerundio_ing": "attacking", "gerundio_esp": "atacando",
        "oraciones": {
            "infinitivo":   {"ing": "I attack early in the game.",     "esp": "Yo ataco temprano en el juego."},
            "pasadoSimple": {"ing": "You attacked him unfairly.",      "esp": "Tú lo atacaste injustamente."},
            "participio":   {"ing": "She has attacked the enemy.",     "esp": "Ella ha atacado al enemigo."},
            "gerundio":     {"ing": "They are attacking the city.",    "esp": "Ellos están atacando la ciudad."},
            "futuro":       {"ing": "We will attack at dawn.",         "esp": "Nosotros atacaremos al amanecer."},
            "condicional":  {"ing": "It would attack the weakness.",   "esp": "Eso atacaría la debilidad."}
        }
    },
    {
        "ing_inf": "attempt", "esp_inf": "intentar",
        "pasado_ing": "attempted", "pasado_esp": "intentó",
        "participio_ing": "attempted", "participio_esp": "intentado",
        "gerundio_ing": "attempting", "gerundio_esp": "intentando",
        "oraciones": {
            "infinitivo":   {"ing": "I attempt every challenge.",      "esp": "Yo intento cada desafío."},
            "pasadoSimple": {"ing": "You attempted the climb.",        "esp": "Tú intentaste la subida."},
            "participio":   {"ing": "He has attempted the test.",      "esp": "Él ha intentado la prueba."},
            "gerundio":     {"ing": "They are attempting a rescue.",   "esp": "Ellos están intentando un rescate."},
            "futuro":       {"ing": "We will attempt the summit.",     "esp": "Nosotros intentaremos la cima."},
            "condicional":  {"ing": "It would attempt a fix.",         "esp": "Eso intentaría una solución."}
        }
    },
    {
        "ing_inf": "attend", "esp_inf": "asistir",
        "pasado_ing": "attended", "pasado_esp": "asistió",
        "participio_ing": "attended", "participio_esp": "asistido",
        "gerundio_ing": "attending", "gerundio_esp": "asistiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I attend class daily.",           "esp": "Yo asisto a clase a diario."},
            "pasadoSimple": {"ing": "You attended the meeting.",       "esp": "Tú asististe a la reunión."},
            "participio":   {"ing": "She has attended the event.",     "esp": "Ella ha asistido al evento."},
            "gerundio":     {"ing": "They are attending the show.",    "esp": "Ellos están asistiendo al espectáculo."},
            "futuro":       {"ing": "We will attend the wedding.",     "esp": "Nosotros asistiremos a la boda."},
            "condicional":  {"ing": "It would attend automatically.",  "esp": "Eso asistiría automáticamente."}
        }
    },
    {
        "ing_inf": "avoid", "esp_inf": "evitar",
        "pasado_ing": "avoided", "pasado_esp": "evitó",
        "participio_ing": "avoided", "participio_esp": "evitado",
        "gerundio_ing": "avoiding", "gerundio_esp": "evitando",
        "oraciones": {
            "infinitivo":   {"ing": "I avoid junk food.",              "esp": "Yo evito la comida chatarra."},
            "pasadoSimple": {"ing": "You avoided the question.",       "esp": "Tú evitaste la pregunta."},
            "participio":   {"ing": "He has avoided the traffic.",     "esp": "Él ha evitado el tráfico."},
            "gerundio":     {"ing": "They are avoiding the topic.",    "esp": "Ellos están evitando el tema."},
            "futuro":       {"ing": "We will avoid the mistake.",      "esp": "Nosotros evitaremos el error."},
            "condicional":  {"ing": "It would avoid conflict.",        "esp": "Eso evitaría el conflicto."}
        }
    }
]


BLOQUE_3 = [
    {
        "ing_inf": "bake", "esp_inf": "hornear",
        "pasado_ing": "baked", "pasado_esp": "horneó",
        "participio_ing": "baked", "participio_esp": "horneado",
        "gerundio_ing": "baking", "gerundio_esp": "horneando",
        "oraciones": {
            "infinitivo":   {"ing": "I bake bread on Sundays.",       "esp": "Yo horneo pan los domingos."},
            "pasadoSimple": {"ing": "You baked a cake.",               "esp": "Tú horneaste un pastel."},
            "participio":   {"ing": "She has baked cookies.",          "esp": "Ella ha horneado galletas."},
            "gerundio":     {"ing": "They are baking pizza.",          "esp": "Ellos están horneando pizza."},
            "futuro":       {"ing": "We will bake tomorrow.",          "esp": "Nosotros hornaremos mañana."},
            "condicional":  {"ing": "It would bake evenly.",           "esp": "Eso hornearía de forma pareja."}
        }
    },
    {
        "ing_inf": "balance", "esp_inf": "equilibrar",
        "pasado_ing": "balanced", "pasado_esp": "equilibró",
        "participio_ing": "balanced", "participio_esp": "equilibrado",
        "gerundio_ing": "balancing", "gerundio_esp": "equilibrando",
        "oraciones": {
            "infinitivo":   {"ing": "I balance the budget.",          "esp": "Yo equilibro el presupuesto."},
            "pasadoSimple": {"ing": "You balanced the books.",         "esp": "Tú equilibraste los libros."},
            "participio":   {"ing": "He has balanced the load.",       "esp": "Él ha equilibrado la carga."},
            "gerundio":     {"ing": "They are balancing work and life.","esp": "Ellos están equilibrando trabajo y vida."},
            "futuro":       {"ing": "We will balance the scales.",     "esp": "Nosotros equilibraremos la balanza."},
            "condicional":  {"ing": "It would balance out.",           "esp": "Eso se equilibraría."}
        }
    },
    {
        "ing_inf": "ban", "esp_inf": "prohibir",
        "pasado_ing": "banned", "pasado_esp": "prohibió",
        "participio_ing": "banned", "participio_esp": "prohibido",
        "gerundio_ing": "banning", "gerundio_esp": "prohibiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I ban junk food.",                "esp": "Yo prohíbo la comida chatarra."},
            "pasadoSimple": {"ing": "You banned the app.",             "esp": "Tú prohibiste la aplicación."},
            "participio":   {"ing": "She has banned the use.",         "esp": "Ella ha prohibido el uso."},
            "gerundio":     {"ing": "They are banning smoking.",       "esp": "Ellos están prohibiendo fumar."},
            "futuro":       {"ing": "We will ban the practice.",       "esp": "Nosotros prohibiremos la práctica."},
            "condicional":  {"ing": "It would ban the account.",       "esp": "Eso prohibiría la cuenta."}
        }
    },
    {
        "ing_inf": "behave", "esp_inf": "comportarse",
        "pasado_ing": "behaved", "pasado_esp": "se comportó",
        "participio_ing": "behaved", "participio_esp": "comportado",
        "gerundio_ing": "behaving", "gerundio_esp": "comportándose",
        "oraciones": {
            "infinitivo":   {"ing": "I behave well at school.",        "esp": "Yo me comporto bien en la escuela."},
            "pasadoSimple": {"ing": "You behaved badly.",              "esp": "Tú te comportaste mal."},
            "participio":   {"ing": "She has behaved perfectly.",      "esp": "Ella se ha comportado perfectamente."},
            "gerundio":     {"ing": "They are behaving oddly.",        "esp": "Ellos se están comportando de forma extraña."},
            "futuro":       {"ing": "We will behave accordingly.",     "esp": "Nosotros nos comportaremos como corresponde."},
            "condicional":  {"ing": "It would behave correctly.",      "esp": "Eso se comportaría correctamente."}
        }
    },
    {
        "ing_inf": "belong", "esp_inf": "pertenecer",
        "pasado_ing": "belonged", "pasado_esp": "perteneció",
        "participio_ing": "belonged", "participio_esp": "pertenecido",
        "gerundio_ing": "belonging", "gerundio_esp": "perteneciendo",
        "oraciones": {
            "infinitivo":   {"ing": "I belong here.",                  "esp": "Yo pertenezco aquí."},
            "pasadoSimple": {"ing": "You belonged to that group.",     "esp": "Tú pertenecías a ese grupo."},
            "participio":   {"ing": "He has belonged since childhood.","esp": "Él ha pertenecido desde la infancia."},
            "gerundio":     {"ing": "They are belonging to a club.",   "esp": "Ellos están perteneciendo a un club."},
            "futuro":       {"ing": "We will belong to history.",      "esp": "Nosotros pertenecemos a la historia."},
            "condicional":  {"ing": "It would belong to no one.",      "esp": "Eso no pertenecería a nadie."}
        }
    },
    {
        "ing_inf": "bless", "esp_inf": "bendecir",
        "pasado_ing": "blessed", "pasado_esp": "bendijo",
        "participio_ing": "blessed", "participio_esp": "bendecido",
        "gerundio_ing": "blessing", "gerundio_esp": "bendiciendo",
        "oraciones": {
            "infinitivo":   {"ing": "I bless this food.",              "esp": "Yo bendigo esta comida."},
            "pasadoSimple": {"ing": "You blessed the child.",          "esp": "Tú bendijiste al niño."},
            "participio":   {"ing": "She has blessed the union.",      "esp": "Ella ha bendecido la unión."},
            "gerundio":     {"ing": "They are blessing the house.",    "esp": "Ellos están bendiciendo la casa."},
            "futuro":       {"ing": "We will bless the journey.",      "esp": "Nosotros bendeciremos el viaje."},
            "condicional":  {"ing": "It would bless everyone.",        "esp": "Eso bendeciría a todos."}
        }
    },
    {
        "ing_inf": "blink", "esp_inf": "parpadear",
        "pasado_ing": "blinked", "pasado_esp": "parpadeó",
        "participio_ing": "blinked", "participio_esp": "parpadeado",
        "gerundio_ing": "blinking", "gerundio_esp": "parpadeando",
        "oraciones": {
            "infinitivo":   {"ing": "I blink often.",                  "esp": "Yo parpadeo seguido."},
            "pasadoSimple": {"ing": "You blinked twice.",              "esp": "Tú parpadeaste dos veces."},
            "participio":   {"ing": "She has blinked at the light.",   "esp": "Ella ha parpadeado con la luz."},
            "gerundio":     {"ing": "They are blinking fast.",         "esp": "Ellos están parpadeando rápido."},
            "futuro":       {"ing": "We will blink in surprise.",      "esp": "Nosotros parpadearemos sorprendidos."},
            "condicional":  {"ing": "It would blink repeatedly.",      "esp": "Eso parpadearía repetidamente."}
        }
    },
    {
        "ing_inf": "boil", "esp_inf": "hervir",
        "pasado_ing": "boiled", "pasado_esp": "hirvió",
        "participio_ing": "boiled", "participio_esp": "hervido",
        "gerundio_ing": "boiling", "gerundio_esp": "hirviendo",
        "oraciones": {
            "infinitivo":   {"ing": "I boil water for tea.",           "esp": "Yo hiervo agua para el té."},
            "pasadoSimple": {"ing": "You boiled the eggs.",            "esp": "Tú herviste los huevos."},
            "participio":   {"ing": "He has boiled the pasta.",        "esp": "Él ha hervido la pasta."},
            "gerundio":     {"ing": "They are boiling soup.",          "esp": "Ellos están hirviendo sopa."},
            "futuro":       {"ing": "We will boil it later.",          "esp": "Nosotros lo herviremos después."},
            "condicional":  {"ing": "It would boil over.",             "esp": "Eso herviría y se derramaría."}
        }
    },
    {
        "ing_inf": "book", "esp_inf": "reservar",
        "pasado_ing": "booked", "pasado_esp": "reservó",
        "participio_ing": "booked", "participio_esp": "reservado",
        "gerundio_ing": "booking", "gerundio_esp": "reservando",
        "oraciones": {
            "infinitivo":   {"ing": "I book flights online.",          "esp": "Yo reservo vuelos en línea."},
            "pasadoSimple": {"ing": "You booked a hotel.",             "esp": "Tú reservaste un hotel."},
            "participio":   {"ing": "She has booked the tickets.",     "esp": "Ella ha reservado las entradas."},
            "gerundio":     {"ing": "They are booking a table.",       "esp": "Ellos están reservando una mesa."},
            "futuro":       {"ing": "We will book early.",             "esp": "Nosotros reservaremos con tiempo."},
            "condicional":  {"ing": "It would book automatically.",    "esp": "Eso reservaría automáticamente."}
        }
    },
    {
        "ing_inf": "borrow", "esp_inf": "pedir prestado",
        "pasado_ing": "borrowed", "pasado_esp": "pidió prestado",
        "participio_ing": "borrowed", "participio_esp": "pedido prestado",
        "gerundio_ing": "borrowing", "gerundio_esp": "pidiendo prestado",
        "oraciones": {
            "infinitivo":   {"ing": "I borrow books from the library.","esp": "Yo pido libros prestados en la biblioteca."},
            "pasadoSimple": {"ing": "You borrowed my pen.",            "esp": "Tú me pediste mi bolígrafo prestado."},
            "participio":   {"ing": "She has borrowed money.",         "esp": "Ella ha pedido dinero prestado."},
            "gerundio":     {"ing": "They are borrowing tools.",       "esp": "Ellos están pidiendo herramientas prestadas."},
            "futuro":       {"ing": "We will borrow the car.",         "esp": "Nosotros pediremos el coche prestado."},
            "condicional":  {"ing": "It would borrow the model.",      "esp": "Eso tomaría prestado el modelo."}
        }
    }
]


CORRECCIONES = {
    9: {  # disculparse — fix reflexivo
        "ing_inf": "apologize", "esp_inf": "disculparse",
        "pasado_ing": "apologized", "pasado_esp": "se disculpó",
        "participio_ing": "apologized", "participio_esp": "disculpado",
        "gerundio_ing": "apologizing", "gerundio_esp": "disculpándose",
        "futuro_esp": "se disculpará", "cond_esp": "se disculparía",
        "oraciones": {
            "infinitivo":   {"ing": "I apologize for the delay.",       "esp": "Yo me disculpo por el retraso."},
            "pasadoSimple": {"ing": "You apologized sincerely.",       "esp": "Tú te disculpaste sinceramente."},
            "participio":   {"ing": "She has apologized to them.",      "esp": "Ella se ha disculpado con ellos."},
            "gerundio":     {"ing": "They are apologizing now.",        "esp": "Ellos se están disculpando ahora."},
            "futuro":       {"ing": "We will apologize later.",         "esp": "Nosotros nos disculparemos después."},
            "condicional":  {"ing": "The bot would apologize automatically.","esp": "El bot se disculparía automáticamente."}
        }
    },
    23: {  # comportarse — fix reflexivo
        "ing_inf": "behave", "esp_inf": "comportarse",
        "pasado_ing": "behaved", "pasado_esp": "se comportó",
        "participio_ing": "behaved", "participio_esp": "comportado",
        "gerundio_ing": "behaving", "gerundio_esp": "comportándose",
        "futuro_esp": "se comportará", "cond_esp": "se comportaría",
        "oraciones": {
            "infinitivo":   {"ing": "I behave well at school.",        "esp": "Yo me comporto bien en la escuela."},
            "pasadoSimple": {"ing": "You behaved badly.",              "esp": "Tú te comportaste mal."},
            "participio":   {"ing": "She has behaved perfectly.",      "esp": "Ella se ha comportado perfectamente."},
            "gerundio":     {"ing": "They are behaving oddly.",        "esp": "Ellos se están comportando de forma extraña."},
            "futuro":       {"ing": "We will behave accordingly.",     "esp": "Nosotros nos comportaremos como corresponde."},
            "condicional":  {"ing": "The child would behave well.",   "esp": "El niño se comportaría bien."}
        }
    },
    15: {  # ask — unificar a "pedir"
        "ing_inf": "ask", "esp_inf": "pedir",
        "pasado_ing": "asked", "pasado_esp": "pidió",
        "participio_ing": "asked", "participio_esp": "pedido",
        "gerundio_ing": "asking", "gerundio_esp": "pidiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I ask for help.",                 "esp": "Yo pido ayuda."},
            "pasadoSimple": {"ing": "You asked for more time.",        "esp": "Tú pediste más tiempo."},
            "participio":   {"ing": "She has asked for a raise.",      "esp": "Ella ha pedido un aumento."},
            "gerundio":     {"ing": "They are asking for permission.", "esp": "Ellos están pidiendo permiso."},
            "futuro":       {"ing": "We will ask for a refund.",       "esp": "Nosotros pediremos un reembolso."},
            "condicional":  {"ing": "That would ask for credentials.","esp": "Eso pediría credenciales."}
        }
    },
    16: {  # attack
        "ing_inf": "attack", "esp_inf": "atacar",
        "pasado_ing": "attacked", "pasado_esp": "atacó",
        "participio_ing": "attacked", "participio_esp": "atacado",
        "gerundio_ing": "attacking", "gerundio_esp": "atacando",
        "oraciones": {
            "infinitivo":   {"ing": "I attack early in the game.",     "esp": "Yo ataco temprano en el juego."},
            "pasadoSimple": {"ing": "You attacked him unfairly.",      "esp": "Tú lo atacaste injustamente."},
            "participio":   {"ing": "She has attacked the enemy.",     "esp": "Ella ha atacado al enemigo."},
            "gerundio":     {"ing": "They are attacking the city.",    "esp": "Ellos están atacando la ciudad."},
            "futuro":       {"ing": "We will attack at dawn.",         "esp": "Nosotros atacaremos al amanecer."},
            "condicional":  {"ing": "That would expose the weakness.", "esp": "Eso explotaría la debilidad."}
        }
    },
    18: {  # attend
        "ing_inf": "attend", "esp_inf": "asistir",
        "pasado_ing": "attended", "pasado_esp": "asistió",
        "participio_ing": "attended", "participio_esp": "asistido",
        "gerundio_ing": "attending", "gerundio_esp": "asistiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I attend class daily.",           "esp": "Yo asisto a clase a diario."},
            "pasadoSimple": {"ing": "You attended the meeting.",       "esp": "Tú asististe a la reunión."},
            "participio":   {"ing": "She has attended the event.",     "esp": "Ella ha asistido al evento."},
            "gerundio":     {"ing": "They are attending the show.",    "esp": "Ellos están asistiendo al espectáculo."},
            "futuro":       {"ing": "We will attend the wedding.",     "esp": "Nosotros asistiremos a la boda."},
            "condicional":  {"ing": "The bot would attend automatically.","esp": "El bot asistiría automáticamente."}
        }
    },
    24: {  # belong — corregir conjugaciones
        "ing_inf": "belong", "esp_inf": "pertenecer",
        "pasado_ing": "belonged", "pasado_esp": "perteneció",
        "participio_ing": "belonged", "participio_esp": "pertenecido",
        "gerundio_ing": "belonging", "gerundio_esp": "perteneciendo",
        "oraciones": {
            "infinitivo":   {"ing": "I belong to this team.",          "esp": "Yo pertenezco a este equipo."},
            "pasadoSimple": {"ing": "You belonged to that group.",     "esp": "Tú pertenecías a ese grupo."},
            "participio":   {"ing": "He has belonged since childhood.","esp": "Él ha pertenecido desde la infancia."},
            "gerundio":     {"ing": "They are belonging to a club.",   "esp": "Ellos están perteneciendo a un club."},
            "futuro":       {"ing": "We will belong to history.",      "esp": "Nosotros perteneceremos a la historia."},
            "condicional":  {"ing": "That would belong to no one.",    "esp": "Eso no pertenecería a nadie."}
        }
    },
    30: {  # bounce — corregir condicional mal traducido
        "ing_inf": "bounce", "esp_inf": "rebotar",
        "pasado_ing": "bounced", "pasado_esp": "rebotó",
        "participio_ing": "bounced", "participio_esp": "rebotado",
        "gerundio_ing": "bouncing", "gerundio_esp": "rebotando",
        "oraciones": {
            "infinitivo":   {"ing": "I bounce the ball high.",         "esp": "Yo reboto la pelota alto."},
            "pasadoSimple": {"ing": "You bounced back quickly.",       "esp": "Tú te recuperaste rápido."},
            "participio":   {"ing": "She has bounced ideas around.",   "esp": "Ella ha intercambiado ideas."},
            "gerundio":     {"ing": "They are bouncing emails.",       "esp": "Ellos están reenviando correos."},
            "futuro":       {"ing": "We will bounce back stronger.",   "esp": "Nosotros volveremos más fuertes."},
            "condicional":  {"ing": "That would bounce off the wall.","esp": "Eso rebotaría en la pared."}
        }
    },
    31: {  # brush — condicional forzado
        "ing_inf": "brush", "esp_inf": "cepillar",
        "pasado_ing": "brushed", "pasado_esp": "cepilló",
        "participio_ing": "brushed", "participio_esp": "cepillado",
        "gerundio_ing": "brushing", "gerundio_esp": "cepillando",
        "oraciones": {
            "infinitivo":   {"ing": "I brush my teeth twice a day.",   "esp": "Yo me cepillo los dientes dos veces al día."},
            "pasadoSimple": {"ing": "You brushed your hair.",          "esp": "Tú te cepillaste el pelo."},
            "participio":   {"ing": "He has brushed the dust off.",    "esp": "Él ha sacudido el polvo."},
            "gerundio":     {"ing": "They are brushing the floor.",    "esp": "Ellos están barriendo el piso."},
            "futuro":       {"ing": "We will brush before bed.",      "esp": "Nosotros nos cepillaremos antes de dormir."},
            "condicional":  {"ing": "The coat would brush off easily.","esp": "El abrigo se sacudiría fácilmente."}
        }
    },
    34: {  # camp — condicional forzado
        "ing_inf": "camp", "esp_inf": "acampar",
        "pasado_ing": "camped", "pasado_esp": "acampó",
        "participio_ing": "camped", "participio_esp": "acampado",
        "gerundio_ing": "camping", "gerundio_esp": "acampando",
        "oraciones": {
            "infinitivo":   {"ing": "I camp in the mountains every summer.","esp": "Yo acampo en las montañas cada verano."},
            "pasadoSimple": {"ing": "You camped by the river.",        "esp": "Tú acampaste junto al río."},
            "participio":   {"ing": "She has camped alone before.",    "esp": "Ella ha acampado sola antes."},
            "gerundio":     {"ing": "They are camping in tents.",      "esp": "Ellos están acampando en tiendas."},
            "futuro":       {"ing": "We will camp near the lake.",     "esp": "Nosotros acamparemos cerca del lago."},
            "condicional":  {"ing": "The scouts would camp outdoors.","esp": "Los scouts acamparían al aire libre."}
        }
    },
    35: {  # care — traducción incorrecta + fix reflexivo
        "ing_inf": "care", "esp_inf": "preocuparse",
        "pasado_ing": "cared", "pasado_esp": "se preocupó",
        "participio_ing": "cared", "participio_esp": "preocupado",
        "gerundio_ing": "caring", "gerundio_esp": "preocupándose",
        "futuro_esp": "se preocupará", "cond_esp": "se preocuparía",
        "oraciones": {
            "infinitivo":   {"ing": "I care about my family.",         "esp": "Yo me preocupo por mi familia."},
            "pasadoSimple": {"ing": "You cared deeply about it.",     "esp": "Tú te preocupaste mucho por eso."},
            "participio":   {"ing": "She has cared for him for years.","esp": "Ella lo ha cuidado durante años."},
            "gerundio":     {"ing": "They are caring for the patient.","esp": "Ellos están cuidando al paciente."},
            "futuro":       {"ing": "We will care for the garden.",    "esp": "Nosotros cuidaremos el jardín."},
            "condicional":  {"ing": "That would care less about money.","esp": "Eso se preocuparía menos por el dinero."}
        }
    },
    36: {  # carry — condicional mal traducido
        "ing_inf": "carry", "esp_inf": "llevar",
        "pasado_ing": "carried", "pasado_esp": "llevó",
        "participio_ing": "carried", "participio_esp": "llevado",
        "gerundio_ing": "carrying", "gerundio_esp": "llevando",
        "oraciones": {
            "infinitivo":   {"ing": "I carry the groceries home.",    "esp": "Yo llevo las compras a casa."},
            "pasadoSimple": {"ing": "You carried the box upstairs.",  "esp": "Tú subiste la caja."},
            "participio":   {"ing": "She has carried the team well.", "esp": "Ella ha dirigido bien al equipo."},
            "gerundio":     {"ing": "They are carrying the bags.",     "esp": "Ellos están cargando las bolsas."},
            "futuro":       {"ing": "We will carry this project.",     "esp": "Nosotros llevaremos este proyecto."},
            "condicional":  {"ing": "That policy would carry weight.","esp": "Esa política tendría peso."}
        }
    },
    53: {  # quejarse — fix reflexivo
        "ing_inf": "complain", "esp_inf": "quejarse",
        "pasado_ing": "complained", "pasado_esp": "se quejó",
        "participio_ing": "complained", "participio_esp": "quejado",
        "gerundio_ing": "complaining", "gerundio_esp": "quejándose",
        "futuro_esp": "se quejará", "cond_esp": "se quejaría",
        "oraciones": {
            "infinitivo":   {"ing": "I complain about the noise at night.","esp": "Yo me quejo del ruido por la noche."},
            "pasadoSimple": {"ing": "You complained to the manager.",     "esp": "Tú te quejaste al gerente."},
            "participio":   {"ing": "He has complained repeatedly.",      "esp": "Él se ha quejado repetidamente."},
            "gerundio":     {"ing": "They are complaining about the service.","esp": "Ellos se están quejando del servicio."},
            "futuro":       {"ing": "We will complain if needed.",        "esp": "Nosotros nos quejaremos si es necesario."},
            "condicional":  {"ing": "The customer would complain again.","esp": "El cliente volvería a quejarse."}
        }
    },
    55: {  # concentrarse — fix reflexivo
        "ing_inf": "concentrate", "esp_inf": "concentrarse",
        "pasado_ing": "concentrated", "pasado_esp": "se concentró",
        "participio_ing": "concentrated", "participio_esp": "concentrado",
        "gerundio_ing": "concentrating", "gerundio_esp": "concentrándose",
        "futuro_esp": "se concentrará", "cond_esp": "se concentraría",
        "oraciones": {
            "infinitivo":   {"ing": "I concentrate better with music.",   "esp": "Yo me concentro mejor con música."},
            "pasadoSimple": {"ing": "You concentrated too hard.",         "esp": "Tú te concentraste demasiado."},
            "participio":   {"ing": "She has concentrated on her goals.", "esp": "Ella se ha concentrado en sus metas."},
            "gerundio":     {"ing": "They are concentrating their forces.","esp": "Ellos están concentrando sus fuerzas."},
            "futuro":       {"ing": "We will concentrate on this issue.", "esp": "Nosotros nos concentraremos en este tema."},
            "condicional":  {"ing": "That merger would concentrate power.","esp": "Esa fusión concentraría el poder."}
        }
    }
}


BLOQUE_4 = [
    {
        "ing_inf": "bounce", "esp_inf": "rebotar",
        "pasado_ing": "bounced", "pasado_esp": "rebotó",
        "participio_ing": "bounced", "participio_esp": "rebotado",
        "gerundio_ing": "bouncing", "gerundio_esp": "rebotando",
        "oraciones": {
            "infinitivo":   {"ing": "I bounce the ball.",              "esp": "Yo reboto la pelota."},
            "pasadoSimple": {"ing": "You bounced high.",               "esp": "Tú rebotaste alto."},
            "participio":   {"ing": "She has bounced back.",           "esp": "Ella ha regresado con fuerza."},
            "gerundio":     {"ing": "They are bouncing around.",       "esp": "Ellos están rebotando por todos lados."},
            "futuro":       {"ing": "We will bounce the idea.",        "esp": "Nosotros consideraremos la idea."},
            "condicional":  {"ing": "It would bounce back.",           "esp": "Eso rebotaría de vuelta."}
        }
    },
    {
        "ing_inf": "brush", "esp_inf": "cepillar",
        "pasado_ing": "brushed", "pasado_esp": "cepilló",
        "participio_ing": "brushed", "participio_esp": "cepillado",
        "gerundio_ing": "brushing", "gerundio_esp": "cepillando",
        "oraciones": {
            "infinitivo":   {"ing": "I brush my teeth.",               "esp": "Yo me cepillo los dientes."},
            "pasadoSimple": {"ing": "You brushed your hair.",          "esp": "Tú te cepillaste el pelo."},
            "participio":   {"ing": "He has brushed the dust off.",    "esp": "Él ha cepillado el polvo."},
            "gerundio":     {"ing": "They are brushing the floor.",    "esp": "Ellos están cepillando el piso."},
            "futuro":       {"ing": "We will brush before bed.",      "esp": "Nosotros nos cepillaremos antes de dormir."},
            "condicional":  {"ing": "It would brush off easily.",      "esp": "Eso se quitaría fácilmente con un cepillo."}
        }
    },
    {
        "ing_inf": "burn", "esp_inf": "quemar",
        "pasado_ing": "burned", "pasado_esp": "quemó",
        "participio_ing": "burned", "participio_esp": "quemado",
        "gerundio_ing": "burning", "gerundio_esp": "quemando",
        "oraciones": {
            "infinitivo":   {"ing": "I burn the toast.",               "esp": "Yo quemo el pan tostado."},
            "pasadoSimple": {"ing": "You burned the food.",            "esp": "Tú quemaste la comida."},
            "participio":   {"ing": "She has burned the logs.",        "esp": "Ella ha quemado los troncos."},
            "gerundio":     {"ing": "They are burning trash.",         "esp": "Ellos están quemando basura."},
            "futuro":       {"ing": "We will burn the paper.",         "esp": "Nosotros quemaremos el papel."},
            "condicional":  {"ing": "It would burn quickly.",          "esp": "Eso se quemaría rápido."}
        }
    },
    {
        "ing_inf": "call", "esp_inf": "llamar",
        "pasado_ing": "called", "pasado_esp": "llamó",
        "participio_ing": "called", "participio_esp": "llamado",
        "gerundio_ing": "calling", "gerundio_esp": "llamando",
        "oraciones": {
            "infinitivo":   {"ing": "I call my mom daily.",            "esp": "Yo llamo a mi mamá a diario."},
            "pasadoSimple": {"ing": "You called me yesterday.",        "esp": "Tú me llamaste ayer."},
            "participio":   {"ing": "She has called twice.",           "esp": "Ella ha llamado dos veces."},
            "gerundio":     {"ing": "They are calling for help.",      "esp": "Ellos están pidiendo ayuda a gritos."},
            "futuro":       {"ing": "We will call later.",             "esp": "Nosotros llamaremos después."},
            "condicional":  {"ing": "It would call automatically.",    "esp": "Eso llamaría automáticamente."}
        }
    },
    {
        "ing_inf": "camp", "esp_inf": "acampar",
        "pasado_ing": "camped", "pasado_esp": "acampó",
        "participio_ing": "camped", "participio_esp": "acampado",
        "gerundio_ing": "camping", "gerundio_esp": "acampando",
        "oraciones": {
            "infinitivo":   {"ing": "I camp in the mountains.",        "esp": "Yo acampo en las montañas."},
            "pasadoSimple": {"ing": "You camped by the river.",        "esp": "Tú acampaste junto al río."},
            "participio":   {"ing": "She has camped alone.",           "esp": "Ella ha acampado sola."},
            "gerundio":     {"ing": "They are camping in tents.",      "esp": "Ellos están acampando en tiendas."},
            "futuro":       {"ing": "We will camp tomorrow.",          "esp": "Nosotros acamparemos mañana."},
            "condicional":  {"ing": "It would camp out.",              "esp": "Eso acamparía afuera."}
        }
    },
    {
        "ing_inf": "care", "esp_inf": "importar",
        "pasado_ing": "cared", "pasado_esp": "importó",
        "participio_ing": "cared", "participio_esp": "importado",
        "gerundio_ing": "caring", "gerundio_esp": "importando",
        "oraciones": {
            "infinitivo":   {"ing": "I care about you.",               "esp": "Yo me preocupo por ti."},
            "pasadoSimple": {"ing": "You cared deeply.",               "esp": "Tú te preocupaste mucho."},
            "participio":   {"ing": "He has cared for years.",         "esp": "Él ha cuidado durante años."},
            "gerundio":     {"ing": "They are caring for him.",        "esp": "Ellos están cuidándolo."},
            "futuro":       {"ing": "We will care for the garden.",    "esp": "Nosotros cuidaremos el jardín."},
            "condicional":  {"ing": "It would care less.",             "esp": "Eso importaría menos."}
        }
    },
    {
        "ing_inf": "carry", "esp_inf": "llevar",
        "pasado_ing": "carried", "pasado_esp": "llevó",
        "participio_ing": "carried", "participio_esp": "llevado",
        "gerundio_ing": "carrying", "gerundio_esp": "llevando",
        "oraciones": {
            "infinitivo":   {"ing": "I carry the groceries.",          "esp": "Yo llevo las compras."},
            "pasadoSimple": {"ing": "You carried the box.",            "esp": "Tú llevaste la caja."},
            "participio":   {"ing": "She has carried the team.",       "esp": "Ella ha llevado al equipo."},
            "gerundio":     {"ing": "They are carrying bags.",         "esp": "Ellos están llevando bolsas."},
            "futuro":       {"ing": "We will carry forward.",          "esp": "Nosotros seguiremos adelante."},
            "condicional":  {"ing": "It would carry weight.",          "esp": "Eso tendría peso."}
        }
    },
    {
        "ing_inf": "celebrate", "esp_inf": "celebrar",
        "pasado_ing": "celebrated", "pasado_esp": "celebró",
        "participio_ing": "celebrated", "participio_esp": "celebrado",
        "gerundio_ing": "celebrating", "gerundio_esp": "celebrando",
        "oraciones": {
            "infinitivo":   {"ing": "I celebrate my birthday.",        "esp": "Yo celebro mi cumpleaños."},
            "pasadoSimple": {"ing": "You celebrated the win.",         "esp": "Tú celebraste la victoria."},
            "participio":   {"ing": "She has celebrated alone.",       "esp": "Ella ha celebrado sola."},
            "gerundio":     {"ing": "They are celebrating tonight.",   "esp": "Ellos están celebrando esta noche."},
            "futuro":       {"ing": "We will celebrate together.",     "esp": "Nosotros celebraremos juntos."},
            "condicional":  {"ing": "It would celebrate success.",     "esp": "Eso celebraría el éxito."}
        }
    },
    {
        "ing_inf": "challenge", "esp_inf": "desafiar",
        "pasado_ing": "challenged", "pasado_esp": "desafió",
        "participio_ing": "challenged", "participio_esp": "desafiado",
        "gerundio_ing": "challenging", "gerundio_esp": "desafiando",
        "oraciones": {
            "infinitivo":   {"ing": "I challenge you to a duel.",      "esp": "Yo te desafío a un duelo."},
            "pasadoSimple": {"ing": "You challenged his theory.",      "esp": "Tú desafiaste su teoría."},
            "participio":   {"ing": "She has challenged the rules.",   "esp": "Ella ha desafiado las reglas."},
            "gerundio":     {"ing": "They are challenging each other.","esp": "Ellos se están desafiando mutuamente."},
            "futuro":       {"ing": "We will challenge the decision.", "esp": "Nosotros desafiaremos la decisión."},
            "condicional":  {"ing": "It would challenge the norms.",   "esp": "Eso desafiaría las normas."}
        }
    },
    {
        "ing_inf": "change", "esp_inf": "cambiar",
        "pasado_ing": "changed", "pasado_esp": "cambió",
        "participio_ing": "changed", "participio_esp": "cambiado",
        "gerundio_ing": "changing", "gerundio_esp": "cambiando",
        "oraciones": {
            "infinitivo":   {"ing": "I change the channel.",           "esp": "Yo cambio el canal."},
            "pasadoSimple": {"ing": "You changed your mind.",          "esp": "Tú cambiaste de opinión."},
            "participio":   {"ing": "He has changed jobs.",            "esp": "Él ha cambiado de trabajo."},
            "gerundio":     {"ing": "They are changing clothes.",      "esp": "Ellos se están cambiando de ropa."},
            "futuro":       {"ing": "We will change the plan.",        "esp": "Nosotros cambiaremos el plan."},
            "condicional":  {"ing": "It would change everything.",     "esp": "Eso lo cambiaría todo."}
        }
    }
]


BLOQUE_5 = [
    {
        "ing_inf": "charge", "esp_inf": "cobrar",
        "pasado_ing": "charged", "pasado_esp": "cobró",
        "participio_ing": "charged", "participio_esp": "cobrado",
        "gerundio_ing": "charging", "gerundio_esp": "cobrando",
        "oraciones": {
            "infinitivo":   {"ing": "I charge my phone at night.",      "esp": "Yo cargo mi celular por la noche."},
            "pasadoSimple": {"ing": "You charged too much for that.",  "esp": "Tú cobraste demasiado por eso."},
            "participio":   {"ing": "She has charged the battery.",    "esp": "Ella ha cargado la batería."},
            "gerundio":     {"ing": "They are charging extra fees.",   "esp": "Ellos están cobrando tarifas extra."},
            "futuro":       {"ing": "We will charge hourly.",          "esp": "Nosotros cobraremos por hora."},
            "condicional":  {"ing": "That would charge interest.",     "esp": "Eso cobraría intereses."}
        }
    },
    {
        "ing_inf": "chase", "esp_inf": "perseguir",
        "pasado_ing": "chased", "pasado_esp": "persiguió",
        "participio_ing": "chased", "participio_esp": "perseguido",
        "gerundio_ing": "chasing", "gerundio_esp": "persiguiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I chase my dreams every day.",    "esp": "Yo persigo mis sueños cada día."},
            "pasadoSimple": {"ing": "You chased the thief down the street.","esp": "Tú perseguiste al ladrón por la calle."},
            "participio":   {"ing": "He has chased success for years.","esp": "Él ha perseguido el éxito durante años."},
            "gerundio":     {"ing": "They are chasing the bus.",       "esp": "Ellos están persiguiendo al autobús."},
            "futuro":       {"ing": "We will chase the suspect.",      "esp": "Nosotros perseguiremos al sospechoso."},
            "condicional":  {"ing": "The dog would chase the squirrel.","esp": "El perro perseguiría a la ardilla."}
        }
    },
    {
        "ing_inf": "check", "esp_inf": "revisar",
        "pasado_ing": "checked", "pasado_esp": "revisó",
        "participio_ing": "checked", "participio_esp": "revisado",
        "gerundio_ing": "checking", "gerundio_esp": "revisando",
        "oraciones": {
            "infinitivo":   {"ing": "I check my email every morning.", "esp": "Yo reviso mi correo cada mañana."},
            "pasadoSimple": {"ing": "You checked the oil yesterday.",  "esp": "Tú revisaste el aceite ayer."},
            "participio":   {"ing": "She has checked the report twice.","esp": "Ella ha revisado el informe dos veces."},
            "gerundio":     {"ing": "They are checking tickets at the door.","esp": "Ellos están revisando boletos en la puerta."},
            "futuro":       {"ing": "We will check again tomorrow.",   "esp": "Nosotros revisaremos de nuevo mañana."},
            "condicional":  {"ing": "The system would check the input.","esp": "El sistema verificaría la entrada."}
        }
    },
    {
        "ing_inf": "chew", "esp_inf": "masticar",
        "pasado_ing": "chewed", "pasado_esp": "masticó",
        "participio_ing": "chewed", "participio_esp": "masticado",
        "gerundio_ing": "chewing", "gerundio_esp": "masticando",
        "oraciones": {
            "infinitivo":   {"ing": "I chew gum after lunch.",         "esp": "Yo mastico chicle después del almuerzo."},
            "pasadoSimple": {"ing": "You chewed the food slowly.",     "esp": "Tú masticaste la comida despacio."},
            "participio":   {"ing": "He has chewed his nails all day.","esp": "Él se ha mordido las uñas todo el día."},
            "gerundio":     {"ing": "They are chewing loudly at the table.","esp": "Ellos están masticando ruidosamente en la mesa."},
            "futuro":       {"ing": "We will chew carefully.",         "esp": "Nosotros masticaremos con cuidado."},
            "condicional":  {"ing": "The dog would chew the shoe.",    "esp": "El perro mordería el zapato."}
        }
    },
    {
        "ing_inf": "clean", "esp_inf": "limpiar",
        "pasado_ing": "cleaned", "pasado_esp": "limpió",
        "participio_ing": "cleaned", "participio_esp": "limpiado",
        "gerundio_ing": "cleaning", "gerundio_esp": "limpiando",
        "oraciones": {
            "infinitivo":   {"ing": "I clean my room every weekend.",  "esp": "Yo limpio mi cuarto cada fin de semana."},
            "pasadoSimple": {"ing": "You cleaned the kitchen yesterday.","esp": "Tú limpiaste la cocina ayer."},
            "participio":   {"ing": "She has cleaned the windows.",    "esp": "Ella ha limpiado las ventanas."},
            "gerundio":     {"ing": "They are cleaning the office.",   "esp": "Ellos están limpiando la oficina."},
            "futuro":       {"ing": "We will clean after the party.", "esp": "Nosotros limpiaremos después de la fiesta."},
            "condicional":  {"ing": "That stain would clean easily.", "esp": "Esa mancha se limpiaría fácilmente."}
        }
    },
    {
        "ing_inf": "clear", "esp_inf": "despejar",
        "pasado_ing": "cleared", "pasado_esp": "despejó",
        "participio_ing": "cleared", "participio_esp": "despejado",
        "gerundio_ing": "clearing", "gerundio_esp": "despejando",
        "oraciones": {
            "infinitivo":   {"ing": "I clear my desk before leaving.", "esp": "Yo despejo mi escritorio antes de salir."},
            "pasadoSimple": {"ing": "You cleared the table after dinner.","esp": "Tú despejaste la mesa después de cenar."},
            "participio":   {"ing": "She has cleared the doubts.",     "esp": "Ella ha aclarado las dudas."},
            "gerundio":     {"ing": "They are clearing the road after the storm.","esp": "Ellos están despejando el camino tras la tormenta."},
            "futuro":       {"ing": "We will clear the area tomorrow.","esp": "Nosotros despejaremos el área mañana."},
            "condicional":  {"ing": "That action would clear the cache.","esp": "Esa acción borraría el caché."}
        }
    },
    {
        "ing_inf": "climb", "esp_inf": "escalar",
        "pasado_ing": "climbed", "pasado_esp": "escaló",
        "participio_ing": "climbed", "participio_esp": "escalado",
        "gerundio_ing": "climbing", "gerundio_esp": "escalando",
        "oraciones": {
            "infinitivo":   {"ing": "I climb mountains for fun.",      "esp": "Yo escalo montañas por diversión."},
            "pasadoSimple": {"ing": "You climbed the tree easily.",    "esp": "Tú subiste al árbol con facilidad."},
            "participio":   {"ing": "She has climbed the highest peak.","esp": "Ella ha escalado la cima más alta."},
            "gerundio":     {"ing": "They are climbing the stairs now.","esp": "Ellos están subiendo las escaleras ahora."},
            "futuro":       {"ing": "We will climb higher next time.","esp": "Nosotros escalaremos más alto la próxima vez."},
            "condicional":  {"ing": "The cat would climb the fence.", "esp": "El gato treparía la valla."}
        }
    },
    {
        "ing_inf": "close", "esp_inf": "cerrar",
        "pasado_ing": "closed", "pasado_esp": "cerró",
        "participio_ing": "closed", "participio_esp": "cerrado",
        "gerundio_ing": "closing", "gerundio_esp": "cerrando",
        "oraciones": {
            "infinitivo":   {"ing": "I close the door quietly at night.","esp": "Yo cierro la puerta en silencio por la noche."},
            "pasadoSimple": {"ing": "You closed the window before bed.","esp": "Tú cerraste la ventana antes de dormir."},
            "participio":   {"ing": "She has closed the shop early.",  "esp": "Ella ha cerrado la tienda temprano."},
            "gerundio":     {"ing": "They are closing the deal today.","esp": "Ellos están cerrando el trato hoy."},
            "futuro":       {"ing": "We will close at nine o'clock.", "esp": "Nosotros cerraremos a las nueve."},
            "condicional":  {"ing": "That door would close automatically.","esp": "Esa puerta se cerraría automáticamente."}
        }
    },
    {
        "ing_inf": "collect", "esp_inf": "recoger",
        "pasado_ing": "collected", "pasado_esp": "recogió",
        "participio_ing": "collected", "participio_esp": "recogido",
        "gerundio_ing": "collecting", "gerundio_esp": "recogiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I collect stamps from around the world.","esp": "Yo colecciono estampas de todo el mundo."},
            "pasadoSimple": {"ing": "You collected the trash this morning.","esp": "Tú recogiste la basura esta mañana."},
            "participio":   {"ing": "She has collected enough data.", "esp": "Ella ha recopilado suficientes datos."},
            "gerundio":     {"ing": "They are collecting signatures for the petition.","esp": "Ellos están reuniendo firmas para la petición."},
            "futuro":       {"ing": "We will collect the packages at noon.","esp": "Nosotros recogeremos los paquetes al mediodía."},
            "condicional":  {"ing": "That shelf would collect dust.","esp": "Ese estante acumularía polvo."}
        }
    },
    {
        "ing_inf": "combine", "esp_inf": "combinar",
        "pasado_ing": "combined", "pasado_esp": "combinó",
        "participio_ing": "combined", "participio_esp": "combinado",
        "gerundio_ing": "combining", "gerundio_esp": "combinando",
        "oraciones": {
            "infinitivo":   {"ing": "I combine work and study every day.","esp": "Yo combino trabajo y estudio cada día."},
            "pasadoSimple": {"ing": "You combined the ingredients well.","esp": "Tú combinaste bien los ingredientes."},
            "participio":   {"ing": "She has combined the colors perfectly.","esp": "Ella ha combinado los colores a la perfección."},
            "gerundio":     {"ing": "They are combining their efforts.","esp": "Ellos están uniendo sus esfuerzos."},
            "futuro":       {"ing": "We will combine both teams tomorrow.","esp": "Nosotros combinaremos ambos equipos mañana."},
            "condicional":  {"ing": "That recipe would combine flavors.","esp": "Esa receta combinaría sabores."}
        }
    }
]


BLOQUE_6 = [
    {
        "ing_inf": "command", "esp_inf": "ordenar",
        "pasado_ing": "commanded", "pasado_esp": "ordenó",
        "participio_ing": "commanded", "participio_esp": "ordenado",
        "gerundio_ing": "commanding", "gerundio_esp": "ordenando",
        "oraciones": {
            "infinitivo":   {"ing": "I command attention when I speak.",   "esp": "Yo llamo la atención cuando hablo."},
            "pasadoSimple": {"ing": "You commanded respect from everyone.","esp": "Tú impusiste respeto de todos."},
            "participio":   {"ing": "She has commanded the troops well.",  "esp": "Ella ha mandado bien a las tropas."},
            "gerundio":     {"ing": "They are commanding high prices now.","esp": "Ellos están exigiendo precios altos."},
            "futuro":       {"ing": "We will command the fleet tomorrow.","esp": "Nosotros comandaremos la flota mañana."},
            "condicional":  {"ing": "That voice would command authority.","esp": "Esa voz impondría autoridad."}
        }
    },
    {
        "ing_inf": "communicate", "esp_inf": "comunicar",
        "pasado_ing": "communicated", "pasado_esp": "comunicó",
        "participio_ing": "communicated", "participio_esp": "comunicado",
        "gerundio_ing": "communicating", "gerundio_esp": "comunicando",
        "oraciones": {
            "infinitivo":   {"ing": "I communicate clearly in meetings.","esp": "Yo me comunico con claridad en reuniones."},
            "pasadoSimple": {"ing": "You communicated the news yesterday.","esp": "Tú comunicaste la noticia ayer."},
            "participio":   {"ing": "She has communicated her concerns.","esp": "Ella ha comunicado sus preocupaciones."},
            "gerundio":     {"ing": "They are communicating via email.","esp": "Ellos se están comunicando por correo."},
            "futuro":       {"ing": "We will communicate the results soon.","esp": "Nosotros comunicaremos los resultados pronto."},
            "condicional":  {"ing": "That logo would communicate trust.","esp": "Ese logo transmitiría confianza."}
        }
    },
    {
        "ing_inf": "compare", "esp_inf": "comparar",
        "pasado_ing": "compared", "pasado_esp": "comparó",
        "participio_ing": "compared", "participio_esp": "comparado",
        "gerundio_ing": "comparing", "gerundio_esp": "comparando",
        "oraciones": {
            "infinitivo":   {"ing": "I compare prices before buying.",    "esp": "Yo comparo precios antes de comprar."},
            "pasadoSimple": {"ing": "You compared both options carefully.","esp": "Tú comparaste ambas opciones con cuidado."},
            "participio":   {"ing": "She has compared the results.",      "esp": "Ella ha comparado los resultados."},
            "gerundio":     {"ing": "They are comparing notes after class.","esp": "Ellos están comparando notas después de clase."},
            "futuro":       {"ing": "We will compare the candidates.",    "esp": "Nosotros compararemos a los candidatos."},
            "condicional":  {"ing": "That model would compare well.",     "esp": "Ese modelo se compararía bien."}
        }
    },
    {
        "ing_inf": "complain", "esp_inf": "quejarse",
        "pasado_ing": "complained", "pasado_esp": "se quejó",
        "participio_ing": "complained", "participio_esp": "quejado",
        "gerundio_ing": "complaining", "gerundio_esp": "quejándose",
        "oraciones": {
            "infinitivo":   {"ing": "I complain about the noise at night.","esp": "Yo me quejo del ruido por la noche."},
            "pasadoSimple": {"ing": "You complained to the manager.",     "esp": "Tú te quejaste al gerente."},
            "participio":   {"ing": "He has complained repeatedly.",      "esp": "Él se ha quejado repetidamente."},
            "gerundio":     {"ing": "They are complaining about the service.","esp": "Ellos se están quejando del servicio."},
            "futuro":       {"ing": "We will complain if needed.",        "esp": "Nosotros nos quejaremos si es necesario."},
            "condicional":  {"ing": "The customer would complain again.","esp": "El cliente volvería a quejarse."}
        }
    },
    {
        "ing_inf": "complete", "esp_inf": "completar",
        "pasado_ing": "completed", "pasado_esp": "completó",
        "participio_ing": "completed", "participio_esp": "completado",
        "gerundio_ing": "completing", "gerundio_esp": "completando",
        "oraciones": {
            "infinitivo":   {"ing": "I complete the form online.",        "esp": "Yo completo el formulario en línea."},
            "pasadoSimple": {"ing": "You completed the task on time.",    "esp": "Tú completaste la tarea a tiempo."},
            "participio":   {"ing": "She has completed the course.",      "esp": "Ella ha completado el curso."},
            "gerundio":     {"ing": "They are completing the project.",  "esp": "Ellos están completando el proyecto."},
            "futuro":       {"ing": "We will complete it by Friday.",     "esp": "Nosotros lo completaremos para el viernes."},
            "condicional":  {"ing": "That move would complete the puzzle.","esp": "Ese movimiento completaría el rompecabezas."}
        }
    },
    {
        "ing_inf": "concentrate", "esp_inf": "concentrarse",
        "pasado_ing": "concentrated", "pasado_esp": "se concentró",
        "participio_ing": "concentrated", "participio_esp": "concentrado",
        "gerundio_ing": "concentrating", "gerundio_esp": "concentrándose",
        "oraciones": {
            "infinitivo":   {"ing": "I concentrate better with music.",   "esp": "Yo me concentro mejor con música."},
            "pasadoSimple": {"ing": "You concentrated too hard.",         "esp": "Tú te concentraste demasiado."},
            "participio":   {"ing": "She has concentrated on her goals.", "esp": "Ella se ha concentrado en sus metas."},
            "gerundio":     {"ing": "They are concentrating their forces.","esp": "Ellos están concentrando sus fuerzas."},
            "futuro":       {"ing": "We will concentrate on this issue.", "esp": "Nosotros nos concentraremos en este tema."},
            "condicional":  {"ing": "That merger would concentrate power.","esp": "Esa fusión concentraría el poder."}
        }
    },
    {
        "ing_inf": "concern", "esp_inf": "preocupar",
        "pasado_ing": "concerned", "pasado_esp": "preocupó",
        "participio_ing": "concerned", "participio_esp": "preocupado",
        "gerundio_ing": "concerning", "gerundio_esp": "preocupando",
        "oraciones": {
            "infinitivo":   {"ing": "I concern myself with details.",     "esp": "Yo me preocupo por los detalles."},
            "pasadoSimple": {"ing": "You concerned me deeply.",            "esp": "Tú me preocupaste mucho."},
            "participio":   {"ing": "She has concerned the investors.",   "esp": "Ella ha preocupado a los inversores."},
            "gerundio":     {"ing": "They are concerning the public.",    "esp": "Ellos están preocupando al público."},
            "futuro":       {"ing": "We will concern the board members.","esp": "Nosotros preocuparemos a la junta."},
            "condicional":  {"ing": "That decision would concern the authorities.","esp": "Esa decisión preocuparía a las autoridades."}
        }
    },
    {
        "ing_inf": "confess", "esp_inf": "confesar",
        "pasado_ing": "confessed", "pasado_esp": "confesó",
        "participio_ing": "confessed", "participio_esp": "confesado",
        "gerundio_ing": "confessing", "gerundio_esp": "confesando",
        "oraciones": {
            "infinitivo":   {"ing": "I confess my love for you.",         "esp": "Yo confieso mi amor por ti."},
            "pasadoSimple": {"ing": "You confessed the whole truth.",    "esp": "Tú confesaste toda la verdad."},
            "participio":   {"ing": "She has confessed her mistake.",     "esp": "Ella ha confesado su error."},
            "gerundio":     {"ing": "They are confessing at church.",     "esp": "Ellos se están confesando en la iglesia."},
            "futuro":       {"ing": "We will confess everything.",        "esp": "Nosotros confesaremos todo."},
            "condicional":  {"ing": "That witness would confess under oath.","esp": "Ese testigo confesaría bajo juramento."}
        }
    },
    {
        "ing_inf": "connect", "esp_inf": "conectar",
        "pasado_ing": "connected", "pasado_esp": "conectó",
        "participio_ing": "connected", "participio_esp": "conectado",
        "gerundio_ing": "connecting", "gerundio_esp": "conectando",
        "oraciones": {
            "infinitivo":   {"ing": "I connect devices via Bluetooth.",  "esp": "Yo conecto dispositivos por Bluetooth."},
            "pasadoSimple": {"ing": "You connected the cables correctly.","esp": "Tú conectaste los cables correctamente."},
            "participio":   {"ing": "She has connected with the audience.","esp": "Ella se ha conectado con el público."},
            "gerundio":     {"ing": "They are connecting to the server.","esp": "Ellos se están conectando al servidor."},
            "futuro":       {"ing": "We will connect the dots later.",    "esp": "Nosotros conectaremos los puntos después."},
            "condicional":  {"ing": "That hub would connect all devices.","esp": "Ese concentrador conectaría todos los dispositivos."}
        }
    },
    {
        "ing_inf": "consider", "esp_inf": "considerar",
        "pasado_ing": "considered", "pasado_esp": "consideró",
        "participio_ing": "considered", "participio_esp": "considerado",
        "gerundio_ing": "considering", "gerundio_esp": "considerando",
        "oraciones": {
            "infinitivo":   {"ing": "I consider your offer carefully.",  "esp": "Yo considero tu oferta con cuidado."},
            "pasadoSimple": {"ing": "You considered all the risks.",     "esp": "Tú consideraste todos los riesgos."},
            "participio":   {"ing": "She has considered every option.",  "esp": "Ella ha considerado cada opción."},
            "gerundio":     {"ing": "They are considering a move abroad.","esp": "Ellos están considerando mudarse al extranjero."},
            "futuro":       {"ing": "We will consider it tomorrow.",     "esp": "Nosotros lo consideraremos mañana."},
            "condicional":  {"ing": "That factor would consider the impact.","esp": "Ese factor tomaría en cuenta el impacto."}
        }
    }
]


BLOQUE_7 = [
    {
        "ing_inf": "consist", "esp_inf": "consistir",
        "pasado_ing": "consisted", "pasado_esp": "consistió",
        "participio_ing": "consisted", "participio_esp": "consistido",
        "gerundio_ing": "consisting", "gerundio_esp": "consistiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I consist mostly of curiosity and courage.","esp": "Yo consisto principalmente de curiosidad y valor."},
            "pasadoSimple": {"ing": "You consisted of three layers.",   "esp": "Tú consistías de tres capas."},
            "participio":   {"ing": "She has consisted of the best ingredients.","esp": "Ella ha consistido de los mejores ingredientes."},
            "gerundio":     {"ing": "The menu consists mainly of fish.","esp": "El menú consiste principalmente de pescado."},
            "futuro":       {"ing": "We will consist of five members.", "esp": "Nosotros consistiremos de cinco miembros."},
            "condicional":  {"ing": "That package would consist of multiple parts.","esp": "Ese paquete constaría de varias partes."}
        }
    },
    {
        "ing_inf": "contain", "esp_inf": "contener",
        "pasado_ing": "contained", "pasado_esp": "contuvo",
        "participio_ing": "contained", "participio_esp": "contenido",
        "gerundio_ing": "containing", "gerundio_esp": "conteniendo",
        "oraciones": {
            "infinitivo":   {"ing": "I contain my excitement in meetings.","esp": "Yo contengo mi emoción en las reuniones."},
            "pasadoSimple": {"ing": "You contained the spill quickly.",  "esp": "Tú contuviste el derrame rápidamente."},
            "participio":   {"ing": "She has contained the outbreak.",   "esp": "Ella ha contenido el brote."},
            "gerundio":     {"ing": "They are containing their laughter.","esp": "Ellos están conteniendo la risa."},
            "futuro":       {"ing": "We will contain the damage.",       "esp": "Nosotros contendremos los daños."},
            "condicional":  {"ing": "That box would contain surprises.","esp": "Esa caja contendría sorpresas."}
        }
    },
    {
        "ing_inf": "continue", "esp_inf": "continuar",
        "pasado_ing": "continued", "pasado_esp": "continuó",
        "participio_ing": "continued", "participio_esp": "continuado",
        "gerundio_ing": "continuing", "gerundio_esp": "continuando",
        "oraciones": {
            "infinitivo":   {"ing": "I continue learning new things every day.","esp": "Yo sigo aprendiendo cosas nuevas cada día."},
            "pasadoSimple": {"ing": "You continued the search all night.","esp": "Tú continuaste la búsqueda toda la noche."},
            "participio":   {"ing": "She has continued working late.",   "esp": "Ella ha continuado trabajando hasta tarde."},
            "gerundio":     {"ing": "They are continuing the family tradition.","esp": "Ellos están continuando la tradición familiar."},
            "futuro":       {"ing": "We will continue tomorrow morning.","esp": "Nosotros continuaremos mañana por la mañana."},
            "condicional":  {"ing": "That trend would continue rising.","esp": "Esa tendencia seguiría subiendo."}
        }
    },
    {
        "ing_inf": "control", "esp_inf": "controlar",
        "pasado_ing": "controlled", "pasado_esp": "controló",
        "participio_ing": "controlled", "participio_esp": "controlado",
        "gerundio_ing": "controlling", "gerundio_esp": "controlando",
        "oraciones": {
            "infinitivo":   {"ing": "I control my temper at work.",     "esp": "Yo controlo mi genio en el trabajo."},
            "pasadoSimple": {"ing": "You controlled the meeting well.","esp": "Tú controlaste bien la reunión."},
            "participio":   {"ing": "She has controlled the budget carefully.","esp": "Ella ha controlado el presupuesto con cuidado."},
            "gerundio":     {"ing": "They are controlling the traffic flow.","esp": "Ellos están controlando el flujo de tráfico."},
            "futuro":       {"ing": "We will control the costs strictly.","esp": "Nosotros controlaremos los costos estrictamente."},
            "condicional":  {"ing": "That device would control the lights remotely.","esp": "Ese dispositivo controlaría las luces a distancia."}
        }
    },
    {
        "ing_inf": "cook", "esp_inf": "cocinar",
        "pasado_ing": "cooked", "pasado_esp": "cocinó",
        "participio_ing": "cooked", "participio_esp": "cocinado",
        "gerundio_ing": "cooking", "gerundio_esp": "cocinando",
        "oraciones": {
            "infinitivo":   {"ing": "I cook dinner for my family every night.","esp": "Yo cocino la cena para mi familia cada noche."},
            "pasadoSimple": {"ing": "You cooked a great meal last Sunday.","esp": "Tú cocinaste una gran comida el domingo pasado."},
            "participio":   {"ing": "She has cooked for years as a chef.","esp": "Ella ha cocinado durante años como chef."},
            "gerundio":     {"ing": "They are cooking together in the kitchen.","esp": "Ellos están cocinando juntos en la cocina."},
            "futuro":       {"ing": "We will cook paella this weekend.","esp": "Nosotros cocinaremos paella este fin de semana."},
            "condicional":  {"ing": "That recipe would cook in 30 minutes.","esp": "Esa receta se cocinaría en 30 minutos."}
        }
    },
    {
        "ing_inf": "copy", "esp_inf": "copiar",
        "pasado_ing": "copied", "pasado_esp": "copió",
        "participio_ing": "copied", "participio_esp": "copiado",
        "gerundio_ing": "copying", "gerundio_esp": "copiando",
        "oraciones": {
            "infinitivo":   {"ing": "I copy the text into a new file.","esp": "Yo copio el texto en un archivo nuevo."},
            "pasadoSimple": {"ing": "You copied my homework yesterday.","esp": "Tú copiaste mi tarea ayer."},
            "participio":   {"ing": "She has copied all the files to USB.","esp": "Ella ha copiado todos los archivos al USB."},
            "gerundio":     {"ing": "They are copying the documents right now.","esp": "Ellos están copiando los documentos ahora mismo."},
            "futuro":       {"ing": "We will copy the data to the cloud.","esp": "Nosotros copiaremos los datos a la nube."},
            "condicional":  {"ing": "That feature would copy files automatically.","esp": "Esa función copiaría archivos automáticamente."}
        }
    },
    {
        "ing_inf": "correct", "esp_inf": "corregir",
        "pasado_ing": "corrected", "pasado_esp": "corrigió",
        "participio_ing": "corrected", "participio_esp": "corregido",
        "gerundio_ing": "correcting", "gerundio_esp": "corrigiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I correct mistakes carefully before submitting.","esp": "Yo corrijo errores con cuidado antes de enviar."},
            "pasadoSimple": {"ing": "You corrected the teacher politely.","esp": "Tú corregiste al profesor con educación."},
            "participio":   {"ing": "She has corrected all the typos.","esp": "Ella ha corregido todos los errores tipográficos."},
            "gerundio":     {"ing": "They are correcting the historical record.","esp": "Ellos están corrigiendo el registro histórico."},
            "futuro":       {"ing": "We will correct the course immediately.","esp": "Nosotros corregiremos el rumbo de inmediato."},
            "condicional":  {"ing": "That update would correct the security bug.","esp": "Esa actualización corregiría el error de seguridad."}
        }
    },
    {
        "ing_inf": "count", "esp_inf": "contar",
        "pasado_ing": "counted", "pasado_esp": "contó",
        "participio_ing": "counted", "participio_esp": "contado",
        "gerundio_ing": "counting", "gerundio_esp": "contando",
        "oraciones": {
            "infinitivo":   {"ing": "I count my blessings every night.","esp": "Yo cuento mis bendiciones cada noche."},
            "pasadoSimple": {"ing": "You counted the money twice.",      "esp": "Tú contaste el dinero dos veces."},
            "participio":   {"ing": "She has counted all the votes.",    "esp": "Ella ha contado todos los votos."},
            "gerundio":     {"ing": "They are counting the stars tonight.","esp": "Ellos están contando las estrellas esta noche."},
            "futuro":       {"ing": "We will count the attendees tomorrow.","esp": "Nosotros contaremos los asistentes mañana."},
            "condicional":  {"ing": "That vote would count double.","esp": "Ese voto contaría doble."}
        }
    },
    {
        "ing_inf": "cover", "esp_inf": "cubrir",
        "pasado_ing": "covered", "pasado_esp": "cubrió",
        "participio_ing": "covered", "participio_esp": "cubierto",
        "gerundio_ing": "covering", "gerundio_esp": "cubriendo",
        "oraciones": {
            "infinitivo":   {"ing": "I cover my mouth when I cough.",   "esp": "Yo me cubro la boca al toser."},
            "pasadoSimple": {"ing": "You covered the news live yesterday.","esp": "Tú cubriste la noticia en vivo ayer."},
            "participio":   {"ing": "She has covered all the expenses.","esp": "Ella ha cubierto todos los gastos."},
            "gerundio":     {"ing": "They are covering the roof today.","esp": "Ellos están cubriendo el techo hoy."},
            "futuro":       {"ing": "We will cover the event live.","esp": "Nosotros cubriremos el evento en vivo."},
            "condicional":  {"ing": "That insurance would cover everything.","esp": "Ese seguro cubriría todo."}
        }
    },
    {
        "ing_inf": "crash", "esp_inf": "caerse",
        "pasado_ing": "crashed", "pasado_esp": "se cayó",
        "participio_ing": "crashed", "participio_esp": "caído",
        "gerundio_ing": "crashing", "gerundio_esp": "cayéndose",
        "futuro_esp": "se caerá", "cond_esp": "se caería",
        "oraciones": {
            "infinitivo":   {"ing": "I crash the app by opening too many tabs.","esp": "Yo tumbo la app abriendo muchas pestañas."},
            "pasadoSimple": {"ing": "You crashed the whole system.",   "esp": "Tú tumbaste todo el sistema."},
            "participio":   {"ing": "The server has crashed twice today.","esp": "El servidor se ha caído dos veces hoy."},
            "gerundio":     {"ing": "They are crashing the network.","esp": "Ellos están tumbando la red."},
            "futuro":       {"ing": "We will crash if we don't optimize.","esp": "Nosotros nos caeremos si no optimizamos."},
            "condicional":  {"ing": "That bug would crash the entire app.","esp": "Ese error tumbaría la aplicación entera."}
        }
    }
]


BLOQUE_8 = [
    {
        "ing_inf": "create", "esp_inf": "crear",
        "pasado_ing": "created", "pasado_esp": "creó",
        "participio_ing": "created", "participio_esp": "creado",
        "gerundio_ing": "creating", "gerundio_esp": "creando",
        "oraciones": {
            "infinitivo":   {"ing": "I create content for my blog every week.","esp": "Yo creo contenido para mi blog cada semana."},
            "pasadoSimple": {"ing": "You created a beautiful design.",    "esp": "Tú creaste un diseño hermoso."},
            "participio":   {"ing": "She has created a successful startup.","esp": "Ella ha creado una startup exitosa."},
            "gerundio":     {"ing": "They are creating new products.","esp": "Ellos están creando nuevos productos."},
            "futuro":       {"ing": "We will create a detailed plan.","esp": "Nosotros crearemos un plan detallado."},
            "condicional":  {"ing": "That tool would create real value.","esp": "Esa herramienta crearía valor real."}
        }
    },
    {
        "ing_inf": "cross", "esp_inf": "cruzar",
        "pasado_ing": "crossed", "pasado_esp": "cruzó",
        "participio_ing": "crossed", "participio_esp": "cruzado",
        "gerundio_ing": "crossing", "gerundio_esp": "cruzando",
        "oraciones": {
            "infinitivo":   {"ing": "I cross the street at the corner.","esp": "Yo cruzo la calle en la esquina."},
            "pasadoSimple": {"ing": "You crossed the border yesterday.","esp": "Tú cruzaste la frontera ayer."},
            "participio":   {"ing": "She has crossed the finish line.","esp": "Ella ha cruzado la meta."},
            "gerundio":     {"ing": "They are crossing the river now.","esp": "Ellos están cruzando el río ahora."},
            "futuro":       {"ing": "We will cross the bridge tomorrow.","esp": "Nosotros cruzaremos el puente mañana."},
            "condicional":  {"ing": "That road would cross the mountain.","esp": "Esa carretera atravesaría la montaña."}
        }
    },
    {
        "ing_inf": "cry", "esp_inf": "llorar",
        "pasado_ing": "cried", "pasado_esp": "lloró",
        "participio_ing": "cried", "participio_esp": "llorado",
        "gerundio_ing": "crying", "gerundio_esp": "llorando",
        "oraciones": {
            "infinitivo":   {"ing": "I cry when I watch sad movies.",   "esp": "Yo lloro cuando veo películas tristes."},
            "pasadoSimple": {"ing": "You cried at the wedding.",         "esp": "Tú lloraste en la boda."},
            "participio":   {"ing": "She has cried for hours.",          "esp": "Ella ha llorado por horas."},
            "gerundio":     {"ing": "They are crying for help.","esp": "Ellos están pidiendo ayuda a gritos."},
            "futuro":       {"ing": "We will cry with joy.","esp": "Nosotros lloraremos de alegría."},
            "condicional":  {"ing": "That story would make anyone cry.","esp": "Esa historia haría llorar a cualquiera."}
        }
    },
    {
        "ing_inf": "cure", "esp_inf": "curar",
        "pasado_ing": "cured", "pasado_esp": "curó",
        "participio_ing": "cured", "participio_esp": "curado",
        "gerundio_ing": "curing", "gerundio_esp": "curando",
        "oraciones": {
            "infinitivo":   {"ing": "I cure my own meats at home.","esp": "Yo cur mis propias carnes en casa."},
            "pasadoSimple": {"ing": "You cured the patient completely.","esp": "Tú curaste al paciente por completo."},
            "participio":   {"ing": "She has cured the disease.","esp": "Ella ha curado la enfermedad."},
            "gerundio":     {"ing": "They are curing rare cancers.","esp": "Ellos están curando cánceres raros."},
            "futuro":       {"ing": "We will cure the infection soon.","esp": "Nosotros curaremos la infección pronto."},
            "condicional":  {"ing": "That treatment would cure it.","esp": "Ese tratamiento lo curaría."}
        }
    },
    {
        "ing_inf": "curl", "esp_inf": "rizar",
        "pasado_ing": "curled", "pasado_esp": "rizó",
        "participio_ing": "curled", "participio_esp": "rizado",
        "gerundio_ing": "curling", "gerundio_esp": "rizando",
        "oraciones": {
            "infinitivo":   {"ing": "I curl my hair with a flat iron.","esp": "Yo rizo mi pelo con una plancha."},
            "pasadoSimple": {"ing": "You curled the ribbon nicely.","esp": "Tú rizaste el listón con gracia."},
            "participio":   {"ing": "She has curled the paper edges.","esp": "Ella ha rizado los bordes del papel."},
            "gerundio":     {"ing": "They are curling their hair for the party.","esp": "Ellos están rizando su pelo para la fiesta."},
            "futuro":       {"ing": "We will curl the leaves for decoration.","esp": "Nosotros rizaremos las hojas para decorar."},
            "condicional":  {"ing": "That perm would curl even straight hair.","esp": "Esa permanente rizaría incluso el pelo lacio."}
        }
    },
    {
        "ing_inf": "dance", "esp_inf": "bailar",
        "pasado_ing": "danced", "pasado_esp": "bailó",
        "participio_ing": "danced", "participio_esp": "bailado",
        "gerundio_ing": "dancing", "gerundio_esp": "bailando",
        "oraciones": {
            "infinitivo":   {"ing": "I dance salsa on weekends.",      "esp": "Yo bailo salsa los fines de semana."},
            "pasadoSimple": {"ing": "You danced beautifully at the party.","esp": "Tú bailaste hermosamente en la fiesta."},
            "participio":   {"ing": "She has danced since she was five.","esp": "Ella ha bailado desde los cinco años."},
            "gerundio":     {"ing": "They are dancing all night long.","esp": "Ellos están bailando toda la noche."},
            "futuro":       {"ing": "We will dance at the wedding.","esp": "Nosotros bailaremos en la boda."},
            "condicional":  {"ing": "That song would make anyone dance.","esp": "Esa canción haría bailar a cualquiera."}
        }
    },
    {
        "ing_inf": "dare", "esp_inf": "atreverse",
        "pasado_ing": "dared", "pasado_esp": "se atrevió",
        "participio_ing": "dared", "participio_esp": "atrevido",
        "gerundio_ing": "daring", "gerundio_esp": "atreviéndose",
        "futuro_esp": "se atreverá", "cond_esp": "se atrevería",
        "oraciones": {
            "infinitivo":   {"ing": "I dare to dream big every day.",  "esp": "Yo me atrevo a soñar en grande cada día."},
            "pasadoSimple": {"ing": "You dared to challenge the boss.","esp": "Tú te atreviste a desafiar al jefe."},
            "participio":   {"ing": "She has dared to be different.",  "esp": "Ella se ha atrevido a ser diferente."},
            "gerundio":     {"ing": "They are daring to try something new.","esp": "Ellos se están atreviendo a intentar algo nuevo."},
            "futuro":       {"ing": "We will dare to change the rules.","esp": "Nosotros nos atreveremos a cambiar las reglas."},
            "condicional":  {"ing": "That startup would dare to compete.","esp": "Esa startup se atrevería a competir."}
        }
    },
    {
        "ing_inf": "date", "esp_inf": "fechar",
        "pasado_ing": "dated", "pasado_esp": "fechó",
        "participio_ing": "dated", "participio_esp": "fechado",
        "gerundio_ing": "dating", "gerundio_esp": "fechando",
        "oraciones": {
            "infinitivo":   {"ing": "I date every entry in my journal.","esp": "Yo fecho cada entrada de mi diario."},
            "pasadoSimple": {"ing": "You dated the check correctly.","esp": "Tú fechaste el cheque correctamente."},
            "participio":   {"ing": "She has dated the historical photos.","esp": "Ella ha fechado las fotos históricas."},
            "gerundio":     {"ing": "They are dating the ancient fossils.","esp": "Ellos están fechando los fósiles antiguos."},
            "futuro":       {"ing": "We will date the contract tomorrow.","esp": "Nosotros fecharemos el contrato mañana."},
            "condicional":  {"ing": "That signature would date the letter.","esp": "Esa firma fecharía la carta."}
        }
    },
    {
        "ing_inf": "decay", "esp_inf": "deteriorarse",
        "pasado_ing": "decayed", "pasado_esp": "se deterioró",
        "participio_ing": "decayed", "participio_esp": "deteriorado",
        "gerundio_ing": "decaying", "gerundio_esp": "deteriorándose",
        "futuro_esp": "se deteriorará", "cond_esp": "se deterioraría",
        "oraciones": {
            "infinitivo":   {"ing": "I let old wood decay naturally.",  "esp": "Yo dejo que la madera vieja se deteriore naturalmente."},
            "pasadoSimple": {"ing": "You let the fence decay completely.","esp": "Tú dejaste que la valla se deteriorara por completo."},
            "participio":   {"ing": "The building has decayed over the years.","esp": "El edificio se ha deteriorado con los años."},
            "gerundio":     {"ing": "The ruins are decaying fast.",     "esp": "Las ruinas se están deteriorando rápido."},
            "futuro":       {"ing": "We will prevent the bridge from decaying.","esp": "Nosotros evitaremos que el puente se deteriore."},
            "condicional":  {"ing": "That material would decay quickly outdoors.","esp": "Ese material se deterioraría rápido al aire libre."}
        }
    },
    {
        "ing_inf": "deceive", "esp_inf": "engañar",
        "pasado_ing": "deceived", "pasado_esp": "engañó",
        "participio_ing": "deceived", "participio_esp": "engañado",
        "gerundio_ing": "deceiving", "gerundio_esp": "engañando",
        "oraciones": {
            "infinitivo":   {"ing": "I deceive no one in my life.",     "esp": "Yo no engaño a nadie en mi vida."},
            "pasadoSimple": {"ing": "You deceived me completely.",     "esp": "Tú me engañaste por completo."},
            "participio":   {"ing": "She has deceived her partner.",   "esp": "Ella ha engañado a su pareja."},
            "gerundio":     {"ing": "They are deceiving the public.","esp": "Ellos están engañando al público."},
            "futuro":       {"ing": "We will deceive the enemy.","esp": "Nosotros engañaremos al enemigo."},
            "condicional":  {"ing": "That smile would deceive anyone.","esp": "Esa sonrisa engañaría a cualquiera."}
        }
    }
]


BLOQUE_9 = [
    {
        "ing_inf": "decide", "esp_inf": "decidir",
        "pasado_ing": "decided", "pasado_esp": "decidió",
        "participio_ing": "decided", "participio_esp": "decidido",
        "gerundio_ing": "deciding", "gerundio_esp": "decidiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I decide quickly under pressure.","esp": "Yo decido rápido bajo presión."},
            "pasadoSimple": {"ing": "You decided to stay home.",      "esp": "Tú decidiste quedarte en casa."},
            "participio":   {"ing": "She has decided already.",       "esp": "Ella ya ha decidido."},
            "gerundio":     {"ing": "They are deciding right now.",   "esp": "Ellos están decidiendo ahora mismo."},
            "futuro":       {"ing": "We will decide tomorrow morning.","esp": "Nosotros decidiremos mañana por la mañana."},
            "condicional":  {"ing": "That vote would decide the election.","esp": "Ese voto decidiría la elección."}
        }
    },
    {
        "ing_inf": "decorate", "esp_inf": "decorar",
        "pasado_ing": "decorated", "pasado_esp": "decoró",
        "participio_ing": "decorated", "participio_esp": "decorado",
        "gerundio_ing": "decorating", "gerundio_esp": "decorando",
        "oraciones": {
            "infinitivo":   {"ing": "I decorate the tree every Christmas.","esp": "Yo decoro el árbol cada Navidad."},
            "pasadoSimple": {"ing": "You decorated the room nicely.","esp": "Tú decoraste el cuarto con buen gusto."},
            "participio":   {"ing": "She has decorated the cake beautifully.","esp": "Ella ha decorado el pastel bellamente."},
            "gerundio":     {"ing": "They are decorating the office.","esp": "Ellos están decorando la oficina."},
            "futuro":       {"ing": "We will decorate the hall for the party.","esp": "Nosotros decoraremos el salón para la fiesta."},
            "condicional":  {"ing": "That color would decorate any room.","esp": "Ese color decoraría cualquier cuarto."}
        }
    },
    {
        "ing_inf": "deliver", "esp_inf": "entregar",
        "pasado_ing": "delivered", "pasado_esp": "entregó",
        "participio_ing": "delivered", "participio_esp": "entregado",
        "gerundio_ing": "delivering", "gerundio_esp": "entregando",
        "oraciones": {
            "infinitivo":   {"ing": "I deliver packages on weekends.","esp": "Yo entrego paquetes los fines de semana."},
            "pasadoSimple": {"ing": "You delivered the speech well.","esp": "Tú entregaste bien el discurso."},
            "participio":   {"ing": "She has delivered the baby safely.","esp": "Ella ha dado a luz al bebé sin problemas."},
            "gerundio":     {"ing": "They are delivering food right now.","esp": "Ellos están entregando comida ahora mismo."},
            "futuro":       {"ing": "We will deliver the report by noon.","esp": "Nosotros entregaremos el informe al mediodía."},
            "condicional":  {"ing": "That courier would deliver it fast.","esp": "Ese servicio de mensajería lo entregaría rápido."}
        }
    },
    {
        "ing_inf": "depend", "esp_inf": "depender",
        "pasado_ing": "depended", "pasado_esp": "dependió",
        "participio_ing": "depended", "participio_esp": "dependido",
        "gerundio_ing": "depending", "gerundio_esp": "dependiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I depend on coffee every morning.","esp": "Yo dependo del café cada mañana."},
            "pasadoSimple": {"ing": "You depended on your parents a lot.","esp": "Tú dependías mucho de tus padres."},
            "participio":   {"ing": "She has depended on herself always.","esp": "Ella siempre ha dependido de sí misma."},
            "gerundio":     {"ing": "They are depending on pure luck.","esp": "Ellos están dependiendo de la pura suerte."},
            "futuro":       {"ing": "We will depend on the weather forecast.","esp": "Nosotros dependeremos del pronóstico del clima."},
            "condicional":  {"ing": "That would depend on the circumstances.","esp": "Eso dependería de las circunstancias."}
        }
    },
    {
        "ing_inf": "describe", "esp_inf": "describir",
        "pasado_ing": "described", "pasado_esp": "describió",
        "participio_ing": "described", "participio_esp": "descrito",
        "gerundio_ing": "describing", "gerundio_esp": "describiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I describe my feelings openly.","esp": "Yo describo mis sentimientos abiertamente."},
            "pasadoSimple": {"ing": "You described the scene vividly.","esp": "Tú describiste la escena vívidamente."},
            "participio":   {"ing": "She has described the suspect in detail.","esp": "Ella ha descrito al sospechoso en detalle."},
            "gerundio":     {"ing": "They are describing the workflow now.","esp": "Ellos están describiendo el flujo de trabajo ahora."},
            "futuro":       {"ing": "We will describe the new features.","esp": "Nosotros describiremos las nuevas funciones."},
            "condicional":  {"ing": "That word would describe it perfectly.","esp": "Esa palabra lo describiría a la perfección."}
        }
    },
    {
        "ing_inf": "deserve", "esp_inf": "merecer",
        "pasado_ing": "deserved", "pasado_esp": "mereció",
        "participio_ing": "deserved", "participio_esp": "merecido",
        "gerundio_ing": "deserving", "gerundio_esp": "mereciendo",
        "oraciones": {
            "infinitivo":   {"ing": "I deserve a vacation after this year.","esp": "Yo merezco unas vacaciones después de este año."},
            "pasadoSimple": {"ing": "You deserved that promotion.",   "esp": "Tú mereciste ese ascenso."},
            "participio":   {"ing": "She has deserved recognition for years.","esp": "Ella ha merecido el reconocimiento durante años."},
            "gerundio":     {"ing": "They are deserving better opportunities.","esp": "Ellos están mereciendo mejores oportunidades."},
            "futuro":       {"ing": "We will deserve the reward after the effort.","esp": "Nosotros mereceremos la recompensa tras el esfuerzo."},
            "condicional":  {"ing": "That effort would deserve public praise.","esp": "Ese esfuerzo merecería un elogio público."}
        }
    },
    {
        "ing_inf": "design", "esp_inf": "diseñar",
        "pasado_ing": "designed", "pasado_esp": "diseñó",
        "participio_ing": "designed", "participio_esp": "diseñado",
        "gerundio_ing": "designing", "gerundio_esp": "diseñando",
        "oraciones": {
            "infinitivo":   {"ing": "I design websites for a living.","esp": "Yo diseño sitios web para vivir."},
            "pasadoSimple": {"ing": "You designed this beautiful logo.","esp": "Tú diseñaste este logo hermoso."},
            "participio":   {"ing": "She has designed the wedding dress.","esp": "Ella ha diseñado el vestido de novia."},
            "gerundio":     {"ing": "They are designing a new mobile app.","esp": "Ellos están diseñando una aplicación móvil nueva."},
            "futuro":       {"ing": "We will design the user interface.","esp": "Nosotros diseñaremos la interfaz de usuario."},
            "condicional":  {"ing": "That architect would design something bold.","esp": "Ese arquitecto diseñaría algo audaz."}
        }
    },
    {
        "ing_inf": "destroy", "esp_inf": "destruir",
        "pasado_ing": "destroyed", "pasado_esp": "destruyó",
        "participio_ing": "destroyed", "participio_esp": "destruido",
        "gerundio_ing": "destroying", "gerundio_esp": "destruyendo",
        "oraciones": {
            "infinitivo":   {"ing": "I destroy my doubts with action.","esp": "Yo destruyo mis dudas con acción."},
            "pasadoSimple": {"ing": "You destroyed the evidence.","esp": "Tú destruiste la evidencia."},
            "participio":   {"ing": "She has destroyed his career.","esp": "Ella ha destruido su carrera."},
            "gerundio":     {"ing": "They are destroying the old building.","esp": "Ellos están destruyendo el edificio viejo."},
            "futuro":       {"ing": "We will destroy the competition.","esp": "Nosotros destruiremos a la competencia."},
            "condicional":  {"ing": "That virus would destroy all the data.","esp": "Ese virus destruiría todos los datos."}
        }
    },
    {
        "ing_inf": "detect", "esp_inf": "detectar",
        "pasado_ing": "detected", "pasado_esp": "detectó",
        "participio_ing": "detected", "participio_esp": "detectado",
        "gerundio_ing": "detecting", "gerundio_esp": "detectando",
        "oraciones": {
            "infinitivo":   {"ing": "I detect lies pretty easily.","esp": "Yo detecto mentiras con bastante facilidad."},
            "pasadoSimple": {"ing": "You detected the bug early.","esp": "Tú detectaste el error temprano."},
            "participio":   {"ing": "She has detected the problem.","esp": "Ella ha detectado el problema."},
            "gerundio":     {"ing": "They are detecting suspicious movements.","esp": "Ellos están detectando movimientos sospechosos."},
            "futuro":       {"ing": "We will detect anomalies in the data.","esp": "Nosotros detectaremos anomalías en los datos."},
            "condicional":  {"ing": "That sensor would detect smoke instantly.","esp": "Ese sensor detectaría humo al instante."}
        }
    },
    {
        "ing_inf": "develop", "esp_inf": "desarrollar",
        "pasado_ing": "developed", "pasado_esp": "desarrolló",
        "participio_ing": "developed", "participio_esp": "desarrollado",
        "gerundio_ing": "developing", "gerundio_esp": "desarrollando",
        "oraciones": {
            "infinitivo":   {"ing": "I develop apps in my free time.","esp": "Yo desarrollo aplicaciones en mi tiempo libre."},
            "pasadoSimple": {"ing": "You developed the strategy quickly.","esp": "Tú desarrollaste la estrategia rápidamente."},
            "participio":   {"ing": "She has developed a new skill.","esp": "Ella ha desarrollado una habilidad nueva."},
            "gerundio":     {"ing": "They are developing the project.","esp": "Ellos están desarrollando el proyecto."},
            "futuro":       {"ing": "We will develop the software next year.","esp": "Nosotros desarrollaremos el software el próximo año."},
            "condicional":  {"ing": "That habit would develop over time.","esp": "Ese hábito se desarrollaría con el tiempo."}
        }
    }
]


BLOQUE_10 = [
    {
        "ing_inf": "disagree", "esp_inf": "discrepar",
        "pasado_ing": "disagreed", "pasado_esp": "discrepó",
        "participio_ing": "disagreed", "participio_esp": "discrepado",
        "gerundio_ing": "disagreeing", "gerundio_esp": "discrepando",
        "oraciones": {
            "infinitivo":   {"ing": "I disagree with that opinion.",   "esp": "Yo discrepo de esa opinión."},
            "pasadoSimple": {"ing": "You disagreed politely yesterday.","esp": "Tú discrepaste respetuosamente ayer."},
            "participio":   {"ing": "She has disagreed with the report.","esp": "Ella ha discrepado del informe."},
            "gerundio":     {"ing": "They are disagreeing about politics.","esp": "Ellos están discrepando sobre política."},
            "futuro":       {"ing": "We will disagree on this point.","esp": "Nosotros discreparemos en este punto."},
            "condicional":  {"ing": "That study would disagree with the theory.","esp": "Ese estudio discreparía con la teoría."}
        }
    },
    {
        "ing_inf": "disappear", "esp_inf": "desaparecer",
        "pasado_ing": "disappeared", "pasado_esp": "desapareció",
        "participio_ing": "disappeared", "participio_esp": "desaparecido",
        "gerundio_ing": "disappearing", "gerundio_esp": "desapareciendo",
        "oraciones": {
            "infinitivo":   {"ing": "I disappear when I'm stressed.", "esp": "Yo desaparezco cuando estoy estresado."},
            "pasadoSimple": {"ing": "You disappeared without warning.","esp": "Tú desapareciste sin avisar."},
            "participio":   {"ing": "She has disappeared from social media.","esp": "Ella ha desaparecido de las redes sociales."},
            "gerundio":     {"ing": "They are disappearing one by one.","esp": "Ellos están desapareciendo uno a uno."},
            "futuro":       {"ing": "We will disappear into the crowd.","esp": "Nosotros desapareceremos entre la multitud."},
            "condicional":  {"ing": "That file would disappear quickly.","esp": "Ese archivo desaparecería rápido."}
        }
    },
    {
        "ing_inf": "disappoint", "esp_inf": "decepcionar",
        "pasado_ing": "disappointed", "pasado_esp": "decepcionó",
        "participio_ing": "disappointed", "participio_esp": "decepcionado",
        "gerundio_ing": "disappointing", "gerundio_esp": "decepcionando",
        "oraciones": {
            "infinitivo":   {"ing": "I disappoint myself sometimes.","esp": "Yo me decepciono a veces."},
            "pasadoSimple": {"ing": "You disappointed your parents.","esp": "Tú decepcionaste a tus padres."},
            "participio":   {"ing": "She has disappointed everyone.","esp": "Ella ha decepcionado a todos."},
            "gerundio":     {"ing": "They are disappointing the fans.","esp": "Ellos están decepcionando a los fans."},
            "futuro":       {"ing": "We will disappoint the critics.","esp": "Nosotros decepcionaremos a los críticos."},
            "condicional":  {"ing": "That ending would disappoint viewers.","esp": "Ese final decepcionaría a los espectadores."}
        }
    },
    {
        "ing_inf": "discover", "esp_inf": "descubrir",
        "pasado_ing": "discovered", "pasado_esp": "descubrió",
        "participio_ing": "discovered", "participio_esp": "descubierto",
        "gerundio_ing": "discovering", "gerundio_esp": "descubriendo",
        "oraciones": {
            "infinitivo":   {"ing": "I discover new music every week.","esp": "Yo descubro música nueva cada semana."},
            "pasadoSimple": {"ing": "You discovered a great restaurant.","esp": "Tú descubriste un gran restaurante."},
            "participio":   {"ing": "She has discovered the truth at last.","esp": "Ella ha descubierto la verdad por fin."},
            "gerundio":     {"ing": "They are discovering new species.","esp": "Ellos están descubriendo especies nuevas."},
            "futuro":       {"ing": "We will discover the solution soon.","esp": "Nosotros descubriremos la solución pronto."},
            "condicional":  {"ing": "That research would discover more clues.","esp": "Esa investigación descubriría más pistas."}
        }
    },
    {
        "ing_inf": "discuss", "esp_inf": "discutir",
        "pasado_ing": "discussed", "pasado_esp": "discutió",
        "participio_ing": "discussed", "participio_esp": "discutido",
        "gerundio_ing": "discussing", "gerundio_esp": "discutiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I discuss ideas openly at work.","esp": "Yo discuto ideas abiertamente en el trabajo."},
            "pasadoSimple": {"ing": "You discussed the topic calmly.","esp": "Tú discutiste el tema con calma."},
            "participio":   {"ing": "She has discussed the contract terms.","esp": "Ella ha discutido los términos del contrato."},
            "gerundio":     {"ing": "They are discussing the budget now.","esp": "Ellos están discutiendo el presupuesto ahora."},
            "futuro":       {"ing": "We will discuss it tomorrow morning.","esp": "Nosotros lo discutiremos mañana por la mañana."},
            "condicional":  {"ing": "That proposal would discuss alternatives.","esp": "Esa propuesta discutiría alternativas."}
        }
    },
    {
        "ing_inf": "dislike", "esp_inf": "detestar",
        "pasado_ing": "disliked", "pasado_esp": "detestó",
        "participio_ing": "disliked", "participio_esp": "detestado",
        "gerundio_ing": "disliking", "gerundio_esp": "detestando",
        "oraciones": {
            "infinitivo":   {"ing": "I dislike spicy food a lot.",      "esp": "Yo detesto mucho la comida picante."},
            "pasadoSimple": {"ing": "You disliked the new teacher.",    "esp": "Tú detestaste al nuevo profesor."},
            "participio":   {"ing": "She has disliked him since then.","esp": "Ella lo ha detestado desde entonces."},
            "gerundio":     {"ing": "They are disliking the new policy.","esp": "Ellos están detestando la nueva política."},
            "futuro":       {"ing": "We will dislike the construction noise.","esp": "Nosotros detestaremos el ruido de la construcción."},
            "condicional":  {"ing": "That flavor would dislike the kids.","esp": "Ese sabor disgustaría a los niños."}
        }
    },
    {
        "ing_inf": "divide", "esp_inf": "dividir",
        "pasado_ing": "divided", "pasado_esp": "dividió",
        "participio_ing": "divided", "participio_esp": "dividido",
        "gerundio_ing": "dividing", "gerundio_esp": "dividiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I divide the work fairly among us.","esp": "Yo divido el trabajo justamente entre nosotros."},
            "pasadoSimple": {"ing": "You divided the cake into eight pieces.","esp": "Tú dividiste el pastel en ocho trozos."},
            "participio":   {"ing": "She has divided the team into groups.","esp": "Ella ha dividido al equipo en grupos."},
            "gerundio":     {"ing": "They are dividing the profits evenly.","esp": "Ellos están dividiendo las ganancias equitativamente."},
            "futuro":       {"ing": "We will divide the costs in three.","esp": "Nosotros dividiremos los costos en tres."},
            "condicional":  {"ing": "That wall would divide the room in two.","esp": "Esa pared dividiría el cuarto en dos."}
        }
    },
    {
        "ing_inf": "doubt", "esp_inf": "dudar",
        "pasado_ing": "doubted", "pasado_esp": "dudó",
        "participio_ing": "doubted", "participio_esp": "dudado",
        "gerundio_ing": "doubting", "gerundio_esp": "dudando",
        "oraciones": {
            "infinitivo":   {"ing": "I doubt his true intentions.",   "esp": "Yo dudo de sus verdaderas intenciones."},
            "pasadoSimple": {"ing": "You doubted my word again.",     "esp": "Tú dudaste de mi palabra otra vez."},
            "participio":   {"ing": "She has doubted the news since morning.","esp": "Ella ha dudado de la noticia desde la mañana."},
            "gerundio":     {"ing": "They are doubting the evidence presented.","esp": "Ellos están dudando de la evidencia presentada."},
            "futuro":       {"ing": "We will doubt the result until we see proof.","esp": "Nosotros dudaremos del resultado hasta ver pruebas."},
            "condicional":  {"ing": "That statement would doubt the credibility.","esp": "Esa declaración dudaría de la credibilidad."}
        }
    },
    {
        "ing_inf": "drag", "esp_inf": "arrastrar",
        "pasado_ing": "dragged", "pasado_esp": "arrastró",
        "participio_ing": "dragged", "participio_esp": "arrastrado",
        "gerundio_ing": "dragging", "gerundio_esp": "arrastrando",
        "oraciones": {
            "infinitivo":   {"ing": "I drag heavy boxes at work every day.","esp": "Yo arrastro cajas pesadas en el trabajo cada día."},
            "pasadoSimple": {"ing": "You dragged the suitcase across the room.","esp": "Tú arrastraste la maleta al otro lado del cuarto."},
            "participio":   {"ing": "She has dragged the file into the folder.","esp": "Ella ha arrastrado el archivo a la carpeta."},
            "gerundio":     {"ing": "They are dragging the heavy log.","esp": "Ellos están arrastrando el tronco pesado."},
            "futuro":       {"ing": "We will drag the boat to shore.","esp": "Nosotros arrastraremos el bote a la orilla."},
            "condicional":  {"ing": "That anchor would drag in the storm.","esp": "Esa ancla se arrastraría con la tormenta."}
        }
    },
    {
        "ing_inf": "drain", "esp_inf": "drenar",
        "pasado_ing": "drained", "pasado_esp": "drenó",
        "participio_ing": "drained", "participio_esp": "drenado",
        "gerundio_ing": "draining", "gerundio_esp": "drenando",
        "oraciones": {
            "infinitivo":   {"ing": "I drain the pasta before serving it.","esp": "Yo escurro la pasta antes de servirla."},
            "pasadoSimple": {"ing": "You drained the pool yesterday.","esp": "Tú drenaste la piscina ayer."},
            "participio":   {"ing": "She has drained the battery completely.","esp": "Ella ha agotado la batería por completo."},
            "gerundio":     {"ing": "They are draining the swamp area.","esp": "Ellos están drenando el área del pantano."},
            "futuro":       {"ing": "We will drain the tank tomorrow.","esp": "Nosotros drenaremos el tanque mañana."},
            "condicional":  {"ing": "That pipe would drain the water quickly.","esp": "Esa tubería drenaría el agua rápidamente."}
        }
    }
]


BLOQUE_11 = [
    {
        "ing_inf": "dream", "esp_inf": "soñar",
        "pasado_ing": "dreamed", "pasado_esp": "soñó",
        "participio_ing": "dreamed", "participio_esp": "soñado",
        "gerundio_ing": "dreaming", "gerundio_esp": "soñando",
        "oraciones": {
            "infinitivo":   {"ing": "I dream of traveling the world.", "esp": "Yo sueño con viajar por el mundo."},
            "pasadoSimple": {"ing": "You dreamed of being an astronaut.","esp": "Tú soñaste con ser astronauta."},
            "participio":   {"ing": "She has dreamed about this day.","esp": "Ella ha soñado con este día."},
            "gerundio":     {"ing": "They are dreaming of success.","esp": "Ellos están soñando con el éxito."},
            "futuro":       {"ing": "We will dream big tonight.","esp": "Nosotros soñaremos en grande esta noche."},
            "condicional":  {"ing": "That film would dream of sequels.","esp": "Esa película soñaría con secuelas."}
        }
    },
    {
        "ing_inf": "dress", "esp_inf": "vestir",
        "pasado_ing": "dressed", "pasado_esp": "vistió",
        "participio_ing": "dressed", "participio_esp": "vestido",
        "gerundio_ing": "dressing", "gerundio_esp": "vistiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I dress casually for work.",   "esp": "Yo me visto casual para el trabajo."},
            "pasadoSimple": {"ing": "You dressed up for the party.","esp": "Tú te vestiste elegante para la fiesta."},
            "participio":   {"ing": "She has dressed the baby.",     "esp": "Ella ha vestido al bebé."},
            "gerundio":     {"ing": "They are dressing the mannequins.","esp": "Ellos están vistiendo los maniquíes."},
            "futuro":       {"ing": "We will dress warmly tomorrow.","esp": "Nosotros nos vestiremos con abrigo mañana."},
            "condicional":  {"ing": "That boutique would dress any star.","esp": "Esa boutique vestiría a cualquier estrella."}
        }
    },
    {
        "ing_inf": "drip", "esp_inf": "gotear",
        "pasado_ing": "dripped", "pasado_esp": "goteó",
        "participio_ing": "dripped", "participio_esp": "goteado",
        "gerundio_ing": "dripping", "gerundio_esp": "goteando",
        "oraciones": {
            "infinitivo":   {"ing": "I drip sweat when I exercise.","esp": "Yo goteo sudor cuando hago ejercicio."},
            "pasadoSimple": {"ing": "You dripped water on the floor.","esp": "Tú goteaste agua en el piso."},
            "participio":   {"ing": "The faucet has dripped all night.","esp": "El grifo ha goteado toda la noche."},
            "gerundio":     {"ing": "They are dripping oil from the engine.","esp": "Ellos están goteando aceite del motor."},
            "futuro":       {"ing": "We will drip the sauce slowly.","esp": "Nosotros gotaremos la salsa lentamente."},
            "condicional":  {"ing": "That pipe would drip constantly.","esp": "Esa tubería gotearía constantemente."}
        }
    },
    {
        "ing_inf": "drop", "esp_inf": "soltar",
        "pasado_ing": "dropped", "pasado_esp": "soltó",
        "participio_ing": "dropped", "participio_esp": "soltado",
        "gerundio_ing": "dropping", "gerundio_esp": "soltando",
        "oraciones": {
            "infinitivo":   {"ing": "I drop everything when I'm exhausted.","esp": "Yo suelto todo cuando estoy agotado."},
            "pasadoSimple": {"ing": "You dropped your wallet.","esp": "Tú soltaste tu billetera."},
            "participio":   {"ing": "She has dropped the class.","esp": "Ella ha soltado la clase."},
            "gerundio":     {"ing": "They are dropping prices this week.","esp": "Ellos están bajando precios esta semana."},
            "futuro":       {"ing": "We will drop the plan.","esp": "Nosotros soltaremos el plan."},
            "condicional":  {"ing": "That move would drop the temperature.","esp": "Ese movimiento bajaría la temperatura."}
        }
    },
    {
        "ing_inf": "drown", "esp_inf": "ahogar",
        "pasado_ing": "drowned", "pasado_esp": "ahogó",
        "participio_ing": "drowned", "participio_esp": "ahogado",
        "gerundio_ing": "drowning", "gerundio_esp": "ahogando",
        "oraciones": {
            "infinitivo":   {"ing": "I drown my sorrows in music.","esp": "Yo ahogo mis penas en la música."},
            "pasadoSimple": {"ing": "You drowned the noise with laughter.","esp": "Tú ahogaste el ruido con risas."},
            "participio":   {"ing": "She has drowned in work lately.","esp": "Ella se ha ahogado en el trabajo últimamente."},
            "gerundio":     {"ing": "They are drowning the fire with water.","esp": "Ellos están ahogando el fuego con agua."},
            "futuro":       {"ing": "We will drown the pasta in sauce.","esp": "Nosotros ahogaremos la pasta en salsa."},
            "condicional":  {"ing": "That current would drown anyone.","esp": "Esa corriente ahogaría a cualquiera."}
        }
    },
    {
        "ing_inf": "dry", "esp_inf": "secar",
        "pasado_ing": "dried", "pasado_esp": "secó",
        "participio_ing": "dried", "participio_esp": "secado",
        "gerundio_ing": "drying", "gerundio_esp": "secando",
        "oraciones": {
            "infinitivo":   {"ing": "I dry my hands with a towel.","esp": "Yo me seco las manos con una toalla."},
            "pasadoSimple": {"ing": "You dried the dishes quickly.","esp": "Tú secaste los platos rápidamente."},
            "participio":   {"ing": "She has dried her hair already.","esp": "Ella ya ha secado su pelo."},
            "gerundio":     {"ing": "They are drying the clothes outside.","esp": "Ellos están secando la ropa afuera."},
            "futuro":       {"ing": "We will dry the herbs for tea.","esp": "Nosotros secaremos las hierbas para el té."},
            "condicional":  {"ing": "That machine would dry everything fast.","esp": "Esa máquina secaría todo rápido."}
        }
    },
    {
        "ing_inf": "dust", "esp_inf": "sacudir",
        "pasado_ing": "dusted", "pasado_esp": "sacudió",
        "participio_ing": "dusted", "participio_esp": "sacudido",
        "gerundio_ing": "dusting", "gerundio_esp": "sacudiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I dust the shelves every week.","esp": "Yo sacudo el polvo de los estantes cada semana."},
            "pasadoSimple": {"ing": "You dusted the furniture this morning.","esp": "Tú sacudiste el polvo de los muebles esta mañana."},
            "participio":   {"ing": "She has dusted the books off.","esp": "Ella ha sacudido el polvo de los libros."},
            "gerundio":     {"ing": "They are dusting the old photos.","esp": "Ellos están sacudiendo el polvo de las fotos viejas."},
            "futuro":       {"ing": "We will dust the entire house.","esp": "Nosotros sacudiremos toda la casa."},
            "condicional":  {"ing": "That cloth would dust perfectly.","esp": "Ese paño sacudiría el polvo perfectamente."}
        }
    },
    {
        "ing_inf": "earn", "esp_inf": "ganar",
        "pasado_ing": "earned", "pasado_esp": "ganó",
        "participio_ing": "earned", "participio_esp": "ganado",
        "gerundio_ing": "earning", "gerundio_esp": "ganando",
        "oraciones": {
            "infinitivo":   {"ing": "I earn a good salary.",        "esp": "Yo gano un buen salario."},
            "pasadoSimple": {"ing": "You earned extra money last month.","esp": "Tú ganaste dinero extra el mes pasado."},
            "participio":   {"ing": "She has earned his trust.","esp": "Ella se ha ganado su confianza."},
            "gerundio":     {"ing": "They are earning bonuses this year.","esp": "Ellos están ganando bonos este año."},
            "futuro":       {"ing": "We will earn more next year.","esp": "Nosotros ganaremos más el próximo año."},
            "condicional":  {"ing": "That job would earn respect.","esp": "Ese trabajo ganaría respeto."}
        }
    },
    {
        "ing_inf": "educate", "esp_inf": "educar",
        "pasado_ing": "educated", "pasado_esp": "educó",
        "participio_ing": "educated", "participio_esp": "educado",
        "gerundio_ing": "educating", "gerundio_esp": "educando",
        "oraciones": {
            "infinitivo":   {"ing": "I educate my kids at home.",   "esp": "Yo educo a mis hijos en casa."},
            "pasadoSimple": {"ing": "You educated yourself online.","esp": "Tú te educaste en línea."},
            "participio":   {"ing": "She has educated thousands of students.","esp": "Ella ha educado a miles de estudiantes."},
            "gerundio":     {"ing": "They are educating the public about health.","esp": "Ellos están educando al público sobre la salud."},
            "futuro":       {"ing": "We will educate future generations.","esp": "Nosotros educaremos a las futuras generaciones."},
            "condicional":  {"ing": "That program would educate many.","esp": "Ese programa educaría a muchos."}
        }
    },
    {
        "ing_inf": "embarrass", "esp_inf": "avergonzar",
        "pasado_ing": "embarrassed", "pasado_esp": "avergonzó",
        "participio_ing": "embarrassed", "participio_esp": "avergonzado",
        "gerundio_ing": "embarrassing", "gerundio_esp": "avergonzando",
        "oraciones": {
            "infinitivo":   {"ing": "I embarrass myself in public sometimes.","esp": "Yo me avergüenzo en público a veces."},
            "pasadoSimple": {"ing": "You embarrassed me in front of everyone.","esp": "Tú me avergonzaste frente a todos."},
            "participio":   {"ing": "She has embarrassed her family.","esp": "Ella ha avergonzado a su familia."},
            "gerundio":     {"ing": "They are embarrassing themselves online.","esp": "Ellos se están avergonzando en línea."},
            "futuro":       {"ing": "We will embarrass the opponents.","esp": "Nosotros avergonzaremos a los oponentes."},
            "condicional":  {"ing": "That outfit would embarrass anyone.","esp": "Ese outfit avergonzaría a cualquiera."}
        }
    },
    {
        "ing_inf": "employ", "esp_inf": "emplear",
        "pasado_ing": "employed", "pasado_esp": "empleó",
        "participio_ing": "employed", "participio_esp": "empleado",
        "gerundio_ing": "employing", "gerundio_esp": "empleando",
        "oraciones": {
            "infinitivo":   {"ing": "I employ twenty people at my company.","esp": "Yo empleo a veinte personas en mi empresa."},
            "pasadoSimple": {"ing": "You employed new strategies last year.","esp": "Tú empleaste nuevas estrategias el año pasado."},
            "participio":   {"ing": "She has employed several consultants.","esp": "Ella ha empleado varios consultores."},
            "gerundio":     {"ing": "They are employing part-time workers.","esp": "Ellos están empleando trabajadores de medio tiempo."},
            "futuro":       {"ing": "We will employ more staff soon.","esp": "Nosotros emplearemos más personal pronto."},
            "condicional":  {"ing": "That factory would employ hundreds.","esp": "Esa fábrica emplearía a cientos."}
        }
    },
    {
        "ing_inf": "empty", "esp_inf": "vaciar",
        "pasado_ing": "emptied", "pasado_esp": "vació",
        "participio_ing": "emptied", "participio_esp": "vaciado",
        "gerundio_ing": "emptying", "gerundio_esp": "vaciando",
        "oraciones": {
            "infinitivo":   {"ing": "I empty the trash every night.","esp": "Yo vacío la basura cada noche."},
            "pasadoSimple": {"ing": "You emptied the bucket quickly.","esp": "Tú vaciaste el balde rápidamente."},
            "participio":   {"ing": "She has emptied the closet already.","esp": "Ella ya ha vaciado el armario."},
            "gerundio":     {"ing": "They are emptying the pool.","esp": "Ellos están vaciando la piscina."},
            "futuro":       {"ing": "We will empty the warehouse.","esp": "Nosotros vaciaremos el almacén."},
            "condicional":  {"ing": "That container would empty easily.","esp": "Ese contenedor se vaciaría fácilmente."}
        }
    },
    {
        "ing_inf": "encourage", "esp_inf": "alentar",
        "pasado_ing": "encouraged", "pasado_esp": "alentó",
        "participio_ing": "encouraged", "participio_esp": "alentado",
        "gerundio_ing": "encouraging", "gerundio_esp": "alentando",
        "oraciones": {
            "infinitivo":   {"ing": "I encourage my team to try new things.","esp": "Yo aliento a mi equipo a probar cosas nuevas."},
            "pasadoSimple": {"ing": "You encouraged him to keep going.","esp": "Tú lo alentaste a seguir."},
            "participio":   {"ing": "She has encouraged open discussion.","esp": "Ella ha alentado la discusión abierta."},
            "gerundio":     {"ing": "They are encouraging healthy habits.","esp": "Ellos están alentando hábitos saludables."},
            "futuro":       {"ing": "We will encourage participation.","esp": "Nosotros alentaremos la participación."},
            "condicional":  {"ing": "That speech would encourage anyone.","esp": "Ese discurso alentaría a cualquiera."}
        }
    },
    {
        "ing_inf": "end", "esp_inf": "terminar",
        "pasado_ing": "ended", "pasado_esp": "terminó",
        "participio_ing": "ended", "participio_esp": "terminado",
        "gerundio_ing": "ending", "gerundio_esp": "terminando",
        "oraciones": {
            "infinitivo":   {"ing": "I end my day with tea.",       "esp": "Yo termino mi día con un té."},
            "pasadoSimple": {"ing": "You ended the meeting on time.","esp": "Tú terminaste la reunión a tiempo."},
            "participio":   {"ing": "She has ended the relationship.","esp": "Ella ha terminado la relación."},
            "gerundio":     {"ing": "They are ending the season soon.","esp": "Ellos están terminando la temporada pronto."},
            "futuro":       {"ing": "We will end the project by June.","esp": "Nosotros terminaremos el proyecto en junio."},
            "condicional":  {"ing": "That war would end eventually.","esp": "Esa guerra terminaría eventualmente."}
        }
    },
    {
        "ing_inf": "enjoy", "esp_inf": "disfrutar",
        "pasado_ing": "enjoyed", "pasado_esp": "disfrutó",
        "participio_ing": "enjoyed", "participio_esp": "disfrutado",
        "gerundio_ing": "enjoying", "gerundio_esp": "disfrutando",
        "oraciones": {
            "infinitivo":   {"ing": "I enjoy reading before bed.",  "esp": "Yo disfruto leer antes de dormir."},
            "pasadoSimple": {"ing": "You enjoyed the concert a lot.","esp": "Tú disfrutaste mucho el concierto."},
            "participio":   {"ing": "She has enjoyed the trip so far.","esp": "Ella ha disfrutado el viaje hasta ahora."},
            "gerundio":     {"ing": "They are enjoying the sunset.","esp": "Ellos están disfrutando el atardecer."},
            "futuro":       {"ing": "We will enjoy the weekend.","esp": "Nosotros disfrutaremos el fin de semana."},
            "condicional":  {"ing": "That movie would enjoy great success.","esp": "Esa película disfrutaría de gran éxito."}
        }
    },
    {
        "ing_inf": "enter", "esp_inf": "entrar",
        "pasado_ing": "entered", "pasado_esp": "entró",
        "participio_ing": "entered", "participio_esp": "entrado",
        "gerundio_ing": "entering", "gerundio_esp": "entrando",
        "oraciones": {
            "infinitivo":   {"ing": "I enter the building every morning.","esp": "Yo entro al edificio cada mañana."},
            "pasadoSimple": {"ing": "You entered the contest last week.","esp": "Tú entraste al concurso la semana pasada."},
            "participio":   {"ing": "She has entered the room quietly.","esp": "Ella ha entrado al cuarto en silencio."},
            "gerundio":     {"ing": "They are entering the competition now.","esp": "Ellos están entrando a la competencia ahora."},
            "futuro":       {"ing": "We will enter the data later.","esp": "Nosotros entraremos los datos después."},
            "condicional":  {"ing": "That door would enter the garden.","esp": "Esa puerta entraría al jardín."}
        }
    },
    {
        "ing_inf": "entertain", "esp_inf": "entretener",
        "pasado_ing": "entertained", "pasado_esp": "entretuvo",
        "participio_ing": "entertained", "participio_esp": "entretenido",
        "gerundio_ing": "entertaining", "gerundio_esp": "entreteniendo",
        "oraciones": {
            "infinitivo":   {"ing": "I entertain myself with puzzles.","esp": "Yo me entretengo con rompecabezas."},
            "pasadoSimple": {"ing": "You entertained the kids all afternoon.","esp": "Tú entretuviste a los niños toda la tarde."},
            "participio":   {"ing": "She has entertained audiences worldwide.","esp": "Ella ha entretenido al público mundial."},
            "gerundio":     {"ing": "They are entertaining guests tonight.","esp": "Ellos están entreteniendo a invitados esta noche."},
            "futuro":       {"ing": "We will entertain the idea briefly.","esp": "Nosotros entretendremos la idea brevemente."},
            "condicional":  {"ing": "That show would entertain millions.","esp": "Ese show entretendría a millones."}
        }
    },
    {
        "ing_inf": "escape", "esp_inf": "escapar",
        "pasado_ing": "escaped", "pasado_esp": "escapó",
        "participio_ing": "escaped", "participio_esp": "escapado",
        "gerundio_ing": "escaping", "gerundio_esp": "escapando",
        "oraciones": {
            "infinitivo":   {"ing": "I escape the city on weekends.","esp": "Yo escapo de la ciudad los fines de semana."},
            "pasadoSimple": {"ing": "You escaped from danger.","esp": "Tú escapaste del peligro."},
            "participio":   {"ing": "She has escaped three times.","esp": "Ella ha escapado tres veces."},
            "gerundio":     {"ing": "They are escaping through the window.","esp": "Ellos están escapando por la ventana."},
            "futuro":       {"ing": "We will escape the heat tomorrow.","esp": "Nosotros escaparemos del calor mañana."},
            "condicional":  {"ing": "That loophole would escape detection.","esp": "Ese vacío legal escaparía a la detección."}
        }
    },
    {
        "ing_inf": "examine", "esp_inf": "examinar",
        "pasado_ing": "examined", "pasado_esp": "examinó",
        "participio_ing": "examined", "participio_esp": "examinado",
        "gerundio_ing": "examining", "gerundio_esp": "examinando",
        "oraciones": {
            "infinitivo":   {"ing": "I examine the data carefully.","esp": "Yo examino los datos con cuidado."},
            "pasadoSimple": {"ing": "You examined the patient thoroughly.","esp": "Tú examinaste al paciente a fondo."},
            "participio":   {"ing": "She has examined the evidence.","esp": "Ella ha examinado la evidencia."},
            "gerundio":     {"ing": "They are examining the documents now.","esp": "Ellos están examinando los documentos ahora."},
            "futuro":       {"ing": "We will examine the proposal later.","esp": "Nosotros examinaremos la propuesta después."},
            "condicional":  {"ing": "That test would examine all skills.","esp": "Esa prueba examinaría todas las habilidades."}
        }
    },
    {
        "ing_inf": "excite", "esp_inf": "emocionar",
        "pasado_ing": "excited", "pasado_esp": "emocionó",
        "participio_ing": "excited", "participio_esp": "emocionado",
        "gerundio_ing": "exciting", "gerundio_esp": "emocionando",
        "oraciones": {
            "infinitivo":   {"ing": "I excite myself with new projects.","esp": "Yo me emociono con proyectos nuevos."},
            "pasadoSimple": {"ing": "You excited the crowd with your speech.","esp": "Tú emocionaste a la multitud con tu discurso."},
            "participio":   {"ing": "She has excited the fans with news.","esp": "Ella ha emocionado a los fans con la noticia."},
            "gerundio":     {"ing": "They are exciting the children with games.","esp": "Ellos están emocionando a los niños con juegos."},
            "futuro":       {"ing": "We will excite the investors soon.","esp": "Nosotros emocionaremos a los inversores pronto."},
            "condicional":  {"ing": "That announcement would excite everyone.","esp": "Ese anuncio emocionaría a todos."}
        }
    },
    {
        "ing_inf": "excuse", "esp_inf": "disculpar",
        "pasado_ing": "excused", "pasado_esp": "disculpó",
        "participio_ing": "excused", "participio_esp": "disculpado",
        "gerundio_ing": "excusing", "gerundio_esp": "disculpando",
        "oraciones": {
            "infinitivo":   {"ing": "I excuse myself from the meeting.","esp": "Yo me disculpo de la reunión."},
            "pasadoSimple": {"ing": "You excused his bad behavior.","esp": "Tú disculpaste su mal comportamiento."},
            "participio":   {"ing": "She has excused herself already.","esp": "Ella ya se ha disculpado."},
            "gerundio":     {"ing": "They are excusing themselves repeatedly.","esp": "Ellos se están disculpando repetidamente."},
            "futuro":       {"ing": "We will excuse the late arrivals.","esp": "Nosotros disculparemos los retrasos."},
            "condicional":  {"ing": "That reason would excuse anyone.","esp": "Esa razón disculparía a cualquiera."}
        }
    },
    {
        "ing_inf": "exercise", "esp_inf": "ejercitar",
        "pasado_ing": "exercised", "pasado_esp": "ejercitó",
        "participio_ing": "exercised", "participio_esp": "ejercitado",
        "gerundio_ing": "exercising", "gerundio_esp": "ejercitando",
        "oraciones": {
            "infinitivo":   {"ing": "I exercise every morning at the gym.","esp": "Yo me ejercito cada mañana en el gimnasio."},
            "pasadoSimple": {"ing": "You exercised too much yesterday.","esp": "Tú te ejercitaste demasiado ayer."},
            "participio":   {"ing": "She has exercised her right to vote.","esp": "Ella ha ejercitado su derecho al voto."},
            "gerundio":     {"ing": "They are exercising in the park.","esp": "Ellos se están ejercitando en el parque."},
            "futuro":       {"ing": "We will exercise daily from now on.","esp": "Nosotros nos ejercitaremos a diario de ahora en adelante."},
            "condicional":  {"ing": "That routine would exercise every muscle.","esp": "Esa rutina ejercitaría cada músculo."}
        }
    },
    {
        "ing_inf": "exist", "esp_inf": "existir",
        "pasado_ing": "existed", "pasado_esp": "existió",
        "participio_ing": "existed", "participio_esp": "existido",
        "gerundio_ing": "existing", "gerundio_esp": "existiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I exist, therefore I think.","esp": "Yo existo, luego pienso."},
            "pasadoSimple": {"ing": "You existed before the internet.","esp": "Tú existías antes del internet."},
            "participio":   {"ing": "She has existed in legends.","esp": "Ella ha existido en leyendas."},
            "gerundio":     {"ing": "They are existing peacefully.","esp": "Ellos están existiendo en paz."},
            "futuro":       {"ing": "We will exist forever.","esp": "Nosotros existiremos por siempre."},
            "condicional":  {"ing": "That species would exist no more.","esp": "Esa especie ya no existiría."}
        }
    },
    {
        "ing_inf": "expand", "esp_inf": "expandir",
        "pasado_ing": "expanded", "pasado_esp": "expandió",
        "participio_ing": "expanded", "participio_esp": "expandido",
        "gerundio_ing": "expanding", "gerundio_esp": "expandiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I expand my mind with reading.","esp": "Yo expando mi mente con la lectura."},
            "pasadoSimple": {"ing": "You expanded the business last year.","esp": "Tú expandiste el negocio el año pasado."},
            "participio":   {"ing": "She has expanded her network.","esp": "Ella ha expandido su red."},
            "gerundio":     {"ing": "They are expanding to new markets.","esp": "Ellos se están expandiendo a nuevos mercados."},
            "futuro":       {"ing": "We will expand the team soon.","esp": "Nosotros expandiremos el equipo pronto."},
            "condicional":  {"ing": "That gas would expand quickly.","esp": "Ese gas se expandiría rápidamente."}
        }
    },
    {
        "ing_inf": "expect", "esp_inf": "esperar",
        "pasado_ing": "expected", "pasado_esp": "esperó",
        "participio_ing": "expected", "participio_esp": "esperado",
        "gerundio_ing": "expecting", "gerundio_esp": "esperando",
        "oraciones": {
            "infinitivo":   {"ing": "I expect good news soon.",    "esp": "Yo espero buenas noticias pronto."},
            "pasadoSimple": {"ing": "You expected a different result.","esp": "Tú esperaste un resultado diferente."},
            "participio":   {"ing": "She has expected this outcome.","esp": "Ella ha esperado este resultado."},
            "gerundio":     {"ing": "They are expecting a baby.","esp": "Ellos están esperando un bebé."},
            "futuro":       {"ing": "We will expect you tomorrow.","esp": "Nosotros te esperaremos mañana."},
            "condicional":  {"ing": "That policy would expect compliance.","esp": "Esa política esperaría cumplimiento."}
        }
    },
    {
        "ing_inf": "explain", "esp_inf": "explicar",
        "pasado_ing": "explained", "pasado_esp": "explicó",
        "participio_ing": "explained", "participio_esp": "explicado",
        "gerundio_ing": "explaining", "gerundio_esp": "explicando",
        "oraciones": {
            "infinitivo":   {"ing": "I explain things clearly.",   "esp": "Yo explico las cosas con claridad."},
            "pasadoSimple": {"ing": "You explained the rules well.","esp": "Tú explicaste las reglas bien."},
            "participio":   {"ing": "She has explained her decision.","esp": "Ella ha explicado su decisión."},
            "gerundio":     {"ing": "They are explaining the process.","esp": "Ellos están explicando el proceso."},
            "futuro":       {"ing": "We will explain it later.","esp": "Nosotros lo explicaremos después."},
            "condicional":  {"ing": "That chart would explain everything.","esp": "Ese gráfico lo explicaría todo."}
        }
    },
    {
        "ing_inf": "explode", "esp_inf": "explotar",
        "pasado_ing": "exploded", "pasado_esp": "explotó",
        "participio_ing": "exploded", "participio_esp": "explotado",
        "gerundio_ing": "exploding", "gerundio_esp": "explotando",
        "oraciones": {
            "infinitivo":   {"ing": "I explode with anger sometimes.","esp": "Yo exploto de rabia a veces."},
            "pasadoSimple": {"ing": "You exploded the firecracker.","esp": "Tú explotaste el petardo."},
            "participio":   {"ing": "The bomb has exploded already.","esp": "La bomba ya ha explotado."},
            "gerundio":     {"ing": "They are exploding with joy.","esp": "Ellos están explotando de alegría."},
            "futuro":       {"ing": "We will explode the charges soon.","esp": "Nosotros explotaremos las cargas pronto."},
            "condicional":  {"ing": "That gas would explode easily.","esp": "Ese gas explotaría fácilmente."}
        }
    },
    {
        "ing_inf": "explore", "esp_inf": "explorar",
        "pasado_ing": "explored", "pasado_esp": "exploró",
        "participio_ing": "explored", "participio_esp": "explorado",
        "gerundio_ing": "exploring", "gerundio_esp": "explorando",
        "oraciones": {
            "infinitivo":   {"ing": "I explore new places when I travel.","esp": "Yo exploro lugares nuevos cuando viajo."},
            "pasadoSimple": {"ing": "You explored the cave last summer.","esp": "Tú exploraste la cueva el verano pasado."},
            "participio":   {"ing": "She has explored every continent.","esp": "Ella ha explorado todos los continentes."},
            "gerundio":     {"ing": "They are exploring the ocean floor.","esp": "Ellos están explorando el fondo del océano."},
            "futuro":       {"ing": "We will explore new ideas.","esp": "Nosotros exploraremos ideas nuevas."},
            "condicional":  {"ing": "That mission would explore Mars.","esp": "Esa misión exploraría Marte."}
        }
    },
    {
        "ing_inf": "extend", "esp_inf": "extender",
        "pasado_ing": "extended", "pasado_esp": "extendió",
        "participio_ing": "extended", "participio_esp": "extendido",
        "gerundio_ing": "extending", "gerundio_esp": "extendiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I extend my hand in greeting.","esp": "Yo extiendo la mano en saludo."},
            "pasadoSimple": {"ing": "You extended the deadline yesterday.","esp": "Tú extendiste el plazo ayer."},
            "participio":   {"ing": "She has extended the offer.","esp": "Ella ha extendido la oferta."},
            "gerundio":     {"ing": "They are extending the road.","esp": "Ellos están extendiendo la carretera."},
            "futuro":       {"ing": "We will extend the warranty.","esp": "Nosotros extenderemos la garantía."},
            "condicional":  {"ing": "That branch would extend further.","esp": "Esa rama se extendería más."}
        }
    },
    {
        "ing_inf": "face", "esp_inf": "enfrentar",
        "pasado_ing": "faced", "pasado_esp": "enfrentó",
        "participio_ing": "faced", "participio_esp": "enfrentado",
        "gerundio_ing": "facing", "gerundio_esp": "enfrentando",
        "oraciones": {
            "infinitivo":   {"ing": "I face my fears every day.",  "esp": "Yo enfrento mis miedos cada día."},
            "pasadoSimple": {"ing": "You faced the truth bravely.","esp": "Tú enfrentaste la verdad con valentía."},
            "participio":   {"ing": "She has faced many challenges.","esp": "Ella ha enfrentado muchos retos."},
            "gerundio":     {"ing": "They are facing serious problems.","esp": "Ellos están enfrentando problemas serios."},
            "futuro":       {"ing": "We will face the music together.","esp": "Nosotros enfrentaremos las consecuencias juntos."},
            "condicional":  {"ing": "That decision would face criticism.","esp": "Esa decisión enfrentaría críticas."}
        }
    }
]


BLOQUE_12 = [
    {
        "ing_inf": "fail", "esp_inf": "fallar",
        "pasado_ing": "failed", "pasado_esp": "falló",
        "participio_ing": "failed", "participio_esp": "fallado",
        "gerundio_ing": "failing", "gerundio_esp": "fallando",
        "oraciones": {
            "infinitivo":   {"ing": "I fail at things sometimes.","esp": "Yo fallo en cosas a veces."},
            "pasadoSimple": {"ing": "You failed the exam.","esp": "Tú fallaste el examen."},
            "participio":   {"ing": "She has failed three times.","esp": "Ella ha fallado tres veces."},
            "gerundio":     {"ing": "They are failing the test.","esp": "Ellos están fallando la prueba."},
            "futuro":       {"ing": "We will fail if we don't try.","esp": "Nosotros fallaremos si no lo intentamos."},
            "condicional":  {"ing": "That plan would fail eventually.","esp": "Ese plan fallaría eventualmente."}
        }
    },
    {
        "ing_inf": "fancy", "esp_inf": "desear",
        "pasado_ing": "fancied", "pasado_esp": "deseó",
        "participio_ing": "fancied", "participio_esp": "deseado",
        "gerundio_ing": "fancying", "gerundio_esp": "deseando",
        "oraciones": {
            "infinitivo":   {"ing": "I fancy going to the movies.","esp": "Yo deseo ir al cine."},
            "pasadoSimple": {"ing": "You fancied Italian food.","esp": "Tú deseaste comida italiana."},
            "participio":   {"ing": "She has fancied that job.","esp": "Ella ha deseado ese trabajo."},
            "gerundio":     {"ing": "They are fancying a new house.","esp": "Ellos están deseando una casa nueva."},
            "futuro":       {"ing": "We will fancy a break.","esp": "Nosotros desearemos un descanso."},
            "condicional":  {"ing": "That idea would fancy anyone.","esp": "Esa idea se le antojaría a cualquiera."}
        }
    },
    {
        "ing_inf": "fasten", "esp_inf": "abrochar",
        "pasado_ing": "fastened", "pasado_esp": "abrochó",
        "participio_ing": "fastened", "participio_esp": "abrochado",
        "gerundio_ing": "fastening", "gerundio_esp": "abrochando",
        "oraciones": {
            "infinitivo":   {"ing": "I fasten my seatbelt always.","esp": "Yo me abrocho el cinturón siempre."},
            "pasadoSimple": {"ing": "You fastened the buttons.","esp": "Tú abrochaste los botones."},
            "participio":   {"ing": "She has fastened her necklace.","esp": "Ella se ha abrochado el collar."},
            "gerundio":     {"ing": "They are fastening the bags.","esp": "Ellos están abrochando las bolsas."},
            "futuro":       {"ing": "We will fasten the ropes tightly.","esp": "Nosotros abrocharemos las cuerdas firmemente."},
            "condicional":  {"ing": "That clip would fasten securely.","esp": "Ese clip se abrocharía con firmeza."}
        }
    },
    {
        "ing_inf": "fear", "esp_inf": "temer",
        "pasado_ing": "feared", "pasado_esp": "temió",
        "participio_ing": "feared", "participio_esp": "temido",
        "gerundio_ing": "fearing", "gerundio_esp": "temiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I fear for their safety.","esp": "Yo temo por su seguridad."},
            "pasadoSimple": {"ing": "You feared the worst.","esp": "Tú temiste lo peor."},
            "participio":   {"ing": "She has feared him since then.","esp": "Ella lo ha temido desde entonces."},
            "gerundio":     {"ing": "They are fearing the consequences.","esp": "Ellos están temiendo las consecuencias."},
            "futuro":       {"ing": "We will fear no challenge.","esp": "Nosotros no temeremos ningún desafío."},
            "condicional":  {"ing": "That threat would fear anyone.","esp": "Esa amenaza atemorizaría a cualquiera."}
        }
    },
    {
        "ing_inf": "fetch", "esp_inf": "buscar",
        "pasado_ing": "fetched", "pasado_esp": "buscó",
        "participio_ing": "fetched", "participio_esp": "buscado",
        "gerundio_ing": "fetching", "gerundio_esp": "buscando",
        "oraciones": {
            "infinitivo":   {"ing": "I fetch coffee for everyone.","esp": "Yo busco café para todos."},
            "pasadoSimple": {"ing": "You fetched the ball.","esp": "Tú buscaste la pelota."},
            "participio":   {"ing": "She has fetched the doctor.","esp": "Ella ha buscado al médico."},
            "gerundio":     {"ing": "They are fetching water from the well.","esp": "Ellos están buscando agua del pozo."},
            "futuro":       {"ing": "We will fetch the package later.","esp": "Nosotros buscaremos el paquete después."},
            "condicional":  {"ing": "That dog would fetch the stick.","esp": "Ese perro buscaría el palo."}
        }
    },
    {
        "ing_inf": "file", "esp_inf": "archivar",
        "pasado_ing": "filed", "pasado_esp": "archivó",
        "participio_ing": "filed", "participio_esp": "archivado",
        "gerundio_ing": "filing", "gerundio_esp": "archivando",
        "oraciones": {
            "infinitivo":   {"ing": "I file the documents daily.","esp": "Yo archivo los documentos a diario."},
            "pasadoSimple": {"ing": "You filed the taxes last April.","esp": "Tú archivaste los impuestos en abril pasado."},
            "participio":   {"ing": "She has filed a complaint.","esp": "Ella ha archivado una queja."},
            "gerundio":     {"ing": "They are filing the records now.","esp": "Ellos están archivando los registros ahora."},
            "futuro":       {"ing": "We will file the report tomorrow.","esp": "Nosotros archivaremos el informe mañana."},
            "condicional":  {"ing": "That folder would file automatically.","esp": "Esa carpeta archivaría automáticamente."}
        }
    },
    {
        "ing_inf": "fill", "esp_inf": "llenar",
        "pasado_ing": "filled", "pasado_esp": "llenó",
        "participio_ing": "filled", "participio_esp": "llenado",
        "gerundio_ing": "filling", "gerundio_esp": "llenando",
        "oraciones": {
            "infinitivo":   {"ing": "I fill my water bottle every morning.","esp": "Yo lleno mi botella de agua cada mañana."},
            "pasadoSimple": {"ing": "You filled the tank with gas.","esp": "Tú llenaste el tanque con gasolina."},
            "participio":   {"ing": "She has filled the application.","esp": "Ella ha llenado la solicitud."},
            "gerundio":     {"ing": "They are filling the pool with water.","esp": "Ellos están llenando la piscina con agua."},
            "futuro":       {"ing": "We will fill the positions soon.","esp": "Nosotros llenaremos los puestos pronto."},
            "condicional":  {"ing": "That glass would fill quickly.","esp": "Ese vaso se llenaría rápido."}
        }
    },
    {
        "ing_inf": "film", "esp_inf": "filmar",
        "pasado_ing": "filmed", "pasado_esp": "filmó",
        "participio_ing": "filmed", "participio_esp": "filmado",
        "gerundio_ing": "filming", "gerundio_esp": "filmando",
        "oraciones": {
            "infinitivo":   {"ing": "I film videos for YouTube.","esp": "Yo filmo videos para YouTube."},
            "pasadoSimple": {"ing": "You filmed the wedding beautifully.","esp": "Tú filmaste la boda con belleza."},
            "participio":   {"ing": "She has filmed three movies.","esp": "Ella ha filmado tres películas."},
            "gerundio":     {"ing": "They are filming in the studio.","esp": "Ellos están filmando en el estudio."},
            "futuro":       {"ing": "We will film the event tomorrow.","esp": "Nosotros filmaremos el evento mañana."},
            "condicional":  {"ing": "That camera would film in 4K.","esp": "Esa cámara filmaría en 4K."}
        }
    },
    {
        "ing_inf": "fire", "esp_inf": "disparar",
        "pasado_ing": "fired", "pasado_esp": "disparó",
        "participio_ing": "fired", "participio_esp": "disparado",
        "gerundio_ing": "firing", "gerundio_esp": "disparando",
        "oraciones": {
            "infinitivo":   {"ing": "I fire questions at the suspect.","esp": "Yo disparo preguntas al sospechoso."},
            "pasadoSimple": {"ing": "You fired the gun three times.","esp": "Tú disparaste el arma tres veces."},
            "participio":   {"ing": "She has fired the employee.","esp": "Ella ha despedido al empleado."},
            "gerundio":     {"ing": "They are firing the workers.","esp": "Ellos están despidiendo a los trabajadores."},
            "futuro":       {"ing": "We will fire the rocket soon.","esp": "Nosotros dispararemos el cohete pronto."},
            "condicional":  {"ing": "That engine would fire up quickly.","esp": "Ese motor se encendería rápido."}
        }
    },
    {
        "ing_inf": "fit", "esp_inf": "encajar",
        "pasado_ing": "fit", "pasado_esp": "encajó",
        "participio_ing": "fit", "participio_esp": "encajado",
        "gerundio_ing": "fitting", "gerundio_esp": "encajando",
        "oraciones": {
            "infinitivo":   {"ing": "I fit the role perfectly.","esp": "Yo encajo perfectamente en el papel."},
            "pasadoSimple": {"ing": "You fit the puzzle piece.","esp": "Tú encajaste la pieza del rompecabezas."},
            "participio":   {"ing": "She has fit the description.","esp": "Ella ha encajado en la descripción."},
            "gerundio":     {"ing": "They are fitting the pieces.","esp": "Ellos están encajando las piezas."},
            "futuro":       {"ing": "We will fit everything in.","esp": "Nosotros encajaremos todo."},
            "condicional":  {"ing": "That key would fit the lock.","esp": "Esa llave encajaría en la cerradura."}
        }
    },
    {
        "ing_inf": "fix", "esp_inf": "arreglar",
        "pasado_ing": "fixed", "pasado_esp": "arregló",
        "participio_ing": "fixed", "participio_esp": "arreglado",
        "gerundio_ing": "fixing", "gerundio_esp": "arreglando",
        "oraciones": {
            "infinitivo":   {"ing": "I fix broken things at home.","esp": "Yo arreglo cosas rotas en casa."},
            "pasadoSimple": {"ing": "You fixed the computer yesterday.","esp": "Tú arreglaste el ordenador ayer."},
            "participio":   {"ing": "She has fixed the bug already.","esp": "Ella ya ha arreglado el error."},
            "gerundio":     {"ing": "They are fixing the car now.","esp": "Ellos están arreglando el coche ahora."},
            "futuro":       {"ing": "We will fix the issue tomorrow.","esp": "Nosotros arreglaremos el problema mañana."},
            "condicional":  {"ing": "That update would fix the crash.","esp": "Esa actualización arreglaría el fallo."}
        }
    },
    {
        "ing_inf": "flash", "esp_inf": "destellar",
        "pasado_ing": "flashed", "pasado_esp": "destelló",
        "participio_ing": "flashed", "participio_esp": "destellado",
        "gerundio_ing": "flashing", "gerundio_esp": "destellando",
        "oraciones": {
            "infinitivo":   {"ing": "I flash the lights at night.","esp": "Yo destello las luces por la noche."},
            "pasadoSimple": {"ing": "You flashed the screen briefly.","esp": "Tú destellaste la pantalla brevemente."},
            "participio":   {"ing": "She has flashed a warning.","esp": "Ella ha destellado una advertencia."},
            "gerundio":     {"ing": "They are flashing signals.","esp": "Ellos están destellando señales."},
            "futuro":       {"ing": "We will flash our lights.","esp": "Nosotros destellaremos nuestras luces."},
            "condicional":  {"ing": "That beacon would flash brightly.","esp": "Ese faro destellaría con intensidad."}
        }
    },
    {
        "ing_inf": "float", "esp_inf": "flotar",
        "pasado_ing": "floated", "pasado_esp": "flotó",
        "participio_ing": "floated", "participio_esp": "flotado",
        "gerundio_ing": "floating", "gerundio_esp": "flotando",
        "oraciones": {
            "infinitivo":   {"ing": "I float in the pool on weekends.","esp": "Yo floto en la piscina los fines de semana."},
            "pasadoSimple": {"ing": "You floated down the river.","esp": "Tú flotaste río abajo."},
            "participio":   {"ing": "She has floated the idea at work.","esp": "Ella ha presentado la idea en el trabajo."},
            "gerundio":     {"ing": "They are floating in the sea.","esp": "Ellos están flotando en el mar."},
            "futuro":       {"ing": "We will float the proposal.","esp": "Nosotros presentaremos la propuesta."},
            "condicional":  {"ing": "That balloon would float away.","esp": "Ese globo se alejaría flotando."}
        }
    },
    {
        "ing_inf": "flood", "esp_inf": "inundar",
        "pasado_ing": "flooded", "pasado_esp": "inundó",
        "participio_ing": "flooded", "participio_esp": "inundado",
        "gerundio_ing": "flooding", "gerundio_esp": "inundando",
        "oraciones": {
            "infinitivo":   {"ing": "I flood the market with new products.","esp": "Yo inundo el mercado con productos nuevos."},
            "pasadoSimple": {"ing": "You flooded the basement last night.","esp": "Tú inundaste el sótano anoche."},
            "participio":   {"ing": "The river has flooded the village.","esp": "El río ha inundado la aldea."},
            "gerundio":     {"ing": "They are flooding the area with aid.","esp": "Ellos están inundando la zona con ayuda."},
            "futuro":       {"ing": "We will flood the zone with notifications.","esp": "Nosotros inundaremos la zona con notificaciones."},
            "condicional":  {"ing": "That storm would flood the city.","esp": "Esa tormenta inundaría la ciudad."}
        }
    },
    {
        "ing_inf": "flow", "esp_inf": "fluir",
        "pasado_ing": "flowed", "pasado_esp": "fluyó",
        "participio_ing": "flowed", "participio_esp": "fluido",
        "gerundio_ing": "flowing", "gerundio_esp": "fluyendo",
        "oraciones": {
            "infinitivo":   {"ing": "I flow with the rhythm of life.","esp": "Yo fluyo con el ritmo de la vida."},
            "pasadoSimple": {"ing": "You flowed with creativity yesterday.","esp": "Tú fluiste con creatividad ayer."},
            "participio":   {"ing": "The river has flowed strongly.","esp": "El río ha fluido con fuerza."},
            "gerundio":     {"ing": "They are flowing into the new market.","esp": "Ellos están fluyendo al nuevo mercado."},
            "futuro":       {"ing": "We will flow naturally.","esp": "Nosotros fluiremos naturalmente."},
            "condicional":  {"ing": "That traffic would flow better.","esp": "Ese tráfico fluiría mejor."}
        }
    },
    {
        "ing_inf": "fold", "esp_inf": "doblar",
        "pasado_ing": "folded", "pasado_esp": "dobló",
        "participio_ing": "folded", "participio_esp": "doblado",
        "gerundio_ing": "folding", "gerundio_esp": "doblando",
        "oraciones": {
            "infinitivo":   {"ing": "I fold laundry on Sundays.","esp": "Yo doblo la ropa los domingos."},
            "pasadoSimple": {"ing": "You folded the letter carefully.","esp": "Tú doblaste la carta con cuidado."},
            "participio":   {"ing": "She has folded the napkins nicely.","esp": "Ella ha doblado las servilletas con gracia."},
            "gerundio":     {"ing": "They are folding the tents.","esp": "Ellos están doblando las tiendas."},
            "futuro":       {"ing": "We will fold the paper in half.","esp": "Nosotros doblaremos el papel por la mitad."},
            "condicional":  {"ing": "That chair would fold easily.","esp": "Esa silla se doblaría fácilmente."}
        }
    },
    {
        "ing_inf": "follow", "esp_inf": "seguir",
        "pasado_ing": "followed", "pasado_esp": "siguió",
        "participio_ing": "followed", "participio_esp": "seguido",
        "gerundio_ing": "following", "gerundio_esp": "siguiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I follow the news daily.","esp": "Yo sigo las noticias a diario."},
            "pasadoSimple": {"ing": "You followed the recipe exactly.","esp": "Tú seguiste la receta al pie de la letra."},
            "participio":   {"ing": "She has followed her dreams.","esp": "Ella ha seguido sus sueños."},
            "gerundio":     {"ing": "They are following the leader.","esp": "Ellos están siguiendo al líder."},
            "futuro":       {"ing": "We will follow your advice.","esp": "Nosotros seguiremos tu consejo."},
            "condicional":  {"ing": "That trend would follow the others.","esp": "Esa tendencia seguiría a las otras."}
        }
    },
    {
        "ing_inf": "fool", "esp_inf": "engañar",
        "pasado_ing": "fooled", "pasado_esp": "engañó",
        "participio_ing": "fooled", "participio_esp": "engañado",
        "gerundio_ing": "fooling", "gerundio_esp": "engañando",
        "oraciones": {
            "infinitivo":   {"ing": "I fool myself sometimes.","esp": "Yo me engaño a veces."},
            "pasadoSimple": {"ing": "You fooled me with that trick.","esp": "Tú me engañaste con ese truco."},
            "participio":   {"ing": "She has fooled everyone.","esp": "Ella ha engañado a todos."},
            "gerundio":     {"ing": "They are fooling around.","esp": "Ellos están haciendo el tonto."},
            "futuro":       {"ing": "We will fool the enemy.","esp": "Nosotros engañaremos al enemigo."},
            "condicional":  {"ing": "That disguise would fool anyone.","esp": "Ese disfraz engañaría a cualquiera."}
        }
    },
    {
        "ing_inf": "force", "esp_inf": "forzar",
        "pasado_ing": "forced", "pasado_esp": "forzó",
        "participio_ing": "forced", "participio_esp": "forzado",
        "gerundio_ing": "forcing", "gerundio_esp": "forzando",
        "oraciones": {
            "infinitivo":   {"ing": "I force myself to exercise daily.","esp": "Yo me fuerzo a hacer ejercicio a diario."},
            "pasadoSimple": {"ing": "You forced the door open.","esp": "Tú forzaste la puerta para abrirla."},
            "participio":   {"ing": "She has forced the issue.","esp": "Ella ha forzado el asunto."},
            "gerundio":     {"ing": "They are forcing the decision.","esp": "Ellos están forzando la decisión."},
            "futuro":       {"ing": "We will force the change.","esp": "Nosotros forzaremos el cambio."},
            "condicional":  {"ing": "That storm would force evacuations.","esp": "Esa tormenta forzaría evacuaciones."}
        }
    },
    {
        "ing_inf": "frame", "esp_inf": "enmarcar",
        "pasado_ing": "framed", "pasado_esp": "enmarcó",
        "participio_ing": "framed", "participio_esp": "enmarcado",
        "gerundio_ing": "framing", "gerundio_esp": "enmarcando",
        "oraciones": {
            "infinitivo":   {"ing": "I frame photos for my family.","esp": "Yo enmarco fotos para mi familia."},
            "pasadoSimple": {"ing": "You framed the picture beautifully.","esp": "Tú enmarcaste la foto con belleza."},
            "participio":   {"ing": "She has framed the question carefully.","esp": "Ella ha enmarcado la pregunta con cuidado."},
            "gerundio":     {"ing": "They are framing the new law.","esp": "Ellos están enmarcando la nueva ley."},
            "futuro":       {"ing": "We will frame the contract terms.","esp": "Nosotros enmarcaremos los términos del contrato."},
            "condicional":  {"ing": "That rule would frame the discussion.","esp": "Esa regla enmarcaría la discusión."}
        }
    },
    {
        "ing_inf": "frighten", "esp_inf": "asustar",
        "pasado_ing": "frightened", "pasado_esp": "asustó",
        "participio_ing": "frightened", "participio_esp": "asustado",
        "gerundio_ing": "frightening", "gerundio_esp": "asustando",
        "oraciones": {
            "infinitivo":   {"ing": "I frighten easily at horror movies.","esp": "Yo me asusto fácilmente con películas de terror."},
            "pasadoSimple": {"ing": "You frightened me with that scream.","esp": "Tú me asustaste con ese grito."},
            "participio":   {"ing": "She has frightened the cat away.","esp": "Ella ha asustado al gato."},
            "gerundio":     {"ing": "They are frightening the children.","esp": "Ellos están asustando a los niños."},
            "futuro":       {"ing": "We will frighten the thieves away.","esp": "Nosotros asustaremos a los ladrones."},
            "condicional":  {"ing": "That noise would frighten anyone.","esp": "Ese ruido asustaría a cualquiera."}
        }
    },
    {
        "ing_inf": "fry", "esp_inf": "freír",
        "pasado_ing": "fried", "pasado_esp": "frió",
        "participio_ing": "fried", "participio_esp": "frito",
        "gerundio_ing": "frying", "gerundio_esp": "friendo",
        "oraciones": {
            "infinitivo":   {"ing": "I fry eggs every morning.","esp": "Yo frío huevos cada mañana."},
            "pasadoSimple": {"ing": "You fried the fish perfectly.","esp": "Tú freíste el pescado perfectamente."},
            "participio":   {"ing": "She has fried the chicken already.","esp": "Ella ya ha frito el pollo."},
            "gerundio":     {"ing": "They are frying onions in the pan.","esp": "Ellos están friendo cebollas en la sartén."},
            "futuro":       {"ing": "We will fry the potatoes later.","esp": "Nosotros freiremos las patatas después."},
            "condicional":  {"ing": "That oil would fry anything.","esp": "Ese aceite freiría cualquier cosa."}
        }
    },
    {
        "ing_inf": "gather", "esp_inf": "reunir",
        "pasado_ing": "gathered", "pasado_esp": "reunió",
        "participio_ing": "gathered", "participio_esp": "reunido",
        "gerundio_ing": "gathering", "gerundio_esp": "reuniendo",
        "oraciones": {
            "infinitivo":   {"ing": "I gather information for my work.","esp": "Yo reúno información para mi trabajo."},
            "pasadoSimple": {"ing": "You gathered the team for a meeting.","esp": "Tú reuniste al equipo para una reunión."},
            "participio":   {"ing": "She has gathered enough evidence.","esp": "Ella ha reunido suficiente evidencia."},
            "gerundio":     {"ing": "They are gathering signatures.","esp": "Ellos están reuniendo firmas."},
            "futuro":       {"ing": "We will gather at noon.","esp": "Nosotros nos reuniremos al mediodía."},
            "condicional":  {"ing": "That storm would gather strength.","esp": "Esa tormenta reuniría fuerza."}
        }
    },
    {
        "ing_inf": "glue", "esp_inf": "pegar",
        "pasado_ing": "glued", "pasado_esp": "pegó",
        "participio_ing": "glued", "participio_esp": "pegado",
        "gerundio_ing": "gluing", "gerundio_esp": "pegando",
        "oraciones": {
            "infinitivo":   {"ing": "I glue broken pieces back together.","esp": "Yo pego piezas rotas de nuevo."},
            "pasadoSimple": {"ing": "You glued the cardboard.","esp": "Tú pegaste el cartón."},
            "participio":   {"ing": "She has glued the label on.","esp": "Ella ha pegado la etiqueta."},
            "gerundio":     {"ing": "They are gluing the tiles.","esp": "Ellos están pegando las baldosas."},
            "futuro":       {"ing": "We will glue the parts carefully.","esp": "Nosotros pegaremos las partes con cuidado."},
            "condicional":  {"ing": "That adhesive would glue anything.","esp": "Ese adhesivo pegaría cualquier cosa."}
        }
    },
    {
        "ing_inf": "grab", "esp_inf": "agarrar",
        "pasado_ing": "grabbed", "pasado_esp": "agarró",
        "participio_ing": "grabbed", "participio_esp": "agarrado",
        "gerundio_ing": "grabbing", "gerundio_esp": "agarrando",
        "oraciones": {
            "infinitivo":   {"ing": "I grab coffee on the way to work.","esp": "Yo agarro café de camino al trabajo."},
            "pasadoSimple": {"ing": "You grabbed the opportunity.","esp": "Tú agarraste la oportunidad."},
            "participio":   {"ing": "She has grabbed the headlines.","esp": "Ella ha agarrado los titulares."},
            "gerundio":     {"ing": "They are grabbing lunch quickly.","esp": "Ellos están agarrando el almuerzo rápido."},
            "futuro":       {"ing": "We will grab a taxi.","esp": "Nosotros agarraremos un taxi."},
            "condicional":  {"ing": "That offer would grab attention.","esp": "Esa oferta agarraría la atención."}
        }
    },
    {
        "ing_inf": "grate", "esp_inf": "rallar",
        "pasado_ing": "grated", "pasado_esp": "ralló",
        "participio_ing": "grated", "participio_esp": "rallado",
        "gerundio_ing": "grating", "gerundio_esp": "rallando",
        "oraciones": {
            "infinitivo":   {"ing": "I grate cheese for the pasta.","esp": "Yo rayo queso para la pasta."},
            "pasadoSimple": {"ing": "You grated the carrots finely.","esp": "Tú rallaste las zanahorias finamente."},
            "participio":   {"ing": "She has grated the lemon peel.","esp": "Ella ha rallado la cáscara de limón."},
            "gerundio":     {"ing": "They are grating the cheese.","esp": "Ellos están rallando el queso."},
            "futuro":       {"ing": "We will grate the coconut.","esp": "Nosotros rallaremos el coco."},
            "condicional":  {"ing": "That tool would grate efficiently.","esp": "Esa herramienta rallaría eficientemente."}
        }
    },
    {
        "ing_inf": "greet", "esp_inf": "saludar",
        "pasado_ing": "greeted", "pasado_esp": "saludó",
        "participio_ing": "greeted", "participio_esp": "saludado",
        "gerundio_ing": "greeting", "gerundio_esp": "saludando",
        "oraciones": {
            "infinitivo":   {"ing": "I greet my neighbors every day.","esp": "Yo saludo a mis vecinos cada día."},
            "pasadoSimple": {"ing": "You greeted the guests warmly.","esp": "Tú saludaste a los invitados con calidez."},
            "participio":   {"ing": "She has greeted the new employee.","esp": "Ella ha saludado al nuevo empleado."},
            "gerundio":     {"ing": "They are greeting the visitors.","esp": "Ellos están saludando a los visitantes."},
            "futuro":       {"ing": "We will greet them at the door.","esp": "Nosotros los saludaremos en la puerta."},
            "condicional":  {"ing": "That smile would greet anyone.","esp": "Esa sonrisa saludaría a cualquiera."}
        }
    },
    {
        "ing_inf": "grin", "esp_inf": "sonreír",
        "pasado_ing": "grinned", "pasado_esp": "sonrió",
        "participio_ing": "grinned", "participio_esp": "sonreído",
        "gerundio_ing": "grinning", "gerundio_esp": "sonriendo",
        "oraciones": {
            "infinitivo":   {"ing": "I grin when I see my dog.","esp": "Yo sonrío cuando veo a mi perro."},
            "pasadoSimple": {"ing": "You grinned at the joke.","esp": "Tú sonreíste con el chiste."},
            "participio":   {"ing": "She has grinned from ear to ear.","esp": "Ella ha sonreído de oreja a oreja."},
            "gerundio":     {"ing": "They are grinning nervously.","esp": "Ellos están sonriendo nerviosamente."},
            "futuro":       {"ing": "We will grin at the camera.","esp": "Nosotros sonreiremos a la cámara."},
            "condicional":  {"ing": "That joke would make anyone grin.","esp": "Ese chiste haría sonreír a cualquiera."}
        }
    },
    {
        "ing_inf": "grip", "esp_inf": "agarrar",
        "pasado_ing": "gripped", "pasado_esp": "agarró",
        "participio_ing": "gripped", "participio_esp": "agarrado",
        "gerundio_ing": "gripping", "gerundio_esp": "agarrando",
        "oraciones": {
            "infinitivo":   {"ing": "I grip the steering wheel tightly.","esp": "Yo agarro el volante con fuerza."},
            "pasadoSimple": {"ing": "You gripped the rope firmly.","esp": "Tú agarraste la cuerda con firmeza."},
            "participio":   {"ing": "She has gripped the bat correctly.","esp": "Ella ha agarrado el bate correctamente."},
            "gerundio":     {"ing": "They are gripping the bar.","esp": "Ellos están agarrando la barra."},
            "futuro":       {"ing": "We will grip the handles.","esp": "Nosotros agarraremos las asas."},
            "condicional":  {"ing": "That handle would grip better.","esp": "Esa asa agarraría mejor."}
        }
    },
    {
        "ing_inf": "guard", "esp_inf": "vigilar",
        "pasado_ing": "guarded", "pasado_esp": "vigiló",
        "participio_ing": "guarded", "participio_esp": "vigilado",
        "gerundio_ing": "guarding", "gerundio_esp": "vigilando",
        "oraciones": {
            "infinitivo":   {"ing": "I guard my secrets carefully.","esp": "Yo guardo mis secretos con cuidado."},
            "pasadoSimple": {"ing": "You guarded the door all night.","esp": "Tú vigilaste la puerta toda la noche."},
            "participio":   {"ing": "She has guarded the treasure.","esp": "Ella ha guardado el tesoro."},
            "gerundio":     {"ing": "They are guarding the perimeter.","esp": "Ellos están vigilando el perímetro."},
            "futuro":       {"ing": "We will guard the entrance.","esp": "Nosotros vigilaremos la entrada."},
            "condicional":  {"ing": "That dog would guard the house.","esp": "Ese perro vigilaría la casa."}
        }
    }
]


BLOQUE_13 = [
    {
        "ing_inf": "guess", "esp_inf": "adivinar",
        "pasado_ing": "guessed", "pasado_esp": "adivinó",
        "participio_ing": "guessed", "participio_esp": "adivinado",
        "gerundio_ing": "guessing", "gerundio_esp": "adivinando",
        "oraciones": {
            "infinitivo":   {"ing": "I guess the answer easily.","esp": "Yo adivino la respuesta fácilmente."},
            "pasadoSimple": {"ing": "You guessed my age correctly.","esp": "Tú adivinaste mi edad correctamente."},
            "participio":   {"ing": "She has guessed the password.","esp": "Ella ha adivinado la contraseña."},
            "gerundio":     {"ing": "They are guessing the price.","esp": "Ellos están adivinando el precio."},
            "futuro":       {"ing": "We will guess the right number.","esp": "Nosotros adivinaremos el número correcto."},
            "condicional":  {"ing": "That clue would help anyone guess.","esp": "Esa pista ayudaría a cualquiera a adivinar."}
        }
    },
    {
        "ing_inf": "guide", "esp_inf": "guiar",
        "pasado_ing": "guided", "pasado_esp": "guló",
        "participio_ing": "guided", "participio_esp": "guiado",
        "gerundio_ing": "guiding", "gerundio_esp": "guiando",
        "oraciones": {
            "infinitivo":   {"ing": "I guide new employees at work.","esp": "Yo guío a los empleados nuevos en el trabajo."},
            "pasadoSimple": {"ing": "You guided me through the process.","esp": "Tú me guiaste por el proceso."},
            "participio":   {"ing": "She has guided the team to success.","esp": "Ella ha guiado al equipo al éxito."},
            "gerundio":     {"ing": "They are guiding the tourists.","esp": "Ellos están guiando a los turistas."},
            "futuro":       {"ing": "We will guide you to the hotel.","esp": "Nosotros te guiaremos al hotel."},
            "condicional":  {"ing": "That mentor would guide anyone well.","esp": "Ese mentor guiaría bien a cualquiera."}
        }
    },
    {
        "ing_inf": "hammer", "esp_inf": "martillar",
        "pasado_ing": "hammered", "pasado_esp": "martilló",
        "participio_ing": "hammered", "participio_esp": "martillado",
        "gerundio_ing": "hammering", "gerundio_esp": "martillando",
        "oraciones": {
            "infinitivo":   {"ing": "I hammer nails into wood often.","esp": "Yo martillo clavos en la madera a menudo."},
            "pasadoSimple": {"ing": "You hammered the metal flat.","esp": "Tú martillaste el metal hasta dejarlo plano."},
            "participio":   {"ing": "She has hammered the stakes in.","esp": "Ella ha martillado las estacas."},
            "gerundio":     {"ing": "They are hammering the roof.","esp": "Ellos están martillando el techo."},
            "futuro":       {"ing": "We will hammer the posts tomorrow.","esp": "Nosotros martillaremos los postes mañana."},
            "condicional":  {"ing": "That machine would hammer all day.","esp": "Esa máquina martillaría todo el día."}
        }
    },
    {
        "ing_inf": "hand", "esp_inf": "entregar",
        "pasado_ing": "handed", "pasado_esp": "entregó",
        "participio_ing": "handed", "participio_esp": "entregado",
        "gerundio_ing": "handing", "gerundio_esp": "entregando",
        "oraciones": {
            "infinitivo":   {"ing": "I hand out flyers downtown.","esp": "Yo entrego folletos en el centro."},
            "pasadoSimple": {"ing": "You handed me the keys.","esp": "Tú me entregaste las llaves."},
            "participio":   {"ing": "She has handed in her resignation.","esp": "Ella ha entregado su renuncia."},
            "gerundio":     {"ing": "They are handing out food.","esp": "Ellos están repartiendo comida."},
            "futuro":       {"ing": "We will hand over the report.","esp": "Nosotros entregaremos el informe."},
            "condicional":  {"ing": "That clerk would hand the forms.","esp": "Ese empleado entregaría los formularios."}
        }
    },
    {
        "ing_inf": "hang", "esp_inf": "colgar",
        "pasado_ing": "hung", "pasado_esp": "colgó",
        "participio_ing": "hung", "participio_esp": "colgado",
        "gerundio_ing": "hanging", "gerundio_esp": "colgando",
        "oraciones": {
            "infinitivo":   {"ing": "I hang my coat on the hook.","esp": "Yo cuelgo mi abrigo en el gancho."},
            "pasadoSimple": {"ing": "You hung the picture yesterday.","esp": "Tú colgaste el cuadro ayer."},
            "participio":   {"ing": "She has hung the laundry out.","esp": "Ella ha colgado la ropa afuera."},
            "gerundio":     {"ing": "They are hanging decorations.","esp": "Ellos están colgando decoraciones."},
            "futuro":       {"ing": "We will hang the banner tomorrow.","esp": "Nosotros colgaremos el banner mañana."},
            "condicional":  {"ing": "That painting would hang nicely.","esp": "Esa pintura colgaría bien."}
        }
    },
    {
        "ing_inf": "happen", "esp_inf": "pasar",
        "pasado_ing": "happened", "pasado_esp": "pasó",
        "participio_ing": "happened", "participio_esp": "pasado",
        "gerundio_ing": "happening", "gerundio_esp": "pasando",
        "oraciones": {
            "infinitivo":   {"ing": "I let things happen naturally.","esp": "Yo dejo que las cosas pasen naturalmente."},
            "pasadoSimple": {"ing": "You happened to arrive at the right moment.","esp": "Tú llegaste en el momento justo."},
            "participio":   {"ing": "She happened to win the lottery.","esp": "Ella ganó la lotería por casualidad."},
            "gerundio":     {"ing": "Strange things are happening lately.","esp": "Cosas extrañas están pasando últimamente."},
            "futuro":       {"ing": "We will happen upon a solution.","esp": "Nosotros daremos con una solución."},
            "condicional":  {"ing": "That would happen in due time.","esp": "Eso pasaría a su debido tiempo."}
        }
    },
    {
        "ing_inf": "harass", "esp_inf": "acosar",
        "pasado_ing": "harassed", "pasado_esp": "acosó",
        "participio_ing": "harassed", "participio_esp": "acosado",
        "gerundio_ing": "harassing", "gerundio_esp": "acosando",
        "oraciones": {
            "infinitivo":   {"ing": "I don't harass anyone online.","esp": "Yo no acoso a nadie en línea."},
            "pasadoSimple": {"ing": "You harassed me with messages.","esp": "Tú me acosaste con mensajes."},
            "participio":   {"ing": "She has harassed her coworkers.","esp": "Ella ha acosado a sus compañeros."},
            "gerundio":     {"ing": "They are harassing the witnesses.","esp": "Ellos están acosando a los testigos."},
            "futuro":       {"ing": "We will harass the competition.","esp": "Nosotros acosaremos a la competencia."},
            "condicional":  {"ing": "That behavior would harass anyone.","esp": "Ese comportamiento acosaría a cualquiera."}
        }
    },
    {
        "ing_inf": "harm", "esp_inf": "dañar",
        "pasado_ing": "harmed", "pasado_esp": "dañó",
        "participio_ing": "harmed", "participio_esp": "dañado",
        "gerundio_ing": "harming", "gerundio_esp": "dañando",
        "oraciones": {
            "infinitivo":   {"ing": "I harm no one in my life.","esp": "Yo no daño a nadie en mi vida."},
            "pasadoSimple": {"ing": "You harmed the reputation.","esp": "Tú dañaste la reputación."},
            "participio":   {"ing": "She has harmed no one.","esp": "Ella no ha dañado a nadie."},
            "gerundio":     {"ing": "They are harming the environment.","esp": "Ellos están dañando el medio ambiente."},
            "futuro":       {"ing": "We will harm the enemy.","esp": "Nosotros dañaremos al enemigo."},
            "condicional":  {"ing": "That chemical would harm the skin.","esp": "Ese químico dañaría la piel."}
        }
    },
    {
        "ing_inf": "hate", "esp_inf": "odiar",
        "pasado_ing": "hated", "pasado_esp": "odió",
        "participio_ing": "hated", "participio_esp": "odiado",
        "gerundio_ing": "hating", "gerundio_esp": "odiando",
        "oraciones": {
            "infinitivo":   {"ing": "I hate waking up early.","esp": "Yo odio madrugar."},
            "pasadoSimple": {"ing": "You hated that movie.","esp": "Tú odiaste esa película."},
            "participio":   {"ing": "She has hated broccoli since childhood.","esp": "Ella ha odiado el brócoli desde la infancia."},
            "gerundio":     {"ing": "They are hating the new rules.","esp": "Ellos están odiando las nuevas reglas."},
            "futuro":       {"ing": "We will hate the traffic.","esp": "Nosotros odiaremos el tráfico."},
            "condicional":  {"ing": "That smell would make anyone hate it.","esp": "Ese olor haría que cualquiera lo odiara."}
        }
    },
    {
        "ing_inf": "haunt", "esp_inf": "atormentar",
        "pasado_ing": "haunted", "pasado_esp": "atormentó",
        "participio_ing": "haunted", "participio_esp": "atormentado",
        "gerundio_ing": "haunting", "gerundio_esp": "atormentando",
        "oraciones": {
            "infinitivo":   {"ing": "I feel haunted by the past.","esp": "Yo me siento atormentado por el pasado."},
            "pasadoSimple": {"ing": "You haunted me with your words.","esp": "Tú me atormentaste con tus palabras."},
            "participio":   {"ing": "That dream has haunted her for years.","esp": "Ese sueño la ha atormentado durante años."},
            "gerundio":     {"ing": "Regrets are haunting them now.","esp": "Los arrepentimientos los están atormentando ahora."},
            "futuro":       {"ing": "We will be haunted by this decision.","esp": "Nosotros seremos atormentados por esta decisión."},
            "condicional":  {"ing": "That memory would haunt anyone.","esp": "Ese recuerdo atormentaría a cualquiera."}
        }
    },
    {
        "ing_inf": "heal", "esp_inf": "curar",
        "pasado_ing": "healed", "pasado_esp": "curó",
        "participio_ing": "healed", "participio_esp": "curado",
        "gerundio_ing": "healing", "gerundio_esp": "curando",
        "oraciones": {
            "infinitivo":   {"ing": "I heal slowly from heartbreak.","esp": "Yo me curo lentamente de las decepciones."},
            "pasadoSimple": {"ing": "You healed the wound completely.","esp": "Tú curaste la herida por completo."},
            "participio":   {"ing": "She has healed from the surgery.","esp": "Ella se ha curado de la cirugía."},
            "gerundio":     {"ing": "They are healing the sick.","esp": "Ellos están curando a los enfermos."},
            "futuro":       {"ing": "We will heal together.","esp": "Nosotros nos curaremos juntos."},
            "condicional":  {"ing": "That balm would heal the pain.","esp": "Ese bálsamo curaría el dolor."}
        }
    },
    {
        "ing_inf": "heat", "esp_inf": "calentar",
        "pasado_ing": "heated", "pasado_esp": "calentó",
        "participio_ing": "heated", "participio_esp": "calentado",
        "gerundio_ing": "heating", "gerundio_esp": "calentando",
        "oraciones": {
            "infinitivo":   {"ing": "I heat milk for coffee.","esp": "Yo caliento leche para el café."},
            "pasadoSimple": {"ing": "You heated the soup quickly.","esp": "Tú calentaste la sopa rápidamente."},
            "participio":   {"ing": "She has heated the oven.","esp": "Ella ha calentado el horno."},
            "gerundio":     {"ing": "They are heating the pool.","esp": "Ellos están calentando la piscina."},
            "futuro":       {"ing": "We will heat the water later.","esp": "Nosotros calentaremos el agua después."},
            "condicional":  {"ing": "That heater would heat the room.","esp": "Ese calentador calentaría el cuarto."}
        }
    },
    {
        "ing_inf": "help", "esp_inf": "ayudar",
        "pasado_ing": "helped", "pasado_esp": "ayudó",
        "participio_ing": "helped", "participio_esp": "ayudado",
        "gerundio_ing": "helping", "gerundio_esp": "ayudando",
        "oraciones": {
            "infinitivo":   {"ing": "I help my neighbors often.","esp": "Yo ayudo a mis vecinos a menudo."},
            "pasadoSimple": {"ing": "You helped me move last week.","esp": "Tú me ayudaste a mudarme la semana pasada."},
            "participio":   {"ing": "She has helped many charities.","esp": "Ella ha ayudado a muchas caridades."},
            "gerundio":     {"ing": "They are helping the victims.","esp": "Ellos están ayudando a las víctimas."},
            "futuro":       {"ing": "We will help with the project.","esp": "Nosotros ayudaremos con el proyecto."},
            "condicional":  {"ing": "That guide would help anyone.","esp": "Esa guía ayudaría a cualquiera."}
        }
    },
    {
        "ing_inf": "hook", "esp_inf": "enganchar",
        "pasado_ing": "hooked", "pasado_esp": "enganchó",
        "participio_ing": "hooked", "participio_esp": "enganchado",
        "gerundio_ing": "hooking", "gerundio_esp": "enganchando",
        "oraciones": {
            "infinitivo":   {"ing": "I hook the trailer to the car.","esp": "Yo engancho el remolque al coche."},
            "pasadoSimple": {"ing": "You hooked the fish quickly.","esp": "Tú enganchaste el pez rápidamente."},
            "participio":   {"ing": "She has hooked the audience.","esp": "Ella ha enganchado al público."},
            "gerundio":     {"ing": "They are hooking up the cables.","esp": "Ellos están enganchando los cables."},
            "futuro":       {"ing": "We will hook the new system.","esp": "Nosotros engancharemos el nuevo sistema."},
            "condicional":  {"ing": "That lure would hook any fish.","esp": "Ese cebo engancharía cualquier pez."}
        }
    },
    {
        "ing_inf": "hop", "esp_inf": "saltar",
        "pasado_ing": "hopped", "pasado_esp": "saltó",
        "participio_ing": "hopped", "participio_esp": "saltado",
        "gerundio_ing": "hopping", "gerundio_esp": "saltando",
        "oraciones": {
            "infinitivo":   {"ing": "I hopped on one foot as a child.","esp": "Yo saltaba en un pie de niño."},
            "pasadoSimple": {"ing": "You hopped over the puddle.","esp": "Tú saltaste el charco."},
            "participio":   {"ing": "She has hopped off the bike.","esp": "Ella se ha bajado de la bici."},
            "gerundio":     {"ing": "They are hopping around.","esp": "Ellos están saltando por todos lados."},
            "futuro":       {"ing": "We will hop on the bus.","esp": "Nosotros nos subiremos al autobús de un salto."},
            "condicional":  {"ing": "That bird would hop easily.","esp": "Ese pájaro saltaría fácilmente."}
        }
    },
    {
        "ing_inf": "hover", "esp_inf": "flotar",
        "pasado_ing": "hovered", "pasado_esp": "flotó",
        "participio_ing": "hovered", "participio_esp": "flotado",
        "gerundio_ing": "hovering", "gerundio_esp": "flotando",
        "oraciones": {
            "infinitivo":   {"ing": "I hover when I get anxious.","esp": "Yo me quedo pendiente cuando estoy ansioso."},
            "pasadoSimple": {"ing": "You hovered near the door.","esp": "Tú te quedaste cerca de la puerta."},
            "participio":   {"ing": "The helicopter has hovered above.","esp": "El helicóptero ha flotado arriba."},
            "gerundio":     {"ing": "They are hovering around the office.","esp": "Ellos están rondando la oficina."},
            "futuro":       {"ing": "We will hover at this altitude.","esp": "Nosotros nos mantendremos a esta altitud."},
            "condicional":  {"ing": "That drone would hover steadily.","esp": "Ese dron se mantendría estable."}
        }
    },
    {
        "ing_inf": "howl", "esp_inf": "aullar",
        "pasado_ing": "howled", "pasado_esp": "aulló",
        "participio_ing": "howled", "participio_esp": "aullado",
        "gerundio_ing": "howling", "gerundio_esp": "aullando",
        "oraciones": {
            "infinitivo":   {"ing": "I howl with laughter at comedies.","esp": "Yo me muero de risa con las comedias."},
            "pasadoSimple": {"ing": "You howled at the moon.","esp": "Tú aullaste a la luna."},
            "participio":   {"ing": "The wolf has howled all night.","esp": "El lobo ha aullado toda la noche."},
            "gerundio":     {"ing": "They are howling with joy.","esp": "Ellos están aullando de alegría."},
            "futuro":       {"ing": "We will howl at the concert.","esp": "Nosotros aullaremos en el concierto."},
            "condicional":  {"ing": "That joke would make anyone howl.","esp": "Ese chiste haría aullar a cualquiera."}
        }
    },
    {
        "ing_inf": "hug", "esp_inf": "abrazar",
        "pasado_ing": "hugged", "pasado_esp": "abrazó",
        "participio_ing": "hugged", "participio_esp": "abrazado",
        "gerundio_ing": "hugging", "gerundio_esp": "abrazando",
        "oraciones": {
            "infinitivo":   {"ing": "I hug my mom when I arrive.","esp": "Yo abrazo a mi mamá cuando llego."},
            "pasadoSimple": {"ing": "You hugged the child tightly.","esp": "Tú abrazaste al niño con fuerza."},
            "participio":   {"ing": "She has hugged every guest.","esp": "Ella ha abrazado a cada invitado."},
            "gerundio":     {"ing": "They are hugging goodbye.","esp": "Ellos se están abrazando de despedida."},
            "futuro":       {"ing": "We will hug you at the airport.","esp": "Nosotros te abrazaremos en el aeropuerto."},
            "condicional":  {"ing": "That moment would make anyone hug.","esp": "Ese momento haría que cualquiera abrazara."}
        }
    },
    {
        "ing_inf": "hum", "esp_inf": "tararear",
        "pasado_ing": "hummed", "pasado_esp": "tarareó",
        "participio_ing": "hummed", "participio_esp": "tarareado",
        "gerundio_ing": "humming", "gerundio_esp": "tarareando",
        "oraciones": {
            "infinitivo":   {"ing": "I hum my favorite song in the shower.","esp": "Yo tarareo mi canción favorita en la ducha."},
            "pasadoSimple": {"ing": "You hummed along to the music.","esp": "Tú tarareaste con la música."},
            "participio":   {"ing": "She has hummed that tune all day.","esp": "Ella ha tarareado esa melodía todo el día."},
            "gerundio":     {"ing": "They are humming softly.","esp": "Ellos están tarareando suavemente."},
            "futuro":       {"ing": "We will hum the national anthem.","esp": "Nosotros tararearemos el himno nacional."},
            "condicional":  {"ing": "That engine would hum quietly.","esp": "Ese motor zumbaría suavemente."}
        }
    },
    {
        "ing_inf": "hunt", "esp_inf": "cazar",
        "pasado_ing": "hunted", "pasado_esp": "cazó",
        "participio_ing": "hunted", "participio_esp": "cazado",
        "gerundio_ing": "hunting", "gerundio_esp": "cazando",
        "oraciones": {
            "infinitivo":   {"ing": "I hunt for bargains at flea markets.","esp": "Yo busco ofertas en los mercadillos."},
            "pasadoSimple": {"ing": "You hunted ducks last season.","esp": "Tú cazaste patos la temporada pasada."},
            "participio":   {"ing": "She has hunted for the perfect gift.","esp": "Ella ha buscado el regalo perfecto."},
            "gerundio":     {"ing": "They are hunting the criminal.","esp": "Ellos están cazando al criminal."},
            "futuro":       {"ing": "We will hunt for treasure.","esp": "Nosotros buscaremos un tesoro."},
            "condicional":  {"ing": "That dog would hunt well.","esp": "Ese perro cazaría bien."}
        }
    },
    {
        "ing_inf": "hurry", "esp_inf": "apresurarse",
        "pasado_ing": "hurried", "pasado_esp": "se apresuró",
        "participio_ing": "hurried", "participio_esp": "apresurado",
        "gerundio_ing": "hurrying", "gerundio_esp": "apresurándose",
        "futuro_esp": "se apresurará", "cond_esp": "se apresuraría",
        "oraciones": {
            "infinitivo":   {"ing": "I hurry to catch the train.","esp": "Yo me apresuro para alcanzar el tren."},
            "pasadoSimple": {"ing": "You hurried home last night.","esp": "Tú te apresuraste a casa anoche."},
            "participio":   {"ing": "She has hurried through lunch.","esp": "Ella se ha apresurado durante el almuerzo."},
            "gerundio":     {"ing": "They are hurrying to finish.","esp": "Ellos se están apresurando para terminar."},
            "futuro":       {"ing": "We will hurry if needed.","esp": "Nosotros nos apresuraremos si es necesario."},
            "condicional":  {"ing": "That decision would hurry the process.","esp": "Esa decisión apresuraría el proceso."}
        }
    },
    {
        "ing_inf": "identify", "esp_inf": "identificar",
        "pasado_ing": "identified", "pasado_esp": "identificó",
        "participio_ing": "identified", "participio_esp": "identificado",
        "gerundio_ing": "identifying", "gerundio_esp": "identificando",
        "oraciones": {
            "infinitivo":   {"ing": "I identify the issues quickly.","esp": "Yo identifico los problemas rápidamente."},
            "pasadoSimple": {"ing": "You identified the thief immediately.","esp": "Tú identificaste al ladrón de inmediato."},
            "participio":   {"ing": "She has identified the cause.","esp": "Ella ha identificado la causa."},
            "gerundio":     {"ing": "They are identifying the bodies.","esp": "Ellos están identificando los cuerpos."},
            "futuro":       {"ing": "We will identify the risks.","esp": "Nosotros identificaremos los riesgos."},
            "condicional":  {"ing": "That test would identify the disease.","esp": "Esa prueba identificaría la enfermedad."}
        }
    },
    {
        "ing_inf": "ignore", "esp_inf": "ignorar",
        "pasado_ing": "ignored", "pasado_esp": "ignoró",
        "participio_ing": "ignored", "participio_esp": "ignorado",
        "gerundio_ing": "ignoring", "gerundio_esp": "ignorando",
        "oraciones": {
            "infinitivo":   {"ing": "I ignore the noise outside.","esp": "Yo ignoro el ruido de afuera."},
            "pasadoSimple": {"ing": "You ignored my advice.","esp": "Tú ignoraste mi consejo."},
            "participio":   {"ing": "She has ignored the warning signs.","esp": "Ella ha ignorado las señales de advertencia."},
            "gerundio":     {"ing": "They are ignoring the rules.","esp": "Ellos están ignorando las reglas."},
            "futuro":       {"ing": "We will ignore the criticism.","esp": "Nosotros ignoraremos la crítica."},
            "condicional":  {"ing": "That policy would ignore the problem.","esp": "Esa política ignoraría el problema."}
        }
    },
    {
        "ing_inf": "imagine", "esp_inf": "imaginar",
        "pasado_ing": "imagined", "pasado_esp": "imaginó",
        "participio_ing": "imagined", "participio_esp": "imaginado",
        "gerundio_ing": "imagining", "gerundio_esp": "imaginando",
        "oraciones": {
            "infinitivo":   {"ing": "I imagine life on Mars.","esp": "Yo imagino la vida en Marte."},
            "pasadoSimple": {"ing": "You imagined the worst scenario.","esp": "Tú imaginaste el peor escenario."},
            "participio":   {"ing": "She has imagined a better world.","esp": "Ella ha imaginado un mundo mejor."},
            "gerundio":     {"ing": "They are imagining the possibilities.","esp": "Ellos están imaginando las posibilidades."},
            "futuro":       {"ing": "We will imagine new solutions.","esp": "Nosotros imaginaremos soluciones nuevas."},
            "condicional":  {"ing": "That music would make anyone imagine.","esp": "Esa música haría imaginar a cualquiera."}
        }
    },
    {
        "ing_inf": "impress", "esp_inf": "impresionar",
        "pasado_ing": "impressed", "pasado_esp": "impresionó",
        "participio_ing": "impressed", "participio_esp": "impresionado",
        "gerundio_ing": "impressing", "gerundio_esp": "impresionando",
        "oraciones": {
            "infinitivo":   {"ing": "I impress my teachers with hard work.","esp": "Yo impresiono a mis profesores con trabajo duro."},
            "pasadoSimple": {"ing": "You impressed the judges at the contest.","esp": "Tú impresionaste a los jueces en el concurso."},
            "participio":   {"ing": "She has impressed everyone with her talent.","esp": "Ella ha impresionado a todos con su talento."},
            "gerundio":     {"ing": "They are impressing the clients today.","esp": "Ellos están impresionando a los clientes hoy."},
            "futuro":       {"ing": "We will impress them at the meeting.","esp": "Nosotros los impresionaremos en la reunión."},
            "condicional":  {"ing": "That performance would impress anyone.","esp": "Esa actuación impresionaría a cualquiera."}
        }
    },
    {
        "ing_inf": "improve", "esp_inf": "mejorar",
        "pasado_ing": "improved", "pasado_esp": "mejoró",
        "participio_ing": "improved", "participio_esp": "mejorado",
        "gerundio_ing": "improving", "gerundio_esp": "mejorando",
        "oraciones": {
            "infinitivo":   {"ing": "I improve my skills daily.","esp": "Yo mejoro mis habilidades a diario."},
            "pasadoSimple": {"ing": "You improved the design significantly.","esp": "Tú mejoraste el diseño significativamente."},
            "participio":   {"ing": "She has improved her English a lot.","esp": "Ella ha mejorado mucho su inglés."},
            "gerundio":     {"ing": "They are improving the process.","esp": "Ellos están mejorando el proceso."},
            "futuro":       {"ing": "We will improve next quarter.","esp": "Nosotros mejoraremos el próximo trimestre."},
            "condicional":  {"ing": "That tool would improve efficiency.","esp": "Esa herramienta mejoraría la eficiencia."}
        }
    },
    {
        "ing_inf": "include", "esp_inf": "incluir",
        "pasado_ing": "included", "pasado_esp": "incluyó",
        "participio_ing": "included", "participio_esp": "incluido",
        "gerundio_ing": "including", "gerundio_esp": "incluyendo",
        "oraciones": {
            "infinitivo":   {"ing": "I include everyone in my plans.","esp": "Yo incluyo a todos en mis planes."},
            "pasadoSimple": {"ing": "You included the tax in the price.","esp": "Tú incluiste el impuesto en el precio."},
            "participio":   {"ing": "She has included references.","esp": "Ella ha incluido referencias."},
            "gerundio":     {"ing": "They are including the dessert.","esp": "Ellos están incluyendo el postre."},
            "futuro":       {"ing": "We will include feedback.","esp": "Nosotros incluiremos retroalimentación."},
            "condicional":  {"ing": "That package would include insurance.","esp": "Ese paquete incluiría seguro."}
        }
    },
    {
        "ing_inf": "increase", "esp_inf": "aumentar",
        "pasado_ing": "increased", "pasado_esp": "aumentó",
        "participio_ing": "increased", "participio_esp": "aumentado",
        "gerundio_ing": "increasing", "gerundio_esp": "aumentando",
        "oraciones": {
            "infinitivo":   {"ing": "I increase my savings every month.","esp": "Yo aumento mis ahorros cada mes."},
            "pasadoSimple": {"ing": "You increased the volume.","esp": "Tú aumentaste el volumen."},
            "participio":   {"ing": "She has increased sales by 20%.","esp": "Ella ha aumentado las ventas un 20%."},
            "gerundio":     {"ing": "They are increasing prices.","esp": "Ellos están aumentando los precios."},
            "futuro":       {"ing": "We will increase production.","esp": "Nosotros aumentaremos la producción."},
            "condicional":  {"ing": "That demand would increase prices.","esp": "Esa demanda aumentaría los precios."}
        }
    },
    {
        "ing_inf": "influence", "esp_inf": "influir",
        "pasado_ing": "influenced", "pasado_esp": "influyó",
        "participio_ing": "influenced", "participio_esp": "influido",
        "gerundio_ing": "influencing", "gerundio_esp": "influyendo",
        "oraciones": {
            "infinitivo":   {"ing": "I influence my friends' decisions.","esp": "Yo influyo en las decisiones de mis amigos."},
            "pasadoSimple": {"ing": "You influenced the outcome.","esp": "Tú influiste en el resultado."},
            "participio":   {"ing": "She has influenced many students.","esp": "Ella ha influido en muchos estudiantes."},
            "gerundio":     {"ing": "They are influencing public opinion.","esp": "Ellos están influyendo en la opinión pública."},
            "futuro":       {"ing": "We will influence the policy.","esp": "Nosotros influiremos en la política."},
            "condicional":  {"ing": "That factor would influence the result.","esp": "Ese factor influiría en el resultado."}
        }
    },
    {
        "ing_inf": "inform", "esp_inf": "informar",
        "pasado_ing": "informed", "pasado_esp": "informó",
        "participio_ing": "informed", "participio_esp": "informado",
        "gerundio_ing": "informing", "gerundio_esp": "informando",
        "oraciones": {
            "infinitivo":   {"ing": "I inform my boss of changes.","esp": "Yo informo a mi jefe de los cambios."},
            "pasadoSimple": {"ing": "You informed the police yesterday.","esp": "Tú informaste a la policía ayer."},
            "participio":   {"ing": "She has informed the parents.","esp": "Ella ha informado a los padres."},
            "gerundio":     {"ing": "They are informing the staff now.","esp": "Ellos están informando al personal ahora."},
            "futuro":       {"ing": "We will inform you tomorrow.","esp": "Nosotros le informaremos mañana."},
            "condicional":  {"ing": "That document would inform everyone.","esp": "Ese documento informaría a todos."}
        }
    }
]


BLOQUE_14 = [
    {
        "ing_inf": "inject", "esp_inf": "inyectar",
        "pasado_ing": "injected", "pasado_esp": "inyectó",
        "participio_ing": "injected", "participio_esp": "inyectado",
        "gerundio_ing": "injecting", "gerundio_esp": "inyectando",
        "oraciones": {
            "infinitivo":   {"ing": "I inject insulin daily.","esp": "Yo me inyecto insulina a diario."},
            "pasadoSimple": {"ing": "You injected humor into the meeting.","esp": "Tú inyectaste humor a la reunión."},
            "participio":   {"ing": "She has injected the serum.","esp": "Ella ha inyectado el suero."},
            "gerundio":     {"ing": "They are injecting funds into the project.","esp": "Ellos están inyectando fondos al proyecto."},
            "futuro":       {"ing": "We will inject new ideas.","esp": "Nosotros inyectaremos ideas nuevas."},
            "condicional":  {"ing": "That shot would inject energy.","esp": "Esa inyección inyectaría energía."}
        }
    },
    {
        "ing_inf": "injure", "esp_inf": "herir",
        "pasado_ing": "injured", "pasado_esp": "hirió",
        "participio_ing": "injured", "participio_esp": "herido",
        "gerundio_ing": "injuring", "gerundio_esp": "hiriendo",
        "oraciones": {
            "infinitivo":   {"ing": "I injure myself playing sports.","esp": "Yo me hiero jugando deportes."},
            "pasadoSimple": {"ing": "You injured your ankle yesterday.","esp": "Tú te heriste el tobillo ayer."},
            "participio":   {"ing": "She has injured her back.","esp": "Ella se ha herido la espalda."},
            "gerundio":     {"ing": "They are injuring their reputation.","esp": "Ellos están hiriendo su reputación."},
            "futuro":       {"ing": "We will injure the opponent.","esp": "Nosotros heriremos al oponente."},
            "condicional":  {"ing": "That fall would injure anyone.","esp": "Esa caída heriría a cualquiera."}
        }
    },
    {
        "ing_inf": "inquire", "esp_inf": "indagar",
        "pasado_ing": "inquired", "pasado_esp": "indagó",
        "participio_ing": "inquired", "participio_esp": "indagado",
        "gerundio_ing": "inquiring", "gerundio_esp": "indagando",
        "oraciones": {
            "infinitivo":   {"ing": "I inquire about prices before buying.","esp": "Yo indago sobre precios antes de comprar."},
            "pasadoSimple": {"ing": "You inquired about the job opening.","esp": "Tú indagaste sobre la vacante."},
            "participio":   {"ing": "She has inquired into the matter.","esp": "Ella ha indagado sobre el asunto."},
            "gerundio":     {"ing": "They are inquiring about delivery times.","esp": "Ellos están indagando sobre los tiempos de entrega."},
            "futuro":       {"ing": "We will inquire at the front desk.","esp": "Nosotros indagaremos en la recepción."},
            "condicional":  {"ing": "That question would inquire further.","esp": "Esa pregunta indagaría más a fondo."}
        }
    },
    {
        "ing_inf": "instruct", "esp_inf": "instruir",
        "pasado_ing": "instructed", "pasado_esp": "instruyó",
        "participio_ing": "instructed", "participio_esp": "instruido",
        "gerundio_ing": "instructing", "gerundio_esp": "instruyendo",
        "oraciones": {
            "infinitivo":   {"ing": "I instruct new team members.","esp": "Yo instruyo a los nuevos miembros del equipo."},
            "pasadoSimple": {"ing": "You instructed the children well.","esp": "Tú instruiste bien a los niños."},
            "participio":   {"ing": "She has instructed thousands of students.","esp": "Ella ha instruido a miles de estudiantes."},
            "gerundio":     {"ing": "They are instructing the trainees.","esp": "Ellos están instruyendo a los aprendices."},
            "futuro":       {"ing": "We will instruct them tomorrow.","esp": "Nosotros los instruiremos mañana."},
            "condicional":  {"ing": "That manual would instruct anyone.","esp": "Ese manual instruiría a cualquiera."}
        }
    },
    {
        "ing_inf": "intend", "esp_inf": "pretender",
        "pasado_ing": "intended", "pasado_esp": "pretendió",
        "participio_ing": "intended", "participio_esp": "pretendido",
        "gerundio_ing": "intending", "gerundio_esp": "pretendiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I intend to finish today.","esp": "Yo pretendo terminar hoy."},
            "pasadoSimple": {"ing": "You intended to call me back.","esp": "Tú pretendías llamarme de vuelta."},
            "participio":   {"ing": "She has intended to resign for months.","esp": "Ella ha pretendido renunciar durante meses."},
            "gerundio":     {"ing": "They are intending to move abroad.","esp": "Ellos están pretendiendo mudarse al extranjero."},
            "futuro":       {"ing": "We will intend no harm.","esp": "Nosotros no pretenderemos hacer daño."},
            "condicional":  {"ing": "That gesture would intend kindness.","esp": "Ese gesto pretendería ser amable."}
        }
    },
    {
        "ing_inf": "interest", "esp_inf": "interesar",
        "pasado_ing": "interested", "pasado_esp": "interesó",
        "participio_ing": "interested", "participio_esp": "interesado",
        "gerundio_ing": "interesting", "gerundio_esp": "interesando",
        "oraciones": {
            "infinitivo":   {"ing": "I interest myself in science.","esp": "Yo me intereso por la ciencia."},
            "pasadoSimple": {"ing": "You interested me in the project.","esp": "Tú me interesaste en el proyecto."},
            "participio":   {"ing": "She has interested the investors.","esp": "Ella ha interesado a los inversores."},
            "gerundio":     {"ing": "They are interesting the public.","esp": "Ellos están interesando al público."},
            "futuro":       {"ing": "We will interest you in our offer.","esp": "Nosotros te interesaremos en nuestra oferta."},
            "condicional":  {"ing": "That book would interest anyone.","esp": "Ese libro interesaría a cualquiera."}
        }
    },
    {
        "ing_inf": "interfere", "esp_inf": "interferir",
        "pasado_ing": "interfered", "pasado_esp": "interfirió",
        "participio_ing": "interfered", "participio_esp": "interferido",
        "gerundio_ing": "interfering", "gerundio_esp": "interfiriendo",
        "oraciones": {
            "infinitivo":   {"ing": "I don't interfere in others' business.","esp": "Yo no interfiero en los asuntos de otros."},
            "pasadoSimple": {"ing": "You interfered with my plans.","esp": "Tú interferiste en mis planes."},
            "participio":   {"ing": "She has interfered too much.","esp": "Ella ha interferido demasiado."},
            "gerundio":     {"ing": "They are interfering with the signal.","esp": "Ellos están interfiriendo con la señal."},
            "futuro":       {"ing": "We will interfere if needed.","esp": "Nosotros interferiremos si es necesario."},
            "condicional":  {"ing": "That noise would interfere with the call.","esp": "Ese ruido interferiría con la llamada."}
        }
    },
    {
        "ing_inf": "interrupt", "esp_inf": "interrumpir",
        "pasado_ing": "interrupted", "pasado_esp": "interrumpió",
        "participio_ing": "interrupted", "participio_esp": "interrumpido",
        "gerundio_ing": "interrupting", "gerundio_esp": "interrumpiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I interrupt only when necessary.","esp": "Yo interrumpo solo cuando es necesario."},
            "pasadoSimple": {"ing": "You interrupted me mid-sentence.","esp": "Tú me interrumpiste a media frase."},
            "participio":   {"ing": "She has interrupted the meeting.","esp": "Ella ha interrumpido la reunión."},
            "gerundio":     {"ing": "They are interrupting the broadcast.","esp": "Ellos están interrumpiendo la transmisión."},
            "futuro":       {"ing": "We will interrupt the game.","esp": "Nosotros interrumpiremos el juego."},
            "condicional":  {"ing": "That call would interrupt my focus.","esp": "Esa llamada interrumpiría mi concentración."}
        }
    },
    {
        "ing_inf": "introduce", "esp_inf": "introducir",
        "pasado_ing": "introduced", "pasado_esp": "introdujo",
        "participio_ing": "introduced", "participio_esp": "introducido",
        "gerundio_ing": "introducing", "gerundio_esp": "introduciendo",
        "oraciones": {
            "infinitivo":   {"ing": "I introduce myself at parties.","esp": "Yo me presento en las fiestas."},
            "pasadoSimple": {"ing": "You introduced me to your family.","esp": "Tú me presentaste a tu familia."},
            "participio":   {"ing": "She has introduced new products.","esp": "Ella ha introducido productos nuevos."},
            "gerundio":     {"ing": "They are introducing the new law.","esp": "Ellos están introduciendo la nueva ley."},
            "futuro":       {"ing": "We will introduce reforms soon.","esp": "Nosotros introduciremos reformas pronto."},
            "condicional":  {"ing": "That show would introduce new concepts.","esp": "Ese show introduciría conceptos nuevos."}
        }
    },
    {
        "ing_inf": "invent", "esp_inf": "inventar",
        "pasado_ing": "invented", "pasado_esp": "inventó",
        "participio_ing": "invented", "participio_esp": "inventado",
        "gerundio_ing": "inventing", "gerundio_esp": "inventando",
        "oraciones": {
            "infinitivo":   {"ing": "I invent excuses when I'm late.","esp": "Yo invento excusas cuando llego tarde."},
            "pasadoSimple": {"ing": "You invented a clever solution.","esp": "Tú inventaste una solución ingeniosa."},
            "participio":   {"ing": "She has invented a new device.","esp": "Ella ha inventado un dispositivo nuevo."},
            "gerundio":     {"ing": "They are inventing new recipes.","esp": "Ellos están inventando recetas nuevas."},
            "futuro":       {"ing": "We will invent a game.","esp": "Nosotros inventaremos un juego."},
            "condicional":  {"ing": "That mind would invent anything.","esp": "Esa mente inventaría cualquier cosa."}
        }
    },
    {
        "ing_inf": "invite", "esp_inf": "invitar",
        "pasado_ing": "invited", "pasado_esp": "invitó",
        "participio_ing": "invited", "participio_esp": "invitado",
        "gerundio_ing": "inviting", "gerundio_esp": "invitando",
        "oraciones": {
            "infinitivo":   {"ing": "I invite friends over on Fridays.","esp": "Yo invito a amigos los viernes."},
            "pasadoSimple": {"ing": "You invited me to the wedding.","esp": "Tú me invitaste a la boda."},
            "participio":   {"ing": "She has invited the whole class.","esp": "Ella ha invitado a toda la clase."},
            "gerundio":     {"ing": "They are inviting investors.","esp": "Ellos están invitando a inversores."},
            "futuro":       {"ing": "We will invite the neighbors.","esp": "Nosotros invitaremos a los vecinos."},
            "condicional":  {"ing": "That open house would invite anyone.","esp": "Esa jornada de puertas abiertas invitaría a cualquiera."}
        }
    },
    {
        "ing_inf": "irritate", "esp_inf": "irritar",
        "pasado_ing": "irritated", "pasado_esp": "irritó",
        "participio_ing": "irritated", "participio_esp": "irritado",
        "gerundio_ing": "irritating", "gerundio_esp": "irritando",
        "oraciones": {
            "infinitivo":   {"ing": "I get irritated by loud noises.","esp": "Yo me irrito con los ruidos fuertes."},
            "pasadoSimple": {"ing": "You irritated your sister.","esp": "Tú irritaste a tu hermana."},
            "participio":   {"ing": "She has irritated her colleagues.","esp": "Ella ha irritado a sus colegas."},
            "gerundio":     {"ing": "They are irritating the dog.","esp": "Ellos están irritando al perro."},
            "futuro":       {"ing": "We will irritate the boss.","esp": "Nosotros irritaremos al jefe."},
            "condicional":  {"ing": "That noise would irritate anyone.","esp": "Ese ruido irritaría a cualquiera."}
        }
    },
    {
        "ing_inf": "itch", "esp_inf": "picar",
        "pasado_ing": "itched", "pasado_esp": "picó",
        "participio_ing": "itched", "participio_esp": "picado",
        "gerundio_ing": "itching", "gerundio_esp": "picando",
        "oraciones": {
            "infinitivo":   {"ing": "I itch all over in summer.","esp": "Yo me pica todo el cuerpo en verano."},
            "pasadoSimple": {"ing": "You itched from the mosquito bite.","esp": "Te picó la picadura de mosquito."},
            "participio":   {"ing": "She has itched since this morning.","esp": "Le pica desde esta mañana."},
            "gerundio":     {"ing": "They are itching to travel.","esp": "Ellos están que se mueren por viajar."},
            "futuro":       {"ing": "We will itch if we don't shower.","esp": "Nos picará si no nos duchamos."},
            "condicional":  {"ing": "That wool would itch terribly.","esp": "Esa lana picaría muchísimo."}
        }
    },
    {
        "ing_inf": "jail", "esp_inf": "encarcelar",
        "pasado_ing": "jailed", "pasado_esp": "encarceló",
        "participio_ing": "jailed", "participio_esp": "encarcelado",
        "gerundio_ing": "jailing", "gerundio_esp": "encarcelando",
        "oraciones": {
            "infinitivo":   {"ing": "I jail no one in my stories.","esp": "Yo no encarcelo a nadie en mis historias."},
            "pasadoSimple": {"ing": "You jailed the criminal.","esp": "Tú encarcelaste al criminal."},
            "participio":   {"ing": "She has jailed the corrupt officials.","esp": "Ella ha encarcelado a los funcionarios corruptos."},
            "gerundio":     {"ing": "They are jailing the protesters.","esp": "Ellos están encarcelando a los manifestantes."},
            "futuro":       {"ing": "We will jail the thief.","esp": "Nosotros encarcelaremos al ladrón."},
            "condicional":  {"ing": "That judge would jail anyone.","esp": "Ese juez encarcelaría a cualquiera."}
        }
    },
    {
        "ing_inf": "jam", "esp_inf": "atascar",
        "pasado_ing": "jammed", "pasado_esp": "atascó",
        "participio_ing": "jammed", "participio_esp": "atascado",
        "gerundio_ing": "jamming", "gerundio_esp": "atascando",
        "oraciones": {
            "infinitivo":   {"ing": "I jam my keys in the lock sometimes.","esp": "Yo se me atascan las llaves en la cerradura a veces."},
            "pasadoSimple": {"ing": "You jammed the printer again.","esp": "Tú atascaste la impresora otra vez."},
            "participio":   {"ing": "The traffic has jammed completely.","esp": "El tráfico se ha atascado por completo."},
            "gerundio":     {"ing": "They are jamming the signal.","esp": "Ellos están bloqueando la señal."},
            "futuro":       {"ing": "We will jam the mechanism.","esp": "Nosotros atascaremos el mecanismo."},
            "condicional":  {"ing": "That glitch would jam the system.","esp": "Ese fallo atascaría el sistema."}
        }
    },
    {
        "ing_inf": "jog", "esp_inf": "trotar",
        "pasado_ing": "jogged", "pasado_esp": "trotó",
        "participio_ing": "jogged", "participio_esp": "trotado",
        "gerundio_ing": "jogging", "gerundio_esp": "trotando",
        "oraciones": {
            "infinitivo":   {"ing": "I jog in the park every morning.","esp": "Yo troto en el parque cada mañana."},
            "pasadoSimple": {"ing": "You jogged five miles yesterday.","esp": "Tú trotaste cinco millas ayer."},
            "participio":   {"ing": "She has jogged daily for years.","esp": "Ella ha trotado a diario durante años."},
            "gerundio":     {"ing": "They are jogging along the river.","esp": "Ellos están trotando por el río."},
            "futuro":       {"ing": "We will jog together on weekends.","esp": "Nosotros trotaremos juntos los fines de semana."},
            "condicional":  {"ing": "That pace would jog anyone's memory.","esp": "Ese ritmo refrescaría la memoria de cualquiera."}
        }
    },
    {
        "ing_inf": "join", "esp_inf": "unirse",
        "pasado_ing": "joined", "pasado_esp": "se unió",
        "participio_ing": "joined", "participio_esp": "unido",
        "gerundio_ing": "joining", "gerundio_esp": "uniéndose",
        "futuro_esp": "se unirá", "cond_esp": "se uniría",
        "oraciones": {
            "infinitivo":   {"ing": "I join the gym every January.","esp": "Yo me uno al gimnasio cada enero."},
            "pasadoSimple": {"ing": "You joined the club last month.","esp": "Tú te uniste al club el mes pasado."},
            "participio":   {"ing": "She has joined the team.","esp": "Ella se ha unido al equipo."},
            "gerundio":     {"ing": "They are joining forces.","esp": "Ellos se están uniendo en fuerzas."},
            "futuro":       {"ing": "We will join the protest.","esp": "Nosotros nos uniremos a la protesta."},
            "condicional":  {"ing": "That company would join the alliance.","esp": "Esa empresa se uniría a la alianza."}
        }
    },
    {
        "ing_inf": "joke", "esp_inf": "bromear",
        "pasado_ing": "joked", "pasado_esp": "bromeó",
        "participio_ing": "joked", "participio_esp": "bromeado",
        "gerundio_ing": "joking", "gerundio_esp": "bromeando",
        "oraciones": {
            "infinitivo":   {"ing": "I joke around with my coworkers.","esp": "Yo bromeo con mis compañeros de trabajo."},
            "pasadoSimple": {"ing": "You joked about the situation.","esp": "Tú bromaste sobre la situación."},
            "participio":   {"ing": "She has joked too much today.","esp": "Ella ha bromeado demasiado hoy."},
            "gerundio":     {"ing": "They are joking with each other.","esp": "Ellos están bromeando entre ellos."},
            "futuro":       {"ing": "We will joke later.","esp": "Nosotros bromearemos después."},
            "condicional":  {"ing": "That comedian would joke about anything.","esp": "Ese comediante bromearía sobre cualquier cosa."}
        }
    },
    {
        "ing_inf": "judge", "esp_inf": "juzgar",
        "pasado_ing": "judged", "pasado_esp": "juzgó",
        "participio_ing": "judged", "participio_esp": "juzgado",
        "gerundio_ing": "judging", "gerundio_esp": "juzgando",
        "oraciones": {
            "infinitivo":   {"ing": "I judge people by their actions.","esp": "Yo juzgo a las personas por sus acciones."},
            "pasadoSimple": {"ing": "You judged the contest fairly.","esp": "Tú juzgaste el concurso con justicia."},
            "participio":   {"ing": "She has judged many cases.","esp": "Ella ha juzgado muchos casos."},
            "gerundio":     {"ing": "They are judging the competition.","esp": "Ellos están juzgando la competencia."},
            "futuro":       {"ing": "We will judge the finalists tomorrow.","esp": "Nosotros juzgaremos a los finalistas mañana."},
            "condicional":  {"ing": "That panel would judge strictly.","esp": "Ese panel juzgaría con severidad."}
        }
    },
    {
        "ing_inf": "juggle", "esp_inf": "malabarear",
        "pasado_ing": "juggled", "pasado_esp": "malabareó",
        "participio_ing": "juggled", "participio_esp": "malabareado",
        "gerundio_ing": "juggling", "gerundio_esp": "malabareando",
        "oraciones": {
            "infinitivo":   {"ing": "I juggle work and family life.","esp": "Yo hago malabares con el trabajo y la familia."},
            "pasadoSimple": {"ing": "You juggled five balls at once.","esp": "Tú hiciste malabares con cinco pelotas a la vez."},
            "participio":   {"ing": "She has juggled multiple projects.","esp": "Ella ha hecho malabares con varios proyectos."},
            "gerundio":     {"ing": "They are juggling schedules.","esp": "Ellos están haciendo malabares con los horarios."},
            "futuro":       {"ing": "We will juggle the tasks tomorrow.","esp": "Nosotros haremos malabares con las tareas mañana."},
            "condicional":  {"ing": "That performer would juggle anything.","esp": "Ese artista haría malabares con cualquier cosa."}
        }
    },
    {
        "ing_inf": "jump", "esp_inf": "saltar",
        "pasado_ing": "jumped", "pasado_esp": "saltó",
        "participio_ing": "jumped", "participio_esp": "saltado",
        "gerundio_ing": "jumping", "gerundio_esp": "saltando",
        "oraciones": {
            "infinitivo":   {"ing": "I jump rope for exercise.","esp": "Yo salto la cuerda para hacer ejercicio."},
            "pasadoSimple": {"ing": "You jumped over the fence.","esp": "Tú saltaste la valla."},
            "participio":   {"ing": "She has jumped to conclusions.","esp": "Ella ha saltado a conclusiones."},
            "gerundio":     {"ing": "They are jumping on the trampoline.","esp": "Ellos están saltando en el trampolín."},
            "futuro":       {"ing": "We will jump at the chance.","esp": "Nosotros saltaremos ante la oportunidad."},
            "condicional":  {"ing": "That horse would jump easily.","esp": "Ese caballo saltaría fácilmente."}
        }
    },
    {
        "ing_inf": "kick", "esp_inf": "patear",
        "pasado_ing": "kicked", "pasado_esp": "pateó",
        "participio_ing": "kicked", "participio_esp": "pateado",
        "gerundio_ing": "kicking", "gerundio_esp": "pateando",
        "oraciones": {
            "infinitivo":   {"ing": "I kick the ball with my left foot.","esp": "Yo pateo la pelota con el pie izquierdo."},
            "pasadoSimple": {"ing": "You kicked the bucket yesterday.","esp": "Tú pateaste el balde ayer."},
            "participio":   {"ing": "She has kicked the habit.","esp": "Ella ha dejado el hábito."},
            "gerundio":     {"ing": "They are kicking the tires.","esp": "Ellos están pateando las llantas."},
            "futuro":       {"ing": "We will kick off the event.","esp": "Nosotros iniciaremos el evento."},
            "condicional":  {"ing": "That horse would kick anyone.","esp": "Ese caballo patearía a cualquiera."}
        }
    },
    {
        "ing_inf": "kill", "esp_inf": "matar",
        "pasado_ing": "killed", "pasado_esp": "mató",
        "participio_ing": "killed", "participio_esp": "matado",
        "gerundio_ing": "killing", "gerundio_esp": "matando",
        "oraciones": {
            "infinitivo":   {"ing": "I kill weeds in my garden.","esp": "Yo mato maleza en mi jardín."},
            "pasadoSimple": {"ing": "You killed the bug with a magazine.","esp": "Tú mataste al bicho con una revista."},
            "participio":   {"ing": "She has killed the engine.","esp": "Ella ha apagado el motor."},
            "gerundio":     {"ing": "They are killing time at the café.","esp": "Ellos están matando el tiempo en el café."},
            "futuro":       {"ing": "We will kill the lights before bed.","esp": "Nosotros apagaremos las luces antes de dormir."},
            "condicional":  {"ing": "That joke would kill the mood.","esp": "Ese chiste mataría el ambiente."}
        }
    },
    {
        "ing_inf": "kiss", "esp_inf": "besar",
        "pasado_ing": "kissed", "pasado_esp": "besó",
        "participio_ing": "kissed", "participio_esp": "besado",
        "gerundio_ing": "kissing", "gerundio_esp": "besando",
        "oraciones": {
            "infinitivo":   {"ing": "I kiss my partner goodbye.","esp": "Yo beso a mi pareja de despedida."},
            "pasadoSimple": {"ing": "You kissed her on the cheek.","esp": "Tú la besaste en la mejilla."},
            "participio":   {"ing": "She has kissed the baby.","esp": "Ella ha besado al bebé."},
            "gerundio":     {"ing": "They are kissing under the mistletoe.","esp": "Ellos se están besando bajo el muérdago."},
            "futuro":       {"ing": "We will kiss at midnight.","esp": "Nosotros nos besaremos a medianoche."},
            "condicional":  {"ing": "That moment would deserve a kiss.","esp": "Ese momento merecería un beso."}
        }
    },
    {
        "ing_inf": "knit", "esp_inf": "tejer",
        "pasado_ing": "knitted", "pasado_esp": "tejió",
        "participio_ing": "knitted", "participio_esp": "tejido",
        "gerundio_ing": "knitting", "gerundio_esp": "tejiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I knit scarves for my family.","esp": "Yo tejo bufandas para mi familia."},
            "pasadoSimple": {"ing": "You knitted that sweater yourself.","esp": "Tú tejiste ese suéter tú mismo."},
            "participio":   {"ing": "She has knitted since she was young.","esp": "Ella ha tejido desde joven."},
            "gerundio":     {"ing": "They are knitting hats for charity.","esp": "Ellos están tejiendo gorros para caridad."},
            "futuro":       {"ing": "We will knit together this winter.","esp": "Nosotros tejeremos juntos este invierno."},
            "condicional":  {"ing": "That pattern would knit quickly.","esp": "Ese patrón tejería rápidamente."}
        }
    },
    {
        "ing_inf": "knock", "esp_inf": "golpear",
        "pasado_ing": "knocked", "pasado_esp": "golpeó",
        "participio_ing": "knocked", "participio_esp": "golpeado",
        "gerundio_ing": "knocking", "gerundio_esp": "golpeando",
        "oraciones": {
            "infinitivo":   {"ing": "I knock on the door before entering.","esp": "Yo golpeo la puerta antes de entrar."},
            "pasadoSimple": {"ing": "You knocked over the glass.","esp": "Tú tiraste el vaso."},
            "participio":   {"ing": "She has knocked on every door.","esp": "Ella ha tocado cada puerta."},
            "gerundio":     {"ing": "They are knocking down the wall.","esp": "Ellos están derribando el muro."},
            "futuro":       {"ing": "We will knock on wood.","esp": "Nosotros tocaremos madera."},
            "condicional":  {"ing": "That branch would knock anyone out.","esp": "Esa rama noquearía a cualquiera."}
        }
    },
    {
        "ing_inf": "knot", "esp_inf": "anudar",
        "pasado_ing": "knotted", "pasado_esp": "anudó",
        "participio_ing": "knotted", "participio_esp": "anudado",
        "gerundio_ing": "knotting", "gerundio_esp": "anudando",
        "oraciones": {
            "infinitivo":   {"ing": "I knot my tie every morning.","esp": "Yo me anudo la corbata cada mañana."},
            "pasadoSimple": {"ing": "You knotted the rope securely.","esp": "Tú anudaste la cuerda con firmeza."},
            "participio":   {"ing": "She has knotted the thread.","esp": "Ella ha anudado el hilo."},
            "gerundio":     {"ing": "They are knotting the fishing line.","esp": "Ellos están anudando el hilo de pescar."},
            "futuro":       {"ing": "We will knot the scarves.","esp": "Nosotros anudaremos las bufandas."},
            "condicional":  {"ing": "That rope would knot tighter.","esp": "Esa cuerda se anudaría más fuerte."}
        }
    },
    {
        "ing_inf": "label", "esp_inf": "etiquetar",
        "pasado_ing": "labeled", "pasado_esp": "etiquetó",
        "participio_ing": "labeled", "participio_esp": "etiquetado",
        "gerundio_ing": "labeling", "gerundio_esp": "etiquetando",
        "oraciones": {
            "infinitivo":   {"ing": "I label all my jars at home.","esp": "Yo etiqueto todos mis frascos en casa."},
            "pasadoSimple": {"ing": "You labeled the boxes correctly.","esp": "Tú etiquetaste las cajas correctamente."},
            "participio":   {"ing": "She has labeled the documents.","esp": "Ella ha etiquetado los documentos."},
            "gerundio":     {"ing": "They are labeling the products.","esp": "Ellos están etiquetando los productos."},
            "futuro":       {"ing": "We will label the cables.","esp": "Nosotros etiquetaremos los cables."},
            "condicional":  {"ing": "That system would label automatically.","esp": "Ese sistema etiquetaría automáticamente."}
        }
    },
    {
        "ing_inf": "land", "esp_inf": "aterrizar",
        "pasado_ing": "landed", "pasado_esp": "aterrizó",
        "participio_ing": "landed", "participio_esp": "aterrizado",
        "gerundio_ing": "landing", "gerundio_esp": "aterrizando",
        "oraciones": {
            "infinitivo":   {"ing": "I land safely every time I fly.","esp": "Yo aterrizo seguro cada vez que vuelo."},
            "pasadoSimple": {"ing": "You landed the plane smoothly.","esp": "Tú aterrizaste el avión sin problemas."},
            "participio":   {"ing": "She has landed a great job.","esp": "Ella ha conseguido un gran trabajo."},
            "gerundio":     {"ing": "They are landing in Madrid now.","esp": "Ellos están aterrizando en Madrid ahora."},
            "futuro":       {"ing": "We will land before sunset.","esp": "Nosotros aterrizaremos antes del atardecer."},
            "condicional":  {"ing": "That bird would land gracefully.","esp": "Ese pájaro aterrizaría con gracia."}
        }
    },
    {
        "ing_inf": "last", "esp_inf": "durar",
        "pasado_ing": "lasted", "pasado_esp": "duró",
        "participio_ing": "lasted", "participio_esp": "durado",
        "gerundio_ing": "lasting", "gerundio_esp": "durando",
        "oraciones": {
            "infinitivo":   {"ing": "I last about an hour at the gym.","esp": "Yo duro como una hora en el gimnasio."},
            "pasadoSimple": {"ing": "You lasted longer than expected.","esp": "Tú duraste más de lo esperado."},
            "participio":   {"ing": "The battery has lasted all day.","esp": "La batería ha durado todo el día."},
            "gerundio":     {"ing": "They are lasting through the storm.","esp": "Ellos están durando durante la tormenta."},
            "futuro":       {"ing": "We will last until next week.","esp": "Nosotros duraremos hasta la próxima semana."},
            "condicional":  {"ing": "That memory would last forever.","esp": "Ese recuerdo duraría para siempre."}
        }
    }
]


BLOQUE_15 = [
    {
        "ing_inf": "laugh", "esp_inf": "reír",
        "pasado_ing": "laughed", "pasado_esp": "rió",
        "participio_ing": "laughed", "participio_esp": "reído",
        "gerundio_ing": "laughing", "gerundio_esp": "riendo",
        "oraciones": {
            "infinitivo":   {"ing": "I laugh at funny videos.",     "esp": "Yo me río de videos graciosos."},
            "pasadoSimple": {"ing": "You laughed at my joke.",       "esp": "Tú te reíste de mi chiste."},
            "participio":   {"ing": "She has laughed all afternoon.","esp": "Ella se ha reído toda la tarde."},
            "gerundio":     {"ing": "They are laughing loudly.",     "esp": "Ellos se están riendo a carcajadas."},
            "futuro":       {"ing": "We will laugh about this later.","esp": "Nosotros nos reiremos de esto después."},
            "condicional":  {"ing": "That joke would make anyone laugh.","esp": "Ese chiste haría reír a cualquiera."}
        }
    },
    {
        "ing_inf": "learn", "esp_inf": "aprender",
        "pasado_ing": "learned", "pasado_esp": "aprendió",
        "participio_ing": "learned", "participio_esp": "aprendido",
        "gerundio_ing": "learning", "gerundio_esp": "aprendiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I learn new things every day.","esp": "Yo aprendo cosas nuevas cada día."},
            "pasadoSimple": {"ing": "You learned to drive last year.","esp": "Tú aprendiste a manejar el año pasado."},
            "participio":   {"ing": "She has learned Spanish quickly.","esp": "Ella ha aprendido español rápidamente."},
            "gerundio":     {"ing": "They are learning the basics.","esp": "Ellos están aprendiendo lo básico."},
            "futuro":       {"ing": "We will learn from mistakes.","esp": "Nosotros aprenderemos de los errores."},
            "condicional":  {"ing": "That experience would teach anyone to learn.","esp": "Esa experiencia enseñaría a cualquiera a aprender."}
        }
    },
    {
        "ing_inf": "lick", "esp_inf": "lamer",
        "pasado_ing": "licked", "pasado_esp": "lamió",
        "participio_ing": "licked", "participio_esp": "lamido",
        "gerundio_ing": "licking", "gerundio_esp": "lamiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I lick my fingers when eating pizza.","esp": "Yo me lamo los dedos cuando como pizza."},
            "pasadoSimple": {"ing": "You licked the ice cream.",     "esp": "Tú lamiste el helado."},
            "participio":   {"ing": "The cat has licked its paw.",   "esp": "El gato se ha lamido la pata."},
            "gerundio":     {"ing": "They are licking the stamps.",  "esp": "Ellos están lamiendo los sellos."},
            "futuro":       {"ing": "We will lick the envelopes.","esp": "Nosotros lameremos los sobres."},
            "condicional":  {"ing": "That flame would lick everything.","esp": "Esa llama lamería todo."}
        }
    },
    {
        "ing_inf": "lighten", "esp_inf": "aligerar",
        "pasado_ing": "lightened", "pasado_esp": "aligeró",
        "participio_ing": "lightened", "participio_esp": "aligerado",
        "gerundio_ing": "lightening", "gerundio_esp": "aligerando",
        "oraciones": {
            "infinitivo":   {"ing": "I lighten my mood with music.","esp": "Yo me alivio el ánimo con música."},
            "pasadoSimple": {"ing": "You lightened the load.",      "esp": "Tú aligeraste la carga."},
            "participio":   {"ing": "She has lightened her hair color.","esp": "Ella ha aclarado el color de su pelo."},
            "gerundio":     {"ing": "They are lightening the atmosphere.","esp": "Ellos están aligerando el ambiente."},
            "futuro":       {"ing": "We will lighten the taxes.","esp": "Nosotros aligeraremos los impuestos."},
            "condicional":  {"ing": "That color would lighten the room.","esp": "Ese color aclararía el cuarto."}
        }
    },
    {
        "ing_inf": "like", "esp_inf": "gustar",
        "pasado_ing": "liked", "pasado_esp": "gustó",
        "participio_ing": "liked", "participio_esp": "gustado",
        "gerundio_ing": "liking", "gerundio_esp": "gustando",
        "oraciones": {
            "infinitivo":   {"ing": "I like chocolate ice cream.", "esp": "Me gusta el helado de chocolate."},
            "pasadoSimple": {"ing": "You liked the movie a lot.",   "esp": "Te gustó mucho la película."},
            "participio":   {"ing": "She has liked him for years.", "esp": "Le ha gustado él durante años."},
            "gerundio":     {"ing": "They are liking the new house.","esp": "Les está gustando la casa nueva."},
            "futuro":       {"ing": "We will like the change.",     "esp": "Nos gustará el cambio."},
            "condicional":  {"ing": "That song would please everyone.","esp": "Esa canción le gustaría a todos."}
        }
    },
    {
        "ing_inf": "listen", "esp_inf": "escuchar",
        "pasado_ing": "listened", "pasado_esp": "escuchó",
        "participio_ing": "listened", "participio_esp": "escuchado",
        "gerundio_ing": "listening", "gerundio_esp": "escuchando",
        "oraciones": {
            "infinitivo":   {"ing": "I listen to podcasts on my commute.","esp": "Yo escucho podcasts en mi trayecto."},
            "pasadoSimple": {"ing": "You listened to my advice.",   "esp": "Tú escuchaste mi consejo."},
            "participio":   {"ing": "She has listened to classical music.","esp": "Ella ha escuchado música clásica."},
            "gerundio":     {"ing": "They are listening to the lecture.","esp": "Ellos están escuchando la conferencia."},
            "futuro":       {"ing": "We will listen carefully.",    "esp": "Nosotros escucharemos con atención."},
            "condicional":  {"ing": "That song would make anyone listen.","esp": "Esa canción haría escuchar a cualquiera."}
        }
    },
    {
        "ing_inf": "live", "esp_inf": "vivir",
        "pasado_ing": "lived", "pasado_esp": "vivió",
        "participio_ing": "lived", "participio_esp": "vivido",
        "gerundio_ing": "living", "gerundio_esp": "viviendo",
        "oraciones": {
            "infinitivo":   {"ing": "I live in a small apartment.","esp": "Yo vivo en un apartamento pequeño."},
            "pasadoSimple": {"ing": "You lived abroad for years.","esp": "Tú viviste en el extranjero durante años."},
            "participio":   {"ing": "She has lived a full life.",  "esp": "Ella ha vivido una vida plena."},
            "gerundio":     {"ing": "They are living their dream.","esp": "Ellos están viviendo su sueño."},
            "futuro":       {"ing": "We will live happily ever after.","esp": "Nosotros viviremos felices para siempre."},
            "condicional":  {"ing": "That idea would live forever.","esp": "Esa idea viviría para siempre."}
        }
    },
    {
        "ing_inf": "load", "esp_inf": "cargar",
        "pasado_ing": "loaded", "pasado_esp": "cargó",
        "participio_ing": "loaded", "participio_esp": "cargado",
        "gerundio_ing": "loading", "gerundio_esp": "cargando",
        "oraciones": {
            "infinitivo":   {"ing": "I load the dishwasher every night.","esp": "Yo cargo el lavavajillas cada noche."},
            "pasadoSimple": {"ing": "You loaded the truck this morning.","esp": "Tú cargaste el camión esta mañana."},
            "participio":   {"ing": "She has loaded the software.","esp": "Ella ha cargado el software."},
            "gerundio":     {"ing": "They are loading the boxes.","esp": "Ellos están cargando las cajas."},
            "futuro":       {"ing": "We will load the page.","esp": "Nosotros cargaremos la página."},
            "condicional":  {"ing": "That script would load automatically.","esp": "Ese script cargaría automáticamente."}
        }
    },
    {
        "ing_inf": "lock", "esp_inf": "cerrar",
        "pasado_ing": "locked", "pasado_esp": "cerró",
        "participio_ing": "locked", "participio_esp": "cerrado",
        "gerundio_ing": "locking", "gerundio_esp": "cerrando",
        "oraciones": {
            "infinitivo":   {"ing": "I lock the door every night.","esp": "Yo cierro con llave la puerta cada noche."},
            "pasadoSimple": {"ing": "You locked the car.",          "esp": "Tú cerraste el coche con llave."},
            "participio":   {"ing": "She has locked the safe.",    "esp": "Ella ha cerrado la caja fuerte."},
            "gerundio":     {"ing": "They are locking the gate.",  "esp": "Ellos están cerrando la verja con llave."},
            "futuro":       {"ing": "We will lock the files.",     "esp": "Nosotros bloquearemos los archivos."},
            "condicional":  {"ing": "That password would lock the account.","esp": "Esa contraseña bloquearía la cuenta."}
        }
    },
    {
        "ing_inf": "look", "esp_inf": "mirar",
        "pasado_ing": "looked", "pasado_esp": "miró",
        "participio_ing": "looked", "participio_esp": "mirado",
        "gerundio_ing": "looking", "gerundio_esp": "mirando",
        "oraciones": {
            "infinitivo":   {"ing": "I look at the stars at night.","esp": "Yo miro las estrellas por la noche."},
            "pasadoSimple": {"ing": "You looked both ways.",        "esp": "Tú miraste a ambos lados."},
            "participio":   {"ing": "She has looked at the data.", "esp": "Ella ha mirado los datos."},
            "gerundio":     {"ing": "They are looking for the key.","esp": "Ellos están buscando la llave."},
            "futuro":       {"ing": "We will look into it.",       "esp": "Nosotros lo investigaremos."},
            "condicional":  {"ing": "That view would look amazing.","esp": "Esa vista se vería increíble."}
        }
    },
    {
        "ing_inf": "love", "esp_inf": "amar",
        "pasado_ing": "loved", "pasado_esp": "amó",
        "participio_ing": "loved", "participio_esp": "amado",
        "gerundio_ing": "loving", "gerundio_esp": "amando",
        "oraciones": {
            "infinitivo":   {"ing": "I love reading before bed.",  "esp": "Yo amo leer antes de dormir."},
            "pasadoSimple": {"ing": "You loved the concert.",      "esp": "Tú amaste el concierto."},
            "participio":   {"ing": "She has loved him forever.",  "esp": "Ella lo ha amado por siempre."},
            "gerundio":     {"ing": "They are loving the vacation.","esp": "Ellos están disfrutando las vacaciones."},
            "futuro":       {"ing": "We will love this place.",    "esp": "Nosotros amaremos este lugar."},
            "condicional":  {"ing": "That movie would delight audiences.","esp": "Esa película encantaría al público."}
        }
    },
    {
        "ing_inf": "manage", "esp_inf": "manejar",
        "pasado_ing": "managed", "pasado_esp": "manejó",
        "participio_ing": "managed", "participio_esp": "manejado",
        "gerundio_ing": "managing", "gerundio_esp": "manejando",
        "oraciones": {
            "infinitivo":   {"ing": "I manage a team of ten people.","esp": "Yo manejo un equipo de diez personas."},
            "pasadoSimple": {"ing": "You managed the project well.","esp": "Tú manejaste bien el proyecto."},
            "participio":   {"ing": "She has managed the company for years.","esp": "Ella ha manejado la empresa durante años."},
            "gerundio":     {"ing": "They are managing the crisis.","esp": "Ellos están manejando la crisis."},
            "futuro":       {"ing": "We will manage the budget.","esp": "Nosotros manejaremos el presupuesto."},
            "condicional":  {"ing": "That manager would handle any team.","esp": "Ese gerente manejaría cualquier equipo."}
        }
    },
    {
        "ing_inf": "march", "esp_inf": "marchar",
        "pasado_ing": "marched", "pasado_esp": "marchó",
        "participio_ing": "marched", "participio_esp": "marchado",
        "gerundio_ing": "marching", "gerundio_esp": "marchando",
        "oraciones": {
            "infinitivo":   {"ing": "I march to the beat of my own drum.","esp": "Yo sigo mi propio ritmo."},
            "pasadoSimple": {"ing": "You marched in the parade.","esp": "Tú marchaste en el desfile."},
            "participio":   {"ing": "She has marched for civil rights.","esp": "Ella ha marchado por los derechos civiles."},
            "gerundio":     {"ing": "They are marching toward the capital.","esp": "Ellos están marchando hacia la capital."},
            "futuro":       {"ing": "We will march tomorrow.","esp": "Nosotros marcharemos mañana."},
            "condicional":  {"ing": "That protest would march peacefully.","esp": "Esa protesta marcharía pacíficamente."}
        }
    },
    {
        "ing_inf": "mark", "esp_inf": "marcar",
        "pasado_ing": "marked", "pasado_esp": "marcó",
        "participio_ing": "marked", "participio_esp": "marcado",
        "gerundio_ing": "marking", "gerundio_esp": "marcando",
        "oraciones": {
            "infinitivo":   {"ing": "I mark my calendar with important dates.","esp": "Yo marco mi calendario con fechas importantes."},
            "pasadoSimple": {"ing": "You marked the wrong answer.","esp": "Tú marcaste la respuesta incorrecta."},
            "participio":   {"ing": "She has marked the test.",   "esp": "Ella ha marcado el examen."},
            "gerundio":     {"ing": "They are marking the territory.","esp": "Ellos están marcando el territorio."},
            "futuro":       {"ing": "We will mark the occasion.","esp": "Nosotros marcaremos la ocasión."},
            "condicional":  {"ing": "That scar would mark him forever.","esp": "Esa cicatriz lo marcaría para siempre."}
        }
    },
    {
        "ing_inf": "match", "esp_inf": "combinar",
        "pasado_ing": "matched", "pasado_esp": "combinó",
        "participio_ing": "matched", "participio_esp": "combinado",
        "gerundio_ing": "matching", "gerundio_esp": "combinando",
        "oraciones": {
            "infinitivo":   {"ing": "I match my socks by color.","esp": "Yo combino mis calcetines por color."},
            "pasadoSimple": {"ing": "You matched the description perfectly.","esp": "Tú coincidías perfectamente con la descripción."},
            "participio":   {"ing": "She has matched the donation.","esp": "Ella ha igualado la donación."},
            "gerundio":     {"ing": "They are matching the colors.","esp": "Ellos están combinando los colores."},
            "futuro":       {"ing": "We will match their offer.","esp": "Nosotros igualaremos su oferta."},
            "condicional":  {"ing": "That tie would match the suit.","esp": "Esa corbata combinaría con el traje."}
        }
    },
    {
        "ing_inf": "matter", "esp_inf": "importar",
        "pasado_ing": "mattered", "pasado_esp": "importó",
        "participio_ing": "mattered", "participio_esp": "importado",
        "gerundio_ing": "mattering", "gerundio_esp": "importando",
        "oraciones": {
            "infinitivo":   {"ing": "I matter to my family.",      "esp": "Yo le importo a mi familia."},
            "pasadoSimple": {"ing": "You mattered to the team.",   "esp": "Tú le importabas al equipo."},
            "participio":   {"ing": "She has mattered in this project.","esp": "Ella ha importado en este proyecto."},
            "gerundio":     {"ing": "They are mattering more each day.","esp": "Ellos están importando más cada día."},
            "futuro":       {"ing": "We will matter in the decision.","esp": "Nosotros importaremos en la decisión."},
            "condicional":  {"ing": "That detail would matter to the judge.","esp": "Ese detalle importaría al juez."}
        }
    },
    {
        "ing_inf": "measure", "esp_inf": "medir",
        "pasado_ing": "measured", "pasado_esp": "midió",
        "participio_ing": "measured", "participio_esp": "medido",
        "gerundio_ing": "measuring", "gerundio_esp": "midiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I measure the ingredients carefully.","esp": "Yo mido los ingredientes con cuidado."},
            "pasadoSimple": {"ing": "You measured the window yesterday.","esp": "Tú mediste la ventana ayer."},
            "participio":   {"ing": "She has measured the room.","esp": "Ella ha medido el cuarto."},
            "gerundio":     {"ing": "They are measuring the distance.","esp": "Ellos están midiendo la distancia."},
            "futuro":       {"ing": "We will measure the impact.","esp": "Nosotros mediremos el impacto."},
            "condicional":  {"ing": "That tool would measure precisely.","esp": "Esa herramienta mediría con precisión."}
        }
    },
    {
        "ing_inf": "melt", "esp_inf": "derretir",
        "pasado_ing": "melted", "pasado_esp": "derritió",
        "participio_ing": "melted", "participio_esp": "derretido",
        "gerundio_ing": "melting", "gerundio_esp": "derritiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I melt chocolate for desserts.","esp": "Yo derrito chocolate para postres."},
            "pasadoSimple": {"ing": "You melted the butter already.","esp": "Tú derretiste la mantequilla ya."},
            "participio":   {"ing": "She has melted the ice.",      "esp": "Ella ha derretido el hielo."},
            "gerundio":     {"ing": "They are melting in the heat.","esp": "Ellos se están derritiendo con el calor."},
            "futuro":       {"ing": "We will melt the cheese on top.","esp": "Nosotros derretiremos el queso encima."},
            "condicional":  {"ing": "That ice cream would melt fast.","esp": "Ese helado se derretiría rápido."}
        }
    },
    {
        "ing_inf": "mention", "esp_inf": "mencionar",
        "pasado_ing": "mentioned", "pasado_esp": "mencionó",
        "participio_ing": "mentioned", "participio_esp": "mencionado",
        "gerundio_ing": "mentioning", "gerundio_esp": "mencionando",
        "oraciones": {
            "infinitivo":   {"ing": "I mention it to everyone I meet.","esp": "Yo lo menciono a todos los que conozco."},
            "pasadoSimple": {"ing": "You mentioned the issue earlier.","esp": "Tú mencionaste el problema antes."},
            "participio":   {"ing": "She has mentioned the rumor.","esp": "Ella ha mencionado el rumor."},
            "gerundio":     {"ing": "They are mentioning the new policy.","esp": "Ellos están mencionando la nueva política."},
            "futuro":       {"ing": "We will mention it in the meeting.","esp": "Nosotros lo mencionaremos en la reunión."},
            "condicional":  {"ing": "That report would mention the facts.","esp": "Ese informe mencionaría los hechos."}
        }
    },
    {
        "ing_inf": "mess", "esp_inf": "desordenar",
        "pasado_ing": "messed", "pasado_esp": "desordenó",
        "participio_ing": "messed", "participio_esp": "desordenado",
        "gerundio_ing": "messing", "gerundio_esp": "desordenando",
        "oraciones": {
            "infinitivo":   {"ing": "I mess up sometimes.",         "esp": "Yo me equivoco a veces."},
            "pasadoSimple": {"ing": "You messed up the recipe.",    "esp": "Tú echaste a perder la receta."},
            "participio":   {"ing": "She has messed up her room.",  "esp": "Ella ha desordenado su cuarto."},
            "gerundio":     {"ing": "They are messing with the controls.","esp": "Ellos están jugando con los controles."},
            "futuro":       {"ing": "We will mess around later.","esp": "Nosotros haremos travesuras después."},
            "condicional":  {"ing": "That code would mess up the system.","esp": "Ese código descontrolaría el sistema."}
        }
    },
    {
        "ing_inf": "miss", "esp_inf": "extrañar",
        "pasado_ing": "missed", "pasado_esp": "extrañó",
        "participio_ing": "missed", "participio_esp": "extrañado",
        "gerundio_ing": "missing", "gerundio_esp": "extrañando",
        "oraciones": {
            "infinitivo":   {"ing": "I miss my family when traveling.","esp": "Yo extraño a mi familia cuando viajo."},
            "pasadoSimple": {"ing": "You missed the bus this morning.","esp": "Tú perdiste el autobús esta mañana."},
            "participio":   {"ing": "She has missed the deadline.","esp": "Ella ha perdido el plazo."},
            "gerundio":     {"ing": "They are missing their friends.","esp": "Ellos están extrañando a sus amigos."},
            "futuro":       {"ing": "We will miss the opportunity.","esp": "Nosotros perderemos la oportunidad."},
            "condicional":  {"ing": "That shot would miss the target.","esp": "Ese disparo fallaría el objetivo."}
        }
    },
    {
        "ing_inf": "mix", "esp_inf": "mezclar",
        "pasado_ing": "mixed", "pasado_esp": "mezcló",
        "participio_ing": "mixed", "participio_esp": "mezclado",
        "gerundio_ing": "mixing", "gerundio_esp": "mezclando",
        "oraciones": {
            "infinitivo":   {"ing": "I mix the colors to get green.","esp": "Yo mezclo los colores para obtener verde."},
            "pasadoSimple": {"ing": "You mixed up the names.",      "esp": "Tú confundiste los nombres."},
            "participio":   {"ing": "She has mixed the batter.",   "esp": "Ella ha mezclado la masa."},
            "gerundio":     {"ing": "They are mixing the drinks.", "esp": "Ellos están mezclando las bebidas."},
            "futuro":       {"ing": "We will mix the ingredients.","esp": "Nosotros mezclaremos los ingredientes."},
            "condicional":  {"ing": "That shade would mix well.","esp": "Esa tonalidad combinaría bien."}
        }
    },
    {
        "ing_inf": "move", "esp_inf": "mover",
        "pasado_ing": "moved", "pasado_esp": "movió",
        "participio_ing": "moved", "participio_esp": "movido",
        "gerundio_ing": "moving", "gerundio_esp": "moviendo",
        "oraciones": {
            "infinitivo":   {"ing": "I move to a new city every few years.","esp": "Yo me mudo a una ciudad nueva cada pocos años."},
            "pasadoSimple": {"ing": "You moved the furniture yesterday.","esp": "Tú moviste los muebles ayer."},
            "participio":   {"ing": "She has moved on from the breakup.","esp": "Ella ha seguido adelante tras la ruptura."},
            "gerundio":     {"ing": "They are moving boxes all day.","esp": "Ellos están moviendo cajas todo el día."},
            "futuro":       {"ing": "We will move forward with the plan.","esp": "Nosotros avanzaremos con el plan."},
            "condicional":  {"ing": "That speech would move the audience.","esp": "Ese discurso conmovería al público."}
        }
    },
    {
        "ing_inf": "name", "esp_inf": "nombrar",
        "pasado_ing": "named", "pasado_esp": "nombró",
        "participio_ing": "named", "participio_esp": "nombrado",
        "gerundio_ing": "naming", "gerundio_esp": "nombrando",
        "oraciones": {
            "infinitivo":   {"ing": "I name my plants after famous scientists.","esp": "Yo nombro mis plantas como científicos famosos."},
            "pasadoSimple": {"ing": "You named the baby yesterday.","esp": "Tú nombraste al bebé ayer."},
            "participio":   {"ing": "She has named the project.","esp": "Ella ha nombrado el proyecto."},
            "gerundio":     {"ing": "They are naming the suspects.","esp": "Ellos están nombrando a los sospechosos."},
            "futuro":       {"ing": "We will name the winner soon.","esp": "Nosotros nombraremos al ganador pronto."},
            "condicional":  {"ing": "That brand would name anything.","esp": "Esa marca nombraría cualquier cosa."}
        }
    },
    {
        "ing_inf": "need", "esp_inf": "necesitar",
        "pasado_ing": "needed", "pasado_esp": "necesitó",
        "participio_ing": "needed", "participio_esp": "necesitado",
        "gerundio_ing": "needing", "gerundio_esp": "necesitando",
        "oraciones": {
            "infinitivo":   {"ing": "I need more coffee in the morning.","esp": "Yo necesito más café por la mañana."},
            "pasadoSimple": {"ing": "You needed help yesterday.","esp": "Tú necesitabas ayuda ayer."},
            "participio":   {"ing": "She has needed rest for days.","esp": "Ella ha necesitado descansar durante días."},
            "gerundio":     {"ing": "They are needing support.","esp": "Ellos están necesitando apoyo."},
            "futuro":       {"ing": "We will need more time.","esp": "Nosotros necesitaremos más tiempo."},
            "condicional":  {"ing": "That would need approval.","esp": "Eso necesitaría aprobación."}
        }
    },
    {
        "ing_inf": "notice", "esp_inf": "notar",
        "pasado_ing": "noticed", "pasado_esp": "notó",
        "participio_ing": "noticed", "participio_esp": "notado",
        "gerundio_ing": "noticing", "gerundio_esp": "notando",
        "oraciones": {
            "infinitivo":   {"ing": "I notice small details easily.","esp": "Yo noto pequeños detalles con facilidad."},
            "pasadoSimple": {"ing": "You noticed the change immediately.","esp": "Tú notaste el cambio de inmediato."},
            "participio":   {"ing": "She has noticed the difference.","esp": "Ella ha notado la diferencia."},
            "gerundio":     {"ing": "They are noticing the symptoms.","esp": "Ellos están notando los síntomas."},
            "futuro":       {"ing": "We will notice the result soon.","esp": "Nosotros notaremos el resultado pronto."},
            "condicional":  {"ing": "That flaw would be noticed by anyone.","esp": "Ese defecto sería notado por cualquiera."}
        }
    },
    {
        "ing_inf": "number", "esp_inf": "numerar",
        "pasado_ing": "numbered", "pasado_esp": "numeró",
        "participio_ing": "numbered", "participio_esp": "numerado",
        "gerundio_ing": "numbering", "gerundio_esp": "numerando",
        "oraciones": {
            "infinitivo":   {"ing": "I number the pages in my notebook.","esp": "Yo numero las páginas de mi cuaderno."},
            "pasadoSimple": {"ing": "You numbered the seats.",     "esp": "Tú numeraste los asientos."},
            "participio":   {"ing": "She has numbered the chapters.","esp": "Ella ha numerado los capítulos."},
            "gerundio":     {"ing": "They are numbering the items.","esp": "Ellos están numerando los artículos."},
            "futuro":       {"ing": "We will number the rules.",  "esp": "Nosotros numeraremos las reglas."},
            "condicional":  {"ing": "That street would number the houses.","esp": "Esa calle numeraría las casas."}
        }
    },
    {
        "ing_inf": "obey", "esp_inf": "obedecer",
        "pasado_ing": "obeyed", "pasado_esp": "obedeció",
        "participio_ing": "obeyed", "participio_esp": "obedecido",
        "gerundio_ing": "obeying", "gerundio_esp": "obedeciendo",
        "oraciones": {
            "infinitivo":   {"ing": "I obey the traffic laws.",    "esp": "Yo obedezco las leyes de tránsito."},
            "pasadoSimple": {"ing": "You obeyed your parents.",    "esp": "Tú obedeciste a tus padres."},
            "participio":   {"ing": "She has obeyed the rules.",   "esp": "Ella ha obedecido las reglas."},
            "gerundio":     {"ing": "They are obeying orders.",    "esp": "Ellos están obedeciendo órdenes."},
            "futuro":       {"ing": "We will obey the court.",     "esp": "Nosotros obedeceremos al tribunal."},
            "condicional":  {"ing": "That dog would obey anyone.","esp": "Ese perro obedecería a cualquiera."}
        }
    },
    {
        "ing_inf": "object", "esp_inf": "objetar",
        "pasado_ing": "objected", "pasado_esp": "objetó",
        "participio_ing": "objected", "participio_esp": "objetado",
        "gerundio_ing": "objecting", "gerundio_esp": "objetando",
        "oraciones": {
            "infinitivo":   {"ing": "I object to the proposal.",   "esp": "Yo objeto la propuesta."},
            "pasadoSimple": {"ing": "You objected loudly.",        "esp": "Tú objetaste en voz alta."},
            "participio":   {"ing": "She has objected to the terms.","esp": "Ella ha objetado los términos."},
            "gerundio":     {"ing": "They are objecting to the plan.","esp": "Ellos están objetando el plan."},
            "futuro":       {"ing": "We will object at the meeting.","esp": "Nosotros objetaremos en la reunión."},
            "condicional":  {"ing": "That clause would cause anyone to object.","esp": "Esa cláusula haría que cualquiera objetara."}
        }
    },
    {
        "ing_inf": "observe", "esp_inf": "observar",
        "pasado_ing": "observed", "pasado_esp": "observó",
        "participio_ing": "observed", "participio_esp": "observado",
        "gerundio_ing": "observing", "gerundio_esp": "observando",
        "oraciones": {
            "infinitivo":   {"ing": "I observe the behavior of animals.","esp": "Yo observo el comportamiento de los animales."},
            "pasadoSimple": {"ing": "You observed the experiment carefully.","esp": "Tú observaste el experimento con cuidado."},
            "participio":   {"ing": "She has observed the patterns.","esp": "Ella ha observado los patrones."},
            "gerundio":     {"ing": "They are observing the eclipse.","esp": "Ellos están observando el eclipse."},
            "futuro":       {"ing": "We will observe the results.","esp": "Nosotros observaremos los resultados."},
            "condicional":  {"ing": "That telescope would observe stars.","esp": "Ese telescopio observaría estrellas."}
        }
    }
]


BLOQUE_16 = [
    {
        "ing_inf": "offer", "esp_inf": "ofrecer",
        "pasado_ing": "offered", "pasado_esp": "ofreció",
        "participio_ing": "offered", "participio_esp": "ofrecido",
        "gerundio_ing": "offering", "gerundio_esp": "ofreciendo",
        "oraciones": {
            "infinitivo":   {"ing": "I offer help to anyone in need.","esp": "Yo ofrezco ayuda a quien la necesite."},
            "pasadoSimple": {"ing": "You offered me your seat.","esp": "Tú me ofreciste tu asiento."},
            "participio":   {"ing": "She has offered a discount.","esp": "Ella ha ofrecido un descuento."},
            "gerundio":     {"ing": "They are offering free samples.","esp": "Ellos están ofreciendo muestras gratis."},
            "futuro":       {"ing": "We will offer our support.","esp": "Nosotros ofreceremos nuestro apoyo."},
            "condicional":  {"ing": "That company would offer better terms.","esp": "Esa empresa ofrecería mejores condiciones."}
        }
    },
    {
        "ing_inf": "open", "esp_inf": "abrir",
        "pasado_ing": "opened", "pasado_esp": "abrió",
        "participio_ing": "opened", "participio_esp": "abierto",
        "gerundio_ing": "opening", "gerundio_esp": "abriendo",
        "oraciones": {
            "infinitivo":   {"ing": "I open the windows every morning.","esp": "Yo abro las ventanas cada mañana."},
            "pasadoSimple": {"ing": "You opened the package yesterday.","esp": "Tú abriste el paquete ayer."},
            "participio":   {"ing": "She has opened a new shop.","esp": "Ella ha abierto una tienda nueva."},
            "gerundio":     {"ing": "They are opening the gates now.","esp": "Ellos están abriendo las puertas ahora."},
            "futuro":       {"ing": "We will open early tomorrow.","esp": "Nosotros abriremos temprano mañana."},
            "condicional":  {"ing": "That door would open easily.","esp": "Esa puerta se abriría fácilmente."}
        }
    },
    {
        "ing_inf": "order", "esp_inf": "ordenar",
        "pasado_ing": "ordered", "pasado_esp": "ordenó",
        "participio_ing": "ordered", "participio_esp": "ordenado",
        "gerundio_ing": "ordering", "gerundio_esp": "ordenando",
        "oraciones": {
            "infinitivo":   {"ing": "I order food online often.","esp": "Yo pido comida en línea a menudo."},
            "pasadoSimple": {"ing": "You ordered pizza last night.","esp": "Tú pediste pizza anoche."},
            "participio":   {"ing": "She has ordered the books.","esp": "Ella ha pedido los libros."},
            "gerundio":     {"ing": "They are ordering more supplies.","esp": "Ellos están pidiendo más suministros."},
            "futuro":       {"ing": "We will order at noon.","esp": "Nosotros pediremos al mediodía."},
            "condicional":  {"ing": "That app would order automatically.","esp": "Esa app pediría automáticamente."}
        }
    },
    {
        "ing_inf": "organize", "esp_inf": "organizar",
        "pasado_ing": "organized", "pasado_esp": "organizó",
        "participio_ing": "organized", "participio_esp": "organizado",
        "gerundio_ing": "organizing", "gerundio_esp": "organizando",
        "oraciones": {
            "infinitivo":   {"ing": "I organize my closet every spring.","esp": "Yo organizo mi armario cada primavera."},
            "pasadoSimple": {"ing": "You organized the event beautifully.","esp": "Tú organizaste el evento con belleza."},
            "participio":   {"ing": "She has organized a charity drive.","esp": "Ella ha organizado una colecta benéfica."},
            "gerundio":     {"ing": "They are organizing the conference.","esp": "Ellos están organizando la conferencia."},
            "futuro":       {"ing": "We will organize the files later.","esp": "Nosotros organizaremos los archivos después."},
            "condicional":  {"ing": "That planner would organize everything.","esp": "Ese organizador lo organizaría todo."}
        }
    },
    {
        "ing_inf": "paint", "esp_inf": "pintar",
        "pasado_ing": "painted", "pasado_esp": "pintó",
        "participio_ing": "painted", "participio_esp": "pintado",
        "gerundio_ing": "painting", "gerundio_esp": "pintando",
        "oraciones": {
            "infinitivo":   {"ing": "I paint landscapes on weekends.","esp": "Yo pinto paisajes los fines de semana."},
            "pasadoSimple": {"ing": "You painted the bedroom blue.","esp": "Tú pintaste el cuarto de azul."},
            "participio":   {"ing": "She has painted her nails red.","esp": "Ella se ha pintado las uñas de rojo."},
            "gerundio":     {"ing": "They are painting the mural.","esp": "Ellos están pintando el mural."},
            "futuro":       {"ing": "We will paint the fence tomorrow.","esp": "Nosotros pintaremos la valla mañana."},
            "condicional":  {"ing": "That artist would paint anything.","esp": "Ese artista pintaría cualquier cosa."}
        }
    },
    {
        "ing_inf": "park", "esp_inf": "estacionar",
        "pasado_ing": "parked", "pasado_esp": "estacionó",
        "participio_ing": "parked", "participio_esp": "estacionado",
        "gerundio_ing": "parking", "gerundio_esp": "estacionando",
        "oraciones": {
            "infinitivo":   {"ing": "I park on the street.","esp": "Yo estaciono en la calle."},
            "pasadoSimple": {"ing": "You parked too far away.","esp": "Tú estacionaste demasiado lejos."},
            "participio":   {"ing": "She has parked the car.","esp": "Ella ha estacionado el coche."},
            "gerundio":     {"ing": "They are parking illegally.","esp": "Ellos están estacionando ilegalmente."},
            "futuro":       {"ing": "We will park near the entrance.","esp": "Nosotros estacionaremos cerca de la entrada."},
            "condicional":  {"ing": "That lot would park hundreds.","esp": "Ese estacionamiento albergaría cientos."}
        }
    },
    {
        "ing_inf": "pass", "esp_inf": "pasar",
        "pasado_ing": "passed", "pasado_esp": "pasó",
        "participio_ing": "passed", "participio_esp": "pasado",
        "gerundio_ing": "passing", "gerundio_esp": "pasando",
        "oraciones": {
            "infinitivo":   {"ing": "I pass the bakery on my way home.","esp": "Yo paso por la panadería de camino a casa."},
            "pasadoSimple": {"ing": "You passed the exam easily.","esp": "Tú pasaste el examen fácilmente."},
            "participio":   {"ing": "She has passed the ball to him.","esp": "Ella le ha pasado la pelota a él."},
            "gerundio":     {"ing": "They are passing the salt.","esp": "Ellos están pasando la sal."},
            "futuro":       {"ing": "We will pass through Madrid.","esp": "Nosotros pasaremos por Madrid."},
            "condicional":  {"ing": "That bill would pass quickly.","esp": "Ese proyecto de ley pasaría rápido."}
        }
    },
    {
        "ing_inf": "paste", "esp_inf": "pegar",
        "pasado_ing": "pasted", "pasado_esp": "pegó",
        "participio_ing": "pasted", "participio_esp": "pegado",
        "gerundio_ing": "pasting", "gerundio_esp": "pegando",
        "oraciones": {
            "infinitivo":   {"ing": "I paste screenshots in my notes.","esp": "Yo pego capturas en mis notas."},
            "pasadoSimple": {"ing": "You pasted the wrong text.","esp": "Tú pegaste el texto incorrecto."},
            "participio":   {"ing": "She has pasted the photos in the album.","esp": "Ella ha pegado las fotos en el álbum."},
            "gerundio":     {"ing": "They are pasting posters on the wall.","esp": "Ellos están pegando carteles en la pared."},
            "futuro":       {"ing": "We will paste the labels later.","esp": "Nosotros pegaremos las etiquetas después."},
            "condicional":  {"ing": "That shortcut would paste automatically.","esp": "Ese atajo pegaría automáticamente."}
        }
    },
    {
        "ing_inf": "pat", "esp_inf": "acariciar",
        "pasado_ing": "patted", "pasado_esp": "acarició",
        "participio_ing": "patted", "participio_esp": "acariciado",
        "gerundio_ing": "patting", "gerundio_esp": "acariciando",
        "oraciones": {
            "infinitivo":   {"ing": "I pat my dog on the head.","esp": "Yo acaricio a mi perro en la cabeza."},
            "pasadoSimple": {"ing": "You patted the baby gently.","esp": "Tú acariciaste al bebé con ternura."},
            "participio":   {"ing": "She has patted the cat.","esp": "Ella ha acariciado al gato."},
            "gerundio":     {"ing": "They are patting the horse.","esp": "Ellos están acariciando al caballo."},
            "futuro":       {"ing": "We will pat him on the back.","esp": "Nosotros le daremos una palmada en la espalda."},
            "condicional":  {"ing": "That touch would settle the dust.","esp": "Ese toque asentaría el polvo."}
        }
    },
    {
        "ing_inf": "pause", "esp_inf": "pausar",
        "pasado_ing": "paused", "pasado_esp": "pausó",
        "participio_ing": "paused", "participio_esp": "pausado",
        "gerundio_ing": "pausing", "gerundio_esp": "pausando",
        "oraciones": {
            "infinitivo":   {"ing": "I pause the movie to grab snacks.","esp": "Yo pauso la película para agarrar bocadillos."},
            "pasadoSimple": {"ing": "You paused at the red light.","esp": "Tú pausaste en el semáforo rojo."},
            "participio":   {"ing": "She has paused the music.","esp": "Ella ha pausado la música."},
            "gerundio":     {"ing": "They are pausing for a break.","esp": "Ellos están pausando para un descanso."},
            "futuro":       {"ing": "We will pause the meeting.","esp": "Nosotros pausaremos la reunión."},
            "condicional":  {"ing": "That program would pause automatically.","esp": "Ese programa se pausaría automáticamente."}
        }
    },
    {
        "ing_inf": "perform", "esp_inf": "actuar",
        "pasado_ing": "performed", "pasado_esp": "actuó",
        "participio_ing": "performed", "participio_esp": "actuado",
        "gerundio_ing": "performing", "gerundio_esp": "actuando",
        "oraciones": {
            "infinitivo":   {"ing": "I perform magic tricks at parties.","esp": "Yo hago trucos de magia en las fiestas."},
            "pasadoSimple": {"ing": "You performed well on stage.","esp": "Tú actuaste bien en el escenario."},
            "participio":   {"ing": "She has performed surgery before.","esp": "Ella ha realizado cirugías antes."},
            "gerundio":     {"ing": "They are performing tonight.","esp": "Ellos están actuando esta noche."},
            "futuro":       {"ing": "We will perform better next time.","esp": "Nosotros actuaremos mejor la próxima vez."},
            "condicional":  {"ing": "That band would perform live.","esp": "Esa banda actuaría en vivo."}
        }
    },
    {
        "ing_inf": "permit", "esp_inf": "permitir",
        "pasado_ing": "permitted", "pasado_esp": "permitió",
        "participio_ing": "permitted", "participio_esp": "permitido",
        "gerundio_ing": "permitting", "gerundio_esp": "permitiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I permit my kids to play outside.","esp": "Yo permito que mis hijos jueguen afuera."},
            "pasadoSimple": {"ing": "You permitted late entry.","esp": "Tú permitiste la entrada tarde."},
            "participio":   {"ing": "She has permitted the changes.","esp": "Ella ha permitido los cambios."},
            "gerundio":     {"ing": "They are permitting access now.","esp": "Ellos están permitiendo el acceso ahora."},
            "futuro":       {"ing": "We will permit modifications.","esp": "Nosotros permitiremos modificaciones."},
            "condicional":  {"ing": "That rule would permit exceptions.","esp": "Esa regla permitiría excepciones."}
        }
    },
    {
        "ing_inf": "phone", "esp_inf": "llamar",
        "pasado_ing": "phoned", "pasado_esp": "llamó",
        "participio_ing": "phoned", "participio_esp": "llamado",
        "gerundio_ing": "phoning", "gerundio_esp": "llamando",
        "oraciones": {
            "infinitivo":   {"ing": "I phone my mom every Sunday.","esp": "Yo llamo a mi mamá cada domingo."},
            "pasadoSimple": {"ing": "You phoned me last night.","esp": "Tú me llamaste anoche."},
            "participio":   {"ing": "She has phoned the doctor.","esp": "Ella ha llamado al médico."},
            "gerundio":     {"ing": "They are phoning for a taxi.","esp": "Ellos están llamando un taxi."},
            "futuro":       {"ing": "We will phone you tomorrow.","esp": "Nosotros te llamaremos mañana."},
            "condicional":  {"ing": "That service would phone automatically.","esp": "Ese servicio llamaría automáticamente."}
        }
    },
    {
        "ing_inf": "pick", "esp_inf": "recoger",
        "pasado_ing": "picked", "pasado_esp": "recogió",
        "participio_ing": "picked", "participio_esp": "recogido",
        "gerundio_ing": "picking", "gerundio_esp": "recogiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I pick fresh tomatoes from the garden.","esp": "Yo recojo tomates frescos del jardín."},
            "pasadoSimple": {"ing": "You picked the perfect gift.","esp": "Tú elegiste el regalo perfecto."},
            "participio":   {"ing": "She has picked up the package.","esp": "Ella ha recogido el paquete."},
            "gerundio":     {"ing": "They are picking flowers.","esp": "Ellos están recogiendo flores."},
            "futuro":       {"ing": "We will pick the best option.","esp": "Nosotros elegiremos la mejor opción."},
            "condicional":  {"ing": "That machine would pick automatically.","esp": "Esa máquina seleccionaría automáticamente."}
        }
    },
    {
        "ing_inf": "place", "esp_inf": "colocar",
        "pasado_ing": "placed", "pasado_esp": "colocó",
        "participio_ing": "placed", "participio_esp": "colocado",
        "gerundio_ing": "placing", "gerundio_esp": "colocando",
        "oraciones": {
            "infinitivo":   {"ing": "I place my keys on the hook.","esp": "Yo coloco mis llaves en el gancho."},
            "pasadoSimple": {"ing": "You placed the order yesterday.","esp": "Tú hiciste el pedido ayer."},
            "participio":   {"ing": "She has placed third in the race.","esp": "Ella ha quedado en tercer lugar en la carrera."},
            "gerundio":     {"ing": "They are placing bets online.","esp": "Ellos están haciendo apuestas en línea."},
            "futuro":       {"ing": "We will place the chairs in rows.","esp": "Nosotros colocaremos las sillas en filas."},
            "condicional":  {"ing": "That ad would place automatically.","esp": "Ese anuncio se colocaría automáticamente."}
        }
    },
    {
        "ing_inf": "plan", "esp_inf": "planificar",
        "pasado_ing": "planned", "pasado_esp": "planificó",
        "participio_ing": "planned", "participio_esp": "planificado",
        "gerundio_ing": "planning", "gerundio_esp": "planificando",
        "oraciones": {
            "infinitivo":   {"ing": "I plan my week every Sunday.","esp": "Yo planifico mi semana cada domingo."},
            "pasadoSimple": {"ing": "You planned the trip carefully.","esp": "Tú planificaste el viaje con cuidado."},
            "participio":   {"ing": "She has planned a surprise party.","esp": "Ella ha planificado una fiesta sorpresa."},
            "gerundio":     {"ing": "They are planning their wedding.","esp": "Ellos están planificando su boda."},
            "futuro":       {"ing": "We will plan ahead next time.","esp": "Nosotros planificaremos con anticipación la próxima vez."},
            "condicional":  {"ing": "That strategy would plan everything.","esp": "Esa estrategia lo planificaría todo."}
        }
    },
    {
        "ing_inf": "plant", "esp_inf": "plantar",
        "pasado_ing": "planted", "pasado_esp": "plantó",
        "participio_ing": "planted", "participio_esp": "plantado",
        "gerundio_ing": "planting", "gerundio_esp": "plantando",
        "oraciones": {
            "infinitivo":   {"ing": "I plant vegetables every spring.","esp": "Yo planto verduras cada primavera."},
            "pasadoSimple": {"ing": "You planted roses in the garden.","esp": "Tú plantaste rosas en el jardín."},
            "participio":   {"ing": "She has planted a tree in the yard.","esp": "Ella ha plantado un árbol en el patio."},
            "gerundio":     {"ing": "They are planting seedlings.","esp": "Ellos están plantando plántulas."},
            "futuro":       {"ing": "We will plant herbs next month.","esp": "Nosotros plantaremos hierbas el próximo mes."},
            "condicional":  {"ing": "That tree would plant easily.","esp": "Ese árbol se plantaría fácilmente."}
        }
    },
    {
        "ing_inf": "play", "esp_inf": "jugar",
        "pasado_ing": "played", "pasado_esp": "jugó",
        "participio_ing": "played", "participio_esp": "jugado",
        "gerundio_ing": "playing", "gerundio_esp": "jugando",
        "oraciones": {
            "infinitivo":   {"ing": "I play guitar in my free time.","esp": "Yo toco la guitarra en mi tiempo libre."},
            "pasadoSimple": {"ing": "You played soccer as a kid.","esp": "Tú jugabas fútbol de niño."},
            "participio":   {"ing": "She has played the violin since age five.","esp": "Ella ha tocado el violín desde los cinco años."},
            "gerundio":     {"ing": "They are playing video games.","esp": "Ellos están jugando videojuegos."},
            "futuro":       {"ing": "We will play cards tonight.","esp": "Nosotros jugaremos cartas esta noche."},
            "condicional":  {"ing": "That song would play anywhere.","esp": "Esa canción sonaría en cualquier lugar."}
        }
    },
    {
        "ing_inf": "please", "esp_inf": "complacer",
        "pasado_ing": "pleased", "pasado_esp": "complació",
        "participio_ing": "pleased", "participio_esp": "complacido",
        "gerundio_ing": "pleasing", "gerundio_esp": "complaciendo",
        "oraciones": {
            "infinitivo":   {"ing": "I please my boss with hard work.","esp": "Yo complazco a mi jefe con trabajo duro."},
            "pasadoSimple": {"ing": "You pleased your parents.","esp": "Tú complaciste a tus padres."},
            "participio":   {"ing": "She has pleased the judges.","esp": "Ella ha complacido a los jueces."},
            "gerundio":     {"ing": "They are pleasing the audience.","esp": "Ellos están complaciendo al público."},
            "futuro":       {"ing": "We will please the customers.","esp": "Nosotros complaceremos a los clientes."},
            "condicional":  {"ing": "That gift would please anyone.","esp": "Ese regalo complacería a cualquiera."}
        }
    },
    {
        "ing_inf": "point", "esp_inf": "señalar",
        "pasado_ing": "pointed", "pasado_esp": "señaló",
        "participio_ing": "pointed", "participio_esp": "señalado",
        "gerundio_ing": "pointing", "gerundio_esp": "señalando",
        "oraciones": {
            "infinitivo":   {"ing": "I point out errors when I see them.","esp": "Yo señalo errores cuando los veo."},
            "pasadoSimple": {"ing": "You pointed at the door.","esp": "Tú señalaste la puerta."},
            "participio":   {"ing": "She has pointed the way.","esp": "Ella ha señalado el camino."},
            "gerundio":     {"ing": "They are pointing fingers at each other.","esp": "Ellos se están señalando con el dedo."},
            "futuro":       {"ing": "We will point the telescope north.","esp": "Nosotros apuntaremos el telescopio al norte."},
            "condicional":  {"ing": "That arrow would point the way.","esp": "Esa flecha señalaría el camino."}
        }
    },
    {
        "ing_inf": "polish", "esp_inf": "pulir",
        "pasado_ing": "polished", "pasado_esp": "pulió",
        "participio_ing": "polished", "participio_esp": "pulido",
        "gerundio_ing": "polishing", "gerundio_esp": "puliendo",
        "oraciones": {
            "infinitivo":   {"ing": "I polish my shoes before work.","esp": "Yo pulo mis zapatos antes del trabajo."},
            "pasadoSimple": {"ing": "You polished the silver yesterday.","esp": "Tú puliste la plata ayer."},
            "participio":   {"ing": "She has polished her presentation.","esp": "Ella ha pulido su presentación."},
            "gerundio":     {"ing": "They are polishing the marble floor.","esp": "Ellos están puliendo el piso de mármol."},
            "futuro":       {"ing": "We will polish the wood tomorrow.","esp": "Nosotros puliremos la madera mañana."},
            "condicional":  {"ing": "That wax would polish perfectly.","esp": "Esa cera puliría perfectamente."}
        }
    },
    {
        "ing_inf": "pop", "esp_inf": "reventar",
        "pasado_ing": "popped", "pasado_esp": "reventó",
        "participio_ing": "popped", "participio_esp": "reventado",
        "gerundio_ing": "popping", "gerundio_esp": "reventando",
        "oraciones": {
            "infinitivo":   {"ing": "I pop popcorn for movie night.","esp": "Yo reviento palomitas para la noche de cine."},
            "pasadoSimple": {"ing": "You popped the balloon by accident.","esp": "Tú reventaste el globo por accidente."},
            "participio":   {"ing": "She has popped a balloon.","esp": "Ella ha reventado un globo."},
            "gerundio":     {"ing": "They are popping champagne.","esp": "Ellos están descorchando champán."},
            "futuro":       {"ing": "We will pop the question soon.","esp": "Nosotros haremos la pregunta pronto."},
            "condicional":  {"ing": "That bubble would pop easily.","esp": "Esa burbuja reventaría fácilmente."}
        }
    },
    {
        "ing_inf": "possess", "esp_inf": "poseer",
        "pasado_ing": "possessed", "pasado_esp": "poseyó",
        "participio_ing": "possessed", "participio_esp": "poseído",
        "gerundio_ing": "possessing", "gerundio_esp": "poseyendo",
        "oraciones": {
            "infinitivo":   {"ing": "I possess great patience.","esp": "Yo poseo gran paciencia."},
            "pasadoSimple": {"ing": "You possessed the rare coin.","esp": "Tú poseías la moneda rara."},
            "participio":   {"ing": "She has possessed that talent since birth.","esp": "Ella ha poseído ese talento desde el nacimiento."},
            "gerundio":     {"ing": "They are possessing too much power.","esp": "Ellos están poseyendo demasiado poder."},
            "futuro":       {"ing": "We will possess the truth eventually.","esp": "Nosotros poseeremos la verdad eventualmente."},
            "condicional":  {"ing": "That document would possess legal value.","esp": "Ese documento poseería valor legal."}
        }
    },
    {
        "ing_inf": "post", "esp_inf": "publicar",
        "pasado_ing": "posted", "pasado_esp": "publicó",
        "participio_ing": "posted", "participio_esp": "publicado",
        "gerundio_ing": "posting", "gerundio_esp": "publicando",
        "oraciones": {
            "infinitivo":   {"ing": "I post photos on Instagram daily.","esp": "Yo publico fotos en Instagram a diario."},
            "pasadoSimple": {"ing": "You posted the letter yesterday.","esp": "Tú enviaste la carta ayer."},
            "participio":   {"ing": "She has posted a new video.","esp": "Ella ha publicado un video nuevo."},
            "gerundio":     {"ing": "They are posting updates online.","esp": "Ellos están publicando actualizaciones en línea."},
            "futuro":       {"ing": "We will post the results tomorrow.","esp": "Nosotros publicaremos los resultados mañana."},
            "condicional":  {"ing": "That job would post automatically.","esp": "Ese trabajo se publicaría automáticamente."}
        }
    },
    {
        "ing_inf": "pour", "esp_inf": "verter",
        "pasado_ing": "poured", "pasado_esp": "vertió",
        "participio_ing": "poured", "participio_esp": "vertido",
        "gerundio_ing": "pouring", "gerundio_esp": "vertiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I pour coffee for my family each morning.","esp": "Yo sirvo café para mi familia cada mañana."},
            "pasadoSimple": {"ing": "You poured water on the plants.","esp": "Tú vertiste agua sobre las plantas."},
            "participio":   {"ing": "She has poured her heart into it.","esp": "Ella ha puesto su corazón en ello."},
            "gerundio":     {"ing": "They are pouring concrete.","esp": "Ellos están vertiendo concreto."},
            "futuro":       {"ing": "We will pour the foundation tomorrow.","esp": "Nosotros verteremos los cimientos mañana."},
            "condicional":  {"ing": "That faucet would pour constantly.","esp": "Ese grifo gotearía constantemente."}
        }
    },
    {
        "ing_inf": "practice", "esp_inf": "practicar",
        "pasado_ing": "practiced", "pasado_esp": "practicó",
        "participio_ing": "practiced", "participio_esp": "practicado",
        "gerundio_ing": "practicing", "gerundio_esp": "practicando",
        "oraciones": {
            "infinitivo":   {"ing": "I practice the piano every day.","esp": "Yo practico el piano cada día."},
            "pasadoSimple": {"ing": "You practiced the speech for hours.","esp": "Tú practicaste el discurso por horas."},
            "participio":   {"ing": "She has practiced law for ten years.","esp": "Ella ha practicado derecho durante diez años."},
            "gerundio":     {"ing": "They are practicing for the game.","esp": "Ellos están practicando para el partido."},
            "futuro":       {"ing": "We will practice more next week.","esp": "Nosotros practicaremos más la próxima semana."},
            "condicional":  {"ing": "That routine would make perfect practice.","esp": "Esa rutina haría que la práctica fuera perfecta."}
        }
    },
    {
        "ing_inf": "praise", "esp_inf": "alabar",
        "pasado_ing": "praised", "pasado_esp": "alabó",
        "participio_ing": "praised", "participio_esp": "alabado",
        "gerundio_ing": "praising", "gerundio_esp": "alabando",
        "oraciones": {
            "infinitivo":   {"ing": "I praise good work when I see it.","esp": "Yo alabo el buen trabajo cuando lo veo."},
            "pasadoSimple": {"ing": "You praised the chef personally.","esp": "Tú alabaste al chef personalmente."},
            "participio":   {"ing": "She has praised the team publicly.","esp": "Ella ha alabado al equipo públicamente."},
            "gerundio":     {"ing": "They are praising the new policy.","esp": "Ellos están alabando la nueva política."},
            "futuro":       {"ing": "We will praise the volunteers.","esp": "Nosotros alabaremos a los voluntarios."},
            "condicional":  {"ing": "That review would praise the author.","esp": "Esa reseña alabaría al autor."}
        }
    },
    {
        "ing_inf": "pray", "esp_inf": "rezar",
        "pasado_ing": "prayed", "pasado_esp": "rezó",
        "participio_ing": "prayed", "participio_esp": "rezado",
        "gerundio_ing": "praying", "gerundio_esp": "rezando",
        "oraciones": {
            "infinitivo":   {"ing": "I pray every night before bed.","esp": "Yo rezo cada noche antes de dormir."},
            "pasadoSimple": {"ing": "You prayed for her recovery.","esp": "Tú rezaste por su recuperación."},
            "participio":   {"ing": "She has prayed daily for years.","esp": "Ella ha rezado a diario durante años."},
            "gerundio":     {"ing": "They are praying in the temple.","esp": "Ellos están rezando en el templo."},
            "futuro":       {"ing": "We will pray for peace.","esp": "Nosotros rezaremos por la paz."},
            "condicional":  {"ing": "That gesture would comfort anyone who prays.","esp": "Ese gesto consolaría a cualquiera que rece."}
        }
    },
    {
        "ing_inf": "preach", "esp_inf": "predicar",
        "pasado_ing": "preached", "pasado_esp": "predicó",
        "participio_ing": "preached", "participio_esp": "predicado",
        "gerundio_ing": "preaching", "gerundio_esp": "predicando",
        "oraciones": {
            "infinitivo":   {"ing": "I preach kindness to my kids.","esp": "Yo predico la amabilidad a mis hijos."},
            "pasadoSimple": {"ing": "You preached the sermon yesterday.","esp": "Tú predicaste el sermón ayer."},
            "participio":   {"ing": "She has preached about forgiveness.","esp": "Ella ha predicado sobre el perdón."},
            "gerundio":     {"ing": "They are preaching in the streets.","esp": "Ellos están predicando en las calles."},
            "futuro":       {"ing": "We will preach the gospel tomorrow.","esp": "Nosotros predicaremos el evangelio mañana."},
            "condicional":  {"ing": "That message would preach to many.","esp": "Ese mensaje predicaría a muchos."}
        }
    },
    {
        "ing_inf": "prefer", "esp_inf": "preferir",
        "pasado_ing": "preferred", "pasado_esp": "prefirió",
        "participio_ing": "preferred", "participio_esp": "preferido",
        "gerundio_ing": "preferring", "gerundio_esp": "prefiriendo",
        "oraciones": {
            "infinitivo":   {"ing": "I prefer tea over coffee.","esp": "Yo prefiero el té sobre el café."},
            "pasadoSimple": {"ing": "You preferred the red one.","esp": "Tú preferiste el rojo."},
            "participio":   {"ing": "She has preferred silence lately.","esp": "Ella ha preferido el silencio últimamente."},
            "gerundio":     {"ing": "They are preferring takeout tonight.","esp": "Ellos están prefiriendo comida para llevar esta noche."},
            "futuro":       {"ing": "We will prefer walking.","esp": "Nosotros preferiremos caminar."},
            "condicional":  {"ing": "That option would be preferred by everyone.","esp": "Esa opción sería preferida por todos."}
        }
    }
]


BLOQUE_17 = [
    {
        "ing_inf": "prepare", "esp_inf": "preparar",
        "pasado_ing": "prepared", "pasado_esp": "preparó",
        "participio_ing": "prepared", "participio_esp": "preparado",
        "gerundio_ing": "preparing", "gerundio_esp": "preparando",
        "oraciones": {
            "infinitivo":   {"ing": "I prepare breakfast every morning.","esp": "Yo preparo el desayuno cada mañana."},
            "pasadoSimple": {"ing": "You prepared the meal well.","esp": "Tú preparaste la comida bien."},
            "participio":   {"ing": "She has prepared the presentation.","esp": "Ella ha preparado la presentación."},
            "gerundio":     {"ing": "They are preparing for the trip.","esp": "Ellos se están preparando para el viaje."},
            "futuro":       {"ing": "We will prepare the materials.","esp": "Nosotros prepararemos los materiales."},
            "condicional":  {"ing": "That recipe would prepare quickly.","esp": "Esa receta se prepararía rápido."}
        }
    },
    {
        "ing_inf": "present", "esp_inf": "presentar",
        "pasado_ing": "presented", "pasado_esp": "presentó",
        "participio_ing": "presented", "participio_esp": "presentado",
        "gerundio_ing": "presenting", "gerundio_esp": "presentando",
        "oraciones": {
            "infinitivo":   {"ing": "I present ideas clearly at meetings.","esp": "Yo presento ideas con claridad en las reuniones."},
            "pasadoSimple": {"ing": "You presented the proposal yesterday.","esp": "Tú presentaste la propuesta ayer."},
            "participio":   {"ing": "She has presented the research.","esp": "Ella ha presentado la investigación."},
            "gerundio":     {"ing": "They are presenting the awards tonight.","esp": "Ellos están presentando los premios esta noche."},
            "futuro":       {"ing": "We will present our findings tomorrow.","esp": "Nosotros presentaremos nuestros hallazgos mañana."},
            "condicional":  {"ing": "That opportunity would present itself.","esp": "Esa oportunidad se presentaría sola."}
        }
    },
    {
        "ing_inf": "press", "esp_inf": "presionar",
        "pasado_ing": "pressed", "pasado_esp": "presionó",
        "participio_ing": "pressed", "participio_esp": "presionado",
        "gerundio_ing": "pressing", "gerundio_esp": "presionando",
        "oraciones": {
            "infinitivo":   {"ing": "I press the button to start.","esp": "Yo presiono el botón para empezar."},
            "pasadoSimple": {"ing": "You pressed the shirt yesterday.","esp": "Tú planchaste la camisa ayer."},
            "participio":   {"ing": "She has pressed the issue hard.","esp": "Ella ha presionado mucho sobre el asunto."},
            "gerundio":     {"ing": "They are pressing for answers.","esp": "Ellos están presionando para obtener respuestas."},
            "futuro":       {"ing": "We will press the grapes tomorrow.","esp": "Nosotros prensaremos las uvas mañana."},
            "condicional":  {"ing": "That pedal would press easily.","esp": "Ese pedal se presionaría fácilmente."}
        }
    },
    {
        "ing_inf": "pretend", "esp_inf": "fingir",
        "pasado_ing": "pretended", "pasado_esp": "fingió",
        "participio_ing": "pretended", "participio_esp": "fingido",
        "gerundio_ing": "pretending", "gerundio_esp": "fingiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I pretend to understand sometimes.","esp": "Yo finjo entender a veces."},
            "pasadoSimple": {"ing": "You pretended to be sick.","esp": "Tú fingiste estar enfermo."},
            "participio":   {"ing": "She has pretended not to see.","esp": "Ella ha fingido no ver."},
            "gerundio":     {"ing": "They are pretending to work.","esp": "Ellos están fingiendo trabajar."},
            "futuro":       {"ing": "We will pretend nothing happened.","esp": "Nosotros fingiremos que no pasó nada."},
            "condicional":  {"ing": "That smile would pretend happiness.","esp": "Esa sonrisa fingiría felicidad."}
        }
    },
    {
        "ing_inf": "prevent", "esp_inf": "prevenir",
        "pasado_ing": "prevented", "pasado_esp": "previno",
        "participio_ing": "prevented", "participio_esp": "prevenido",
        "gerundio_ing": "preventing", "gerundio_esp": "previniendo",
        "oraciones": {
            "infinitivo":   {"ing": "I prevent problems by planning ahead.","esp": "Yo prevengo problemas planificando con tiempo."},
            "pasadoSimple": {"ing": "You prevented the disaster.","esp": "Tú preveniste el desastre."},
            "participio":   {"ing": "She has prevented the spread.","esp": "Ella ha prevenido la propagación."},
            "gerundio":     {"ing": "They are preventing access.","esp": "Ellos están previniendo el acceso."},
            "futuro":       {"ing": "We will prevent the failure.","esp": "Nosotros preveniremos el fallo."},
            "condicional":  {"ing": "That measure would prevent damage.","esp": "Esa medida prevendría daños."}
        }
    },
    {
        "ing_inf": "print", "esp_inf": "imprimir",
        "pasado_ing": "printed", "pasado_esp": "imprimió",
        "participio_ing": "printed", "participio_esp": "impreso",
        "gerundio_ing": "printing", "gerundio_esp": "imprimiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I print documents at the office.","esp": "Yo imprimo documentos en la oficina."},
            "pasadoSimple": {"ing": "You printed the photos yesterday.","esp": "Tú imprimiste las fotos ayer."},
            "participio":   {"ing": "She has printed the report.","esp": "Ella ha impreso el informe."},
            "gerundio":     {"ing": "They are printing the invitations.","esp": "Ellos están imprimiendo las invitaciones."},
            "futuro":       {"ing": "We will print the tickets soon.","esp": "Nosotros imprimiremos los boletos pronto."},
            "condicional":  {"ing": "That printer would print faster.","esp": "Esa impresora imprimiría más rápido."}
        }
    },
    {
        "ing_inf": "produce", "esp_inf": "producir",
        "pasado_ing": "produced", "pasado_esp": "produjo",
        "participio_ing": "produced", "participio_esp": "producido",
        "gerundio_ing": "producing", "gerundio_esp": "produciendo",
        "oraciones": {
            "infinitivo":   {"ing": "I produce videos for my channel.","esp": "Yo produzco videos para mi canal."},
            "pasadoSimple": {"ing": "You produced a great show.","esp": "Tú produjiste un gran espectáculo."},
            "participio":   {"ing": "She has produced three albums.","esp": "Ella ha producido tres álbumes."},
            "gerundio":     {"ing": "They are producing electric cars.","esp": "Ellos están produciendo coches eléctricos."},
            "futuro":       {"ing": "We will produce more next year.","esp": "Nosotros produciremos más el próximo año."},
            "condicional":  {"ing": "That factory would produce millions.","esp": "Esa fábrica produciría millones."}
        }
    },
    {
        "ing_inf": "program", "esp_inf": "programar",
        "pasado_ing": "programmed", "pasado_esp": "programó",
        "participio_ing": "programmed", "participio_esp": "programado",
        "gerundio_ing": "programming", "gerundio_esp": "programando",
        "oraciones": {
            "infinitivo":   {"ing": "I program in Python at work.","esp": "Yo programo en Python en el trabajo."},
            "pasadoSimple": {"ing": "You programmed the robot well.","esp": "Tú programaste el robot bien."},
            "participio":   {"ing": "She has programmed the app.","esp": "Ella ha programado la aplicación."},
            "gerundio":     {"ing": "They are programming the new feature.","esp": "Ellos están programando la nueva función."},
            "futuro":       {"ing": "We will program the schedule tomorrow.","esp": "Nosotros programaremos el horario mañana."},
            "condicional":  {"ing": "That tool would program automatically.","esp": "Esa herramienta programaría automáticamente."}
        }
    },
    {
        "ing_inf": "promise", "esp_inf": "prometer",
        "pasado_ing": "promised", "pasado_esp": "prometió",
        "participio_ing": "promised", "participio_esp": "prometido",
        "gerundio_ing": "promising", "gerundio_esp": "prometiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I promise to call you back.","esp": "Yo prometo llamarte de vuelta."},
            "pasadoSimple": {"ing": "You promised to be there.","esp": "Tú prometiste estar allí."},
            "participio":   {"ing": "She has promised to help.","esp": "Ella ha prometido ayudar."},
            "gerundio":     {"ing": "They are promising reforms.","esp": "Ellos están prometiendo reformas."},
            "futuro":       {"ing": "We will promise nothing more.","esp": "Nosotros no prometeremos nada más."},
            "condicional":  {"ing": "That candidate would promise anything.","esp": "Ese candidato prometería cualquier cosa."}
        }
    },
    {
        "ing_inf": "protect", "esp_inf": "proteger",
        "pasado_ing": "protected", "pasado_esp": "protegió",
        "participio_ing": "protected", "participio_esp": "protegido",
        "gerundio_ing": "protecting", "gerundio_esp": "protegiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I protect my family above all.","esp": "Yo protejo a mi familia sobre todo."},
            "pasadoSimple": {"ing": "You protected the data well.","esp": "Tú protegiste los datos bien."},
            "participio":   {"ing": "She has protected the children.","esp": "Ella ha protegido a los niños."},
            "gerundio":     {"ing": "They are protecting the environment.","esp": "Ellos están protegiendo el medio ambiente."},
            "futuro":       {"ing": "We will protect our rights.","esp": "Nosotros protegeremos nuestros derechos."},
            "condicional":  {"ing": "That vaccine would protect everyone.","esp": "Esa vacuna protegería a todos."}
        }
    },
    {
        "ing_inf": "provide", "esp_inf": "proporcionar",
        "pasado_ing": "provided", "pasado_esp": "proporcionó",
        "participio_ing": "provided", "participio_esp": "proporcionado",
        "gerundio_ing": "providing", "gerundio_esp": "proporcionando",
        "oraciones": {
            "infinitivo":   {"ing": "I provide support to my team.","esp": "Yo proporciono apoyo a mi equipo."},
            "pasadoSimple": {"ing": "You provided excellent service.","esp": "Tú proporcionaste un servicio excelente."},
            "participio":   {"ing": "She has provided the documents.","esp": "Ella ha proporcionado los documentos."},
            "gerundio":     {"ing": "They are providing aid.","esp": "Ellos están proporcionando ayuda."},
            "futuro":       {"ing": "We will provide more details.","esp": "Nosotros proporcionaremos más detalles."},
            "condicional":  {"ing": "That service would provide value.","esp": "Ese servicio proporcionaría valor."}
        }
    },
    {
        "ing_inf": "pull", "esp_inf": "jalar",
        "pasado_ing": "pulled", "pasado_esp": "jaló",
        "participio_ing": "pulled", "participio_esp": "jalado",
        "gerundio_ing": "pulling", "gerundio_esp": "jalando",
        "oraciones": {
            "infinitivo":   {"ing": "I pull the door to open it.","esp": "Yo jalo la puerta para abrirla."},
            "pasadoSimple": {"ing": "You pulled the trigger.","esp": "Tú jalaste el gatillo."},
            "participio":   {"ing": "She has pulled the rope.","esp": "Ella ha jalado la cuerda."},
            "gerundio":     {"ing": "They are pulling weeds.","esp": "Ellos están arrancando maleza."},
            "futuro":       {"ing": "We will pull together.","esp": "Nosotros uniremos fuerzas."},
            "condicional":  {"ing": "That cart would pull easily.","esp": "Ese carro se jalaría fácilmente."}
        }
    },
    {
        "ing_inf": "pump", "esp_inf": "bombear",
        "pasado_ing": "pumped", "pasado_esp": "bombeó",
        "participio_ing": "pumped", "participio_esp": "bombeado",
        "gerundio_ing": "pumping", "gerundio_esp": "bombeando",
        "oraciones": {
            "infinitivo":   {"ing": "I pump gas at the station.","esp": "Yo bombo gasolina en la estación."},
            "pasadoSimple": {"ing": "You pumped up the tires.","esp": "Tú inflaste las llantas."},
            "participio":   {"ing": "She has pumped the water out.","esp": "Ella ha bombeado el agua."},
            "gerundio":     {"ing": "They are pumping oil.","esp": "Ellos están bombeando petróleo."},
            "futuro":       {"ing": "We will pump the brakes gently.","esp": "Nosotros bombearemos los frenos suavemente."},
            "condicional":  {"ing": "That heart would pump strongly.","esp": "Ese corazón bombearía con fuerza."}
        }
    },
    {
        "ing_inf": "punch", "esp_inf": "golpear",
        "pasado_ing": "punched", "pasado_esp": "golpeó",
        "participio_ing": "punched", "participio_esp": "golpeado",
        "gerundio_ing": "punching", "gerundio_esp": "golpeando",
        "oraciones": {
            "infinitivo":   {"ing": "I punch the time clock daily.","esp": "Yo marco el reloj diariamente."},
            "pasadoSimple": {"ing": "You punched him in the face.","esp": "Tú le pegaste en la cara."},
            "participio":   {"ing": "She has punched the ticket.","esp": "Ella ha perforado el boleto."},
            "gerundio":     {"ing": "They are punching numbers.","esp": "Ellos están marcando números."},
            "futuro":       {"ing": "We will punch the cards later.","esp": "Nosotros perforaremos las tarjetas después."},
            "condicional":  {"ing": "That boxer would punch hard.","esp": "Ese boxeador golpearía con fuerza."}
        }
    },
    {
        "ing_inf": "puncture", "esp_inf": "pinchar",
        "pasado_ing": "punctured", "pasado_esp": "pinchó",
        "participio_ing": "punctured", "participio_esp": "pinchado",
        "gerundio_ing": "puncturing", "gerundio_esp": "pinchando",
        "oraciones": {
            "infinitivo":   {"ing": "I puncture the balloon by accident.","esp": "Yo pincho el globo por accidente."},
            "pasadoSimple": {"ing": "You punctured the tire.","esp": "Tú pinchaste la llanta."},
            "participio":   {"ing": "She has punctured the skin.","esp": "Ella ha pinchado la piel."},
            "gerundio":     {"ing": "They are puncturing the cyst.","esp": "Ellos están pinchando el quiste."},
            "futuro":       {"ing": "We will puncture the balloon later.","esp": "Nosotros pincharemos el globo después."},
            "condicional":  {"ing": "That nail would puncture easily.","esp": "Ese clavo pincharía fácilmente."}
        }
    },
    {
        "ing_inf": "punish", "esp_inf": "castigar",
        "pasado_ing": "punished", "pasado_esp": "castigó",
        "participio_ing": "punished", "participio_esp": "castigado",
        "gerundio_ing": "punishing", "gerundio_esp": "castigando",
        "oraciones": {
            "infinitivo":   {"ing": "I punish bad behavior in my class.","esp": "Yo castigo el mal comportamiento en mi clase."},
            "pasadoSimple": {"ing": "You punished the child.","esp": "Tú castigaste al niño."},
            "participio":   {"ing": "She has punished the offender.","esp": "Ella ha castigado al infractor."},
            "gerundio":     {"ing": "They are punishing the criminal.","esp": "Ellos están castigando al criminal."},
            "futuro":       {"ing": "We will punish cheating.","esp": "Nosotros castigaremos la trampa."},
            "condicional":  {"ing": "That law would punish fraud.","esp": "Esa ley castigaría el fraude."}
        }
    },
    {
        "ing_inf": "push", "esp_inf": "empujar",
        "pasado_ing": "pushed", "pasado_esp": "empujó",
        "participio_ing": "pushed", "participio_esp": "empujado",
        "gerundio_ing": "pushing", "gerundio_esp": "empujando",
        "oraciones": {
            "infinitivo":   {"ing": "I push myself to the limit.","esp": "Yo me esfuerzo al límite."},
            "pasadoSimple": {"ing": "You pushed the door open.","esp": "Tú empujaste la puerta para abrirla."},
            "participio":   {"ing": "She has pushed the cart.","esp": "Ella ha empujado el carrito."},
            "gerundio":     {"ing": "They are pushing for change.","esp": "Ellos están presionando para el cambio."},
            "futuro":       {"ing": "We will push forward.","esp": "Nosotros avanzaremos con fuerza."},
            "condicional":  {"ing": "That button would push easily.","esp": "Ese botón se empujaría fácilmente."}
        }
    },
    {
        "ing_inf": "question", "esp_inf": "cuestionar",
        "pasado_ing": "questioned", "pasado_esp": "cuestionó",
        "participio_ing": "questioned", "participio_esp": "cuestionado",
        "gerundio_ing": "questioning", "gerundio_esp": "cuestionando",
        "oraciones": {
            "infinitivo":   {"ing": "I question everything I read.","esp": "Yo cuestiono todo lo que leo."},
            "pasadoSimple": {"ing": "You questioned the witness.","esp": "Tú cuestionaste al testigo."},
            "participio":   {"ing": "She has questioned the decision.","esp": "Ella ha cuestionado la decisión."},
            "gerundio":     {"ing": "They are questioning the motives.","esp": "Ellos están cuestionando los motivos."},
            "futuro":       {"ing": "We will question the suspect.","esp": "Nosotros cuestionaremos al sospechoso."},
            "condicional":  {"ing": "That evidence would question the theory.","esp": "Esa evidencia cuestionaría la teoría."}
        }
    },
    {
        "ing_inf": "queue", "esp_inf": "hacer cola",
        "pasado_ing": "queued", "pasado_esp": "hizo cola",
        "participio_ing": "queued", "participio_esp": "hecho cola",
        "gerundio_ing": "queuing", "gerundio_esp": "haciendo cola",
        "futuro_esp": "hará cola", "cond_esp": "haría cola",
        "oraciones": {
            "infinitivo":   {"ing": "I queue up at the coffee shop.","esp": "Yo hago cola en la cafetería."},
            "pasadoSimple": {"ing": "You queued patiently.","esp": "Tú hiciste cola pacientemente."},
            "participio":   {"ing": "She has queued for hours.","esp": "Ella ha hecho cola por horas."},
            "gerundio":     {"ing": "They are queuing outside.","esp": "Ellos están haciendo cola afuera."},
            "futuro":       {"ing": "We will queue up early.","esp": "Nosotros haremos cola temprano."},
            "condicional":  {"ing": "That line would queue forever.","esp": "Esa fila haría cola para siempre."}
        }
    },
    {
        "ing_inf": "race", "esp_inf": "correr",
        "pasado_ing": "raced", "pasado_esp": "corrió",
        "participio_ing": "raced", "participio_esp": "corrido",
        "gerundio_ing": "racing", "gerundio_esp": "corriendo",
        "oraciones": {
            "infinitivo":   {"ing": "I race against the clock.","esp": "Yo compito contra el reloj."},
            "pasadoSimple": {"ing": "You raced your friend.","esp": "Tú corriste contra tu amigo."},
            "participio":   {"ing": "She has raced in marathons.","esp": "Ella ha corrido en maratones."},
            "gerundio":     {"ing": "They are racing for the prize.","esp": "Ellos están compitiendo por el premio."},
            "futuro":       {"ing": "We will race next Sunday.","esp": "Nosotros correremos el próximo domingo."},
            "condicional":  {"ing": "That car would race faster.","esp": "Ese coche correría más rápido."}
        }
    },
    {
        "ing_inf": "rain", "esp_inf": "llover",
        "pasado_ing": "rained", "pasado_esp": "llovió",
        "participio_ing": "rained", "participio_esp": "llovido",
        "gerundio_ing": "raining", "gerundio_esp": "lloviendo",
        "oraciones": {
            "infinitivo":   {"ing": "I hope it rains today.","esp": "Yo espero que llueva hoy."},
            "pasadoSimple": {"ing": "It rained heavily yesterday.","esp": "Llovió mucho ayer."},
            "participio":   {"ing": "It has rained all week.","esp": "Ha llovido toda la semana."},
            "gerundio":     {"ing": "It's raining right now.","esp": "Está lloviendo ahora mismo."},
            "futuro":       {"ing": "It will rain tomorrow.","esp": "Lloverá mañana."},
            "condicional":  {"ing": "It would rain if it could.","esp": "Llovería si pudiera."}
        }
    },
    {
        "ing_inf": "raise", "esp_inf": "levantar",
        "pasado_ing": "raised", "pasado_esp": "levantó",
        "participio_ing": "raised", "participio_esp": "levantado",
        "gerundio_ing": "raising", "gerundio_esp": "levantando",
        "oraciones": {
            "infinitivo":   {"ing": "I raise my hand in class.","esp": "Yo levanto la mano en clase."},
            "pasadoSimple": {"ing": "You raised the flag this morning.","esp": "Tú levantaste la bandera esta mañana."},
            "participio":   {"ing": "She has raised three children.","esp": "Ella ha criado a tres niños."},
            "gerundio":     {"ing": "They are raising prices again.","esp": "Ellos están subiendo los precios otra vez."},
            "futuro":       {"ing": "We will raise funds for charity.","esp": "Nosotros recaudaremos fondos para caridad."},
            "condicional":  {"ing": "That salary would raise morale.","esp": "Ese salario levantaría la moral."}
        }
    },
    {
        "ing_inf": "reach", "esp_inf": "alcanzar",
        "pasado_ing": "reached", "pasado_esp": "alcanzó",
        "participio_ing": "reached", "participio_esp": "alcanzado",
        "gerundio_ing": "reaching", "gerundio_esp": "alcanzando",
        "oraciones": {
            "infinitivo":   {"ing": "I reach the office by nine.","esp": "Yo llego a la oficina a las nueve."},
            "pasadoSimple": {"ing": "You reached the summit yesterday.","esp": "Tú alcanzaste la cima ayer."},
            "participio":   {"ing": "She has reached her goal.","esp": "Ella ha alcanzado su meta."},
            "gerundio":     {"ing": "They are reaching for the stars.","esp": "Ellos están intentando llegar a las estrellas."},
            "futuro":       {"ing": "We will reach out tomorrow.","esp": "Nosotros nos pondremos en contacto mañana."},
            "condicional":  {"ing": "That message would reach millions.","esp": "Ese mensaje alcanzaría a millones."}
        }
    },
    {
        "ing_inf": "realize", "esp_inf": "darse cuenta",
        "pasado_ing": "realized", "pasado_esp": "se dio cuenta",
        "participio_ing": "realized", "participio_esp": "dado cuenta",
        "gerundio_ing": "realizing", "gerundio_esp": "dándose cuenta",
        "futuro_esp": "se dará cuenta", "cond_esp": "se daría cuenta",
        "oraciones": {
            "infinitivo":   {"ing": "I realize my mistakes eventually.","esp": "Yo me doy cuenta de mis errores eventualmente."},
            "pasadoSimple": {"ing": "You realized it was too late.","esp": "Tú te diste cuenta de que era tarde."},
            "participio":   {"ing": "She has realized her dream.","esp": "Ella se ha dado cuenta de su sueño."},
            "gerundio":     {"ing": "They are realizing the truth.","esp": "Ellos se están dando cuenta de la verdad."},
            "futuro":       {"ing": "We will realize our potential.","esp": "Nosotros nos daremos cuenta de nuestro potencial."},
            "condicional":  {"ing": "That would realize the error.","esp": "Eso se daría cuenta del error."}
        }
    },
    {
        "ing_inf": "receive", "esp_inf": "recibir",
        "pasado_ing": "received", "pasado_esp": "recibió",
        "participio_ing": "received", "participio_esp": "recibido",
        "gerundio_ing": "receiving", "gerundio_esp": "recibiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I receive emails every day.","esp": "Yo recibo correos cada día."},
            "pasadoSimple": {"ing": "You received the package.","esp": "Tú recibiste el paquete."},
            "participio":   {"ing": "She has received an award.","esp": "Ella ha recibido un premio."},
            "gerundio":     {"ing": "They are receiving donations.","esp": "Ellos están recibiendo donaciones."},
            "futuro":       {"ing": "We will receive the guests.","esp": "Nosotros recibiremos a los invitados."},
            "condicional":  {"ing": "That offer would receive attention.","esp": "Esa oferta recibiría atención."}
        }
    },
    {
        "ing_inf": "recognize", "esp_inf": "reconocer",
        "pasado_ing": "recognized", "pasado_esp": "reconoció",
        "participio_ing": "recognized", "participio_esp": "reconocido",
        "gerundio_ing": "recognizing", "gerundio_esp": "reconociendo",
        "oraciones": {
            "infinitivo":   {"ing": "I recognize your voice anywhere.","esp": "Yo reconozco tu voz en cualquier lugar."},
            "pasadoSimple": {"ing": "You recognized the place immediately.","esp": "Tú reconociste el lugar de inmediato."},
            "participio":   {"ing": "She has recognized his talent.","esp": "Ella ha reconocido su talento."},
            "gerundio":     {"ing": "They are recognizing the issue.","esp": "Ellos están reconociendo el problema."},
            "futuro":       {"ing": "We will recognize the winners.","esp": "Nosotros reconoceremos a los ganadores."},
            "condicional":  {"ing": "That face would be recognized by anyone.","esp": "Esa cara la reconocería cualquiera."}
        }
    },
    {
        "ing_inf": "record", "esp_inf": "grabar",
        "pasado_ing": "recorded", "pasado_esp": "grabó",
        "participio_ing": "recorded", "participio_esp": "grabado",
        "gerundio_ing": "recording", "gerundio_esp": "grabando",
        "oraciones": {
            "infinitivo":   {"ing": "I record podcasts on weekends.","esp": "Yo grabo podcasts los fines de semana."},
            "pasadoSimple": {"ing": "You recorded the song yesterday.","esp": "Tú grabaste la canción ayer."},
            "participio":   {"ing": "She has recorded a new album.","esp": "Ella ha grabado un álbum nuevo."},
            "gerundio":     {"ing": "They are recording the interview.","esp": "Ellos están grabando la entrevista."},
            "futuro":       {"ing": "We will record the show tonight.","esp": "Nosotros grabaremos el show esta noche."},
            "condicional":  {"ing": "That microphone would record clearly.","esp": "Ese micrófono grabaría con claridad."}
        }
    },
    {
        "ing_inf": "reduce", "esp_inf": "reducir",
        "pasado_ing": "reduced", "pasado_esp": "redujo",
        "participio_ing": "reduced", "participio_esp": "reducido",
        "gerundio_ing": "reducing", "gerundio_esp": "reduciendo",
        "oraciones": {
            "infinitivo":   {"ing": "I reduce stress by meditating.","esp": "Yo reduzco el estrés meditando."},
            "pasadoSimple": {"ing": "You reduced the price.","esp": "Tú redujiste el precio."},
            "participio":   {"ing": "She has reduced waste significantly.","esp": "Ella ha reducido los residuos significativamente."},
            "gerundio":     {"ing": "They are reducing staff.","esp": "Ellos están reduciendo personal."},
            "futuro":       {"ing": "We will reduce emissions.","esp": "Nosotros reduciremos las emisiones."},
            "condicional":  {"ing": "That measure would reduce costs.","esp": "Esa medida reduciría costos."}
        }
    },
    {
        "ing_inf": "reflect", "esp_inf": "reflejar",
        "pasado_ing": "reflected", "pasado_esp": "reflejó",
        "participio_ing": "reflected", "participio_esp": "reflejado",
        "gerundio_ing": "reflecting", "gerundio_esp": "reflejando",
        "oraciones": {
            "infinitivo":   {"ing": "I reflect on my decisions.","esp": "Yo reflexiono sobre mis decisiones."},
            "pasadoSimple": {"ing": "You reflected light perfectly.","esp": "Tú reflejaste la luz perfectamente."},
            "participio":   {"ing": "She has reflected deeply.","esp": "Ella ha reflexionado profundamente."},
            "gerundio":     {"ing": "They are reflecting the sun.","esp": "Ellos están reflejando el sol."},
            "futuro":       {"ing": "We will reflect on this.","esp": "Nosotros reflexionaremos sobre esto."},
            "condicional":  {"ing": "That mirror would reflect clearly.","esp": "Ese espejo reflejaría con claridad."}
        }
    },
    {
        "ing_inf": "refuse", "esp_inf": "rechazar",
        "pasado_ing": "refused", "pasado_esp": "rechazó",
        "participio_ing": "refused", "participio_esp": "rechazado",
        "gerundio_ing": "refusing", "gerundio_esp": "rechazando",
        "oraciones": {
            "infinitivo":   {"ing": "I refuse to give up.","esp": "Yo me niego a rendirme."},
            "pasadoSimple": {"ing": "You refused the offer.","esp": "Tú rechazaste la oferta."},
            "participio":   {"ing": "She has refused the invitation.","esp": "Ella ha rechazado la invitación."},
            "gerundio":     {"ing": "They are refusing to negotiate.","esp": "Ellos se están negando a negociar."},
            "futuro":       {"ing": "We will refuse the terms.","esp": "Nosotros rechazaremos los términos."},
            "condicional":  {"ing": "That door would refuse entry.","esp": "Esa puerta rechazaría la entrada."}
        }
    }
]


BLOQUE_18 = [
    {
        "ing_inf": "regret", "esp_inf": "lamentar",
        "pasado_ing": "regretted", "pasado_esp": "lamentó",
        "participio_ing": "regretted", "participio_esp": "lamentado",
        "gerundio_ing": "regretting", "gerundio_esp": "lamentando",
        "oraciones": {
            "infinitivo":   {"ing": "I regret not studying harder.","esp": "Yo lamento no haber estudiado más."},
            "pasadoSimple": {"ing": "You regretted your decision.","esp": "Tú lamentaste tu decisión."},
            "participio":   {"ing": "She has regretted that choice.","esp": "Ella ha lamentado esa elección."},
            "gerundio":     {"ing": "They are regretting the move.","esp": "Ellos están lamentando la mudanza."},
            "futuro":       {"ing": "We will regret this later.","esp": "Nosotros lamentaremos esto después."},
            "condicional":  {"ing": "That choice would be regretted.","esp": "Esa elección sería lamentada."}
        }
    },
    {
        "ing_inf": "relate", "esp_inf": "relacionar",
        "pasado_ing": "related", "pasado_esp": "relacionó",
        "participio_ing": "related", "participio_esp": "relacionado",
        "gerundio_ing": "relating", "gerundio_esp": "relacionando",
        "oraciones": {
            "infinitivo":   {"ing": "I relate the story to my kids.","esp": "Yo relaciono la historia con mis hijos."},
            "pasadoSimple": {"ing": "You related well to the audience.","esp": "Tú te relacionaste bien con el público."},
            "participio":   {"ing": "She has related the data to sales.","esp": "Ella ha relacionado los datos con las ventas."},
            "gerundio":     {"ing": "They are relating the issues.","esp": "Ellos están relacionando los problemas."},
            "futuro":       {"ing": "We will relate the concepts tomorrow.","esp": "Nosotros relacionaremos los conceptos mañana."},
            "condicional":  {"ing": "That theory would relate both ideas.","esp": "Esa teoría relacionaría ambas ideas."}
        }
    },
    {
        "ing_inf": "relax", "esp_inf": "relajar",
        "pasado_ing": "relaxed", "pasado_esp": "relajó",
        "participio_ing": "relaxed", "participio_esp": "relajado",
        "gerundio_ing": "relaxing", "gerundio_esp": "relajando",
        "oraciones": {
            "infinitivo":   {"ing": "I relax by reading at night.","esp": "Yo me relajo leyendo por la noche."},
            "pasadoSimple": {"ing": "You relaxed during the vacation.","esp": "Tú te relajaste durante las vacaciones."},
            "participio":   {"ing": "She has relaxed the rules.","esp": "Ella ha relajado las reglas."},
            "gerundio":     {"ing": "They are relaxing by the pool.","esp": "Ellos se están relajando junto a la piscina."},
            "futuro":       {"ing": "We will relax this weekend.","esp": "Nosotros nos relajaremos este fin de semana."},
            "condicional":  {"ing": "That music would relax anyone.","esp": "Esa música relajaría a cualquiera."}
        }
    },
    {
        "ing_inf": "release", "esp_inf": "liberar",
        "pasado_ing": "released", "pasado_esp": "liberó",
        "participio_ing": "released", "participio_esp": "liberado",
        "gerundio_ing": "releasing", "gerundio_esp": "liberando",
        "oraciones": {
            "infinitivo":   {"ing": "I release stress through exercise.","esp": "Yo libero estrés con el ejercicio."},
            "pasadoSimple": {"ing": "You released the balloon.","esp": "Tú soltaste el globo."},
            "participio":   {"ing": "She has released the new album.","esp": "Ella ha lanzado el álbum nuevo."},
            "gerundio":     {"ing": "They are releasing the prisoners.","esp": "Ellos están liberando a los prisioneros."},
            "futuro":       {"ing": "We will release the report tomorrow.","esp": "Nosotros lanzaremos el informe mañana."},
            "condicional":  {"ing": "That button would release pressure.","esp": "Ese botón liberaría presión."}
        }
    },
    {
        "ing_inf": "rely", "esp_inf": "confiar",
        "pasado_ing": "relied", "pasado_esp": "confió",
        "participio_ing": "relied", "participio_esp": "confiado",
        "gerundio_ing": "relying", "gerundio_esp": "confiando",
        "oraciones": {
            "infinitivo":   {"ing": "I rely on my instincts.","esp": "Yo confío en mis instintos."},
            "pasadoSimple": {"ing": "You relied on the map.","esp": "Tú confiaste en el mapa."},
            "participio":   {"ing": "She has relied on her team.","esp": "Ella ha confiado en su equipo."},
            "gerundio":     {"ing": "They are relying on luck.","esp": "Ellos están confiando en la suerte."},
            "futuro":       {"ing": "We will rely on data.","esp": "Nosotros confiaremos en los datos."},
            "condicional":  {"ing": "That system would rely on backups.","esp": "Ese sistema confiaría en respaldos."}
        }
    },
    {
        "ing_inf": "remain", "esp_inf": "permanecer",
        "pasado_ing": "remained", "pasado_esp": "permaneció",
        "participio_ing": "remained", "participio_esp": "permanecido",
        "gerundio_ing": "remaining", "gerundio_esp": "permaneciendo",
        "oraciones": {
            "infinitivo":   {"ing": "I remain calm under pressure.","esp": "Yo permanezco calmado bajo presión."},
            "pasadoSimple": {"ing": "You remained silent.","esp": "Tú permaneciste en silencio."},
            "participio":   {"ing": "She has remained loyal.","esp": "Ella ha permanecido leal."},
            "gerundio":     {"ing": "They are remaining hopeful.","esp": "Ellos están permaneciendo esperanzados."},
            "futuro":       {"ing": "We will remain at home.","esp": "Nosotros permaneceremos en casa."},
            "condicional":  {"ing": "That problem would remain unsolved.","esp": "Ese problema permanecería sin resolver."}
        }
    },
    {
        "ing_inf": "remember", "esp_inf": "recordar",
        "pasado_ing": "remembered", "pasado_esp": "recordó",
        "participio_ing": "remembered", "participio_esp": "recordado",
        "gerundio_ing": "remembering", "gerundio_esp": "recordando",
        "oraciones": {
            "infinitivo":   {"ing": "I remember my first day.","esp": "Yo recuerdo mi primer día."},
            "pasadoSimple": {"ing": "You remembered the lyrics.","esp": "Tú recordaste la letra."},
            "participio":   {"ing": "She has remembered the password.","esp": "Ella ha recordado la contraseña."},
            "gerundio":     {"ing": "They are remembering the past.","esp": "Ellos están recordando el pasado."},
            "futuro":       {"ing": "We will remember this day.","esp": "Nosotros recordaremos este día."},
            "condicional":  {"ing": "That melody would be remembered by anyone.","esp": "Esa melodía sería recordada por cualquiera."}
        }
    },
    {
        "ing_inf": "remind", "esp_inf": "recordar",
        "pasado_ing": "reminded", "pasado_esp": "recordó",
        "participio_ing": "reminded", "participio_esp": "recordado",
        "gerundio_ing": "reminding", "gerundio_esp": "recordando",
        "oraciones": {
            "infinitivo":   {"ing": "I remind my kids to brush their teeth.","esp": "Yo les recuerdo a mis hijos que se cepillen los dientes."},
            "pasadoSimple": {"ing": "You reminded me of the meeting.","esp": "Tú me recordaste la reunión."},
            "participio":   {"ing": "She has reminded everyone.","esp": "Ella ha recordado a todos."},
            "gerundio":     {"ing": "They are reminding the staff.","esp": "Ellos están recordando al personal."},
            "futuro":       {"ing": "We will remind you tomorrow.","esp": "Nosotros te recordaremos mañana."},
            "condicional":  {"ing": "That smell would remind anyone of childhood.","esp": "Ese olor recordaría a cualquiera su infancia."}
        }
    },
    {
        "ing_inf": "remove", "esp_inf": "quitar",
        "pasado_ing": "removed", "pasado_esp": "quitó",
        "participio_ing": "removed", "participio_esp": "quitado",
        "gerundio_ing": "removing", "gerundio_esp": "quitando",
        "oraciones": {
            "infinitivo":   {"ing": "I remove my shoes at the door.","esp": "Yo me quito los zapatos en la puerta."},
            "pasadoSimple": {"ing": "You removed the stain.","esp": "Tú quitaste la mancha."},
            "participio":   {"ing": "She has removed her makeup.","esp": "Ella se ha quitado el maquillaje."},
            "gerundio":     {"ing": "They are removing the debris.","esp": "Ellos están quitando los escombros."},
            "futuro":       {"ing": "We will remove the old furniture.","esp": "Nosotros quitaremos los muebles viejos."},
            "condicional":  {"ing": "That tool would remove the stain.","esp": "Esa herramienta quitaría la mancha."}
        }
    },
    {
        "ing_inf": "repair", "esp_inf": "reparar",
        "pasado_ing": "repaired", "pasado_esp": "reparó",
        "participio_ing": "repaired", "participio_esp": "reparado",
        "gerundio_ing": "repairing", "gerundio_esp": "reparando",
        "oraciones": {
            "infinitivo":   {"ing": "I repair electronics as a hobby.","esp": "Yo reparo electrónica como pasatiempo."},
            "pasadoSimple": {"ing": "You repaired the broken fence.","esp": "Tú reparaste la valla rota."},
            "participio":   {"ing": "She has repaired the relationship.","esp": "Ella ha reparado la relación."},
            "gerundio":     {"ing": "They are repairing the road.","esp": "Ellos están reparando el camino."},
            "futuro":       {"ing": "We will repair the damage soon.","esp": "Nosotros repararemos el daño pronto."},
            "condicional":  {"ing": "That technician would repair anything.","esp": "Ese técnico repararía cualquier cosa."}
        }
    },
    {
        "ing_inf": "repeat", "esp_inf": "repetir",
        "pasado_ing": "repeated", "pasado_esp": "repitió",
        "participio_ing": "repeated", "participio_esp": "repetido",
        "gerundio_ing": "repeating", "gerundio_esp": "repitiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I repeat the lesson if needed.","esp": "Yo repito la lección si es necesario."},
            "pasadoSimple": {"ing": "You repeated the question.","esp": "Tú repetiste la pregunta."},
            "participio":   {"ing": "She has repeated the mistake.","esp": "Ella ha repetido el error."},
            "gerundio":     {"ing": "They are repeating the course.","esp": "Ellos están repitiendo el curso."},
            "futuro":       {"ing": "We will repeat the experiment.","esp": "Nosotros repetiremos el experimento."},
            "condicional":  {"ing": "That cycle would repeat forever.","esp": "Ese ciclo se repetiría para siempre."}
        }
    },
    {
        "ing_inf": "replace", "esp_inf": "reemplazar",
        "pasado_ing": "replaced", "pasado_esp": "reemplazó",
        "participio_ing": "replaced", "participio_esp": "reemplazado",
        "gerundio_ing": "replacing", "gerundio_esp": "reemplazando",
        "oraciones": {
            "infinitivo":   {"ing": "I replace my phone every two years.","esp": "Yo reemplazo mi teléfono cada dos años."},
            "pasadoSimple": {"ing": "You replaced the broken glass.","esp": "Tú reemplazaste el cristal roto."},
            "participio":   {"ing": "She has replaced the manager.","esp": "Ella ha reemplazado al gerente."},
            "gerundio":     {"ing": "They are replacing the old system.","esp": "Ellos están reemplazando el sistema viejo."},
            "futuro":       {"ing": "We will replace the broken tiles.","esp": "Nosotros reemplazaremos las baldosas rotas."},
            "condicional":  {"ing": "That update would replace the old one.","esp": "Esa actualización reemplazaría la anterior."}
        }
    },
    {
        "ing_inf": "reply", "esp_inf": "responder",
        "pasado_ing": "replied", "pasado_esp": "respondió",
        "participio_ing": "replied", "participio_esp": "respondido",
        "gerundio_ing": "replying", "gerundio_esp": "respondiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I reply to emails within an hour.","esp": "Yo respondo correos en menos de una hora."},
            "pasadoSimple": {"ing": "You replied politely.","esp": "Tú respondiste con educación."},
            "participio":   {"ing": "She has replied to the message.","esp": "Ella ha respondido al mensaje."},
            "gerundio":     {"ing": "They are replying to the comments.","esp": "Ellos están respondiendo a los comentarios."},
            "futuro":       {"ing": "We will reply tomorrow.","esp": "Nosotros responderemos mañana."},
            "condicional":  {"ing": "That letter would receive a formal reply.","esp": "Esa carta tendría una respuesta formal."}
        }
    },
    {
        "ing_inf": "report", "esp_inf": "reportar",
        "pasado_ing": "reported", "pasado_esp": "reportó",
        "participio_ing": "reported", "participio_esp": "reportado",
        "gerundio_ing": "reporting", "gerundio_esp": "reportando",
        "oraciones": {
            "infinitivo":   {"ing": "I report to my manager daily.","esp": "Yo le reporto a mi gerente a diario."},
            "pasadoSimple": {"ing": "You reported the incident.","esp": "Tú reportaste el incidente."},
            "participio":   {"ing": "She has reported the bug.","esp": "Ella ha reportado el error."},
            "gerundio":     {"ing": "They are reporting live.","esp": "Ellos están reportando en vivo."},
            "futuro":       {"ing": "We will report to the police.","esp": "Nosotros reportaremos a la policía."},
            "condicional":  {"ing": "That journalist would report fairly.","esp": "Ese periodista reportaría con objetividad."}
        }
    },
    {
        "ing_inf": "request", "esp_inf": "solicitar",
        "pasado_ing": "requested", "pasado_esp": "solicitó",
        "participio_ing": "requested", "participio_esp": "solicitado",
        "gerundio_ing": "requesting", "gerundio_esp": "solicitando",
        "oraciones": {
            "infinitivo":   {"ing": "I request feedback from users.","esp": "Yo solicito retroalimentación de los usuarios."},
            "pasadoSimple": {"ing": "You requested a refund.","esp": "Tú solicitaste un reembolso."},
            "participio":   {"ing": "She has requested more time.","esp": "Ella ha solicitado más tiempo."},
            "gerundio":     {"ing": "They are requesting access.","esp": "Ellos están solicitando acceso."},
            "futuro":       {"ing": "We will request a meeting.","esp": "Nosotros solicitaremos una reunión."},
            "condicional":  {"ing": "That form would request more info.","esp": "Ese formulario solicitaría más información."}
        }
    },
    {
        "ing_inf": "rescue", "esp_inf": "rescatar",
        "pasado_ing": "rescued", "pasado_esp": "rescató",
        "participio_ing": "rescued", "participio_esp": "rescatado",
        "gerundio_ing": "rescuing", "gerundio_esp": "rescatando",
        "oraciones": {
            "infinitivo":   {"ing": "I rescue stray cats sometimes.","esp": "Yo rescato gatos callejeros a veces."},
            "pasadoSimple": {"ing": "You rescued the drowning swimmer.","esp": "Tú rescataste al nadador ahogándose."},
            "participio":   {"ing": "She has rescued the documents.","esp": "Ella ha rescatado los documentos."},
            "gerundio":     {"ing": "They are rescuing the hostages.","esp": "Ellos están rescatando a los rehenes."},
            "futuro":       {"ing": "We will rescue the data.","esp": "Nosotros rescataremos los datos."},
            "condicional":  {"ing": "That helicopter would rescue anyone.","esp": "Ese helicóptero rescataría a cualquiera."}
        }
    },
    {
        "ing_inf": "retire", "esp_inf": "jubilarse",
        "pasado_ing": "retired", "pasado_esp": "se jubiló",
        "participio_ing": "retired", "participio_esp": "jubilado",
        "gerundio_ing": "retiring", "gerundio_esp": "jubilándose",
        "futuro_esp": "se jubilará", "cond_esp": "se jubilaría",
        "oraciones": {
            "infinitivo":   {"ing": "I retire at 65.","esp": "Yo me jubilo a los 65."},
            "pasadoSimple": {"ing": "You retired from the company.","esp": "Tú te jubilaste de la empresa."},
            "participio":   {"ing": "She has retired after 30 years.","esp": "Ella se ha jubilado después de 30 años."},
            "gerundio":     {"ing": "They are retiring the old model.","esp": "Ellos están retirando el modelo viejo."},
            "futuro":       {"ing": "We will retire next year.","esp": "Nosotros nos jubilaremos el próximo año."},
            "condicional":  {"ing": "That player would retire soon.","esp": "Ese jugador se jubilaría pronto."}
        }
    },
    {
        "ing_inf": "return", "esp_inf": "regresar",
        "pasado_ing": "returned", "pasado_esp": "regresó",
        "participio_ing": "returned", "participio_esp": "regresado",
        "gerundio_ing": "returning", "gerundio_esp": "regresando",
        "oraciones": {
            "infinitivo":   {"ing": "I return books to the library weekly.","esp": "Yo devuelvo libros a la biblioteca semanalmente."},
            "pasadoSimple": {"ing": "You returned the money.","esp": "Tú regresaste el dinero."},
            "participio":   {"ing": "She has returned from vacation.","esp": "Ella ha regresado de las vacaciones."},
            "gerundio":     {"ing": "They are returning home.","esp": "Ellos están regresando a casa."},
            "futuro":       {"ing": "We will return tomorrow.","esp": "Nosotros regresaremos mañana."},
            "condicional":  {"ing": "That investment would return profits.","esp": "Esa inversión regresaría ganancias."}
        }
    },
    {
        "ing_inf": "review", "esp_inf": "revisar",
        "pasado_ing": "reviewed", "pasado_esp": "revisó",
        "participio_ing": "reviewed", "participio_esp": "revisado",
        "gerundio_ing": "reviewing", "gerundio_esp": "revisando",
        "oraciones": {
            "infinitivo":   {"ing": "I review my notes before tests.","esp": "Yo reviso mis apuntes antes de los exámenes."},
            "pasadoSimple": {"ing": "You reviewed the contract.","esp": "Tú revisaste el contrato."},
            "participio":   {"ing": "She has reviewed the case.","esp": "Ella ha revisado el caso."},
            "gerundio":     {"ing": "They are reviewing the proposal.","esp": "Ellos están revisando la propuesta."},
            "futuro":       {"ing": "We will review the code.","esp": "Nosotros revisaremos el código."},
            "condicional":  {"ing": "That committee would review the application.","esp": "Ese comité revisaría la solicitud."}
        }
    },
    {
        "ing_inf": "rinse", "esp_inf": "enjuagar",
        "pasado_ing": "rinsed", "pasado_esp": "enjuagó",
        "participio_ing": "rinsed", "participio_esp": "enjuagado",
        "gerundio_ing": "rinsing", "gerundio_esp": "enjuagando",
        "oraciones": {
            "infinitivo":   {"ing": "I rinse my hair with cold water.","esp": "Yo me enjuago el pelo con agua fría."},
            "pasadoSimple": {"ing": "You rinsed the dishes.","esp": "Tú enjuagaste los platos."},
            "participio":   {"ing": "She has rinsed the vegetables.","esp": "Ella ha enjuagado las verduras."},
            "gerundio":     {"ing": "They are rinsing the clothes.","esp": "Ellos están enjuagando la ropa."},
            "futuro":       {"ing": "We will rinse the paintbrush.","esp": "Nosotros enjuagaremos el pincel."},
            "condicional":  {"ing": "That shower would rinse off easily.","esp": "Esa ducha enjuagaría fácilmente."}
        }
    },
    {
        "ing_inf": "risk", "esp_inf": "arriesgar",
        "pasado_ing": "risked", "pasado_esp": "arriesgó",
        "participio_ing": "risked", "participio_esp": "arriesgado",
        "gerundio_ing": "risking", "gerundio_esp": "arriesgando",
        "oraciones": {
            "infinitivo":   {"ing": "I risk my life for my family.","esp": "Yo arriesgo mi vida por mi familia."},
            "pasadoSimple": {"ing": "You risked everything.","esp": "Tú arriesgaste todo."},
            "participio":   {"ing": "She has risked her career.","esp": "Ella ha arriesgado su carrera."},
            "gerundio":     {"ing": "They are risking too much.","esp": "Ellos están arriesgando demasiado."},
            "futuro":       {"ing": "We will risk failure.","esp": "Nosotros arriesgaremos el fracaso."},
            "condicional":  {"ing": "That move would risk everything.","esp": "Ese movimiento arriesgaría todo."}
        }
    },
    {
        "ing_inf": "rob", "esp_inf": "robar",
        "pasado_ing": "robbed", "pasado_esp": "robó",
        "participio_ing": "robbed", "participio_esp": "robado",
        "gerundio_ing": "robbing", "gerundio_esp": "robando",
        "oraciones": {
            "infinitivo":   {"ing": "I rob the spotlight sometimes.","esp": "Yo me robo el protagonismo a veces."},
            "pasadoSimple": {"ing": "You robbed the bank.","esp": "Tú robaste el banco."},
            "participio":   {"ing": "She has robbed my heart.","esp": "Ella me ha robado el corazón."},
            "gerundio":     {"ing": "They are robbing the museum.","esp": "Ellos están robando el museo."},
            "futuro":       {"ing": "We will rob the base.","esp": "Nosotros robaremos la base."},
            "condicional":  {"ing": "That thief would rob anyone.","esp": "Ese ladrón robaría a cualquiera."}
        }
    },
    {
        "ing_inf": "roll", "esp_inf": "rodar",
        "pasado_ing": "rolled", "pasado_esp": "rodó",
        "participio_ing": "rolled", "participio_esp": "rodado",
        "gerundio_ing": "rolling", "gerundio_esp": "rodando",
        "oraciones": {
            "infinitivo":   {"ing": "I roll the dough for pizza.","esp": "Yo amaso la masa para pizza."},
            "pasadoSimple": {"ing": "You rolled the dice.","esp": "Tú lanzaste los dados."},
            "participio":   {"ing": "She has rolled the carpet.","esp": "Ella ha enrollado la alfombra."},
            "gerundio":     {"ing": "They are rolling down the hill.","esp": "Ellos están rodando colina abajo."},
            "futuro":       {"ing": "We will roll the windows up.","esp": "Nosotros subiremos las ventanas."},
            "condicional":  {"ing": "That ball would roll easily.","esp": "Esa pelota rodaría fácilmente."}
        }
    },
    {
        "ing_inf": "rot", "esp_inf": "pudrirse",
        "pasado_ing": "rotted", "pasado_esp": "se pudrió",
        "participio_ing": "rotted", "participio_esp": "podrido",
        "gerundio_ing": "rotting", "gerundio_esp": "pudriéndose",
        "futuro_esp": "se pudrirá", "cond_esp": "se pudriría",
        "oraciones": {
            "infinitivo":   {"ing": "I let the leaves rot for compost.","esp": "Yo dejo que las hojas se pudran para compost."},
            "pasadoSimple": {"ing": "You let the fruit rot.","esp": "Tú dejaste que la fruta se pudriera."},
            "participio":   {"ing": "The wood has rotted away.","esp": "La madera se ha podrido."},
            "gerundio":     {"ing": "They are rotting from neglect.","esp": "Ellos se están pudriendo por el abandono."},
            "futuro":       {"ing": "The wood will rot without treatment.","esp": "La madera se pudrirá sin tratamiento."},
            "condicional":  {"ing": "That food would rot quickly.","esp": "Esa comida se pudriría rápido."}
        }
    },
    {
        "ing_inf": "rub", "esp_inf": "frotar",
        "pasado_ing": "rubbed", "pasado_esp": "frotó",
        "participio_ing": "rubbed", "participio_esp": "frotado",
        "gerundio_ing": "rubbing", "gerundio_esp": "frotando",
        "oraciones": {
            "infinitivo":   {"ing": "I rub my eyes when tired.","esp": "Yo me froto los ojos cuando estoy cansado."},
            "pasadoSimple": {"ing": "You rubbed the stain.","esp": "Tú frotaste la mancha."},
            "participio":   {"ing": "She has rubbed her shoulder.","esp": "Ella se ha frotado el hombro."},
            "gerundio":     {"ing": "They are rubbing the surface.","esp": "Ellos están frotando la superficie."},
            "futuro":       {"ing": "We will rub the lotion in.","esp": "Nosotros nos untaremos la loción."},
            "condicional":  {"ing": "That cloth would rub easily.","esp": "Ese paño frotaría fácilmente."}
        }
    },
    {
        "ing_inf": "ruin", "esp_inf": "arruinar",
        "pasado_ing": "ruined", "pasado_esp": "arruinó",
        "participio_ing": "ruined", "participio_esp": "arruinado",
        "gerundio_ing": "ruining", "gerundio_esp": "arruinando",
        "oraciones": {
            "infinitivo":   {"ing": "I ruin surprises easily.","esp": "Yo arruino las sorpresas con facilidad."},
            "pasadoSimple": {"ing": "You ruined the dress.","esp": "Tú arruinaste el vestido."},
            "participio":   {"ing": "She has ruined her reputation.","esp": "Ella ha arruinado su reputación."},
            "gerundio":     {"ing": "They are ruining the party.","esp": "Ellos están arruinando la fiesta."},
            "futuro":       {"ing": "We will ruin the surprise.","esp": "Nosotros arruinaremos la sorpresa."},
            "condicional":  {"ing": "That stain would ruin the shirt.","esp": "Esa mancha arruinaría la camisa."}
        }
    },
    {
        "ing_inf": "rule", "esp_inf": "gobernar",
        "pasado_ing": "ruled", "pasado_esp": "gobernó",
        "participio_ing": "ruled", "participio_esp": "gobernado",
        "gerundio_ing": "ruling", "gerundio_esp": "gobernando",
        "oraciones": {
            "infinitivo":   {"ing": "I rule out impossible options.","esp": "Yo descarto opciones imposibles."},
            "pasadoSimple": {"ing": "You ruled the country.","esp": "Tú gobernaste el país."},
            "participio":   {"ing": "She has ruled the company for years.","esp": "Ella ha dirigido la empresa durante años."},
            "gerundio":     {"ing": "They are ruling on the case.","esp": "Ellos están fallando en el caso."},
            "futuro":       {"ing": "We will rule in your favor.","esp": "Nosotros fallaremos a tu favor."},
            "condicional":  {"ing": "That king would rule wisely.","esp": "Ese rey gobernaría con sabiduría."}
        }
    },
    {
        "ing_inf": "rush", "esp_inf": "apresurar",
        "pasado_ing": "rushed", "pasado_esp": "apresuró",
        "participio_ing": "rushed", "participio_esp": "apresurado",
        "gerundio_ing": "rushing", "gerundio_esp": "apresurando",
        "oraciones": {
            "infinitivo":   {"ing": "I rush to work every morning.","esp": "Yo me apresuro al trabajo cada mañana."},
            "pasadoSimple": {"ing": "You rushed through the meal.","esp": "Tú te apresuraste durante la comida."},
            "participio":   {"ing": "She has rushed the deadline.","esp": "Ella se ha apresurado por el plazo."},
            "gerundio":     {"ing": "They are rushing to the hospital.","esp": "Ellos se están apresurando al hospital."},
            "futuro":       {"ing": "We will rush if necessary.","esp": "Nosotros nos apresuraremos si es necesario."},
            "condicional":  {"ing": "That decision would rush the process.","esp": "Esa decisión apresuraría el proceso."}
        }
    },
    {
        "ing_inf": "sack", "esp_inf": "saquear",
        "pasado_ing": "sacked", "pasado_esp": "saqueó",
        "participio_ing": "sacked", "participio_esp": "saqueado",
        "gerundio_ing": "sacking", "gerundio_esp": "saqueando",
        "oraciones": {
            "infinitivo":   {"ing": "I sack the groceries carefully.","esp": "Yo empaco las compras con cuidado."},
            "pasadoSimple": {"ing": "You sacked the city long ago.","esp": "Tú saqueaste la ciudad hace mucho."},
            "participio":   {"ing": "She has sacked the employee.","esp": "Ella ha despedido al empleado."},
            "gerundio":     {"ing": "They are sacking the village.","esp": "Ellos están saqueando la aldea."},
            "futuro":       {"ing": "We will sack the thief.","esp": "Nosotros capturaremos al ladrón."},
            "condicional":  {"ing": "That team would sack the coach.","esp": "Ese equipo despediría al entrenador."}
        }
    },
    {
        "ing_inf": "sail", "esp_inf": "navegar",
        "pasado_ing": "sailed", "pasado_esp": "navegó",
        "participio_ing": "sailed", "participio_esp": "navegado",
        "gerundio_ing": "sailing", "gerundio_esp": "navegando",
        "oraciones": {
            "infinitivo":   {"ing": "I sail on weekends at the lake.","esp": "Yo navego los fines de semana en el lago."},
            "pasadoSimple": {"ing": "You sailed across the ocean.","esp": "Tú navegaste por el océano."},
            "participio":   {"ing": "She has sailed solo before.","esp": "Ella ha navegado sola antes."},
            "gerundio":     {"ing": "They are sailing toward the island.","esp": "Ellos están navegando hacia la isla."},
            "futuro":       {"ing": "We will sail at sunrise.","esp": "Nosotros navegaremos al amanecer."},
            "condicional":  {"ing": "That boat would sail smoothly.","esp": "Ese barco navegaría sin problemas."}
        }
    }
]


BLOQUE_19 = [
    {
        "ing_inf": "satisfy", "esp_inf": "satisfacer",
        "pasado_ing": "satisfied", "pasado_esp": "satisfizo",
        "participio_ing": "satisfied", "participio_esp": "satisfecho",
        "gerundio_ing": "satisfying", "gerundio_esp": "satisfaciendo",
        "oraciones": {
            "infinitivo":   {"ing": "I satisfy my curiosity daily.","esp": "Yo satisfago mi curiosidad a diario."},
            "pasadoSimple": {"ing": "You satisfied the customers.","esp": "Tú satisfaciste a los clientes."},
            "participio":   {"ing": "She has satisfied the requirements.","esp": "Ella ha satisfecho los requisitos."},
            "gerundio":     {"ing": "They are satisfying demand.","esp": "Ellos están satisfaciendo la demanda."},
            "futuro":       {"ing": "We will satisfy expectations.","esp": "Nosotros satisfaremos las expectativas."},
            "condicional":  {"ing": "That meal would satisfy anyone.","esp": "Esa comida satisfaría a cualquiera."}
        }
    },
    {
        "ing_inf": "save", "esp_inf": "ahorrar",
        "pasado_ing": "saved", "pasado_esp": "ahorró",
        "participio_ing": "saved", "participio_esp": "ahorrado",
        "gerundio_ing": "saving", "gerundio_esp": "ahorrando",
        "oraciones": {
            "infinitivo":   {"ing": "I save money every month.","esp": "Yo ahorro dinero cada mes."},
            "pasadoSimple": {"ing": "You saved my life.","esp": "Tú salvaste mi vida."},
            "participio":   {"ing": "She has saved the file.","esp": "Ella ha guardado el archivo."},
            "gerundio":     {"ing": "They are saving energy.","esp": "Ellos están ahorrando energía."},
            "futuro":       {"ing": "We will save the environment.","esp": "Nosotros salvaremos el medio ambiente."},
            "condicional":  {"ing": "That app would save time.","esp": "Esa app ahorraría tiempo."}
        }
    },
    {
        "ing_inf": "saw", "esp_inf": "serrar",
        "pasado_ing": "sawed", "pasado_esp": "serró",
        "participio_ing": "sawed", "participio_esp": "serrado",
        "gerundio_ing": "sawing", "gerundio_esp": "serrando",
        "oraciones": {
            "infinitivo":   {"ing": "I saw wood for the project.","esp": "Yo serrucho madera para el proyecto."},
            "pasadoSimple": {"ing": "You sawed the branch.","esp": "Tú serrast la rama."},
            "participio":   {"ing": "She has sawed the planks.","esp": "Ella ha serrado las tablas."},
            "gerundio":     {"ing": "They are sawing the logs.","esp": "Ellos están serrando los troncos."},
            "futuro":       {"ing": "We will saw the boards tomorrow.","esp": "Nosotros serrremos las tablas mañana."},
            "condicional":  {"ing": "That tool would saw faster.","esp": "Esa herramienta serrjaría más rápido."}
        }
    },
    {
        "ing_inf": "scan", "esp_inf": "escanear",
        "pasado_ing": "scanned", "pasado_esp": "escaneó",
        "participio_ing": "scanned", "participio_esp": "escaneado",
        "gerundio_ing": "scanning", "gerundio_esp": "escaneando",
        "oraciones": {
            "infinitivo":   {"ing": "I scan documents at work.","esp": "Yo escaneo documentos en el trabajo."},
            "pasadoSimple": {"ing": "You scanned the receipt.","esp": "Tú escaneaste el recibo."},
            "participio":   {"ing": "She has scanned the barcode.","esp": "Ella ha escaneado el código de barras."},
            "gerundio":     {"ing": "They are scanning the area.","esp": "Ellos están escaneando el área."},
            "futuro":       {"ing": "We will scan for viruses.","esp": "Nosotros escanearemos en busca de virus."},
            "condicional":  {"ing": "That radar would scan the sky.","esp": "Ese radar escanearía el cielo."}
        }
    },
    {
        "ing_inf": "scare", "esp_inf": "asustar",
        "pasado_ing": "scared", "pasado_esp": "asustó",
        "participio_ing": "scared", "participio_esp": "asustado",
        "gerundio_ing": "scaring", "gerundio_esp": "asustando",
        "oraciones": {
            "infinitivo":   {"ing": "I scare myself with horror movies.","esp": "Yo me asusto con películas de terror."},
            "pasadoSimple": {"ing": "You scared the children.","esp": "Tú asustaste a los niños."},
            "participio":   {"ing": "She has scared the neighbors.","esp": "Ella ha asustado a los vecinos."},
            "gerundio":     {"ing": "They are scaring the cat.","esp": "Ellos están asustando al gato."},
            "futuro":       {"ing": "We will scare the intruders.","esp": "Nosotros asustaremos a los intrusos."},
            "condicional":  {"ing": "That noise would scare anyone.","esp": "Ese ruido asustaría a cualquiera."}
        }
    },
    {
        "ing_inf": "scold", "esp_inf": "regañar",
        "pasado_ing": "scolded", "pasado_esp": "regañó",
        "participio_ing": "scolded", "participio_esp": "regañado",
        "gerundio_ing": "scolding", "gerundio_esp": "regañando",
        "oraciones": {
            "infinitivo":   {"ing": "I scold my kids when they misbehave.","esp": "Yo regaño a mis hijos cuando se portan mal."},
            "pasadoSimple": {"ing": "You scolded the waiter unfairly.","esp": "Tú regañaste al mesero injustamente."},
            "participio":   {"ing": "She has scolded the team.","esp": "Ella ha regañado al equipo."},
            "gerundio":     {"ing": "They are scolding the children.","esp": "Ellos están regañando a los niños."},
            "futuro":       {"ing": "We will scold him later.","esp": "Nosotros lo regañaremos después."},
            "condicional":  {"ing": "That teacher would scold anyone.","esp": "Ese profesor regañaría a cualquiera."}
        }
    },
    {
        "ing_inf": "scrape", "esp_inf": "raspar",
        "pasado_ing": "scraped", "pasado_esp": "raspó",
        "participio_ing": "scraped", "participio_esp": "raspado",
        "gerundio_ing": "scraping", "gerundio_esp": "raspando",
        "oraciones": {
            "infinitivo":   {"ing": "I scrape the ice off the windshield.","esp": "Yo raspo el hielo del parabrisas."},
            "pasadoSimple": {"ing": "You scraped the paint.","esp": "Tú raspaste la pintura."},
            "participio":   {"ing": "She has scraped her knee.","esp": "Ella se ha raspado la rodilla."},
            "gerundio":     {"ing": "They are scraping the floor.","esp": "Ellos están raspando el piso."},
            "futuro":       {"ing": "We will scrape the old wallpaper.","esp": "Nosotros rasparemos el papel tapiz viejo."},
            "condicional":  {"ing": "That knife would scrape easily.","esp": "Ese cuchillo rasparía fácilmente."}
        }
    },
    {
        "ing_inf": "scratch", "esp_inf": "rascar",
        "pasado_ing": "scratched", "pasado_esp": "rascó",
        "participio_ing": "scratched", "participio_esp": "rascado",
        "gerundio_ing": "scratching", "gerundio_esp": "rascando",
        "oraciones": {
            "infinitivo":   {"ing": "I scratch my head when confused.","esp": "Yo me rasco la cabeza cuando estoy confundido."},
            "pasadoSimple": {"ing": "You scratched the car.","esp": "Tú rayaste el coche."},
            "participio":   {"ing": "The cat has scratched the sofa.","esp": "El gato ha rayado el sofá."},
            "gerundio":     {"ing": "They are scratching the lottery tickets.","esp": "Ellos están rascando los boletos de lotería."},
            "futuro":       {"ing": "We will scratch the surface.","esp": "Nosotros rascaremos la superficie."},
            "condicional":  {"ing": "That branch would scratch easily.","esp": "Esa rama rayaría fácilmente."}
        }
    },
    {
        "ing_inf": "scream", "esp_inf": "gritar",
        "pasado_ing": "screamed", "pasado_esp": "gritó",
        "participio_ing": "screamed", "participio_esp": "gritado",
        "gerundio_ing": "screaming", "gerundio_esp": "gritando",
        "oraciones": {
            "infinitivo":   {"ing": "I scream at horror movies.","esp": "Yo grito en las películas de terror."},
            "pasadoSimple": {"ing": "You screamed last night.","esp": "Tú gritaste anoche."},
            "participio":   {"ing": "She has screamed for help.","esp": "Ella ha gritado pidiendo ayuda."},
            "gerundio":     {"ing": "They are screaming at the concert.","esp": "Ellos están gritando en el concierto."},
            "futuro":       {"ing": "We will scream with joy.","esp": "Nosotros gritaremos de alegría."},
            "condicional":  {"ing": "That siren would scream loudly.","esp": "Esa sirena gritaría fuertemente."}
        }
    },
    {
        "ing_inf": "screw", "esp_inf": "atornillar",
        "pasado_ing": "screwed", "pasado_esp": "atornilló",
        "participio_ing": "screwed", "participio_esp": "atornillado",
        "gerundio_ing": "screwing", "gerundio_esp": "atornillando",
        "oraciones": {
            "infinitivo":   {"ing": "I screw the lid on tight.","esp": "Yo atornillo la tapa con fuerza."},
            "pasadoSimple": {"ing": "You screwed the shelf to the wall.","esp": "Tú atornillaste el estante a la pared."},
            "participio":   {"ing": "She has screwed the pieces together.","esp": "Ella ha atornillado las piezas."},
            "gerundio":     {"ing": "They are screwing in the bolts.","esp": "Ellos están atornillando los pernos."},
            "futuro":       {"ing": "We will screw the hinges later.","esp": "Nosotros atornillaremos las bisagras después."},
            "condicional":  {"ing": "That drill would screw easily.","esp": "Ese taladro atornillaría fácilmente."}
        }
    },
    {
        "ing_inf": "seal", "esp_inf": "sellar",
        "pasado_ing": "sealed", "pasado_esp": "selló",
        "participio_ing": "sealed", "participio_esp": "sellado",
        "gerundio_ing": "sealing", "gerundio_esp": "sellando",
        "oraciones": {
            "infinitivo":   {"ing": "I seal the envelope carefully.","esp": "Yo sello el sobre con cuidado."},
            "pasadoSimple": {"ing": "You sealed the jar tightly.","esp": "Tú sellaste el frasco herméticamente."},
            "participio":   {"ing": "She has sealed the deal.","esp": "Ella ha sellado el trato."},
            "gerundio":     {"ing": "They are sealing the package.","esp": "Ellos están sellando el paquete."},
            "futuro":       {"ing": "We will seal the cracks tomorrow.","esp": "Nosotros sellaremos las grietas mañana."},
            "condicional":  {"ing": "That wax would seal properly.","esp": "Esa cera sellaría correctamente."}
        }
    },
    {
        "ing_inf": "search", "esp_inf": "buscar",
        "pasado_ing": "searched", "pasado_esp": "buscó",
        "participio_ing": "searched", "participio_esp": "buscado",
        "gerundio_ing": "searching", "gerundio_esp": "buscando",
        "oraciones": {
            "infinitivo":   {"ing": "I search for answers online.","esp": "Yo busco respuestas en línea."},
            "pasadoSimple": {"ing": "You searched the house.","esp": "Tú buscaste en la casa."},
            "participio":   {"ing": "She has searched every corner.","esp": "Ella ha buscado en cada rincón."},
            "gerundio":     {"ing": "They are searching for clues.","esp": "Ellos están buscando pistas."},
            "futuro":       {"ing": "We will search the database.","esp": "Nosotros buscaremos en la base de datos."},
            "condicional":  {"ing": "That dog would search everywhere.","esp": "Ese perro buscaría en todos lados."}
        }
    },
    {
        "ing_inf": "separate", "esp_inf": "separar",
        "pasado_ing": "separated", "pasado_esp": "separó",
        "participio_ing": "separated", "participio_esp": "separado",
        "gerundio_ing": "separating", "gerundio_esp": "separando",
        "oraciones": {
            "infinitivo":   {"ing": "I separate the recycling.","esp": "Yo separo el reciclaje."},
            "pasadoSimple": {"ing": "You separated the laundry.","esp": "Tú separaste la ropa."},
            "participio":   {"ing": "She has separated the yolk.","esp": "Ella ha separado la yema."},
            "gerundio":     {"ing": "They are separating the trash.","esp": "Ellos están separando la basura."},
            "futuro":       {"ing": "We will separate the facts.","esp": "Nosotros separaremos los hechos."},
            "condicional":  {"ing": "That wall would separate the rooms.","esp": "Esa pared separaría las habitaciones."}
        }
    },
    {
        "ing_inf": "serve", "esp_inf": "servir",
        "pasado_ing": "served", "pasado_esp": "sirvió",
        "participio_ing": "served", "participio_esp": "servido",
        "gerundio_ing": "serving", "gerundio_esp": "sirviendo",
        "oraciones": {
            "infinitivo":   {"ing": "I serve coffee every morning.","esp": "Yo sirvo café cada mañana."},
            "pasadoSimple": {"ing": "You served in the army.","esp": "Tú serviste en el ejército."},
            "participio":   {"ing": "She has served customers well.","esp": "Ella ha servido bien a los clientes."},
            "gerundio":     {"ing": "They are serving lunch now.","esp": "Ellos están sirviendo el almuerzo ahora."},
            "futuro":       {"ing": "We will serve the community.","esp": "Nosotros serviremos a la comunidad."},
            "condicional":  {"ing": "That dish would serve four people.","esp": "Ese plato serviría para cuatro personas."}
        }
    },
    {
        "ing_inf": "settle", "esp_inf": "establecerse",
        "pasado_ing": "settled", "pasado_esp": "se estableció",
        "participio_ing": "settled", "participio_esp": "establecido",
        "gerundio_ing": "settling", "gerundio_esp": "estableciéndose",
        "futuro_esp": "se establecerá", "cond_esp": "se establecería",
        "oraciones": {
            "infinitivo":   {"ing": "I settle arguments calmly.","esp": "Yo resuelvo discusiones con calma."},
            "pasadoSimple": {"ing": "You settled down in Spain.","esp": "Tú te estableciste en España."},
            "participio":   {"ing": "She has settled the dispute.","esp": "Ella ha resuelto la disputa."},
            "gerundio":     {"ing": "They are settling into the new house.","esp": "Ellos se están estableciendo en la casa nueva."},
            "futuro":       {"ing": "We will settle the matter soon.","esp": "Nosotros resolveremos el asunto pronto."},
            "condicional":  {"ing": "That decision would settle everything.","esp": "Esa decisión resolvería todo."}
        }
    },
    {
        "ing_inf": "shade", "esp_inf": "sombrear",
        "pasado_ing": "shaded", "pasado_esp": "sombreó",
        "participio_ing": "shaded", "participio_esp": "sombreado",
        "gerundio_ing": "shading", "gerundio_esp": "sombreando",
        "oraciones": {
            "infinitivo":   {"ing": "I shade the drawing with pencil.","esp": "Yo sombreo el dibujo con lápiz."},
            "pasadoSimple": {"ing": "You shaded the eyes from the sun.","esp": "Tú sombreaste los ojos del sol."},
            "participio":   {"ing": "She has shaded the patio.","esp": "Ella ha sombreado el patio."},
            "gerundio":     {"ing": "They are shading the illustrations.","esp": "Ellos están sombreando las ilustraciones."},
            "futuro":       {"ing": "We will shade the windows later.","esp": "Nosotros sombrearemos las ventanas después."},
            "condicional":  {"ing": "That umbrella would shade the area.","esp": "Esa sombrilla sombrearía el área."}
        }
    },
    {
        "ing_inf": "share", "esp_inf": "compartir",
        "pasado_ing": "shared", "pasado_esp": "compartió",
        "participio_ing": "shared", "participio_esp": "compartido",
        "gerundio_ing": "sharing", "gerundio_esp": "compartiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I share my lunch with friends.","esp": "Yo comparto mi almuerzo con amigos."},
            "pasadoSimple": {"ing": "You shared the news yesterday.","esp": "Tú compartiste la noticia ayer."},
            "participio":   {"ing": "She has shared the document.","esp": "Ella ha compartido el documento."},
            "gerundio":     {"ing": "They are sharing the workload.","esp": "Ellos están compartiendo la carga de trabajo."},
            "futuro":       {"ing": "We will share the responsibility.","esp": "Nosotros compartiremos la responsabilidad."},
            "condicional":  {"ing": "That moment would share joy.","esp": "Ese momento compartiría alegría."}
        }
    },
    {
        "ing_inf": "shave", "esp_inf": "afeitar",
        "pasado_ing": "shaved", "pasado_esp": "afeitó",
        "participio_ing": "shaved", "participio_esp": "afeitado",
        "gerundio_ing": "shaving", "gerundio_esp": "afeitando",
        "oraciones": {
            "infinitivo":   {"ing": "I shave every morning.","esp": "Yo me afeito cada mañana."},
            "pasadoSimple": {"ing": "You shaved your head.","esp": "Tú te afeitaste la cabeza."},
            "participio":   {"ing": "She has shaved her legs.","esp": "Ella se ha afeitado las piernas."},
            "gerundio":     {"ing": "They are shaving the wood.","esp": "Ellos están cepillando la madera."},
            "futuro":       {"ing": "We will shave before the wedding.","esp": "Nosotros nos afeitaremos antes de la boda."},
            "condicional":  {"ing": "That razor would shave closely.","esp": "Esa navaja afeitaría al ras."}
        }
    },
    {
        "ing_inf": "shelter", "esp_inf": "albergar",
        "pasado_ing": "sheltered", "pasado_esp": "albergó",
        "participio_ing": "sheltered", "participio_esp": "albergado",
        "gerundio_ing": "sheltering", "gerundio_esp": "albergando",
        "oraciones": {
            "infinitivo":   {"ing": "I shelter homeless people on weekends.","esp": "Yo albergo a personas sin hogar los fines de semana."},
            "pasadoSimple": {"ing": "You sheltered from the storm.","esp": "Tú te resguardaste de la tormenta."},
            "participio":   {"ing": "She has sheltered refugees.","esp": "Ella ha albergado a refugiados."},
            "gerundio":     {"ing": "They are sheltering in place.","esp": "Ellos se están resguardando en su lugar."},
            "futuro":       {"ing": "We will shelter the animals tonight.","esp": "Nosotros albergaremos a los animales esta noche."},
            "condicional":  {"ing": "That cave would shelter anyone.","esp": "Esa cueva albergaría a cualquiera."}
        }
    },
    {
        "ing_inf": "ship", "esp_inf": "enviar",
        "pasado_ing": "shipped", "pasado_esp": "envió",
        "participio_ing": "shipped", "participio_esp": "enviado",
        "gerundio_ing": "shipping", "gerundio_esp": "enviando",
        "oraciones": {
            "infinitivo":   {"ing": "I ship orders every morning.","esp": "Yo envío pedidos cada mañana."},
            "pasadoSimple": {"ing": "You shipped the package yesterday.","esp": "Tú enviaste el paquete ayer."},
            "participio":   {"ing": "She has shipped the product.","esp": "Ella ha enviado el producto."},
            "gerundio":     {"ing": "They are shipping internationally.","esp": "Ellos están enviando al extranjero."},
            "futuro":       {"ing": "We will ship tomorrow.","esp": "Nosotros enviaremos mañana."},
            "condicional":  {"ing": "That company would ship worldwide.","esp": "Esa empresa enviaría a todo el mundo."}
        }
    },
    {
        "ing_inf": "shock", "esp_inf": "conmocionar",
        "pasado_ing": "shocked", "pasado_esp": "conmocionó",
        "participio_ing": "shocked", "participio_esp": "conmocionado",
        "gerundio_ing": "shocking", "gerundio_esp": "conmocionando",
        "oraciones": {
            "infinitivo":   {"ing": "I shock myself with bad decisions.","esp": "Yo me sorprendo con mis malas decisiones."},
            "pasadoSimple": {"ing": "You shocked everyone with the news.","esp": "Tú sorprendiste a todos con la noticia."},
            "participio":   {"ing": "She has shocked the audience.","esp": "Ella ha conmocionado al público."},
            "gerundio":     {"ing": "They are shocking the neighbors.","esp": "Ellos están conmocionando a los vecinos."},
            "futuro":       {"ing": "We will shock them with the result.","esp": "Nosotros los conmocionaremos con el resultado."},
            "condicional":  {"ing": "That ending would shock anyone.","esp": "Ese final conmocionaría a cualquiera."}
        }
    },
    {
        "ing_inf": "shop", "esp_inf": "comprar",
        "pasado_ing": "shopped", "pasado_esp": "compró",
        "participio_ing": "shopped", "participio_esp": "comprado",
        "gerundio_ing": "shopping", "gerundio_esp": "comprando",
        "oraciones": {
            "infinitivo":   {"ing": "I shop for groceries on Saturdays.","esp": "Yo compro comestibles los sábados."},
            "pasadoSimple": {"ing": "You shopped online yesterday.","esp": "Tú compraste en línea ayer."},
            "participio":   {"ing": "She has shopped at that store.","esp": "Ella ha comprado en esa tienda."},
            "gerundio":     {"ing": "They are shopping for bargains.","esp": "Ellos están buscando ofertas."},
            "futuro":       {"ing": "We will shop tomorrow morning.","esp": "Nosotros compraremos mañana por la mañana."},
            "condicional":  {"ing": "That mall would attract any shopper.","esp": "Ese centro comercial atraería a cualquier comprador."}
        }
    },
    {
        "ing_inf": "shout", "esp_inf": "gritar",
        "pasado_ing": "shouted", "pasado_esp": "gritó",
        "participio_ing": "shouted", "participio_esp": "gritado",
        "gerundio_ing": "shouting", "gerundio_esp": "gritando",
        "oraciones": {
            "infinitivo":   {"ing": "I shout when I'm angry.","esp": "Yo grito cuando estoy enojado."},
            "pasadoSimple": {"ing": "You shouted at the referee.","esp": "Tú le gritaste al árbitro."},
            "participio":   {"ing": "She has shouted for help.","esp": "Ella ha gritado pidiendo ayuda."},
            "gerundio":     {"ing": "They are shouting slogans.","esp": "Ellos están gritando consignas."},
            "futuro":       {"ing": "We will shout your name.","esp": "Nosotros gritaremos tu nombre."},
            "condicional":  {"ing": "That announcement would shout loud.","esp": "Ese anuncio gritaría fuerte."}
        }
    },
    {
        "ing_inf": "show", "esp_inf": "mostrar",
        "pasado_ing": "showed", "pasado_esp": "mostró",
        "participio_ing": "shown", "participio_esp": "mostrado",
        "gerundio_ing": "showing", "gerundio_esp": "mostrando",
        "oraciones": {
            "infinitivo":   {"ing": "I show my ID at the door.","esp": "Yo muestro mi identificación en la puerta."},
            "pasadoSimple": {"ing": "You showed the photos yesterday.","esp": "Tú mostraste las fotos ayer."},
            "participio":   {"ing": "She has shown great talent.","esp": "Ella ha mostrado gran talento."},
            "gerundio":     {"ing": "They are showing the new movie.","esp": "Ellos están mostrando la nueva película."},
            "futuro":       {"ing": "We will show you around.","esp": "Nosotros te mostraremos el lugar."},
            "condicional":  {"ing": "That result would show the truth.","esp": "Ese resultado mostraría la verdad."}
        }
    },
    {
        "ing_inf": "signal", "esp_inf": "señalar",
        "pasado_ing": "signaled", "pasado_esp": "señaló",
        "participio_ing": "signaled", "participio_esp": "señalado",
        "gerundio_ing": "signaling", "gerundio_esp": "señalando",
        "oraciones": {
            "infinitivo":   {"ing": "I signal before turning.","esp": "Yo señalo antes de girar."},
            "pasadoSimple": {"ing": "You signaled the waiter.","esp": "Tú le hiciste una señal al mesero."},
            "participio":   {"ing": "She has signaled her intentions.","esp": "Ella ha señalado sus intenciones."},
            "gerundio":     {"ing": "They are signaling for help.","esp": "Ellos están pidiendo ayuda con señales."},
            "futuro":       {"ing": "We will signal the start.","esp": "Nosotros señalaremos el inicio."},
            "condicional":  {"ing": "That light would signal danger.","esp": "Esa luz señalaría peligro."}
        }
    },
    {
        "ing_inf": "sin", "esp_inf": "pecar",
        "pasado_ing": "sinned", "pasado_esp": "pecó",
        "participio_ing": "sinned", "participio_esp": "pecado",
        "gerundio_ing": "sinning", "gerundio_esp": "pecando",
        "oraciones": {
            "infinitivo":   {"ing": "I sin less than I used to.","esp": "Yo peco menos que antes."},
            "pasadoSimple": {"ing": "You sinned against them.","esp": "Tú pecaste contra ellos."},
            "participio":   {"ing": "She has sinned before.","esp": "Ella ha pecado antes."},
            "gerundio":     {"ing": "They are sinning repeatedly.","esp": "Ellos están pecando repetidamente."},
            "futuro":       {"ing": "We will sin no more.","esp": "Nosotros no pecaremos más."},
            "condicional":  {"ing": "That act would be a sin against nature.","esp": "Ese acto sería un pecado contra la naturaleza."}
        }
    },
    {
        "ing_inf": "skip", "esp_inf": "saltar",
        "pasado_ing": "skipped", "pasado_esp": "saltó",
        "participio_ing": "skipped", "participio_esp": "saltado",
        "gerundio_ing": "skipping", "gerundio_esp": "saltando",
        "oraciones": {
            "infinitivo":   {"ing": "I skip breakfast sometimes.","esp": "Yo salto el desayuno a veces."},
            "pasadoSimple": {"ing": "You skipped class yesterday.","esp": "Tú faltaste a clase ayer."},
            "participio":   {"ing": "She has skipped the line.","esp": "Ella se ha saltado la fila."},
            "gerundio":     {"ing": "They are skipping rope.","esp": "Ellos están saltando la cuerda."},
            "futuro":       {"ing": "We will skip the meeting.","esp": "Nosotros nos saltaremos la reunión."},
            "condicional":  {"ing": "That step would skip over the issue.","esp": "Ese paso saltaría el problema."}
        }
    },
    {
        "ing_inf": "slap", "esp_inf": "abofetear",
        "pasado_ing": "slapped", "pasado_esp": "abofeteó",
        "participio_ing": "slapped", "participio_esp": "abofeteado",
        "gerundio_ing": "slapping", "gerundio_esp": "abofeteando",
        "oraciones": {
            "infinitivo":   {"ing": "I slap the table when angry.","esp": "Yo golpeo la mesa cuando estoy enojado."},
            "pasadoSimple": {"ing": "You slapped him in the face.","esp": "Tú lo abofeteaste en la cara."},
            "participio":   {"ing": "She has slapped the thief.","esp": "Ella ha abofeteado al ladrón."},
            "gerundio":     {"ing": "They are slapping high fives.","esp": "Ellos se están dando palmadas de celebración."},
            "futuro":       {"ing": "We will slap the paint on.","esp": "Nosotros aplicaremos la pintura a golpes."},
            "condicional":  {"ing": "That wave would slap hard.","esp": "Esa ola golpearía con fuerza."}
        }
    },
    {
        "ing_inf": "slide", "esp_inf": "deslizar",
        "pasado_ing": "slid", "pasado_esp": "deslizó",
        "participio_ing": "slid", "participio_esp": "deslizado",
        "gerundio_ing": "sliding", "gerundio_esp": "deslizando",
        "oraciones": {
            "infinitivo":   {"ing": "I slide into home plate.","esp": "Yo me deslizo hasta la base."},
            "pasadoSimple": {"ing": "You slid down the slide.","esp": "Tú te deslizaste por el tobogán."},
            "participio":   {"ing": "She has slid the door open.","esp": "Ella ha deslizado la puerta para abrirla."},
            "gerundio":     {"ing": "They are sliding on the ice.","esp": "Ellos se están deslizando sobre el hielo."},
            "futuro":       {"ing": "We will slide the document.","esp": "Nosotros deslizaremos el documento."},
            "condicional":  {"ing": "That drawer would slide easily.","esp": "Ese cajón se deslizaría fácilmente."}
        }
    },
    {
        "ing_inf": "slip", "esp_inf": "resbalarse",
        "pasado_ing": "slipped", "pasado_esp": "se resbaló",
        "participio_ing": "slipped", "participio_esp": "resbalado",
        "gerundio_ing": "slipping", "gerundio_esp": "resbalándose",
        "futuro_esp": "se resbalará", "cond_esp": "se resbalaría",
        "oraciones": {
            "infinitivo":   {"ing": "I slip on wet floors.","esp": "Yo me resbalo en pisos mojados."},
            "pasadoSimple": {"ing": "You slipped on the ice.","esp": "Tú te resbalaste en el hielo."},
            "participio":   {"ing": "She has slipped on the rug.","esp": "Ella se ha resbalado en la alfombra."},
            "gerundio":     {"ing": "They are slipping notes under the door.","esp": "Ellos están deslizando notas bajo la puerta."},
            "futuro":       {"ing": "We will slip away quietly.","esp": "Nosotros nos escabulliremos en silencio."},
            "condicional":  {"ing": "That plan would slip through.","esp": "Ese plan se colaría."}
        }
    }
]


BLOQUE_20 = [
    {
        "ing_inf": "smile", "esp_inf": "sonreír",
        "pasado_ing": "smiled", "pasado_esp": "sonrió",
        "participio_ing": "smiled", "participio_esp": "sonreído",
        "gerundio_ing": "smiling", "gerundio_esp": "sonriendo",
        "oraciones": {
            "infinitivo":   {"ing": "I smile at strangers sometimes.","esp": "Yo sonrío a desconocidos a veces."},
            "pasadoSimple": {"ing": "You smiled at the camera.","esp": "Tú sonreíste a la cámara."},
            "participio":   {"ing": "She has smiled all morning.","esp": "Ella ha sonreído toda la mañana."},
            "gerundio":     {"ing": "They are smiling at the baby.","esp": "Ellos están sonriendo al bebé."},
            "futuro":       {"ing": "We will smile for the photo.","esp": "Nosotros sonreiremos para la foto."},
            "condicional":  {"ing": "That gift would make anyone smile.","esp": "Ese regalo haría sonreír a cualquiera."}
        }
    },
    {
        "ing_inf": "smoke", "esp_inf": "fumar",
        "pasado_ing": "smoked", "pasado_esp": "fumó",
        "participio_ing": "smoked", "participio_esp": "fumado",
        "gerundio_ing": "smoking", "gerundio_esp": "fumando",
        "oraciones": {
            "infinitivo":   {"ing": "I smoke the meat low and slow.","esp": "Yo ahúmo la carne a fuego lento."},
            "pasadoSimple": {"ing": "You smoked salmon last weekend.","esp": "Tú ahumaste salmón el fin de semana pasado."},
            "participio":   {"ing": "She has smoked for ten years.","esp": "Ella ha fumado durante diez años."},
            "gerundio":     {"ing": "They are smoking outside.","esp": "Ellos están fumando afuera."},
            "futuro":       {"ing": "We will smoke the brisket tomorrow.","esp": "Nosotros ahumaremos la carne mañana."},
            "condicional":  {"ing": "That wood would smoke well.","esp": "Esa madera ahumaría bien."}
        }
    },
    {
        "ing_inf": "snap", "esp_inf": "romper",
        "pasado_ing": "snapped", "pasado_esp": "rompió",
        "participio_ing": "snapped", "participio_esp": "roto",
        "gerundio_ing": "snapping", "gerundio_esp": "rompiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I snap photos of nature.","esp": "Yo tomo fotos de la naturaleza."},
            "pasadoSimple": {"ing": "You snapped at your sister.","esp": "Tú le gritaste a tu hermana."},
            "participio":   {"ing": "She has snapped the twig.","esp": "Ella ha roto la ramita."},
            "gerundio":     {"ing": "They are snapping their fingers.","esp": "Ellos están chasqueando los dedos."},
            "futuro":       {"ing": "We will snap the candy in half.","esp": "Nosotros partiremos el caramelo por la mitad."},
            "condicional":  {"ing": "That branch would snap easily.","esp": "Esa rama se rompería fácilmente."}
        }
    },
    {
        "ing_inf": "sneeze", "esp_inf": "estornudar",
        "pasado_ing": "sneezed", "pasado_esp": "estornudó",
        "participio_ing": "sneezed", "participio_esp": "estornudado",
        "gerundio_ing": "sneezing", "gerundio_esp": "estornudando",
        "oraciones": {
            "infinitivo":   {"ing": "I sneeze when I'm allergic.","esp": "Yo estornudo cuando estoy alérgico."},
            "pasadoSimple": {"ing": "You sneezed loudly.","esp": "Tú estornudaste fuerte."},
            "participio":   {"ing": "She has sneezed all day.","esp": "Ella ha estornudado todo el día."},
            "gerundio":     {"ing": "They are sneezing nonstop.","esp": "Ellos están estornudando sin parar."},
            "futuro":       {"ing": "We will sneeze from the dust.","esp": "Nosotros estornudaremos por el polvo."},
            "condicional":  {"ing": "That pepper would make anyone sneeze.","esp": "Esa pimienta haría estornudar a cualquiera."}
        }
    },
    {
        "ing_inf": "sniff", "esp_inf": "olfatear",
        "pasado_ing": "sniffed", "pasado_esp": "olfateó",
        "participio_ing": "sniffed", "participio_esp": "olfateado",
        "gerundio_ing": "sniffing", "gerundio_esp": "olfateando",
        "oraciones": {
            "infinitivo":   {"ing": "I sniff the milk before drinking.","esp": "Yo huelo la leche antes de beberla."},
            "pasadoSimple": {"ing": "You sniffed the flowers.","esp": "Tú olíste las flores."},
            "participio":   {"ing": "The dog has sniffed the food.","esp": "El perro ha olfateado la comida."},
            "gerundio":     {"ing": "They are sniffing the air.","esp": "Ellos están olfateando el aire."},
            "futuro":       {"ing": "We will sniff the wine.","esp": "Nosotros oleremos el vino."},
            "condicional":  {"ing": "That smell would make anyone sniff.","esp": "Ese olor haría olfatear a cualquiera."}
        }
    },
    {
        "ing_inf": "soak", "esp_inf": "remojar",
        "pasado_ing": "soaked", "pasado_esp": "remojó",
        "participio_ing": "soaked", "participio_esp": "remojado",
        "gerundio_ing": "soaking", "gerundio_esp": "remojando",
        "oraciones": {
            "infinitivo":   {"ing": "I soak the beans overnight.","esp": "Yo remojo los frijoles durante la noche."},
            "pasadoSimple": {"ing": "You soaked the clothes.","esp": "Tú remojaste la ropa."},
            "participio":   {"ing": "She has soaked the dishes.","esp": "Ella ha remojado los platos."},
            "gerundio":     {"ing": "They are soaking in the hot tub.","esp": "Ellos se están remojando en la tina caliente."},
            "futuro":       {"ing": "We will soak the lentils.","esp": "Nosotros remojaremos las lentejas."},
            "condicional":  {"ing": "That stain would soak in quickly.","esp": "Esa mancha se remojaría rápido."}
        }
    },
    {
        "ing_inf": "solve", "esp_inf": "resolver",
        "pasado_ing": "solved", "pasado_esp": "resolvió",
        "participio_ing": "solved", "participio_esp": "resuelto",
        "gerundio_ing": "solving", "gerundio_esp": "resolviendo",
        "oraciones": {
            "infinitivo":   {"ing": "I solve puzzles on weekends.","esp": "Yo resuelvo rompecabezas los fines de semana."},
            "pasadoSimple": {"ing": "You solved the mystery.","esp": "Tú resolviste el misterio."},
            "participio":   {"ing": "She has solved the equation.","esp": "Ella ha resuelto la ecuación."},
            "gerundio":     {"ing": "They are solving the issue.","esp": "Ellos están resolviendo el problema."},
            "futuro":       {"ing": "We will solve the case.","esp": "Nosotros resolveremos el caso."},
            "condicional":  {"ing": "That clue would solve everything.","esp": "Esa pista resolvería todo."}
        }
    },
    {
        "ing_inf": "sort", "esp_inf": "clasificar",
        "pasado_ing": "sorted", "pasado_esp": "clasificó",
        "participio_ing": "sorted", "participio_esp": "clasificado",
        "gerundio_ing": "sorting", "gerundio_esp": "clasificando",
        "oraciones": {
            "infinitivo":   {"ing": "I sort the laundry by color.","esp": "Yo clasifico la ropa por color."},
            "pasadoSimple": {"ing": "You sorted the mail.","esp": "Tú clasificaste el correo."},
            "participio":   {"ing": "She has sorted the files.","esp": "Ella ha clasificado los archivos."},
            "gerundio":     {"ing": "They are sorting the recyclables.","esp": "Ellos están clasificando los reciclables."},
            "futuro":       {"ing": "We will sort out the details.","esp": "Nosotros aclararemos los detalles."},
            "condicional":  {"ing": "That filter would sort the data.","esp": "Ese filtro clasificaría los datos."}
        }
    },
    {
        "ing_inf": "sound", "esp_inf": "sonar",
        "pasado_ing": "sounded", "pasado_esp": "sonó",
        "participio_ing": "sounded", "participio_esp": "sonado",
        "gerundio_ing": "sounding", "gerundio_esp": "sonando",
        "oraciones": {
            "infinitivo":   {"ing": "I sound professional on calls.","esp": "Yo sueno profesional en las llamadas."},
            "pasadoSimple": {"ing": "You sounded tired yesterday.","esp": "Tú sonabas cansado ayer."},
            "participio":   {"ing": "She has sounded the alarm.","esp": "Ella ha hecho sonar la alarma."},
            "gerundio":     {"ing": "They are sounding confident.","esp": "Ellos están sonando seguros."},
            "futuro":       {"ing": "We will sound the bell.","esp": "Nosotros haremos sonar la campana."},
            "condicional":  {"ing": "That horn would sound loud.","esp": "Esa bocina sonaría fuerte."}
        }
    },
    {
        "ing_inf": "spare", "esp_inf": "ahorrar",
        "pasado_ing": "spared", "pasado_esp": "ahorró",
        "participio_ing": "spared", "participio_esp": "ahorrado",
        "gerundio_ing": "sparing", "gerundio_esp": "ahorrando",
        "oraciones": {
            "infinitivo":   {"ing": "I spare some cash for emergencies.","esp": "Yo ahorro algo de efectivo para emergencias."},
            "pasadoSimple": {"ing": "You spared me the details.","esp": "Tú me ahorraste los detalles."},
            "participio":   {"ing": "She has spared no expense.","esp": "Ella no ha escatimado en gastos."},
            "gerundio":     {"ing": "They are sparing my feelings.","esp": "Ellos están respetando mis sentimientos."},
            "futuro":       {"ing": "We will spare no effort.","esp": "Nosotros no escatimaremos esfuerzos."},
            "condicional":  {"ing": "That tip would spare anyone trouble.","esp": "Ese consejo evitaría problemas a cualquiera."}
        }
    },
    {
        "ing_inf": "sparkle", "esp_inf": "brillar",
        "pasado_ing": "sparkled", "pasado_esp": "brilló",
        "participio_ing": "sparkled", "participio_esp": "brillado",
        "gerundio_ing": "sparkling", "gerundio_esp": "brillando",
        "oraciones": {
            "infinitivo":   {"ing": "I sparkle in the sunlight.","esp": "Yo brillo bajo la luz del sol."},
            "pasadoSimple": {"ing": "You sparkled at the party.","esp": "Tú brillaste en la fiesta."},
            "participio":   {"ing": "Her eyes have sparkled all night.","esp": "Sus ojos han brillado toda la noche."},
            "gerundio":     {"ing": "They are sparkling with excitement.","esp": "Ellos están brillando de emoción."},
            "futuro":       {"ing": "We will sparkle at the wedding.","esp": "Nosotros brillaremos en la boda."},
            "condicional":  {"ing": "That diamond would sparkle brightly.","esp": "Ese diamante brillaría intensamente."}
        }
    },
    {
        "ing_inf": "spell", "esp_inf": "deletrear",
        "pasado_ing": "spelled", "pasado_esp": "deletreó",
        "participio_ing": "spelled", "participio_esp": "deletreado",
        "gerundio_ing": "spelling", "gerundio_esp": "deletreando",
        "oraciones": {
            "infinitivo":   {"ing": "I spell my name clearly.","esp": "Yo deletreo mi nombre con claridad."},
            "pasadoSimple": {"ing": "You spelled the word wrong.","esp": "Tú deletreaste la palabra mal."},
            "participio":   {"ing": "She has spelled success.","esp": "Ella ha significado el éxito."},
            "gerundio":     {"ing": "They are spelling the test.","esp": "Ellos están haciendo el examen de deletreo."},
            "futuro":       {"ing": "We will spell it out.","esp": "Nosotros lo deletrearemos."},
            "condicional":  {"ing": "That move would spell disaster.","esp": "Ese movimiento significaría desastre."}
        }
    },
    {
        "ing_inf": "spill", "esp_inf": "derramar",
        "pasado_ing": "spilled", "pasado_esp": "derramó",
        "participio_ing": "spilled", "participio_esp": "derramado",
        "gerundio_ing": "spilling", "gerundio_esp": "derramando",
        "oraciones": {
            "infinitivo":   {"ing": "I spill coffee on my shirt often.","esp": "Yo derramo café en mi camisa a menudo."},
            "pasadoSimple": {"ing": "You spilled the milk.","esp": "Tú derramaste la leche."},
            "participio":   {"ing": "She has spilled the coffee.","esp": "Ella ha derramado el café."},
            "gerundio":     {"ing": "They are spilling the beans.","esp": "Ellos están revelando el secreto."},
            "futuro":       {"ing": "We will spill the paint.","esp": "Nosotros derramaremos la pintura."},
            "condicional":  {"ing": "That liquid would spill easily.","esp": "Ese líquido se derramaría fácilmente."}
        }
    },
    {
        "ing_inf": "spoil", "esp_inf": "arruinar",
        "pasado_ing": "spoiled", "pasado_esp": "arruinó",
        "participio_ing": "spoiled", "participio_esp": "arruinado",
        "gerundio_ing": "spoiling", "gerundio_esp": "arruinando",
        "oraciones": {
            "infinitivo":   {"ing": "I spoil my dog with treats.","esp": "Yo consiento a mi perro con premios."},
            "pasadoSimple": {"ing": "You spoiled the surprise.","esp": "Tú arruinaste la sorpresa."},
            "participio":   {"ing": "She has spoiled the food.","esp": "Ella ha echado a perder la comida."},
            "gerundio":     {"ing": "They are spoiling the children.","esp": "Ellos están malcriando a los niños."},
            "futuro":       {"ing": "We will spoil the broth.","esp": "Nosotros arruinaremos el caldo."},
            "condicional":  {"ing": "That rain would spoil the picnic.","esp": "Esa lluvia arruinaría el picnic."}
        }
    },
    {
        "ing_inf": "spot", "esp_inf": "distinguir",
        "pasado_ing": "spotted", "pasado_esp": "distinguió",
        "participio_ing": "spotted", "participio_esp": "distinguido",
        "gerundio_ing": "spotting", "gerundio_esp": "distinguiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I spot my friends in the crowd.","esp": "Yo distingo a mis amigos entre la multitud."},
            "pasadoSimple": {"ing": "You spotted the mistake.","esp": "Tú notaste el error."},
            "participio":   {"ing": "She has spotted the celebrity.","esp": "Ella ha visto a la celebridad."},
            "gerundio":     {"ing": "They are spotting the errors.","esp": "Ellos están notando los errores."},
            "futuro":       {"ing": "We will spot the difference.","esp": "Nosotros notaremos la diferencia."},
            "condicional":  {"ing": "That telescope would spot any star.","esp": "Ese telescopio vería cualquier estrella."}
        }
    },
    {
        "ing_inf": "spray", "esp_inf": "rociar",
        "pasado_ing": "sprayed", "pasado_esp": "roció",
        "participio_ing": "sprayed", "participio_esp": "rociado",
        "gerundio_ing": "spraying", "gerundio_esp": "rociando",
        "oraciones": {
            "infinitivo":   {"ing": "I spray perfume before going out.","esp": "Yo me rocío perfume antes de salir."},
            "pasadoSimple": {"ing": "You sprayed the plants yesterday.","esp": "Tú rociaste las plantas ayer."},
            "participio":   {"ing": "She has sprayed the cake.","esp": "Ella ha rociado el pastel."},
            "gerundio":     {"ing": "They are spraying the crops.","esp": "Ellos están rociando los cultivos."},
            "futuro":       {"ing": "We will spray the fence.","esp": "Nosotros rociaremos la valla."},
            "condicional":  {"ing": "That hose would spray far.","esp": "Esa manguera rociaría lejos."}
        }
    },
    {
        "ing_inf": "squash", "esp_inf": "aplastar",
        "pasado_ing": "squashed", "pasado_esp": "aplastó",
        "participio_ing": "squashed", "participio_esp": "aplastado",
        "gerundio_ing": "squashing", "gerundio_esp": "aplastando",
        "oraciones": {
            "infinitivo":   {"ing": "I squash the bug by accident.","esp": "Yo aplasto el bicho por accidente."},
            "pasadoSimple": {"ing": "You squashed the can.","esp": "Tú aplastaste la lata."},
            "participio":   {"ing": "She has squashed the rumor.","esp": "Ella ha desmentido el rumor."},
            "gerundio":     {"ing": "They are squashing grapes.","esp": "Ellos están pisando uvas."},
            "futuro":       {"ing": "We will squash the bugs.","esp": "Nosotros aplastaremos los bichos."},
            "condicional":  {"ing": "That bug would squash easily.","esp": "Ese bicho se aplastaría fácilmente."}
        }
    },
    {
        "ing_inf": "squeak", "esp_inf": "chirriar",
        "pasado_ing": "squeaked", "pasado_esp": "chirrió",
        "participio_ing": "squeaked", "participio_esp": "chirriado",
        "gerundio_ing": "squeaking", "gerundio_esp": "chirriando",
        "oraciones": {
            "infinitivo":   {"ing": "I squeak when I'm nervous.","esp": "Yo chillo cuando estoy nervioso."},
            "pasadoSimple": {"ing": "You squeaked the toy.","esp": "Tú chillaste el juguete."},
            "participio":   {"ing": "The door has squeaked all day.","esp": "La puerta ha chillado todo el día."},
            "gerundio":     {"ing": "They are squeaking the floor.","esp": "Ellos hacen chillar el piso."},
            "futuro":       {"ing": "We will squeak past the guards.","esp": "Nosotros pasaremos sin ser vistos por los guardias."},
            "condicional":  {"ing": "That mouse would squeak loudly.","esp": "Ese ratón chillaría fuerte."}
        }
    },
    {
        "ing_inf": "squeal", "esp_inf": "chillar",
        "pasado_ing": "squealed", "pasado_esp": "chilló",
        "participio_ing": "squealed", "participio_esp": "chillado",
        "gerundio_ing": "squealing", "gerundio_esp": "chillando",
        "oraciones": {
            "infinitivo":   {"ing": "I squeal with delight at surprises.","esp": "Yo chillo de emoción con las sorpresas."},
            "pasadoSimple": {"ing": "You squealed at the sight.","esp": "Tú chillaste al verlo."},
            "participio":   {"ing": "She has squealed on her brother.","esp": "Ella ha delatado a su hermano."},
            "gerundio":     {"ing": "They are squealing in fear.","esp": "Ellos están chillando de miedo."},
            "futuro":       {"ing": "We will squeal with laughter.","esp": "Nosotros chillaremos de risa."},
            "condicional":  {"ing": "That brake would squeal loudly.","esp": "Ese freno chillaría fuerte."}
        }
    },
    {
        "ing_inf": "squeeze", "esp_inf": "apretar",
        "pasado_ing": "squeezed", "pasado_esp": "apretó",
        "participio_ing": "squeezed", "participio_esp": "apretado",
        "gerundio_ing": "squeezing", "gerundio_esp": "apretando",
        "oraciones": {
            "infinitivo":   {"ing": "I squeeze the lemon for juice.","esp": "Yo exprimo el limón para el jugo."},
            "pasadoSimple": {"ing": "You squeezed my hand.","esp": "Tú me apretaste la mano."},
            "participio":   {"ing": "She has squeezed the orange.","esp": "Ella ha exprimido la naranja."},
            "gerundio":     {"ing": "They are squeezing into the car.","esp": "Ellos se están apretando en el coche."},
            "futuro":       {"ing": "We will squeeze through the gap.","esp": "Nosotros pasaremos apretados por la brecha."},
            "condicional":  {"ing": "That tube would squeeze easily.","esp": "Ese tubo se apretaría fácilmente."}
        }
    },
    {
        "ing_inf": "stab", "esp_inf": "apuñalar",
        "pasado_ing": "stabbed", "pasado_esp": "apuñaló",
        "participio_ing": "stabbed", "participio_esp": "apuñalado",
        "gerundio_ing": "stabbing", "gerundio_esp": "apuñalando",
        "oraciones": {
            "infinitivo":   {"ing": "I stab the straw into the juice box.","esp": "Yo pincho el popote en la caja de jugo."},
            "pasadoSimple": {"ing": "You stabbed the meat with a fork.","esp": "Tú pinchaste la carne con un tenedor."},
            "participio":   {"ing": "She has stabbed the vegetables.","esp": "Ella ha cortado las verduras."},
            "gerundio":     {"ing": "They are stabbing at the enemy.","esp": "Ellos están atacando al enemigo."},
            "futuro":       {"ing": "We will stab the firewood.","esp": "Nosotros cortaremos la leña."},
            "condicional":  {"ing": "That knife would stab deep.","esp": "Ese cuchillo apuñalaría profundo."}
        }
    },
    {
        "ing_inf": "stain", "esp_inf": "manchar",
        "pasado_ing": "stained", "pasado_esp": "manchó",
        "participio_ing": "stained", "participio_esp": "manchado",
        "gerundio_ing": "staining", "gerundio_esp": "manchando",
        "oraciones": {
            "infinitivo":   {"ing": "I stain the wood dark brown.","esp": "Yo tiño la madera de marrón oscuro."},
            "pasadoSimple": {"ing": "You stained the carpet.","esp": "Tú manchaste la alfombra."},
            "participio":   {"ing": "She has stained the fabric.","esp": "Ella ha manchado la tela."},
            "gerundio":     {"ing": "They are staining the fence.","esp": "Ellos están tiñendo la valla."},
            "futuro":       {"ing": "We will stain the deck.","esp": "Nosotros teñiremos la cubierta."},
            "condicional":  {"ing": "That juice would stain easily.","esp": "Ese jugo mancharía fácilmente."}
        }
    },
    {
        "ing_inf": "stamp", "esp_inf": "estampar",
        "pasado_ing": "stamped", "pasado_esp": "estampó",
        "participio_ing": "stamped", "participio_esp": "estampado",
        "gerundio_ing": "stamping", "gerundio_esp": "estampando",
        "oraciones": {
            "infinitivo":   {"ing": "I stamp the envelope with my address.","esp": "Yo sello el sobre con mi dirección."},
            "pasadoSimple": {"ing": "You stamped your foot angrily.","esp": "Tú pateaste el piso con enojo."},
            "participio":   {"ing": "She has stamped the document.","esp": "Ella ha sellado el documento."},
            "gerundio":     {"ing": "They are stamping the passports.","esp": "Ellos están sellando los pasaportes."},
            "futuro":       {"ing": "We will stamp out the fire.","esp": "Nosotros apagaremos el fuego."},
            "condicional":  {"ing": "That logo would stamp perfectly.","esp": "Ese logo sellaría perfectamente."}
        }
    },
    {
        "ing_inf": "stare", "esp_inf": "mirar",
        "pasado_ing": "stared", "pasado_esp": "miró",
        "participio_ing": "stared", "participio_esp": "mirado",
        "gerundio_ing": "staring", "gerundio_esp": "mirando",
        "oraciones": {
            "infinitivo":   {"ing": "I stare at the stars.","esp": "Yo miro fijamente las estrellas."},
            "pasadoSimple": {"ing": "You stared at him.","esp": "Tú lo miraste fijamente."},
            "participio":   {"ing": "She has stared at the screen.","esp": "Ella ha mirado fijamente la pantalla."},
            "gerundio":     {"ing": "They are staring at me.","esp": "Ellos me están mirando fijamente."},
            "futuro":       {"ing": "We will stare at the view.","esp": "Nosotros miraremos fijamente la vista."},
            "condicional":  {"ing": "That statue would stare at anyone.","esp": "Esa estatua miraría fijamente a cualquiera."}
        }
    },
    {
        "ing_inf": "start", "esp_inf": "comenzar",
        "pasado_ing": "started", "pasado_esp": "comenzó",
        "participio_ing": "started", "participio_esp": "comenzado",
        "gerundio_ing": "starting", "gerundio_esp": "comenzando",
        "oraciones": {
            "infinitivo":   {"ing": "I start work at nine.","esp": "Yo comienzo el trabajo a las nueve."},
            "pasadoSimple": {"ing": "You started the engine.","esp": "Tú arrancaste el motor."},
            "participio":   {"ing": "She has started a new hobby.","esp": "Ella ha comenzado un pasatiempo nuevo."},
            "gerundio":     {"ing": "They are starting the project.","esp": "Ellos están comenzando el proyecto."},
            "futuro":       {"ing": "We will start tomorrow.","esp": "Nosotros comenzaremos mañana."},
            "condicional":  {"ing": "That event would start at noon.","esp": "Ese evento comenzaría al mediodía."}
        }
    },
    {
        "ing_inf": "stay", "esp_inf": "quedarse",
        "pasado_ing": "stayed", "pasado_esp": "se quedó",
        "participio_ing": "stayed", "participio_esp": "quedado",
        "gerundio_ing": "staying", "gerundio_esp": "quedándose",
        "futuro_esp": "se quedará", "cond_esp": "se quedaría",
        "oraciones": {
            "infinitivo":   {"ing": "I stay home on weekends.","esp": "Yo me quedo en casa los fines de semana."},
            "pasadoSimple": {"ing": "You stayed at a hotel.","esp": "Tú te quedaste en un hotel."},
            "participio":   {"ing": "She has stayed calm.","esp": "Ella se ha mantenido calmada."},
            "gerundio":     {"ing": "They are staying for dinner.","esp": "Ellos se quedan a cenar."},
            "futuro":       {"ing": "We will stay in touch.","esp": "Nosotros nos mantendremos en contacto."},
            "condicional":  {"ing": "That stain would stay forever.","esp": "Esa mancha se quedaría para siempre."}
        }
    },
    {
        "ing_inf": "steer", "esp_inf": "dirigir",
        "pasado_ing": "steered", "pasado_esp": "dirigió",
        "participio_ing": "steered", "participio_esp": "dirigido",
        "gerundio_ing": "steering", "gerundio_esp": "dirigiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I steer the conversation carefully.","esp": "Yo dirijo la conversación con cuidado."},
            "pasadoSimple": {"ing": "You steered the boat to shore.","esp": "Tú dirigiste el barco a la orilla."},
            "participio":   {"ing": "She has steered the company well.","esp": "Ella ha dirigido bien la empresa."},
            "gerundio":     {"ing": "They are steering the discussion.","esp": "Ellos están dirigiendo la discusión."},
            "futuro":       {"ing": "We will steer clear of trouble.","esp": "Nosotros evitaremos los problemas."},
            "condicional":  {"ing": "That advice would steer anyone right.","esp": "Ese consejo guiaría a cualquiera correctamente."}
        }
    },
    {
        "ing_inf": "step", "esp_inf": "pisar",
        "pasado_ing": "stepped", "pasado_esp": "pisó",
        "participio_ing": "stepped", "participio_esp": "pisado",
        "gerundio_ing": "stepping", "gerundio_esp": "pisando",
        "oraciones": {
            "infinitivo":   {"ing": "I step on the scale daily.","esp": "Yo me subo a la báscula a diario."},
            "pasadoSimple": {"ing": "You stepped on the bug.","esp": "Tú pisaste al bicho."},
            "participio":   {"ing": "She has stepped forward.","esp": "Ella ha dado un paso adelante."},
            "gerundio":     {"ing": "They are stepping out.","esp": "Ellos están saliendo."},
            "futuro":       {"ing": "We will step aside.","esp": "Nosotros nos haremos a un lado."},
            "condicional":  {"ing": "That move would step on toes.","esp": "Ese movimiento pisaría callos."}
        }
    },
    {
        "ing_inf": "stir", "esp_inf": "revolver",
        "pasado_ing": "stirred", "pasado_esp": "revolvió",
        "participio_ing": "stirred", "participio_esp": "revuelto",
        "gerundio_ing": "stirring", "gerundio_esp": "revolviendo",
        "oraciones": {
            "infinitivo":   {"ing": "I stir the soup gently.","esp": "Yo revuelvo la sopa con cuidado."},
            "pasadoSimple": {"ing": "You stirred the coffee.","esp": "Tú revolviste el café."},
            "participio":   {"ing": "She has stirred the paint.","esp": "Ella ha revuelto la pintura."},
            "gerundio":     {"ing": "They are stirring the batter.","esp": "Ellos están revolviendo la masa."},
            "futuro":       {"ing": "We will stir up trouble.","esp": "Nosotros causaremos problemas."},
            "condicional":  {"ing": "That speech would stir emotions.","esp": "Ese discurso despertaría emociones."}
        }
    },
    {
        "ing_inf": "stitch", "esp_inf": "coser",
        "pasado_ing": "stitched", "pasado_esp": "cosió",
        "participio_ing": "stitched", "participio_esp": "cosido",
        "gerundio_ing": "stitching", "gerundio_esp": "cosiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I stitch my own clothes.","esp": "Yo coso mi propia ropa."},
            "pasadoSimple": {"ing": "You stitched the wound shut.","esp": "Tú cosiste la herida cerrada."},
            "participio":   {"ing": "She has stitched a beautiful quilt.","esp": "Ella ha cosido una colcha hermosa."},
            "gerundio":     {"ing": "They are stitching the logo.","esp": "Ellos están bordando el logo."},
            "futuro":       {"ing": "We will stitch the hem tomorrow.","esp": "Nosotros coseremos el dobladillo mañana."},
            "condicional":  {"ing": "That thread would stitch easily.","esp": "Ese hilo cosería fácilmente."}
        }
    }
]


BLOQUE_IRREGULARES_1 = [
    {
        "ing_inf": "be", "esp_inf": "ser/estar",
        "pasado_ing": "was/were", "pasado_esp": "fue/estuvo",
        "participio_ing": "been", "participio_esp": "sido",
        "gerundio_ing": "being", "gerundio_esp": "siendo",
        "oraciones": {
            "infinitivo":   {"ing": "I am a teacher.","esp": "Yo soy profesor."},
            "pasadoSimple": {"ing": "You were right.","esp": "Tú estabas en lo correcto."},
            "participio":   {"ing": "She has been working all day.","esp": "Ella ha estado trabajando todo el día."},
            "gerundio":     {"ing": "They are playing outside.","esp": "Ellos están jugando afuera."},
            "futuro":       {"ing": "We will be there soon.","esp": "Nosotros estaremos allí pronto."},
            "condicional":  {"ing": "That would be great.","esp": "Eso sería genial."}
        }
    },
    {
        "ing_inf": "become", "esp_inf": "convertirse",
        "pasado_ing": "became", "pasado_esp": "se convirtió",
        "participio_ing": "become", "participio_esp": "convertido",
        "gerundio_ing": "becoming", "gerundio_esp": "convirtiéndose",
        "futuro_esp": "se convertirá", "cond_esp": "se convertiría",
        "oraciones": {
            "infinitivo":   {"ing": "I become hungry at noon.","esp": "Yo me pongo hambriento al mediodía."},
            "pasadoSimple": {"ing": "You became a doctor.","esp": "Tú te convertiste en médico."},
            "participio":   {"ing": "She has become famous.","esp": "Ella se ha vuelto famosa."},
            "gerundio":     {"ing": "They are becoming friends.","esp": "Ellos se están haciendo amigos."},
            "futuro":       {"ing": "We will become parents.","esp": "Nosotros nos convertiremos en padres."},
            "condicional":  {"ing": "That would become a problem.","esp": "Eso se volvería un problema."}
        }
    },
    {
        "ing_inf": "begin", "esp_inf": "comenzar",
        "pasado_ing": "began", "pasado_esp": "comenzó",
        "participio_ing": "begun", "participio_esp": "comenzado",
        "gerundio_ing": "beginning", "gerundio_esp": "comenzando",
        "oraciones": {
            "infinitivo":   {"ing": "I begin work at nine.","esp": "Yo comienzo a trabajar a las nueve."},
            "pasadoSimple": {"ing": "You began speaking too fast.","esp": "Tú comenzaste a hablar demasiado rápido."},
            "participio":   {"ing": "She has begun the project.","esp": "Ella ha comenzado el proyecto."},
            "gerundio":     {"ing": "They are beginning the lesson.","esp": "Ellos están comenzando la lección."},
            "futuro":       {"ing": "We will begin tomorrow.","esp": "Nosotros comenzaremos mañana."},
            "condicional":  {"ing": "That would begin a new era.","esp": "Eso comenzaría una nueva era."}
        }
    },
    {
        "ing_inf": "bite", "esp_inf": "morder",
        "pasado_ing": "bit", "pasado_esp": "mordió",
        "participio_ing": "bitten", "participio_esp": "mordido",
        "gerundio_ing": "biting", "gerundio_esp": "mordiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I bite my nails when nervous.","esp": "Yo me muerdo las uñas cuando estoy nervioso."},
            "pasadoSimple": {"ing": "You bit into the apple.","esp": "Tú mordiste la manzana."},
            "participio":   {"ing": "She has bitten her tongue.","esp": "Ella se ha mordido la lengua."},
            "gerundio":     {"ing": "They are biting their nails.","esp": "Ellos se están mordiendo las uñas."},
            "futuro":       {"ing": "We will bite the bullet.","esp": "Nosotros nos aguantaremos."},
            "condicional":  {"ing": "That dog would bite anyone.","esp": "Ese perro mordería a cualquiera."}
        }
    },
    {
        "ing_inf": "blow", "esp_inf": "soplar",
        "pasado_ing": "blew", "pasado_esp": "sopló",
        "participio_ing": "blown", "participio_esp": "soplado",
        "gerundio_ing": "blowing", "gerundio_esp": "soplando",
        "oraciones": {
            "infinitivo":   {"ing": "I blow out the candles.","esp": "Yo soplo las velas."},
            "pasadoSimple": {"ing": "You blew the whistle.","esp": "Tú soplaste el silbato."},
            "participio":   {"ing": "The wind has blown the leaves.","esp": "El viento ha soplado las hojas."},
            "gerundio":     {"ing": "They are blowing bubbles.","esp": "Ellos están soplando burbujas."},
            "futuro":       {"ing": "We will blow up the balloons.","esp": "Nosotros inflaremos los globos."},
            "condicional":  {"ing": "That fuse would blow easily.","esp": "Ese fusible se fundiría fácilmente."}
        }
    },
    {
        "ing_inf": "break", "esp_inf": "romper",
        "pasado_ing": "broke", "pasado_esp": "rompió",
        "participio_ing": "broken", "participio_esp": "roto",
        "gerundio_ing": "breaking", "gerundio_esp": "rompiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I break the rules sometimes.","esp": "Yo rompo las reglas a veces."},
            "pasadoSimple": {"ing": "You broke the glass.","esp": "Tú rompiste el vaso."},
            "participio":   {"ing": "She has broken the record.","esp": "Ella ha roto el récord."},
            "gerundio":     {"ing": "They are breaking up.","esp": "Ellos están terminando."},
            "futuro":       {"ing": "We will break for lunch.","esp": "Nosotros pararemos para almorzar."},
            "condicional":  {"ing": "That chain would break easily.","esp": "Esa cadena se rompería fácilmente."}
        }
    },
    {
        "ing_inf": "bring", "esp_inf": "traer",
        "pasado_ing": "brought", "pasado_esp": "trajo",
        "participio_ing": "brought", "participio_esp": "traído",
        "gerundio_ing": "bringing", "gerundio_esp": "trayendo",
        "oraciones": {
            "infinitivo":   {"ing": "I bring lunch to work daily.","esp": "Yo traigo almuerzo al trabajo a diario."},
            "pasadoSimple": {"ing": "You brought flowers yesterday.","esp": "Tú trajiste flores ayer."},
            "participio":   {"ing": "She has brought the documents.","esp": "Ella ha traído los documentos."},
            "gerundio":     {"ing": "They are bringing their friends.","esp": "Ellos están trayendo a sus amigos."},
            "futuro":       {"ing": "We will bring dessert.","esp": "Nosotros traeremos postre."},
            "condicional":  {"ing": "That change would bring hope.","esp": "Ese cambio traería esperanza."}
        }
    },
    {
        "ing_inf": "build", "esp_inf": "construir",
        "pasado_ing": "built", "pasado_esp": "construyó",
        "participio_ing": "built", "participio_esp": "construido",
        "gerundio_ing": "building", "gerundio_esp": "construyendo",
        "oraciones": {
            "infinitivo":   {"ing": "I build furniture as a hobby.","esp": "Yo construyo muebles como pasatiempo."},
            "pasadoSimple": {"ing": "You built that house.","esp": "Tú construiste esa casa."},
            "participio":   {"ing": "She has built a business.","esp": "Ella ha construido un negocio."},
            "gerundio":     {"ing": "They are building a wall.","esp": "Ellos están construyendo un muro."},
            "futuro":       {"ing": "We will build a house.","esp": "Nosotros construiremos una casa."},
            "condicional":  {"ing": "That team would build anything.","esp": "Ese equipo construiría cualquier cosa."}
        }
    },
    {
        "ing_inf": "burn", "esp_inf": "quemar",
        "pasado_ing": "burned/burnt", "pasado_esp": "quemó",
        "participio_ing": "burned/burnt", "participio_esp": "quemado",
        "gerundio_ing": "burning", "gerundio_esp": "quemando",
        "oraciones": {
            "infinitivo":   {"ing": "I burn incense at home.","esp": "Yo quemo incienso en casa."},
            "pasadoSimple": {"ing": "You burned the toast.","esp": "Tú quemaste el pan tostado."},
            "participio":   {"ing": "She has burned the letters.","esp": "Ella ha quemado las cartas."},
            "gerundio":     {"ing": "They are burning the trash.","esp": "Ellos están quemando la basura."},
            "futuro":       {"ing": "We will burn the candles.","esp": "Nosotros quemaremos las velas."},
            "condicional":  {"ing": "That fire would burn out.","esp": "Ese fuego se apagaría."}
        }
    },
    {
        "ing_inf": "buy", "esp_inf": "comprar",
        "pasado_ing": "bought", "pasado_esp": "compró",
        "participio_ing": "bought", "participio_esp": "comprado",
        "gerundio_ing": "buying", "gerundio_esp": "comprando",
        "oraciones": {
            "infinitivo":   {"ing": "I buy groceries every week.","esp": "Yo compro comestibles cada semana."},
            "pasadoSimple": {"ing": "You bought a new car.","esp": "Tú compraste un coche nuevo."},
            "participio":   {"ing": "She has bought the tickets.","esp": "Ella ha comprado los boletos."},
            "gerundio":     {"ing": "They are buying a house.","esp": "Ellos están comprando una casa."},
            "futuro":       {"ing": "We will buy later.","esp": "Nosotros compraremos después."},
            "condicional":  {"ing": "That would buy time.","esp": "Eso compraría tiempo."}
        }
    },
    {
        "ing_inf": "catch", "esp_inf": "atrapar",
        "pasado_ing": "caught", "pasado_esp": "atrapó",
        "participio_ing": "caught", "participio_esp": "atrapado",
        "gerundio_ing": "catching", "gerundio_esp": "atrapando",
        "oraciones": {
            "infinitivo":   {"ing": "I catch the bus every morning.","esp": "Yo atrapo el autobús cada mañana."},
            "pasadoSimple": {"ing": "You caught a cold.","esp": "Tú atrapaste un resfriado."},
            "participio":   {"ing": "She has caught the ball.","esp": "Ella ha atrapado la pelota."},
            "gerundio":     {"ing": "They are catching fish.","esp": "Ellos están atrapando peces."},
            "futuro":       {"ing": "We will catch up later.","esp": "Nosotros nos pondremos al día después."},
            "condicional":  {"ing": "That net would catch anything.","esp": "Esa red atraparía cualquier cosa."}
        }
    },
    {
        "ing_inf": "choose", "esp_inf": "elegir",
        "pasado_ing": "chose", "pasado_esp": "eligió",
        "participio_ing": "chosen", "participio_esp": "elegido",
        "gerundio_ing": "choosing", "gerundio_esp": "eligiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I choose my battles carefully.","esp": "Yo elijo mis batallas con cuidado."},
            "pasadoSimple": {"ing": "You chose the red one.","esp": "Tú elegiste el rojo."},
            "participio":   {"ing": "She has chosen her major.","esp": "Ella ha elegido su carrera."},
            "gerundio":     {"ing": "They are choosing the menu.","esp": "Ellos están eligiendo el menú."},
            "futuro":       {"ing": "We will choose soon.","esp": "Nosotros elegiremos pronto."},
            "condicional":  {"ing": "That option would be chosen wisely.","esp": "Esa opción sería elegida con sabiduría."}
        }
    },
    {
        "ing_inf": "come", "esp_inf": "venir",
        "pasado_ing": "came", "pasado_esp": "vino",
        "participio_ing": "come", "participio_esp": "venido",
        "gerundio_ing": "coming", "gerundio_esp": "viniendo",
        "oraciones": {
            "infinitivo":   {"ing": "I come home at six.","esp": "Yo vengo a casa a las seis."},
            "pasadoSimple": {"ing": "You came to the party.","esp": "Tú viniste a la fiesta."},
            "participio":   {"ing": "She has come a long way.","esp": "Ella ha venido de lejos."},
            "gerundio":     {"ing": "They are coming tomorrow.","esp": "Ellos vienen mañana."},
            "futuro":       {"ing": "We will come if invited.","esp": "Nosotros vendremos si nos invitan."},
            "condicional":  {"ing": "That opportunity would come again.","esp": "Esa oportunidad vendría de nuevo."}
        }
    },
    {
        "ing_inf": "cost", "esp_inf": "costar",
        "pasado_ing": "cost", "pasado_esp": "costó",
        "participio_ing": "cost", "participio_esp": "costado",
        "gerundio_ing": "costing", "gerundio_esp": "costando",
        "oraciones": {
            "infinitivo":   {"ing": "I cost the company time.","esp": "Yo le cuesto tiempo a la empresa."},
            "pasadoSimple": {"ing": "It cost too much.","esp": "Costó demasiado."},
            "participio":   {"ing": "The book has cost twenty dollars.","esp": "El libro ha costado veinte dólares."},
            "gerundio":     {"ing": "They are costing too much.","esp": "Ellos están costando demasiado."},
            "futuro":       {"ing": "It will cost more next year.","esp": "Costará más el próximo año."},
            "condicional":  {"ing": "That mistake would cost dearly.","esp": "Ese error costaría caro."}
        }
    },
    {
        "ing_inf": "cut", "esp_inf": "cortar",
        "pasado_ing": "cut", "pasado_esp": "cortó",
        "participio_ing": "cut", "participio_esp": "cortado",
        "gerundio_ing": "cutting", "gerundio_esp": "cortando",
        "oraciones": {
            "infinitivo":   {"ing": "I cut my hair short.","esp": "Yo me corto el pelo corto."},
            "pasadoSimple": {"ing": "You cut the cake.","esp": "Tú cortaste el pastel."},
            "participio":   {"ing": "She has cut the rope.","esp": "Ella ha cortado la cuerda."},
            "gerundio":     {"ing": "They are cutting the grass.","esp": "Ellos están cortando el césped."},
            "futuro":       {"ing": "We will cut the budget.","esp": "Nosotros recortaremos el presupuesto."},
            "condicional":  {"ing": "That knife would cut easily.","esp": "Ese cuchillo cortaría fácilmente."}
        }
    },
    {
        "ing_inf": "deal", "esp_inf": "tratar",
        "pasado_ing": "dealt", "pasado_esp": "trató",
        "participio_ing": "dealt", "participio_esp": "tratado",
        "gerundio_ing": "dealing", "gerundio_esp": "tratando",
        "oraciones": {
            "infinitivo":   {"ing": "I deal with problems calmly.","esp": "Yo trato los problemas con calma."},
            "pasadoSimple": {"ing": "You dealt the cards.","esp": "Tú repartiste las cartas."},
            "participio":   {"ing": "She has dealt with the issue.","esp": "Ella ha tratado el problema."},
            "gerundio":     {"ing": "They are dealing honestly.","esp": "Ellos están tratando honestamente."},
            "futuro":       {"ing": "We will deal with it tomorrow.","esp": "Nosotros lo trataremos mañana."},
            "condicional":  {"ing": "That would deal a heavy blow.","esp": "Eso asestaría un golpe duro."}
        }
    },
    {
        "ing_inf": "dig", "esp_inf": "cavar",
        "pasado_ing": "dug", "pasado_esp": "cavó",
        "participio_ing": "dug", "participio_esp": "cavado",
        "gerundio_ing": "digging", "gerundio_esp": "cavando",
        "oraciones": {
            "infinitivo":   {"ing": "I dig gardening on weekends.","esp": "Yo me dedico a la jardinería los fines de semana."},
            "pasadoSimple": {"ing": "You dug a hole yesterday.","esp": "Tú cavaste un hoyo ayer."},
            "participio":   {"ing": "She has dug up the treasure.","esp": "Ella ha desenterrado el tesoro."},
            "gerundio":     {"ing": "They are digging the foundation.","esp": "Ellos están cavando los cimientos."},
            "futuro":       {"ing": "We will dig deeper.","esp": "Nosotros cavaremos más profundo."},
            "condicional":  {"ing": "That dog would dig anywhere.","esp": "Ese perro cavaría en cualquier parte."}
        }
    },
    {
        "ing_inf": "do", "esp_inf": "hacer",
        "pasado_ing": "did", "pasado_esp": "hizo",
        "participio_ing": "done", "participio_esp": "hecho",
        "gerundio_ing": "doing", "gerundio_esp": "haciendo",
        "futuro_esp": "hará", "cond_esp": "haría",
        "oraciones": {
            "infinitivo":   {"ing": "I do my best every day.","esp": "Yo hago mi mejor esfuerzo cada día."},
            "pasadoSimple": {"ing": "You did a great job.","esp": "Tú hiciste un gran trabajo."},
            "participio":   {"ing": "She has done the homework.","esp": "Ella ha hecho la tarea."},
            "gerundio":     {"ing": "They are doing research.","esp": "Ellos están haciendo investigación."},
            "futuro":       {"ing": "We will do our best.","esp": "Nosotros haremos nuestro mejor esfuerzo."},
            "condicional":  {"ing": "That would do the trick.","esp": "Eso haría el truco."}
        }
    },
    {
        "ing_inf": "draw", "esp_inf": "dibujar",
        "pasado_ing": "drew", "pasado_esp": "dibujó",
        "participio_ing": "drawn", "participio_esp": "dibujado",
        "gerundio_ing": "drawing", "gerundio_esp": "dibujando",
        "oraciones": {
            "infinitivo":   {"ing": "I draw cartoons in my spare time.","esp": "Yo dibujo caricaturas en mi tiempo libre."},
            "pasadoSimple": {"ing": "You drew a beautiful picture.","esp": "Tú dibujaste una imagen hermosa."},
            "participio":   {"ing": "She has drawn the blueprints.","esp": "Ella ha dibujado los planos."},
            "gerundio":     {"ing": "They are drawing conclusions.","esp": "Ellos están sacando conclusiones."},
            "futuro":       {"ing": "We will draw the winner.","esp": "Nosotros sortearemos al ganador."},
            "condicional":  {"ing": "That artist would draw anything.","esp": "Ese artista dibujaría cualquier cosa."}
        }
    },
    {
        "ing_inf": "drink", "esp_inf": "beber",
        "pasado_ing": "drank", "pasado_esp": "bebió",
        "participio_ing": "drunk", "participio_esp": "bebido",
        "gerundio_ing": "drinking", "gerundio_esp": "bebiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I drink coffee every morning.","esp": "Yo bebo café cada mañana."},
            "pasadoSimple": {"ing": "You drank too much last night.","esp": "Tú bebiste demasiado anoche."},
            "participio":   {"ing": "She has drunk all the juice.","esp": "Ella se ha bebido todo el jugo."},
            "gerundio":     {"ing": "They are drinking tea.","esp": "Ellos están bebiendo té."},
            "futuro":       {"ing": "We will drink to that.","esp": "Nosotros brindaremos por eso."},
            "condicional":  {"ing": "That water would drink well.","esp": "Esa agua se bebería bien."}
        }
    },
    {
        "ing_inf": "drive", "esp_inf": "conducir",
        "pasado_ing": "drove", "pasado_esp": "condujo",
        "participio_ing": "driven", "participio_esp": "conducido",
        "gerundio_ing": "driving", "gerundio_esp": "conduciendo",
        "oraciones": {
            "infinitivo":   {"ing": "I drive to work every day.","esp": "Yo conduzco al trabajo cada día."},
            "pasadoSimple": {"ing": "You drove all night.","esp": "Tú condujiste toda la noche."},
            "participio":   {"ing": "She has driven across the country.","esp": "Ella ha conducido por todo el país."},
            "gerundio":     {"ing": "They are driving to the beach.","esp": "Ellos están conduciendo a la playa."},
            "futuro":       {"ing": "We will drive carefully.","esp": "Nosotros conduciremos con cuidado."},
            "condicional":  {"ing": "That car would drive smoothly.","esp": "Ese coche se conduciría suavemente."}
        }
    },
    {
        "ing_inf": "eat", "esp_inf": "comer",
        "pasado_ing": "ate", "pasado_esp": "comió",
        "participio_ing": "eaten", "participio_esp": "comido",
        "gerundio_ing": "eating", "gerundio_esp": "comiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I eat breakfast at seven.","esp": "Yo desayuno a las siete."},
            "pasadoSimple": {"ing": "You ate too much cake.","esp": "Tú comiste demasiado pastel."},
            "participio":   {"ing": "She has eaten all the sushi.","esp": "Ella se ha comido todo el sushi."},
            "gerundio":     {"ing": "They are eating dinner now.","esp": "Ellos están cenando ahora."},
            "futuro":       {"ing": "We will eat before the movie.","esp": "Nosotros comeremos antes de la película."},
            "condicional":  {"ing": "That dish would eat well.","esp": "Ese plato se comería bien."}
        }
    },
    {
        "ing_inf": "fall", "esp_inf": "caerse",
        "pasado_ing": "fell", "pasado_esp": "se cayó",
        "participio_ing": "fallen", "participio_esp": "caído",
        "gerundio_ing": "falling", "gerundio_esp": "cayéndose",
        "futuro_esp": "se caerá", "cond_esp": "se caería",
        "oraciones": {
            "infinitivo":   {"ing": "I fall asleep easily on the couch.","esp": "Yo me duermo fácilmente en el sofá."},
            "pasadoSimple": {"ing": "You fell down the stairs.","esp": "Tú te caíste por las escaleras."},
            "participio":   {"ing": "She has fallen in love.","esp": "Ella se ha enamorado."},
            "gerundio":     {"ing": "They are falling behind.","esp": "Ellos se están quedando atrás."},
            "futuro":       {"ing": "We will fall asleep soon.","esp": "Nosotros nos dormiremos pronto."},
            "condicional":  {"ing": "That tree would fall in the storm.","esp": "Ese árbol caería en la tormenta."}
        }
    },
    {
        "ing_inf": "feed", "esp_inf": "alimentar",
        "pasado_ing": "fed", "pasado_esp": "alimentó",
        "participio_ing": "fed", "participio_esp": "alimentado",
        "gerundio_ing": "feeding", "gerundio_esp": "alimentando",
        "oraciones": {
            "infinitivo":   {"ing": "I feed my dog twice a day.","esp": "Yo alimento a mi perro dos veces al día."},
            "pasadoSimple": {"ing": "You fed the baby at midnight.","esp": "Tú alimentaste al bebé a medianoche."},
            "participio":   {"ing": "She has fed the birds all winter.","esp": "Ella ha alimentado a los pájaros todo el invierno."},
            "gerundio":     {"ing": "They are feeding the homeless.","esp": "Ellos están alimentando a los sin techo."},
            "futuro":       {"ing": "We will feed the family tonight.","esp": "Nosotros alimentaremos a la familia esta noche."},
            "condicional":  {"ing": "That machine would feed automatically.","esp": "Esa máquina alimentaría automáticamente."}
        }
    },
    {
        "ing_inf": "feel", "esp_inf": "sentir",
        "pasado_ing": "felt", "pasado_esp": "sintió",
        "participio_ing": "felt", "participio_esp": "sentido",
        "gerundio_ing": "feeling", "gerundio_esp": "sintiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I feel happy today.","esp": "Yo me siento feliz hoy."},
            "pasadoSimple": {"ing": "You felt the earthquake.","esp": "Tú sentiste el terremoto."},
            "participio":   {"ing": "She has felt better lately.","esp": "Ella se ha sentido mejor últimamente."},
            "gerundio":     {"ing": "They are feeling tired.","esp": "Ellos se están sintiendo cansados."},
            "futuro":       {"ing": "We will feel better tomorrow.","esp": "Nosotros nos sentiremos mejor mañana."},
            "condicional":  {"ing": "That fabric would feel soft.","esp": "Esa tela se sentiría suave."}
        }
    },
    {
        "ing_inf": "fight", "esp_inf": "pelear",
        "pasado_ing": "fought", "pasado_esp": "peleó",
        "participio_ing": "fought", "participio_esp": "peleado",
        "gerundio_ing": "fighting", "gerundio_esp": "peleando",
        "oraciones": {
            "infinitivo":   {"ing": "I fight for what I believe.","esp": "Yo peleo por lo que creo."},
            "pasadoSimple": {"ing": "You fought bravely yesterday.","esp": "Tú peleaste con valentía ayer."},
            "participio":   {"ing": "She has fought for her rights.","esp": "Ella ha peleado por sus derechos."},
            "gerundio":     {"ing": "They are fighting over money.","esp": "Ellos están peleando por dinero."},
            "futuro":       {"ing": "We will fight for justice.","esp": "Nosotros pelearemos por la justicia."},
            "condicional":  {"ing": "That team would fight to the end.","esp": "Ese equipo pelearía hasta el final."}
        }
    },
    {
        "ing_inf": "find", "esp_inf": "encontrar",
        "pasado_ing": "found", "pasado_esp": "encontró",
        "participio_ing": "found", "participio_esp": "encontrado",
        "gerundio_ing": "finding", "gerundio_esp": "encontrando",
        "oraciones": {
            "infinitivo":   {"ing": "I find errors in every code review.","esp": "Yo encuentro errores en cada revisión."},
            "pasadoSimple": {"ing": "You found your keys yesterday.","esp": "Tú encontraste tus llaves ayer."},
            "participio":   {"ing": "She has found the perfect dress.","esp": "Ella ha encontrado el vestido perfecto."},
            "gerundio":     {"ing": "They are finding solutions.","esp": "Ellos están encontrando soluciones."},
            "futuro":       {"ing": "We will find a way.","esp": "Nosotros encontraremos un camino."},
            "condicional":  {"ing": "That search would find everything.","esp": "Esa búsqueda encontraría todo."}
        }
    },
    {
        "ing_inf": "fly", "esp_inf": "volar",
        "pasado_ing": "flew", "pasado_esp": "voló",
        "participio_ing": "flown", "participio_esp": "volado",
        "gerundio_ing": "flying", "gerundio_esp": "volando",
        "oraciones": {
            "infinitivo":   {"ing": "I fly to Madrid next month.","esp": "Yo vuelo a Madrid el próximo mes."},
            "pasadoSimple": {"ing": "You flew to Paris last year.","esp": "Tú volaste a París el año pasado."},
            "participio":   {"ing": "She has flown over the ocean.","esp": "Ella ha volado sobre el océano."},
            "gerundio":     {"ing": "They are flying kites at the park.","esp": "Ellos están volando cometas en el parque."},
            "futuro":       {"ing": "We will fly first class.","esp": "Nosotros volaremos en primera clase."},
            "condicional":  {"ing": "That bird would fly far.","esp": "Ese pájaro volaría lejos."}
        }
    },
    {
        "ing_inf": "forbid", "esp_inf": "prohibir",
        "pasado_ing": "forbade", "pasado_esp": "prohibió",
        "participio_ing": "forbidden", "participio_esp": "prohibido",
        "gerundio_ing": "forbidding", "gerundio_esp": "prohibiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I forbid my kids from smoking.","esp": "Yo prohíbo a mis hijos fumar."},
            "pasadoSimple": {"ing": "You forbade him to leave.","esp": "Tú le prohibiste salir."},
            "participio":   {"ing": "She has forbidden the use of phones.","esp": "Ella ha prohibido el uso de teléfonos."},
            "gerundio":     {"ing": "They are forbidding access.","esp": "Ellos están prohibiendo el acceso."},
            "futuro":       {"ing": "We will forbid that behavior.","esp": "Nosotros prohibiremos ese comportamiento."},
            "condicional":  {"ing": "That rule would forbid anything.","esp": "Esa regla prohibiría cualquier cosa."}
        }
    },
    {
        "ing_inf": "forget", "esp_inf": "olvidar",
        "pasado_ing": "forgot", "pasado_esp": "olvidó",
        "participio_ing": "forgotten", "participio_esp": "olvidado",
        "gerundio_ing": "forgetting", "gerundio_esp": "olvidando",
        "oraciones": {
            "infinitivo":   {"ing": "I forget names easily.","esp": "Yo olvido nombres fácilmente."},
            "pasadoSimple": {"ing": "You forgot to call me.","esp": "Tú olvidaste llamarme."},
            "participio":   {"ing": "She has forgotten the password.","esp": "Ella ha olvidado la contraseña."},
            "gerundio":     {"ing": "They are forgetting the rules.","esp": "Ellos están olvidando las reglas."},
            "futuro":       {"ing": "We will forget this soon.","esp": "Nosotros olvidaremos esto pronto."},
            "condicional":  {"ing": "That memory would never fade.","esp": "Ese recuerdo nunca se desvanecería."}
        }
    }
]


BLOQUE_IRREGULARES_2 = [
    {
        "ing_inf": "forgive", "esp_inf": "perdonar",
        "pasado_ing": "forgave", "pasado_esp": "perdonó",
        "participio_ing": "forgiven", "participio_esp": "perdonado",
        "gerundio_ing": "forgiving", "gerundio_esp": "perdonando",
        "oraciones": {
            "infinitivo":   {"ing": "I forgive easily.","esp": "Yo perdono fácilmente."},
            "pasadoSimple": {"ing": "You forgave him.","esp": "Tú le perdonaste."},
            "participio":   {"ing": "She has forgiven the debt.","esp": "Ella ha perdonado la deuda."},
            "gerundio":     {"ing": "They are forgiving themselves.","esp": "Ellos se están perdonando."},
            "futuro":       {"ing": "We will forgive you.","esp": "Nosotros te perdonaremos."},
            "condicional":  {"ing": "That would forgive everything.","esp": "Eso lo perdonaría todo."}
        }
    },
    {
        "ing_inf": "freeze", "esp_inf": "congelar",
        "pasado_ing": "froze", "pasado_esp": "congeló",
        "participio_ing": "frozen", "participio_esp": "congelado",
        "gerundio_ing": "freezing", "gerundio_esp": "congelando",
        "oraciones": {
            "infinitivo":   {"ing": "I freeze leftovers for later.","esp": "Yo congelo las sobras para después."},
            "pasadoSimple": {"ing": "You froze the water.","esp": "Tú congelaste el agua."},
            "participio":   {"ing": "The lake has frozen over.","esp": "El lago se ha congelado."},
            "gerundio":     {"ing": "They are freezing in the cold.","esp": "Ellos se están congelando de frío."},
            "futuro":       {"ing": "We will freeze the leftovers.","esp": "Nosotros congelaremos las sobras."},
            "condicional":  {"ing": "That screen would freeze up easily.","esp": "Esa pantalla se congelaría fácilmente."}
        }
    },
    {
        "ing_inf": "get", "esp_inf": "obtener",
        "pasado_ing": "got", "pasado_esp": "obtuvo",
        "participio_ing": "gotten", "participio_esp": "obtenido",
        "gerundio_ing": "getting", "gerundio_esp": "obteniendo",
        "oraciones": {
            "infinitivo":   {"ing": "I get up at seven.","esp": "Yo me levanto a las siete."},
            "pasadoSimple": {"ing": "You got a new job.","esp": "Tú obtuviste un trabajo nuevo."},
            "participio":   {"ing": "She has gotten better.","esp": "Ella ha mejorado."},
            "gerundio":     {"ing": "They are getting ready.","esp": "Ellos se están preparando."},
            "futuro":       {"ing": "We will get there soon.","esp": "Nosotros llegaremos pronto."},
            "condicional":  {"ing": "That would get attention.","esp": "Eso llamaría la atención."}
        }
    },
    {
        "ing_inf": "give", "esp_inf": "dar",
        "pasado_ing": "gave", "pasado_esp": "dio",
        "participio_ing": "given", "participio_esp": "dado",
        "gerundio_ing": "giving", "gerundio_esp": "dando",
        "futuro_esp": "dará", "cond_esp": "daría",
        "oraciones": {
            "infinitivo":   {"ing": "I give my best every day.","esp": "Yo doy mi mejor esfuerzo cada día."},
            "pasadoSimple": {"ing": "You gave me a gift.","esp": "Tú me diste un regalo."},
            "participio":   {"ing": "She has given a speech.","esp": "Ella ha dado un discurso."},
            "gerundio":     {"ing": "They are giving away books.","esp": "Ellos están regalando libros."},
            "futuro":       {"ing": "We will give thanks.","esp": "Nosotros agradeceremos."},
            "condicional":  {"ing": "That would give hope.","esp": "Eso daría esperanza."}
        }
    },
    {
        "ing_inf": "go", "esp_inf": "ir",
        "pasado_ing": "went", "pasado_esp": "fue",
        "participio_ing": "gone", "participio_esp": "ido",
        "gerundio_ing": "going", "gerundio_esp": "yendo",
        "futuro_esp": "irá", "cond_esp": "iría",
        "oraciones": {
            "infinitivo":   {"ing": "I go to the gym daily.","esp": "Yo voy al gimnasio a diario."},
            "pasadoSimple": {"ing": "You went to the party.","esp": "Tú fuiste a la fiesta."},
            "participio":   {"ing": "She has gone home.","esp": "Ella se ha ido a casa."},
            "gerundio":     {"ing": "They are going to travel.","esp": "Ellos van a viajar."},
            "futuro":       {"ing": "We will go tomorrow.","esp": "Nosotros iremos mañana."},
            "condicional":  {"ing": "That would go well.","esp": "Eso iría bien."}
        }
    },
    {
        "ing_inf": "grow", "esp_inf": "crecer",
        "pasado_ing": "grew", "pasado_esp": "creció",
        "participio_ing": "grown", "participio_esp": "crecido",
        "gerundio_ing": "growing", "gerundio_esp": "creciendo",
        "oraciones": {
            "infinitivo":   {"ing": "I grow tomatoes in my garden.","esp": "Yo cultivo tomates en mi jardín."},
            "pasadoSimple": {"ing": "You grew taller last year.","esp": "Tú creciste más el año pasado."},
            "participio":   {"ing": "She has grown her hair long.","esp": "Ella se ha dejado crecer el pelo."},
            "gerundio":     {"ing": "They are growing the business.","esp": "Ellos están haciendo crecer el negocio."},
            "futuro":       {"ing": "We will grow together.","esp": "Nosotros creceremos juntos."},
            "condicional":  {"ing": "That plant would grow fast.","esp": "Esa planta crecería rápido."}
        }
    },
    {
        "ing_inf": "hang", "esp_inf": "colgar",
        "pasado_ing": "hanged/hung", "pasado_esp": "colgó",
        "participio_ing": "hanged/hung", "participio_esp": "colgado",
        "gerundio_ing": "hanging", "gerundio_esp": "colgando",
        "oraciones": {
            "infinitivo":   {"ing": "I hang my coat by the door.","esp": "Yo cuelgo mi abrigo junto a la puerta."},
            "pasadoSimple": {"ing": "You hung the picture yesterday.","esp": "Tú colgaste el cuadro ayer."},
            "participio":   {"ing": "She has hung the laundry.","esp": "Ella ha colgado la ropa."},
            "gerundio":     {"ing": "They are hanging decorations.","esp": "Ellos están colgando decoraciones."},
            "futuro":       {"ing": "We will hang the banner soon.","esp": "Nosotros colgaremos el banner pronto."},
            "condicional":  {"ing": "That picture would hang perfectly.","esp": "Ese cuadro colgaría perfectamente."}
        }
    },
    {
        "ing_inf": "have", "esp_inf": "tener",
        "pasado_ing": "had", "pasado_esp": "tuvo",
        "participio_ing": "had", "participio_esp": "tenido",
        "gerundio_ing": "having", "gerundio_esp": "teniendo",
        "futuro_esp": "tendrá", "cond_esp": "tendría",
        "oraciones": {
            "infinitivo":   {"ing": "I have lunch at noon.","esp": "Yo almuerzo al mediodía."},
            "pasadoSimple": {"ing": "You had a good day.","esp": "Tú tuviste un buen día."},
            "participio":   {"ing": "She has had a cold.","esp": "Ella ha tenido un resfriado."},
            "gerundio":     {"ing": "They are having fun.","esp": "Ellos se están divirtiendo."},
            "futuro":       {"ing": "We will have time.","esp": "Nosotros tendremos tiempo."},
            "condicional":  {"ing": "That would have impact.","esp": "Eso tendría impacto."}
        }
    },
    {
        "ing_inf": "hear", "esp_inf": "oír",
        "pasado_ing": "heard", "pasado_esp": "oyó",
        "participio_ing": "heard", "participio_esp": "oído",
        "gerundio_ing": "hearing", "gerundio_esp": "oyendo",
        "oraciones": {
            "infinitivo":   {"ing": "I hear music from next door.","esp": "Yo oigo música de al lado."},
            "pasadoSimple": {"ing": "You heard the news yesterday.","esp": "Tú oíste la noticia ayer."},
            "participio":   {"ing": "She has heard the warning.","esp": "Ella ha oído la advertencia."},
            "gerundio":     {"ing": "They are hearing the testimony.","esp": "Ellos están oyendo el testimonio."},
            "futuro":       {"ing": "We will hear back soon.","esp": "Nosotros oiremos respuesta pronto."},
            "condicional":  {"ing": "That sound would be heard far away.","esp": "Ese sonido se oiría lejos."}
        }
    },
    {
        "ing_inf": "hide", "esp_inf": "esconder",
        "pasado_ing": "hid", "pasado_esp": "escondió",
        "participio_ing": "hidden", "participio_esp": "escondido",
        "gerundio_ing": "hiding", "gerundio_esp": "escondiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I hide the chocolate from my kids.","esp": "Yo escondo el chocolate de mis hijos."},
            "pasadoSimple": {"ing": "You hid behind the door.","esp": "Tú te escondiste detrás de la puerta."},
            "participio":   {"ing": "She has hidden the gift.","esp": "Ella ha escondido el regalo."},
            "gerundio":     {"ing": "They are hiding from the rain.","esp": "Ellos se están escondiendo de la lluvia."},
            "futuro":       {"ing": "We will hide the surprise.","esp": "Nosotros esconderemos la sorpresa."},
            "condicional":  {"ing": "That would hide the truth.","esp": "Eso escondería la verdad."}
        }
    },
    {
        "ing_inf": "hit", "esp_inf": "golpear",
        "pasado_ing": "hit", "pasado_esp": "golpeó",
        "participio_ing": "hit", "participio_esp": "golpeado",
        "gerundio_ing": "hitting", "gerundio_esp": "golpeando",
        "oraciones": {
            "infinitivo":   {"ing": "I hit the ball hard.","esp": "Yo golpeo la pelota con fuerza."},
            "pasadoSimple": {"ing": "You hit the target.","esp": "Tú golpeaste el blanco."},
            "participio":   {"ing": "She has hit a home run.","esp": "Ella ha conectado un jonrón."},
            "gerundio":     {"ing": "They are hitting the books.","esp": "Ellos están estudiando duro."},
            "futuro":       {"ing": "We will hit the road soon.","esp": "Nosotros saldremos pronto."},
            "condicional":  {"ing": "That car would hit anything.","esp": "Ese coche golpearía cualquier cosa."}
        }
    },
    {
        "ing_inf": "hold", "esp_inf": "sostener",
        "pasado_ing": "held", "pasado_esp": "sostuvo",
        "participio_ing": "held", "participio_esp": "sostenido",
        "gerundio_ing": "holding", "gerundio_esp": "sosteniendo",
        "futuro_esp": "sostendrá", "cond_esp": "sostendría",
        "oraciones": {
            "infinitivo":   {"ing": "I hold my breath underwater.","esp": "Yo contengo la respiración bajo el agua."},
            "pasadoSimple": {"ing": "You held the baby gently.","esp": "Tú sostuviste al bebé con ternura."},
            "participio":   {"ing": "She has held the position for years.","esp": "Ella ha ocupado el puesto durante años."},
            "gerundio":     {"ing": "They are holding a meeting.","esp": "Ellos están teniendo una reunión."},
            "futuro":       {"ing": "We will hold the door open.","esp": "Nosotros mantendremos la puerta abierta."},
            "condicional":  {"ing": "That bag would hold everything.","esp": "Esa bolsa contendría todo."}
        }
    },
    {
        "ing_inf": "hurt", "esp_inf": "doler",
        "pasado_ing": "hurt", "pasado_esp": "dolió",
        "participio_ing": "hurt", "participio_esp": "dolido",
        "gerundio_ing": "hurting", "gerundio_esp": "doliendo",
        "futuro_esp": "dolerá", "cond_esp": "dolería",
        "oraciones": {
            "infinitivo":   {"ing": "I hurt when I exercise.","esp": "Me duele cuando hago ejercicio."},
            "pasadoSimple": {"ing": "You hurt my feelings.","esp": "Tú heriste mis sentimientos."},
            "participio":   {"ing": "Her back has hurt all week.","esp": "A ella le ha dolido la espalda toda la semana."},
            "gerundio":     {"ing": "They are hurting from the loss.","esp": "Ellos están sufriendo por la pérdida."},
            "futuro":       {"ing": "We will hurt no one.","esp": "Nosotros no lastimaremos a nadie."},
            "condicional":  {"ing": "That comment would hurt anyone.","esp": "Ese comentario lastimaría a cualquiera."}
        }
    },
    {
        "ing_inf": "keep", "esp_inf": "mantener",
        "pasado_ing": "kept", "pasado_esp": "mantuvo",
        "participio_ing": "kept", "participio_esp": "mantenido",
        "gerundio_ing": "keeping", "gerundio_esp": "manteniendo",
        "futuro_esp": "mantendrá", "cond_esp": "mantendría",
        "oraciones": {
            "infinitivo":   {"ing": "I keep my promises.","esp": "Yo mantengo mis promesas."},
            "pasadoSimple": {"ing": "You kept the secret.","esp": "Tú guardaste el secreto."},
            "participio":   {"ing": "She has kept the tradition.","esp": "Ella ha mantenido la tradición."},
            "gerundio":     {"ing": "They are keeping busy.","esp": "Ellos se están manteniendo ocupados."},
            "futuro":       {"ing": "We will keep trying.","esp": "Nosotros seguiremos intentando."},
            "condicional":  {"ing": "That secret would keep forever.","esp": "Ese secreto se mantendría para siempre."}
        }
    },
    {
        "ing_inf": "kneel", "esp_inf": "arrodillarse",
        "pasado_ing": "knelt", "pasado_esp": "se arrodilló",
        "participio_ing": "knelt", "participio_esp": "arrodillado",
        "gerundio_ing": "kneeling", "gerundio_esp": "arrodillándose",
        "futuro_esp": "se arrodillará", "cond_esp": "se arrodillaría",
        "oraciones": {
            "infinitivo":   {"ing": "I kneel in church.","esp": "Yo me arrodillo en la iglesia."},
            "pasadoSimple": {"ing": "You knelt down to pray.","esp": "Tú te arrodillaste para rezar."},
            "participio":   {"ing": "She has knelt at the altar.","esp": "Ella se ha arrodillado en el altar."},
            "gerundio":     {"ing": "They are kneeling before the king.","esp": "Ellos se están arrodillando ante el rey."},
            "futuro":       {"ing": "We will kneel together.","esp": "Nosotros nos arrodillaremos juntos."},
            "condicional":  {"ing": "That would kneel humbly.","esp": "Eso se arrodillaría humildemente."}
        }
    },
    {
        "ing_inf": "know", "esp_inf": "saber",
        "pasado_ing": "knew", "pasado_esp": "supo",
        "participio_ing": "known", "participio_esp": "sabido",
        "gerundio_ing": "knowing", "gerundio_esp": "sabiendo",
        "futuro_esp": "sabrá", "cond_esp": "sabría",
        "oraciones": {
            "infinitivo":   {"ing": "I know the answer.","esp": "Yo sé la respuesta."},
            "pasadoSimple": {"ing": "You knew the truth.","esp": "Tú supiste la verdad."},
            "participio":   {"ing": "She has known him for years.","esp": "Ella lo conoce desde hace años."},
            "gerundio":     {"ing": "They are knowing the limits.","esp": "Ellos están conociendo los límites."},
            "futuro":       {"ing": "We will know soon.","esp": "Nosotros sabremos pronto."},
            "condicional":  {"ing": "That would know no bounds.","esp": "Eso no conocería límites."}
        }
    },
    {
        "ing_inf": "lay", "esp_inf": "poner",
        "pasado_ing": "laid", "pasado_esp": "puso",
        "participio_ing": "laid", "participio_esp": "puesto",
        "gerundio_ing": "laying", "gerundio_esp": "poniendo",
        "futuro_esp": "pondrá", "cond_esp": "pondría",
        "oraciones": {
            "infinitivo":   {"ing": "I lay the table for dinner.","esp": "Yo pongo la mesa para cenar."},
            "pasadoSimple": {"ing": "You laid the carpet yesterday.","esp": "Tú pusiste la alfombra ayer."},
            "participio":   {"ing": "She has laid the foundation.","esp": "Ella ha puesto los cimientos."},
            "gerundio":     {"ing": "They are laying the cables.","esp": "Ellos están poniendo los cables."},
            "futuro":       {"ing": "We will lay down the law.","esp": "Nosotros estableceremos las reglas."},
            "condicional":  {"ing": "That policy would lay blame.","esp": "Esa política pondría la culpa."}
        }
    },
    {
        "ing_inf": "lead", "esp_inf": "liderar",
        "pasado_ing": "led", "pasado_esp": "lideró",
        "participio_ing": "led", "participio_esp": "liderado",
        "gerundio_ing": "leading", "gerundio_esp": "liderando",
        "oraciones": {
            "infinitivo":   {"ing": "I lead the marketing team.","esp": "Yo lidero el equipo de marketing."},
            "pasadoSimple": {"ing": "You led the discussion.","esp": "Tú lideraste la discusión."},
            "participio":   {"ing": "She has led the company well.","esp": "Ella ha liderado bien la empresa."},
            "gerundio":     {"ing": "They are leading the parade.","esp": "Ellos están liderando el desfile."},
            "futuro":       {"ing": "We will lead the way.","esp": "Nosotros lideraremos el camino."},
            "condicional":  {"ing": "That would lead nowhere.","esp": "Eso no llevaría a ninguna parte."}
        }
    },
    {
        "ing_inf": "leave", "esp_inf": "salir",
        "pasado_ing": "left", "pasado_esp": "salió",
        "participio_ing": "left", "participio_esp": "salido",
        "gerundio_ing": "leaving", "gerundio_esp": "saliendo",
        "futuro_esp": "saldrá", "cond_esp": "saldría",
        "oraciones": {
            "infinitivo":   {"ing": "I leave work at five.","esp": "Yo salgo del trabajo a las cinco."},
            "pasadoSimple": {"ing": "You left your keys.","esp": "Tú dejaste tus llaves."},
            "participio":   {"ing": "She has left for the airport.","esp": "Ella se ha ido al aeropuerto."},
            "gerundio":     {"ing": "They are leaving tomorrow.","esp": "Ellos se van mañana."},
            "futuro":       {"ing": "We will leave early.","esp": "Nosotros saldremos temprano."},
            "condicional":  {"ing": "That would leave a mark.","esp": "Eso dejaría una marca."}
        }
    },
    {
        "ing_inf": "lend", "esp_inf": "prestar",
        "pasado_ing": "lent", "pasado_esp": "prestó",
        "participio_ing": "lent", "participio_esp": "prestado",
        "gerundio_ing": "lending", "gerundio_esp": "prestando",
        "oraciones": {
            "infinitivo":   {"ing": "I lend books to friends.","esp": "Yo presto libros a amigos."},
            "pasadoSimple": {"ing": "You lent me money.","esp": "Tú me prestaste dinero."},
            "participio":   {"ing": "She has lent her car to me.","esp": "Ella me ha prestado su coche."},
            "gerundio":     {"ing": "They are lending support.","esp": "Ellos están prestando apoyo."},
            "futuro":       {"ing": "We will lend a hand.","esp": "Nosotros echaremos una mano."},
            "condicional":  {"ing": "That bank would lend easily.","esp": "Ese banco prestaría fácilmente."}
        }
    },
    {
        "ing_inf": "let", "esp_inf": "dejar",
        "pasado_ing": "let", "pasado_esp": "dejó",
        "participio_ing": "let", "participio_esp": "dejado",
        "gerundio_ing": "letting", "gerundio_esp": "dejando",
        "oraciones": {
            "infinitivo":   {"ing": "I let my kids play outside.","esp": "Yo dejo que mis hijos jueguen afuera."},
            "pasadoSimple": {"ing": "You let the cat out.","esp": "Tú dejaste salir al gato."},
            "participio":   {"ing": "She has let go of the past.","esp": "Ella ha soltado el pasado."},
            "gerundio":     {"ing": "They are letting him try.","esp": "Ellos lo están dejando intentar."},
            "futuro":       {"ing": "We will let you know.","esp": "Nosotros te avisaremos."},
            "condicional":  {"ing": "That would let anyone in.","esp": "Eso dejaría entrar a cualquiera."}
        }
    },
    {
        "ing_inf": "lie", "esp_inf": "mentir",
        "pasado_ing": "lied", "pasado_esp": "mintió",
        "participio_ing": "lied", "participio_esp": "mentido",
        "gerundio_ing": "lying", "gerundio_esp": "mintiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I lie about my age sometimes.","esp": "Yo miento sobre mi edad a veces."},
            "pasadoSimple": {"ing": "You lied to me yesterday.","esp": "Tú me mentiste ayer."},
            "participio":   {"ing": "She has lied many times.","esp": "Ella ha mentido muchas veces."},
            "gerundio":     {"ing": "They are lying on the beach.","esp": "Ellos están acostados en la playa."},
            "futuro":       {"ing": "We will lie low for a while.","esp": "Nosotros nos esconderemos un tiempo."},
            "condicional":  {"ing": "That would lie easily.","esp": "Eso mentiría fácilmente."}
        }
    },
    {
        "ing_inf": "light", "esp_inf": "encender",
        "pasado_ing": "lit", "pasado_esp": "encendió",
        "participio_ing": "lit", "participio_esp": "encendido",
        "gerundio_ing": "lighting", "gerundio_esp": "encendiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I light candles at night.","esp": "Yo enciendo velas por la noche."},
            "pasadoSimple": {"ing": "You lit the candles.","esp": "Tú encendiste las velas."},
            "participio":   {"ing": "She has lit the fireplace.","esp": "Ella ha encendido la chimenea."},
            "gerundio":     {"ing": "They are lighting fireworks.","esp": "Ellos están encendiendo fuegos artificiales."},
            "futuro":       {"ing": "We will light the bonfire.","esp": "Nosotros encenderemos la fogata."},
            "condicional":  {"ing": "That match would light easily.","esp": "Ese fósforo se encendería fácilmente."}
        }
    },
    {
        "ing_inf": "lose", "esp_inf": "perder",
        "pasado_ing": "lost", "pasado_esp": "perdió",
        "participio_ing": "lost", "participio_esp": "perdido",
        "gerundio_ing": "losing", "gerundio_esp": "perdiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I lose my keys often.","esp": "Yo pierdo mis llaves a menudo."},
            "pasadoSimple": {"ing": "You lost the game.","esp": "Tú perdiste el juego."},
            "participio":   {"ing": "She has lost her passport.","esp": "Ella ha perdido su pasaporte."},
            "gerundio":     {"ing": "They are losing customers.","esp": "Ellos están perdiendo clientes."},
            "futuro":       {"ing": "We will lose weight.","esp": "Nosotros perderemos peso."},
            "condicional":  {"ing": "That team would lose often.","esp": "Ese equipo perdería a menudo."}
        }
    },
    {
        "ing_inf": "make", "esp_inf": "hacer",
        "pasado_ing": "made", "pasado_esp": "hizo",
        "participio_ing": "made", "participio_esp": "hecho",
        "gerundio_ing": "making", "gerundio_esp": "haciendo",
        "futuro_esp": "hará", "cond_esp": "haría",
        "oraciones": {
            "infinitivo":   {"ing": "I make dinner every evening.","esp": "Yo hago la cena cada noche."},
            "pasadoSimple": {"ing": "You made a great cake.","esp": "Tú hiciste un gran pastel."},
            "participio":   {"ing": "She has made a decision.","esp": "Ella ha tomado una decisión."},
            "gerundio":     {"ing": "They are making progress.","esp": "Ellos están progresando."},
            "futuro":       {"ing": "We will make a difference.","esp": "Nosotros haremos la diferencia."},
            "condicional":  {"ing": "That would make sense.","esp": "Eso tendría sentido."}
        }
    },
    {
        "ing_inf": "mean", "esp_inf": "significar",
        "pasado_ing": "meant", "pasado_esp": "significó",
        "participio_ing": "meant", "participio_esp": "significado",
        "gerundio_ing": "meaning", "gerundio_esp": "significando",
        "oraciones": {
            "infinitivo":   {"ing": "I mean what I say.","esp": "Yo digo lo que digo."},
            "pasadoSimple": {"ing": "You meant well.","esp": "Tú lo hiciste con buena intención."},
            "participio":   {"ing": "She has meant a lot to me.","esp": "Ella ha significado mucho para mí."},
            "gerundio":     {"ing": "They are meaning to call.","esp": "Ellos tienen la intención de llamar."},
            "futuro":       {"ing": "We will mean what we say.","esp": "Nosotros diremos lo que pensemos."},
            "condicional":  {"ing": "That would mean disaster.","esp": "Eso significaría desastre."}
        }
    },
    {
        "ing_inf": "meet", "esp_inf": "conocer",
        "pasado_ing": "met", "pasado_esp": "conoció",
        "participio_ing": "met", "participio_esp": "conocido",
        "gerundio_ing": "meeting", "gerundio_esp": "conociendo",
        "futuro_esp": "conocerá", "cond_esp": "conocería",
        "oraciones": {
            "infinitivo":   {"ing": "I meet clients for coffee.","esp": "Yo me reúno con clientes para café."},
            "pasadoSimple": {"ing": "You met my parents yesterday.","esp": "Tú conociste a mis padres ayer."},
            "participio":   {"ing": "She has met the deadline.","esp": "Ella ha cumplido con el plazo."},
            "gerundio":     {"ing": "They are meeting at noon.","esp": "Ellos se están reuniendo al mediodía."},
            "futuro":       {"ing": "We will meet at the airport.","esp": "Nos encontraremos en el aeropuerto."},
            "condicional":  {"ing": "That would meet the requirements.","esp": "Eso cumpliría los requisitos."}
        }
    },
    {
        "ing_inf": "pay", "esp_inf": "pagar",
        "pasado_ing": "paid", "pasado_esp": "pagó",
        "participio_ing": "paid", "participio_esp": "pagado",
        "gerundio_ing": "paying", "gerundio_esp": "pagando",
        "oraciones": {
            "infinitivo":   {"ing": "I pay rent on the first.","esp": "Yo pago la renta el primero."},
            "pasadoSimple": {"ing": "You paid too much.","esp": "Tú pagaste demasiado."},
            "participio":   {"ing": "She has paid off her debt.","esp": "Ella ha pagado su deuda."},
            "gerundio":     {"ing": "They are paying attention.","esp": "Ellos están prestando atención."},
            "futuro":       {"ing": "We will pay in cash.","esp": "Nosotros pagaremos en efectivo."},
            "condicional":  {"ing": "That would pay off well.","esp": "Eso valdría la pena."}
        }
    },
    {
        "ing_inf": "put", "esp_inf": "poner",
        "pasado_ing": "put", "pasado_esp": "puso",
        "participio_ing": "put", "participio_esp": "puesto",
        "gerundio_ing": "putting", "gerundio_esp": "poniendo",
        "futuro_esp": "pondrá", "cond_esp": "pondría",
        "oraciones": {
            "infinitivo":   {"ing": "I put the keys on the table.","esp": "Yo pongo las llaves en la mesa."},
            "pasadoSimple": {"ing": "You put the box down.","esp": "Tú pusiste la caja abajo."},
            "participio":   {"ing": "She has put the book away.","esp": "Ella ha guardado el libro."},
            "gerundio":     {"ing": "They are putting on a show.","esp": "Ellos están montando un espectáculo."},
            "futuro":       {"ing": "We will put effort into it.","esp": "Nosotros pondremos esfuerzo en ello."},
            "condicional":  {"ing": "That would put anyone at ease.","esp": "Eso tranquilizaría a cualquiera."}
        }
    },
    {
        "ing_inf": "read", "esp_inf": "leer",
        "pasado_ing": "read", "pasado_esp": "leyó",
        "participio_ing": "read", "participio_esp": "leído",
        "gerundio_ing": "reading", "gerundio_esp": "leyendo",
        "oraciones": {
            "infinitivo":   {"ing": "I read books every night.","esp": "Yo leo libros cada noche."},
            "pasadoSimple": {"ing": "You read the report yesterday.","esp": "Tú leíste el informe ayer."},
            "participio":   {"ing": "She has read every Harry Potter book.","esp": "Ella ha leído todos los libros de Harry Potter."},
            "gerundio":     {"ing": "They are reading the fine print.","esp": "Ellos están leyendo la letra pequeña."},
            "futuro":       {"ing": "We will read aloud.","esp": "Nosotros leeremos en voz alta."},
            "condicional":  {"ing": "That book would read quickly.","esp": "Ese libro se leería rápido."}
        }
    }
]


BLOQUE_IRREGULARES_3 = [
    {
        "ing_inf": "ride", "esp_inf": "montar",
        "pasado_ing": "rode", "pasado_esp": "montó",
        "participio_ing": "ridden", "participio_esp": "montado",
        "gerundio_ing": "riding", "gerundio_esp": "montando",
        "oraciones": {
            "infinitivo":   {"ing": "I ride my bike to work.","esp": "Yo monto en bicicleta al trabajo."},
            "pasadoSimple": {"ing": "You rode the horse yesterday.","esp": "Tú montaste el caballo ayer."},
            "participio":   {"ing": "She has ridden that roller coaster.","esp": "Ella se ha montado en esa montaña rusa."},
            "gerundio":     {"ing": "They are riding the waves.","esp": "Ellos están surfeando las olas."},
            "futuro":       {"ing": "We will ride bikes tomorrow.","esp": "Nosotros montaremos en bicicleta mañana."},
            "condicional":  {"ing": "That motorcycle would ride smoothly.","esp": "Esa moto se montaría suavemente."}
        }
    },
    {
        "ing_inf": "ring", "esp_inf": "sonar",
        "pasado_ing": "rang", "pasado_esp": "sonó",
        "participio_ing": "rung", "participio_esp": "sonado",
        "gerundio_ing": "ringing", "gerundio_esp": "sonando",
        "oraciones": {
            "infinitivo":   {"ing": "I ring the bell when I arrive.","esp": "Yo toco el timbre cuando llego."},
            "pasadoSimple": {"ing": "You rang the doorbell.","esp": "Tú tocaste el timbre."},
            "participio":   {"ing": "The phone has rung twice.","esp": "El teléfono ha sonado dos veces."},
            "gerundio":     {"ing": "They are ringing the bells.","esp": "Ellos están tocando las campanas."},
            "futuro":       {"ing": "We will ring in the new year.","esp": "Nosotros celebraremos el año nuevo."},
            "condicional":  {"ing": "That alarm would ring loudly.","esp": "Esa alarma sonaría fuerte."}
        }
    },
    {
        "ing_inf": "rise", "esp_inf": "levantarse",
        "pasado_ing": "rose", "pasado_esp": "se levantó",
        "participio_ing": "risen", "participio_esp": "levantado",
        "gerundio_ing": "rising", "gerundio_esp": "levantándose",
        "futuro_esp": "se levantará", "cond_esp": "se levantaría",
        "oraciones": {
            "infinitivo":   {"ing": "I rise early on weekdays.","esp": "Yo me levanto temprano entre semana."},
            "pasadoSimple": {"ing": "You rose before dawn.","esp": "Tú te levantaste antes del amanecer."},
            "participio":   {"ing": "She has risen to fame.","esp": "Ella se ha elevado a la fama."},
            "gerundio":     {"ing": "Prices are rising fast.","esp": "Los precios están subiendo rápido."},
            "futuro":       {"ing": "We will rise early tomorrow.","esp": "Nosotros nos levantaremos temprano mañana."},
            "condicional":  {"ing": "That balloon would rise quickly.","esp": "Ese globo se elevaría rápido."}
        }
    },
    {
        "ing_inf": "run", "esp_inf": "correr",
        "pasado_ing": "ran", "pasado_esp": "corrió",
        "participio_ing": "run", "participio_esp": "corrido",
        "gerundio_ing": "running", "gerundio_esp": "corriendo",
        "oraciones": {
            "infinitivo":   {"ing": "I run five kilometers daily.","esp": "Yo corro cinco kilómetros a diario."},
            "pasadoSimple": {"ing": "You ran the marathon.","esp": "Tú corriste el maratón."},
            "participio":   {"ing": "She has run the business for years.","esp": "Ella ha dirigido el negocio durante años."},
            "gerundio":     {"ing": "They are running errands.","esp": "Ellos están haciendo mandados."},
            "futuro":       {"ing": "We will run tomorrow.","esp": "Nosotros correremos mañana."},
            "condicional":  {"ing": "That program would run smoothly.","esp": "Ese programa funcionaría sin problemas."}
        }
    },
    {
        "ing_inf": "say", "esp_inf": "decir",
        "pasado_ing": "said", "pasado_esp": "dijo",
        "participio_ing": "said", "participio_esp": "dicho",
        "gerundio_ing": "saying", "gerundio_esp": "diciendo",
        "futuro_esp": "dirá", "cond_esp": "diría",
        "oraciones": {
            "infinitivo":   {"ing": "I say what I think.","esp": "Yo digo lo que pienso."},
            "pasadoSimple": {"ing": "You said yes.","esp": "Tú dijiste que sí."},
            "participio":   {"ing": "She has said her piece.","esp": "Ella ha dicho lo suyo."},
            "gerundio":     {"ing": "They are saying goodbye.","esp": "Ellos se están despidiendo."},
            "futuro":       {"ing": "We will say something.","esp": "Nosotros diremos algo."},
            "condicional":  {"ing": "That would say a lot.","esp": "Eso diría mucho."}
        }
    },
    {
        "ing_inf": "see", "esp_inf": "ver",
        "pasado_ing": "saw", "pasado_esp": "vio",
        "participio_ing": "seen", "participio_esp": "visto",
        "gerundio_ing": "seeing", "gerundio_esp": "viendo",
        "futuro_esp": "verá", "cond_esp": "vería",
        "oraciones": {
            "infinitivo":   {"ing": "I see the ocean from here.","esp": "Yo veo el océano desde aquí."},
            "pasadoSimple": {"ing": "You saw the movie yesterday.","esp": "Tú viste la película ayer."},
            "participio":   {"ing": "She has seen the doctor.","esp": "Ella ha visto al médico."},
            "gerundio":     {"ing": "They are seeing each other.","esp": "Ellos se están viendo."},
            "futuro":       {"ing": "We will see you tomorrow.","esp": "Nosotros te veremos mañana."},
            "condicional":  {"ing": "That would see anyone through.","esp": "Eso ayudaría a cualquiera."}
        }
    },
    {
        "ing_inf": "seek", "esp_inf": "buscar",
        "pasado_ing": "sought", "pasado_esp": "buscó",
        "participio_ing": "sought", "participio_esp": "buscado",
        "gerundio_ing": "seeking", "gerundio_esp": "buscando",
        "oraciones": {
            "infinitivo":   {"ing": "I seek adventure when I travel.","esp": "Yo busco aventura cuando viajo."},
            "pasadoSimple": {"ing": "You sought help yesterday.","esp": "Tú buscaste ayuda ayer."},
            "participio":   {"ing": "She has sought revenge.","esp": "Ella ha buscado venganza."},
            "gerundio":     {"ing": "They are seeking investors.","esp": "Ellos están buscando inversores."},
            "futuro":       {"ing": "We will seek justice.","esp": "Nosotros buscaremos justicia."},
            "condicional":  {"ing": "That ad would seek attention.","esp": "Ese anuncio buscaría atención."}
        }
    },
    {
        "ing_inf": "sell", "esp_inf": "vender",
        "pasado_ing": "sold", "pasado_esp": "vendió",
        "participio_ing": "sold", "participio_esp": "vendido",
        "gerundio_ing": "selling", "gerundio_esp": "vendiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I sell crafts online.","esp": "Yo vendo artesanías en línea."},
            "pasadoSimple": {"ing": "You sold the car.","esp": "Tú vendiste el coche."},
            "participio":   {"ing": "She has sold her company.","esp": "Ella ha vendido su empresa."},
            "gerundio":     {"ing": "They are selling tickets.","esp": "Ellos están vendiendo boletos."},
            "futuro":       {"ing": "We will sell at the fair.","esp": "Nosotros venderemos en la feria."},
            "condicional":  {"ing": "That product would sell fast.","esp": "Ese producto se vendería rápido."}
        }
    },
    {
        "ing_inf": "send", "esp_inf": "enviar",
        "pasado_ing": "sent", "pasado_esp": "envió",
        "participio_ing": "sent", "participio_esp": "enviado",
        "gerundio_ing": "sending", "gerundio_esp": "enviando",
        "oraciones": {
            "infinitivo":   {"ing": "I send emails daily.","esp": "Yo envío correos a diario."},
            "pasadoSimple": {"ing": "You sent the package.","esp": "Tú enviaste el paquete."},
            "participio":   {"ing": "She has sent the invitation.","esp": "Ella ha enviado la invitación."},
            "gerundio":     {"ing": "They are sending reinforcements.","esp": "Ellos están enviando refuerzos."},
            "futuro":       {"ing": "We will send the report.","esp": "Nosotros enviaremos el informe."},
            "condicional":  {"ing": "That email would send automatically.","esp": "Ese correo se enviaría automáticamente."}
        }
    },
    {
        "ing_inf": "set", "esp_inf": "establecer",
        "pasado_ing": "set", "pasado_esp": "estableció",
        "participio_ing": "set", "participio_esp": "establecido",
        "gerundio_ing": "setting", "gerundio_esp": "estableciendo",
        "futuro_esp": "establecerá", "cond_esp": "establecería",
        "oraciones": {
            "infinitivo":   {"ing": "I set goals every January.","esp": "Yo establezco metas cada enero."},
            "pasadoSimple": {"ing": "You set the table.","esp": "Tú pusiste la mesa."},
            "participio":   {"ing": "She has set the record.","esp": "Ella ha establecido el récord."},
            "gerundio":     {"ing": "They are setting up the tent.","esp": "Ellos están montando la tienda."},
            "futuro":       {"ing": "We will set the price.","esp": "Nosotros estableceremos el precio."},
            "condicional":  {"ing": "That alarm would set off easily.","esp": "Esa alarma se activaría fácilmente."}
        }
    },
    {
        "ing_inf": "shake", "esp_inf": "sacudir",
        "pasado_ing": "shook", "pasado_esp": "sacudió",
        "participio_ing": "shaken", "participio_esp": "sacudido",
        "gerundio_ing": "shaking", "gerundio_esp": "sacudiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I shake the bottle before opening.","esp": "Yo agito la botella antes de abrirla."},
            "pasadoSimple": {"ing": "You shook the tree.","esp": "Tú sacudiste el árbol."},
            "participio":   {"ing": "She has shaken his hand.","esp": "Ella le ha estrechado la mano."},
            "gerundio":     {"ing": "They are shaking with fear.","esp": "Ellos están temblando de miedo."},
            "futuro":       {"ing": "We will shake hands later.","esp": "Nosotros nos estrecharemos las manos después."},
            "condicional":  {"ing": "That would shake anyone's faith.","esp": "Eso sacudiría la fe de cualquiera."}
        }
    },
    {
        "ing_inf": "shine", "esp_inf": "brillar",
        "pasado_ing": "shone", "pasado_esp": "brilló",
        "participio_ing": "shone", "participio_esp": "brillado",
        "gerundio_ing": "shining", "gerundio_esp": "brillando",
        "oraciones": {
            "infinitivo":   {"ing": "I shine my shoes before work.","esp": "Yo brillo mis zapatos antes del trabajo."},
            "pasadoSimple": {"ing": "You shone the flashlight.","esp": "Tú enfocaste la linterna."},
            "participio":   {"ing": "The sun has shone all day.","esp": "El sol ha brillado todo el día."},
            "gerundio":     {"ing": "They are shining at school.","esp": "Ellos están brillando en la escuela."},
            "futuro":       {"ing": "We will shine tomorrow.","esp": "Nosotros brillaremos mañana."},
            "condicional":  {"ing": "That star would shine brightly.","esp": "Esa estrella brillaría con intensidad."}
        }
    },
    {
        "ing_inf": "shoot", "esp_inf": "disparar",
        "pasado_ing": "shot", "pasado_esp": "disparó",
        "participio_ing": "shot", "participio_esp": "disparado",
        "gerundio_ing": "shooting", "gerundio_esp": "disparando",
        "oraciones": {
            "infinitivo":   {"ing": "I shoot photos on weekends.","esp": "Yo tomo fotos los fines de semana."},
            "pasadoSimple": {"ing": "You shot the target.","esp": "Tú disparaste al blanco."},
            "participio":   {"ing": "She has shot three movies.","esp": "Ella ha filmado tres películas."},
            "gerundio":     {"ing": "They are shooting the commercial.","esp": "Ellos están filmando el comercial."},
            "futuro":       {"ing": "We will shoot the video tomorrow.","esp": "Nosotros filmaremos el video mañana."},
            "condicional":  {"ing": "That camera would shoot in 4K.","esp": "Esa cámara filmaría en 4K."}
        }
    },
    {
        "ing_inf": "show", "esp_inf": "mostrar",
        "pasado_ing": "showed", "pasado_esp": "mostró",
        "participio_ing": "shown", "participio_esp": "mostrado",
        "gerundio_ing": "showing", "gerundio_esp": "mostrando",
        "oraciones": {
            "infinitivo":   {"ing": "I show my ID at the door.","esp": "Yo muestro mi identificación en la puerta."},
            "pasadoSimple": {"ing": "You showed the photos.","esp": "Tú mostraste las fotos."},
            "participio":   {"ing": "She has shown great talent.","esp": "Ella ha mostrado gran talento."},
            "gerundio":     {"ing": "They are showing the new movie.","esp": "Ellos están mostrando la nueva película."},
            "futuro":       {"ing": "We will show you around.","esp": "Nosotros te mostraremos el lugar."},
            "condicional":  {"ing": "That result would show the truth.","esp": "Ese resultado mostraría la verdad."}
        }
    },
    {
        "ing_inf": "shrink", "esp_inf": "encoger",
        "pasado_ing": "shrank", "pasado_esp": "encogió",
        "participio_ing": "shrunk", "participio_esp": "encogido",
        "gerundio_ing": "shrinking", "gerundio_esp": "encogiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I shrink from confrontation.","esp": "Yo me echo atrás ante la confrontación."},
            "pasadoSimple": {"ing": "You shrank the sweater.","esp": "Tú encogiste el suéter."},
            "participio":   {"ing": "The shirt has shrunk in the wash.","esp": "La camisa se ha encogido al lavarse."},
            "gerundio":     {"ing": "They are shrinking the budget.","esp": "Ellos están recortando el presupuesto."},
            "futuro":       {"ing": "We will shrink the image.","esp": "Nosotros encogeremos la imagen."},
            "condicional":  {"ing": "That market would shrink soon.","esp": "Ese mercado se encogería pronto."}
        }
    },
    {
        "ing_inf": "shut", "esp_inf": "cerrar",
        "pasado_ing": "shut", "pasado_esp": "cerró",
        "participio_ing": "shut", "participio_esp": "cerrado",
        "gerundio_ing": "shutting", "gerundio_esp": "cerrando",
        "oraciones": {
            "infinitivo":   {"ing": "I shut the door quietly.","esp": "Yo cierro la puerta en silencio."},
            "pasadoSimple": {"ing": "You shut the window.","esp": "Tú cerraste la ventana."},
            "participio":   {"ing": "She has shut the shop.","esp": "Ella ha cerrado la tienda."},
            "gerundio":     {"ing": "They are shutting down the factory.","esp": "Ellos están cerrando la fábrica."},
            "futuro":       {"ing": "We will shut up about it.","esp": "Nosotros nos callaremos al respecto."},
            "condicional":  {"ing": "That door would shut automatically.","esp": "Esa puerta se cerraría automáticamente."}
        }
    },
    {
        "ing_inf": "sing", "esp_inf": "cantar",
        "pasado_ing": "sang", "pasado_esp": "cantó",
        "participio_ing": "sung", "participio_esp": "cantado",
        "gerundio_ing": "singing", "gerundio_esp": "cantando",
        "oraciones": {
            "infinitivo":   {"ing": "I sing in the shower.","esp": "Yo canto en la ducha."},
            "pasadoSimple": {"ing": "You sang beautifully last night.","esp": "Tú cantaste hermoso anoche."},
            "participio":   {"ing": "She has sung that song before.","esp": "Ella ha cantado esa canción antes."},
            "gerundio":     {"ing": "They are singing karaoke.","esp": "Ellos están cantando karaoke."},
            "futuro":       {"ing": "We will sing at the wedding.","esp": "Nosotros cantaremos en la boda."},
            "condicional":  {"ing": "That song would sing itself.","esp": "Esa canción se canta sola."}
        }
    },
    {
        "ing_inf": "sink", "esp_inf": "hundir",
        "pasado_ing": "sank", "pasado_esp": "hundió",
        "participio_ing": "sunk", "participio_esp": "hundido",
        "gerundio_ing": "sinking", "gerundio_esp": "hundiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I sink into the couch after work.","esp": "Yo me hundo en el sofá después del trabajo."},
            "pasadoSimple": {"ing": "You sank the ship.","esp": "Tú hundiste el barco."},
            "participio":   {"ing": "The boat has sunk in the harbor.","esp": "El barco se ha hundido en el puerto."},
            "gerundio":     {"ing": "They are sinking the basket.","esp": "Ellos están encestando."},
            "futuro":       {"ing": "We will sink the money into this.","esp": "Nosotros invertiremos el dinero en esto."},
            "condicional":  {"ing": "That ship would sink quickly.","esp": "Ese barco se hundiría rápido."}
        }
    },
    {
        "ing_inf": "sit", "esp_inf": "sentarse",
        "pasado_ing": "sat", "pasado_esp": "se sentó",
        "participio_ing": "sat", "participio_esp": "sentado",
        "gerundio_ing": "sitting", "gerundio_esp": "sentándose",
        "futuro_esp": "se sentará", "cond_esp": "se sentaría",
        "oraciones": {
            "infinitivo":   {"ing": "I sit at my desk all day.","esp": "Yo me siento en mi escritorio todo el día."},
            "pasadoSimple": {"ing": "You sat next to me.","esp": "Tú te sentaste a mi lado."},
            "participio":   {"ing": "She has sat through long meetings.","esp": "Ella se ha sentado en reuniones largas."},
            "gerundio":     {"ing": "They are sitting on the couch.","esp": "Ellos están sentados en el sofá."},
            "futuro":       {"ing": "We will sit down soon.","esp": "Nosotros nos sentaremos pronto."},
            "condicional":  {"ing": "That chair would sit comfortably.","esp": "Esa silla sería cómoda para sentarse."}
        }
    },
    {
        "ing_inf": "sleep", "esp_inf": "dormir",
        "pasado_ing": "slept", "pasado_esp": "durmió",
        "participio_ing": "slept", "participio_esp": "dormido",
        "gerundio_ing": "sleeping", "gerundio_esp": "durmiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I sleep eight hours every night.","esp": "Yo duermo ocho horas cada noche."},
            "pasadoSimple": {"ing": "You slept late on Sunday.","esp": "Tú dormiste hasta tarde el domingo."},
            "participio":   {"ing": "She has slept well lately.","esp": "Ella ha dormido bien últimamente."},
            "gerundio":     {"ing": "They are sleeping over at my house.","esp": "Ellos están durmiendo en mi casa."},
            "futuro":       {"ing": "We will sleep at the hotel.","esp": "Nosotros dormiremos en el hotel."},
            "condicional":  {"ing": "That bed would sleep two comfortably.","esp": "Esa cama dormiría a dos cómodamente."}
        }
    },
    {
        "ing_inf": "slide", "esp_inf": "deslizar",
        "pasado_ing": "slid", "pasado_esp": "deslizó",
        "participio_ing": "slid", "participio_esp": "deslizado",
        "gerundio_ing": "sliding", "gerundio_esp": "deslizando",
        "oraciones": {
            "infinitivo":   {"ing": "I slide into home plate.","esp": "Yo me deslizo hasta la base."},
            "pasadoSimple": {"ing": "You slid down the slide.","esp": "Tú te deslizaste por el tobogán."},
            "participio":   {"ing": "She has slid the door open.","esp": "Ella ha deslizado la puerta para abrirla."},
            "gerundio":     {"ing": "They are sliding on the ice.","esp": "Ellos se están deslizando sobre el hielo."},
            "futuro":       {"ing": "We will slide the document.","esp": "Nosotros deslizaremos el documento."},
            "condicional":  {"ing": "That drawer would slide easily.","esp": "Ese cajón se deslizaría fácilmente."}
        }
    },
    {
        "ing_inf": "speak", "esp_inf": "hablar",
        "pasado_ing": "spoke", "pasado_esp": "habló",
        "participio_ing": "spoken", "participio_esp": "hablado",
        "gerundio_ing": "speaking", "gerundio_esp": "hablando",
        "oraciones": {
            "infinitivo":   {"ing": "I speak three languages.","esp": "Yo hablo tres idiomas."},
            "pasadoSimple": {"ing": "You spoke to the manager.","esp": "Tú hablaste con el gerente."},
            "participio":   {"ing": "She has spoken at conferences.","esp": "Ella ha hablado en conferencias."},
            "gerundio":     {"ing": "They are speaking softly.","esp": "Ellos están hablando en voz baja."},
            "futuro":       {"ing": "We will speak later.","esp": "Nosotros hablaremos después."},
            "condicional":  {"ing": "That spokesperson would speak well.","esp": "Ese portavoz hablaría bien."}
        }
    },
    {
        "ing_inf": "spend", "esp_inf": "gastar",
        "pasado_ing": "spent", "pasado_esp": "gastó",
        "participio_ing": "spent", "participio_esp": "gastado",
        "gerundio_ing": "spending", "gerundio_esp": "gastando",
        "oraciones": {
            "infinitivo":   {"ing": "I spend too much on coffee.","esp": "Yo gasto demasiado en café."},
            "pasadoSimple": {"ing": "You spent the weekend at home.","esp": "Tú pasaste el fin de semana en casa."},
            "participio":   {"ing": "She has spent her savings.","esp": "Ella ha gastado sus ahorros."},
            "gerundio":     {"ing": "They are spending time together.","esp": "Ellos están pasando tiempo juntos."},
            "futuro":       {"ing": "We will spend money carefully.","esp": "Nosotros gastaremos dinero con cuidado."},
            "condicional":  {"ing": "That vacation would be worth the spend.","esp": "Esas vacaciones valdrían la pena."}
        }
    },
    {
        "ing_inf": "spin", "esp_inf": "girar",
        "pasado_ing": "spun", "pasado_esp": "giró",
        "participio_ing": "spun", "participio_esp": "girado",
        "gerundio_ing": "spinning", "gerundio_esp": "girando",
        "oraciones": {
            "infinitivo":   {"ing": "I spin the dreidel at Hanukkah.","esp": "Yo giro la peonza en Janucá."},
            "pasadoSimple": {"ing": "You spun around twice.","esp": "Tú giraste dos veces."},
            "participio":   {"ing": "She has spun the wool.","esp": "Ella ha hilado la lana."},
            "gerundio":     {"ing": "They are spinning the wheel.","esp": "Ellos están girando la rueda."},
            "futuro":       {"ing": "We will spin the bottle.","esp": "Nosotros giraremos la botella."},
            "condicional":  {"ing": "That top would spin forever.","esp": "Esa peonza giraría para siempre."}
        }
    },
    {
        "ing_inf": "spread", "esp_inf": "extender",
        "pasado_ing": "spread", "pasado_esp": "extendió",
        "participio_ing": "spread", "participio_esp": "extendido",
        "gerundio_ing": "spreading", "gerundio_esp": "extendiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I spread butter on toast.","esp": "Yo unto mantequilla al pan tostado."},
            "pasadoSimple": {"ing": "You spread the news quickly.","esp": "Tú difundiste la noticia rápidamente."},
            "participio":   {"ing": "She has spread the tablecloth.","esp": "Ella ha extendido el mantel."},
            "gerundio":     {"ing": "They are spreading rumors.","esp": "Ellos están difundiendo rumores."},
            "futuro":       {"ing": "We will spread out later.","esp": "Nosotros nos dispersaremos después."},
            "condicional":  {"ing": "That rumor would spread fast.","esp": "Ese rumor se difundiría rápido."}
        }
    },
    {
        "ing_inf": "stand", "esp_inf": "pararse",
        "pasado_ing": "stood", "pasado_esp": "se paró",
        "participio_ing": "stood", "participio_esp": "parado",
        "gerundio_ing": "standing", "gerundio_esp": "parándose",
        "futuro_esp": "se parará", "cond_esp": "se pararía",
        "oraciones": {
            "infinitivo":   {"ing": "I stand by my decisions.","esp": "Yo respaldo mis decisiones."},
            "pasadoSimple": {"ing": "You stood up for yourself.","esp": "Tú te pusiste de pie por ti mismo."},
            "participio":   {"ing": "She has stood the test of time.","esp": "Ella ha resistido el paso del tiempo."},
            "gerundio":     {"ing": "They are standing in line.","esp": "Ellos están haciendo cola."},
            "futuro":       {"ing": "We will stand together.","esp": "Nosotros nos mantendremos unidos."},
            "condicional":  {"ing": "That building would stand forever.","esp": "Ese edificio permanecería en pie para siempre."}
        }
    },
    {
        "ing_inf": "steal", "esp_inf": "robar",
        "pasado_ing": "stole", "pasado_esp": "robó",
        "participio_ing": "stolen", "participio_esp": "robado",
        "gerundio_ing": "stealing", "gerundio_esp": "robando",
        "oraciones": {
            "infinitivo":   {"ing": "I steal glances at my phone.","esp": "Yo robo miradas a mi teléfono."},
            "pasadoSimple": {"ing": "You stole my idea.","esp": "Tú robaste mi idea."},
            "participio":   {"ing": "She has stolen my heart.","esp": "Ella me ha robado el corazón."},
            "gerundio":     {"ing": "They are stealing bases.","esp": "Ellos están robando bases."},
            "futuro":       {"ing": "We will steal the show.","esp": "Nosotros robaremos el show."},
            "condicional":  {"ing": "That thief would steal anything.","esp": "Ese ladrón robaría cualquier cosa."}
        }
    },
    {
        "ing_inf": "stick", "esp_inf": "pegar",
        "pasado_ing": "stuck", "pasado_esp": "pegó",
        "participio_ing": "stuck", "participio_esp": "pegado",
        "gerundio_ing": "sticking", "gerundio_esp": "pegando",
        "oraciones": {
            "infinitivo":   {"ing": "I stick to my routine.","esp": "Yo me apego a mi rutina."},
            "pasadoSimple": {"ing": "You stuck the label on.","esp": "Tú pegaste la etiqueta."},
            "participio":   {"ing": "She has stuck with the plan.","esp": "Ella se ha mantenido en el plan."},
            "gerundio":     {"ing": "They are sticking posters.","esp": "Ellos están pegando carteles."},
            "futuro":       {"ing": "We will stick together.","esp": "Nosotros nos mantendremos unidos."},
            "condicional":  {"ing": "That glue would stick anything.","esp": "Ese pegamento pegaría cualquier cosa."}
        }
    },
    {
        "ing_inf": "sting", "esp_inf": "picar",
        "pasado_ing": "stung", "pasado_esp": "picó",
        "participio_ing": "stung", "participio_esp": "picado",
        "gerundio_ing": "stinging", "gerundio_esp": "picando",
        "oraciones": {
            "infinitivo":   {"ing": "I gasp when cold water stings.","esp": "Yo contengo el aliento cuando pica el agua fría."},
            "pasadoSimple": {"ing": "You stung me with that comment.","esp": "Tú me lastimaste con ese comentario."},
            "participio":   {"ing": "The bee has stung her twice.","esp": "La abeja le ha picado dos veces."},
            "gerundio":     {"ing": "They are stinging from the criticism.","esp": "Ellos están sufriendo por la crítica."},
            "futuro":       {"ing": "We will sting the attackers.","esp": "Nosotros contraatacaremos."},
            "condicional":  {"ing": "That jellyfish would sting badly.","esp": "Esa medusa picaría fuerte."}
        }
    },
    {
        "ing_inf": "stink", "esp_inf": "apestar",
        "pasado_ing": "stank/stunk", "pasado_esp": "apestó",
        "participio_ing": "stunk", "participio_esp": "apestado",
        "gerundio_ing": "stinking", "gerundio_esp": "apestando",
        "oraciones": {
            "infinitivo":   {"ing": "I stink at math.","esp": "Yo soy malísimo en matemáticas."},
            "pasadoSimple": {"ing": "You stank up the room.","esp": "Tú apestaste el cuarto."},
            "participio":   {"ing": "The fridge has stunk all day.","esp": "El refrigerador ha apestado todo el día."},
            "gerundio":     {"ing": "They are stinking up the place.","esp": "Ellos están apestando el lugar."},
            "futuro":       {"ing": "We will stink after practice.","esp": "Nosotros oleremos mal después de la práctica."},
            "condicional":  {"ing": "That cheese would stink quickly.","esp": "Ese queso apestaría rápido."}
        }
    }
]


BLOQUE_IRREGULARES_4 = [
    {
        "ing_inf": "strike", "esp_inf": "golpear",
        "pasado_ing": "struck", "pasado_esp": "golpeó",
        "participio_ing": "struck/stricken", "participio_esp": "golpeado",
        "gerundio_ing": "striking", "gerundio_esp": "golpeando",
        "oraciones": {
            "infinitivo":   {"ing": "I strike a balance between work and life.","esp": "Yo encuentro un equilibrio entre trabajo y vida."},
            "pasadoSimple": {"ing": "You struck the nail hard.","esp": "Tú golpeaste el clavo con fuerza."},
            "participio":   {"ing": "She has struck a deal.","esp": "Ella ha cerrado un trato."},
            "gerundio":     {"ing": "They are striking for better wages.","esp": "Ellos están en huelga por mejores salarios."},
            "futuro":       {"ing": "We will strike at dawn.","esp": "Nosotros atacaremos al amanecer."},
            "condicional":  {"ing": "That clock would strike twelve.","esp": "Ese reloj daría las doce."}
        }
    },
    {
        "ing_inf": "swear", "esp_inf": "jurar",
        "pasado_ing": "swore", "pasado_esp": "juró",
        "participio_ing": "sworn", "participio_esp": "jurado",
        "gerundio_ing": "swearing", "gerundio_esp": "jurando",
        "oraciones": {
            "infinitivo":   {"ing": "I swear by my mother's cooking.","esp": "Yo juro por la cocina de mi madre."},
            "pasadoSimple": {"ing": "You swore an oath yesterday.","esp": "Tú juraste ayer."},
            "participio":   {"ing": "She has sworn to tell the truth.","esp": "Ella ha jurado decir la verdad."},
            "gerundio":     {"ing": "They are swearing at each other.","esp": "Ellos se están maldiciendo."},
            "futuro":       {"ing": "We will swear in the witnesses.","esp": "Nosotros tomaremos juramento a los testigos."},
            "condicional":  {"ing": "That would swear anyone to secrecy.","esp": "Eso obligaría a cualquiera a guardar el secreto."}
        }
    },
    {
        "ing_inf": "sweep", "esp_inf": "barrer",
        "pasado_ing": "swept", "pasado_esp": "barrió",
        "participio_ing": "swept", "participio_esp": "barrido",
        "gerundio_ing": "sweeping", "gerundio_esp": "barriendo",
        "oraciones": {
            "infinitivo":   {"ing": "I sweep the floor every morning.","esp": "Yo barro el piso cada mañana."},
            "pasadoSimple": {"ing": "You swept the chimney.","esp": "Tú barriste la chimenea."},
            "participio":   {"ing": "She has swept the competition.","esp": "Ella ha arrasado en la competencia."},
            "gerundio":     {"ing": "They are sweeping the leaves.","esp": "Ellos están barriendo las hojas."},
            "futuro":       {"ing": "We will sweep the deck.","esp": "Nosotros barreremos la cubierta."},
            "condicional":  {"ing": "That broom would sweep easily.","esp": "Esa escoba barrería fácilmente."}
        }
    },
    {
        "ing_inf": "swim", "esp_inf": "nadar",
        "pasado_ing": "swam", "pasado_esp": "nadó",
        "participio_ing": "swum", "participio_esp": "nadado",
        "gerundio_ing": "swimming", "gerundio_esp": "nadando",
        "oraciones": {
            "infinitivo":   {"ing": "I swim every weekend at the pool.","esp": "Yo nado cada fin de semana en la piscina."},
            "pasadoSimple": {"ing": "You swam across the lake.","esp": "Tú nadaste a través del lago."},
            "participio":   {"ing": "She has swum in the ocean.","esp": "Ella ha nadado en el océano."},
            "gerundio":     {"ing": "They are swimming competitively.","esp": "Ellos están nadando competitivamente."},
            "futuro":       {"ing": "We will swim tomorrow morning.","esp": "Nosotros nadaremos mañana por la mañana."},
            "condicional":  {"ing": "That fish would swim away.","esp": "Ese pez nadaría lejos."}
        }
    },
    {
        "ing_inf": "swing", "esp_inf": "columpiarse",
        "pasado_ing": "swung", "pasado_esp": "se columpió",
        "participio_ing": "swung", "participio_esp": "columpiado",
        "gerundio_ing": "swinging", "gerundio_esp": "columpiándose",
        "futuro_esp": "se columpiará", "cond_esp": "se columpiaría",
        "oraciones": {
            "infinitivo":   {"ing": "I swing at the playground daily.","esp": "Yo me columpio en el parque cada día."},
            "pasadoSimple": {"ing": "You swung the bat hard.","esp": "Tú balanceaste el bate con fuerza."},
            "participio":   {"ing": "The door has swung open.","esp": "La puerta se ha abierto de golpe."},
            "gerundio":     {"ing": "They are swinging on the ropes.","esp": "Ellos están columpiándose en las cuerdas."},
            "futuro":       {"ing": "We will swing by later.","esp": "Nosotros pasaremos después."},
            "condicional":  {"ing": "That pendulum would swing forever.","esp": "Ese péndulo oscilaría para siempre."}
        }
    },
    {
        "ing_inf": "take", "esp_inf": "tomar",
        "pasado_ing": "took", "pasado_esp": "tomó",
        "participio_ing": "taken", "participio_esp": "tomado",
        "gerundio_ing": "taking", "gerundio_esp": "tomando",
        "oraciones": {
            "infinitivo":   {"ing": "I take the bus to work.","esp": "Yo tomo el autobús al trabajo."},
            "pasadoSimple": {"ing": "You took the last cookie.","esp": "Tú tomaste la última galleta."},
            "participio":   {"ing": "She has taken the exam.","esp": "Ella ha tomado el examen."},
            "gerundio":     {"ing": "They are taking photos.","esp": "Ellos están tomando fotos."},
            "futuro":       {"ing": "We will take a break.","esp": "Nosotros tomaremos un descanso."},
            "condicional":  {"ing": "That pill would take effect.","esp": "Esa pastilla haría efecto."}
        }
    },
    {
        "ing_inf": "teach", "esp_inf": "enseñar",
        "pasado_ing": "taught", "pasado_esp": "enseñó",
        "participio_ing": "taught", "participio_esp": "enseñado",
        "gerundio_ing": "teaching", "gerundio_esp": "enseñando",
        "oraciones": {
            "infinitivo":   {"ing": "I teach English at the school.","esp": "Yo enseño inglés en la escuela."},
            "pasadoSimple": {"ing": "You taught me to swim.","esp": "Tú me enseñaste a nadar."},
            "participio":   {"ing": "She has taught for ten years.","esp": "Ella ha enseñado durante diez años."},
            "gerundio":     {"ing": "They are teaching the kids.","esp": "Ellos están enseñando a los niños."},
            "futuro":       {"ing": "We will teach next semester.","esp": "Nosotros enseñaremos el próximo semestre."},
            "condicional":  {"ing": "That class would teach anyone.","esp": "Esa clase enseñaría a cualquiera."}
        }
    },
    {
        "ing_inf": "tear", "esp_inf": "rasgar",
        "pasado_ing": "tore", "pasado_esp": "rasgó",
        "participio_ing": "torn", "participio_esp": "rasgado",
        "gerundio_ing": "tearing", "gerundio_esp": "rasgando",
        "oraciones": {
            "infinitivo":   {"ing": "I tear up at sad movies.","esp": "Yo lloro en películas tristes."},
            "pasadoSimple": {"ing": "You tore the paper.","esp": "Tú rasgaste el papel."},
            "participio":   {"ing": "She has torn her dress.","esp": "Ella ha roto su vestido."},
            "gerundio":     {"ing": "They are tearing down the building.","esp": "Ellos están demoliendo el edificio."},
            "futuro":       {"ing": "We will tear up the contract.","esp": "Nosotros romperemos el contrato."},
            "condicional":  {"ing": "That fabric would tear easily.","esp": "Esa tela se rasgaría fácilmente."}
        }
    },
    {
        "ing_inf": "tell", "esp_inf": "decir",
        "pasado_ing": "told", "pasado_esp": "dijo",
        "participio_ing": "told", "participio_esp": "dicho",
        "gerundio_ing": "telling", "gerundio_esp": "diciendo",
        "futuro_esp": "dirá", "cond_esp": "diría",
        "oraciones": {
            "infinitivo":   {"ing": "I tell the truth always.","esp": "Yo digo la verdad siempre."},
            "pasadoSimple": {"ing": "You told me yesterday.","esp": "Tú me dijiste ayer."},
            "participio":   {"ing": "She has told the truth.","esp": "Ella ha dicho la verdad."},
            "gerundio":     {"ing": "They are telling jokes.","esp": "Ellos están contando chistes."},
            "futuro":       {"ing": "We will tell you tomorrow.","esp": "Nosotros te diremos mañana."},
            "condicional":  {"ing": "That would tell us everything.","esp": "Eso nos diría todo."}
        }
    },
    {
        "ing_inf": "think", "esp_inf": "pensar",
        "pasado_ing": "thought", "pasado_esp": "pensó",
        "participio_ing": "thought", "participio_esp": "pensado",
        "gerundio_ing": "thinking", "gerundio_esp": "pensando",
        "oraciones": {
            "infinitivo":   {"ing": "I think before I act.","esp": "Yo pienso antes de actuar."},
            "pasadoSimple": {"ing": "You thought it was funny.","esp": "Tú pensaste que era gracioso."},
            "participio":   {"ing": "She has thought it through.","esp": "Ella lo ha pensado bien."},
            "gerundio":     {"ing": "They are thinking about it.","esp": "Ellos están pensando en ello."},
            "futuro":       {"ing": "We will think about your offer.","esp": "Nosotros pensaremos en tu oferta."},
            "condicional":  {"ing": "That would make anyone think.","esp": "Eso haría pensar a cualquiera."}
        }
    },
    {
        "ing_inf": "throw", "esp_inf": "lanzar",
        "pasado_ing": "threw", "pasado_esp": "lanzó",
        "participio_ing": "thrown", "participio_esp": "lanzado",
        "gerundio_ing": "throwing", "gerundio_esp": "lanzando",
        "oraciones": {
            "infinitivo":   {"ing": "I throw the ball to my dog.","esp": "Yo le lanzo la pelota a mi perro."},
            "pasadoSimple": {"ing": "You threw the trash away.","esp": "Tú tiraste la basura."},
            "participio":   {"ing": "She has thrown the party.","esp": "Ella ha organizado la fiesta."},
            "gerundio":     {"ing": "They are throwing stones.","esp": "Ellos están lanzando piedras."},
            "futuro":       {"ing": "We will throw a surprise party.","esp": "Nosotros haremos una fiesta sorpresa."},
            "condicional":  {"ing": "That pitcher would throw fast.","esp": "Ese lanzador lanzaría rápido."}
        }
    },
    {
        "ing_inf": "understand", "esp_inf": "entender",
        "pasado_ing": "understood", "pasado_esp": "entendió",
        "participio_ing": "understood", "participio_esp": "entendido",
        "gerundio_ing": "understanding", "gerundio_esp": "entendiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I understand the problem.","esp": "Yo entiendo el problema."},
            "pasadoSimple": {"ing": "You understood my point.","esp": "Tú entendiste mi punto."},
            "participio":   {"ing": "She has understood the instructions.","esp": "Ella ha entendido las instrucciones."},
            "gerundio":     {"ing": "They are understanding more.","esp": "Ellos están entendiendo más."},
            "futuro":       {"ing": "We will understand eventually.","esp": "Nosotros entenderemos eventualmente."},
            "condicional":  {"ing": "That would help anyone understand.","esp": "Eso ayudaría a cualquiera a entender."}
        }
    },
    {
        "ing_inf": "wake", "esp_inf": "despertarse",
        "pasado_ing": "woke", "pasado_esp": "se despertó",
        "participio_ing": "woken", "participio_esp": "despertado",
        "gerundio_ing": "waking", "gerundio_esp": "despertándose",
        "futuro_esp": "se despertará", "cond_esp": "se despertaría",
        "oraciones": {
            "infinitivo":   {"ing": "I wake up at six daily.","esp": "Yo me despierto a las seis a diario."},
            "pasadoSimple": {"ing": "You woke up late.","esp": "Tú te despertaste tarde."},
            "participio":   {"ing": "She has woken up early.","esp": "Ella se ha despertado temprano."},
            "gerundio":     {"ing": "They are waking up now.","esp": "Ellos se están despertando ahora."},
            "futuro":       {"ing": "We will wake up refreshed.","esp": "Nosotros nos despertaremos refrescados."},
            "condicional":  {"ing": "That noise would wake anyone.","esp": "Ese ruido despertaría a cualquiera."}
        }
    },
    {
        "ing_inf": "wear", "esp_inf": "usar",
        "pasado_ing": "wore", "pasado_esp": "usó",
        "participio_ing": "worn", "participio_esp": "usado",
        "gerundio_ing": "wearing", "gerundio_esp": "usando",
        "oraciones": {
            "infinitivo":   {"ing": "I wear glasses for reading.","esp": "Yo uso gafas para leer."},
            "pasadoSimple": {"ing": "You wore a nice dress.","esp": "Tú usaste un vestido bonito."},
            "participio":   {"ing": "She has worn that hat often.","esp": "Ella ha usado ese sombrero a menudo."},
            "gerundio":     {"ing": "They are wearing masks.","esp": "Ellos están usando mascarillas."},
            "futuro":       {"ing": "We will wear costumes.","esp": "Nosotros usaremos disfraces."},
            "condicional":  {"ing": "That fabric would wear well.","esp": "Esa tela se gastaría bien."}
        }
    },
    {
        "ing_inf": "weep", "esp_inf": "llorar",
        "pasado_ing": "wept", "pasado_esp": "lloró",
        "participio_ing": "wept", "participio_esp": "llorado",
        "gerundio_ing": "weeping", "gerundio_esp": "llorando",
        "oraciones": {
            "infinitivo":   {"ing": "I weep at sad movies.","esp": "Yo lloro en películas tristes."},
            "pasadoSimple": {"ing": "You wept at the funeral.","esp": "Tú lloraste en el funeral."},
            "participio":   {"ing": "She has wept for hours.","esp": "Ella ha llorado por horas."},
            "gerundio":     {"ing": "They are weeping for joy.","esp": "Ellos están llorando de alegría."},
            "futuro":       {"ing": "We will weep with them.","esp": "Nosotros lloraremos con ellos."},
            "condicional":  {"ing": "That story would make anyone weep.","esp": "Esa historia haría llorar a cualquiera."}
        }
    },
    {
        "ing_inf": "win", "esp_inf": "ganar",
        "pasado_ing": "won", "pasado_esp": "ganó",
        "participio_ing": "won", "participio_esp": "ganado",
        "gerundio_ing": "winning", "gerundio_esp": "ganando",
        "oraciones": {
            "infinitivo":   {"ing": "I win at chess sometimes.","esp": "Yo gano al ajedrez a veces."},
            "pasadoSimple": {"ing": "You won the lottery.","esp": "Tú ganaste la lotería."},
            "participio":   {"ing": "She has won three awards.","esp": "Ella ha ganado tres premios."},
            "gerundio":     {"ing": "They are winning the game.","esp": "Ellos están ganando el juego."},
            "futuro":       {"ing": "We will win the championship.","esp": "Nosotros ganaremos el campeonato."},
            "condicional":  {"ing": "That team would win easily.","esp": "Ese equipo ganaría fácilmente."}
        }
    },
    {
        "ing_inf": "write", "esp_inf": "escribir",
        "pasado_ing": "wrote", "pasado_esp": "escribió",
        "participio_ing": "written", "participio_esp": "escrito",
        "gerundio_ing": "writing", "gerundio_esp": "escribiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I write in my journal daily.","esp": "Yo escribo en mi diario a diario."},
            "pasadoSimple": {"ing": "You wrote a beautiful poem.","esp": "Tú escribiste un poema hermoso."},
            "participio":   {"ing": "She has written three books.","esp": "Ella ha escrito tres libros."},
            "gerundio":     {"ing": "They are writing code now.","esp": "Ellos están escribiendo código ahora."},
            "futuro":       {"ing": "We will write the report.","esp": "Nosotros escribiremos el informe."},
            "condicional":  {"ing": "That author would write beautifully.","esp": "Ese autor escribiría hermosamente."}
        }
    },
    {
        "ing_inf": "arise", "esp_inf": "surgir",
        "pasado_ing": "arose", "pasado_esp": "surgió",
        "participio_ing": "arisen", "participio_esp": "surgido",
        "gerundio_ing": "arising", "gerundio_esp": "surgiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I see problems arise daily.","esp": "Yo veo problemas surgir a diario."},
            "pasadoSimple": {"ing": "You arose from poverty.","esp": "Tú surgiste de la pobreza."},
            "participio":   {"ing": "The issue has arisen unexpectedly.","esp": "El problema ha surgido inesperadamente."},
            "gerundio":     {"ing": "They are arising from their seats.","esp": "Ellos se están levantando de sus asientos."},
            "futuro":       {"ing": "We will arise to the challenge.","esp": "Nosotros surgiremos ante el desafío."},
            "condicional":  {"ing": "That problem would arise later.","esp": "Ese problema surgiría después."}
        }
    },
    {
        "ing_inf": "awake", "esp_inf": "despertarse",
        "pasado_ing": "awoke", "pasado_esp": "se despertó",
        "participio_ing": "awoken", "participio_esp": "despierto",
        "gerundio_ing": "awaking", "gerundio_esp": "despertándose",
        "futuro_esp": "se despertará", "cond_esp": "se despertaría",
        "oraciones": {
            "infinitivo":   {"ing": "I awake refreshed after sleep.","esp": "Yo me despierto descansado después de dormir."},
            "pasadoSimple": {"ing": "You awoke to the alarm.","esp": "Tú te despertaste con la alarma."},
            "participio":   {"ing": "She has awoken early today.","esp": "Ella se ha despertado temprano hoy."},
            "gerundio":     {"ing": "They are awaking to reality.","esp": "Ellos se están despertando a la realidad."},
            "futuro":       {"ing": "We will awake refreshed.","esp": "Nosotros nos despertaremos descansados."},
            "condicional":  {"ing": "That would awake anyone.","esp": "Eso despertaría a cualquiera."}
        }
    },
    {
        "ing_inf": "bear", "esp_inf": "soportar",
        "pasado_ing": "bore", "pasado_esp": "soportó",
        "participio_ing": "borne", "participio_esp": "soportado",
        "gerundio_ing": "bearing", "gerundio_esp": "soportando",
        "oraciones": {
            "infinitivo":   {"ing": "I bear the responsibility alone.","esp": "Yo soporto la responsabilidad solo."},
            "pasadoSimple": {"ing": "You bore the weight well.","esp": "Tú soportaste bien el peso."},
            "participio":   {"ing": "She has borne three children.","esp": "Ella ha dado a luz a tres niños."},
            "gerundio":     {"ing": "They are bearing gifts.","esp": "Ellos están llevando regalos."},
            "futuro":       {"ing": "We will bear the cost.","esp": "Nosotros soportaremos el costo."},
            "condicional":  {"ing": "That would bear any weight.","esp": "Eso soportaría cualquier peso."}
        }
    },
    {
        "ing_inf": "beat", "esp_inf": "vencer",
        "pasado_ing": "beat", "pasado_esp": "venció",
        "participio_ing": "beaten", "participio_esp": "vencido",
        "gerundio_ing": "beating", "gerundio_esp": "venciendo",
        "oraciones": {
            "infinitivo":   {"ing": "I beat the eggs for the cake.","esp": "Yo bate los huevos para el pastel."},
            "pasadoSimple": {"ing": "You beat the record.","esp": "Tú venciste el récord."},
            "participio":   {"ing": "She has beaten all opponents.","esp": "Ella ha vencido a todos los oponentes."},
            "gerundio":     {"ing": "They are beating the drums.","esp": "Ellos están tocando los tambores."},
            "futuro":       {"ing": "We will beat the deadline.","esp": "Nosotros venceremos el plazo."},
            "condicional":  {"ing": "That team would beat anyone.","esp": "Ese equipo vencería a cualquiera."}
        }
    },
    {
        "ing_inf": "bend", "esp_inf": "doblar",
        "pasado_ing": "bent", "pasado_esp": "dobló",
        "participio_ing": "bent", "participio_esp": "doblado",
        "gerundio_ing": "bending", "gerundio_esp": "doblando",
        "oraciones": {
            "infinitivo":   {"ing": "I bend the rules sometimes.","esp": "Yo doblo las reglas a veces."},
            "pasadoSimple": {"ing": "You bent the wire.","esp": "Tú doblaste el alambre."},
            "participio":   {"ing": "She has bent over backward.","esp": "Ella se ha inclinado hacia atrás."},
            "gerundio":     {"ing": "They are bending the rules.","esp": "Ellos están doblando las reglas."},
            "futuro":       {"ing": "We will bend but not break.","esp": "Nosotros nos doblaremos pero no romperemos."},
            "condicional":  {"ing": "That branch would bend easily.","esp": "Esa rama se doblaría fácilmente."}
        }
    },
    {
        "ing_inf": "bet", "esp_inf": "apostar",
        "pasado_ing": "bet", "pasado_esp": "apostó",
        "participio_ing": "bet", "participio_esp": "apostado",
        "gerundio_ing": "betting", "gerundio_esp": "apostando",
        "oraciones": {
            "infinitivo":   {"ing": "I bet on horses sometimes.","esp": "Yo apuesto a los caballos a veces."},
            "pasadoSimple": {"ing": "You bet all your money.","esp": "Tú apostaste todo tu dinero."},
            "participio":   {"ing": "She has bet on the underdog.","esp": "Ella ha apostado al más débil."},
            "gerundio":     {"ing": "They are betting on the game.","esp": "Ellos están apostando al juego."},
            "futuro":       {"ing": "We will bet on ourselves.","esp": "Nosotros apostaremos por nosotros mismos."},
            "condicional":  {"ing": "That would bet on anything.","esp": "Eso apostaría a cualquier cosa."}
        }
    },
    {
        "ing_inf": "bind", "esp_inf": "atar",
        "pasado_ing": "bound", "pasado_esp": "ató",
        "participio_ing": "bound", "participio_esp": "atado",
        "gerundio_ing": "binding", "gerundio_esp": "atando",
        "oraciones": {
            "infinitivo":   {"ing": "I bind the books together.","esp": "Yo ato los libros juntos."},
            "pasadoSimple": {"ing": "You bound the rope tightly.","esp": "Tú ataste la cuerda con fuerza."},
            "participio":   {"ing": "The contract has bound them legally.","esp": "El contrato los ha vinculado legalmente."},
            "gerundio":     {"ing": "They are binding the agreement.","esp": "Ellos están formalizando el acuerdo."},
            "futuro":       {"ing": "We will bind the documents.","esp": "Nosotros encuadernaremos los documentos."},
            "condicional":  {"ing": "That contract would bind anyone.","esp": "Ese contrato vincularía a cualquiera."}
        }
    },
    {
        "ing_inf": "bleed", "esp_inf": "sangrar",
        "pasado_ing": "bled", "pasado_esp": "sangró",
        "participio_ing": "bled", "participio_esp": "sangrado",
        "gerundio_ing": "bleeding", "gerundio_esp": "sangrando",
        "oraciones": {
            "infinitivo":   {"ing": "I bleed easily from cuts.","esp": "Yo sangro fácilmente por cortes."},
            "pasadoSimple": {"ing": "You bled a lot yesterday.","esp": "Tú sangraste mucho ayer."},
            "participio":   {"ing": "She has bled from the wound.","esp": "Ella ha sangrado por la herida."},
            "gerundio":     {"ing": "They are bleeding heavily.","esp": "Ellos están sangrando mucho."},
            "futuro":       {"ing": "We will bleed for the cause.","esp": "Nosotros sangraremos por la causa."},
            "condicional":  {"ing": "That cut would bleed badly.","esp": "Ese corte sangraría mucho."}
        }
    },
    {
        "ing_inf": "breed", "esp_inf": "criar",
        "pasado_ing": "bred", "pasado_esp": "crió",
        "participio_ing": "bred", "participio_esp": "criado",
        "gerundio_ing": "breeding", "gerundio_esp": "criando",
        "oraciones": {
            "infinitivo":   {"ing": "I breed dogs as a hobby.","esp": "Yo crio perros como pasatiempo."},
            "pasadoSimple": {"ing": "You bred horses on the farm.","esp": "Tú criaste caballos en la granja."},
            "participio":   {"ing": "She has bred award-winning cats.","esp": "Ella ha criado gatos premiados."},
            "gerundio":     {"ing": "They are breeding cattle.","esp": "Ellos están criando ganado."},
            "futuro":       {"ing": "We will breed awareness.","esp": "Nosotros crearemos conciencia."},
            "condicional":  {"ing": "That situation would breed conflict.","esp": "Esa situación generaría conflicto."}
        }
    },
    {
        "ing_inf": "broadcast", "esp_inf": "transmitir",
        "pasado_ing": "broadcast", "pasado_esp": "transmitió",
        "participio_ing": "broadcast", "participio_esp": "transmitido",
        "gerundio_ing": "broadcasting", "gerundio_esp": "transmitiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I broadcast music online.","esp": "Yo transmito música en línea."},
            "pasadoSimple": {"ing": "You broadcast the news yesterday.","esp": "Tú transmitiste la noticia ayer."},
            "participio":   {"ing": "She has broadcast the show.","esp": "Ella ha transmitido el programa."},
            "gerundio":     {"ing": "They are broadcasting live.","esp": "Ellos están transmitiendo en vivo."},
            "futuro":       {"ing": "We will broadcast the event.","esp": "Nosotros transmitiremos el evento."},
            "condicional":  {"ing": "That station would broadcast worldwide.","esp": "Esa estación transmitiría mundialmente."}
        }
    },
    {
        "ing_inf": "cast", "esp_inf": "lanzar",
        "pasado_ing": "cast", "pasado_esp": "lanzó",
        "participio_ing": "cast", "participio_esp": "lanzado",
        "gerundio_ing": "casting", "gerundio_esp": "lanzando",
        "oraciones": {
            "infinitivo":   {"ing": "I cast my vote every election.","esp": "Yo emito mi voto cada elección."},
            "pasadoSimple": {"ing": "You cast the line into the water.","esp": "Tú lanzaste la línea al agua."},
            "participio":   {"ing": "She has been cast in the movie.","esp": "Ella ha sido elegida para la película."},
            "gerundio":     {"ing": "They are casting the actors.","esp": "Ellos están eligiendo a los actores."},
            "futuro":       {"ing": "We will cast the spell.","esp": "Nosotros lanzaremos el hechizo."},
            "condicional":  {"ing": "That actor would cast well.","esp": "Ese actor encajaría bien."}
        }
    },
    {
        "ing_inf": "cling", "esp_inf": "aferrarse",
        "pasado_ing": "clung", "pasado_esp": "se aferró",
        "participio_ing": "clung", "participio_esp": "aferrado",
        "gerundio_ing": "clinging", "gerundio_esp": "aferrándose",
        "futuro_esp": "se aferrará", "cond_esp": "se aferraría",
        "oraciones": {
            "infinitivo":   {"ing": "I cling to hope in tough times.","esp": "Yo me aferro a la esperanza en tiempos difíciles."},
            "pasadoSimple": {"ing": "You clung to the rope.","esp": "Tú te aferraste a la cuerda."},
            "participio":   {"ing": "She has clung to her beliefs.","esp": "Ella se ha aferrado a sus creencias."},
            "gerundio":     {"ing": "They are clinging to each other.","esp": "Ellos se están aferrando el uno al otro."},
            "futuro":       {"ing": "We will cling to hope.","esp": "Nosotros nos aferraremos a la esperanza."},
            "condicional":  {"ing": "That smell would cling to clothes.","esp": "Ese olor se aferraría a la ropa."}
        }
    },
    {
        "ing_inf": "creep", "esp_inf": "arrastrarse",
        "pasado_ing": "crept", "pasado_esp": "se arrastró",
        "participio_ing": "crept", "participio_esp": "arrastrado",
        "gerundio_ing": "creeping", "gerundio_esp": "arrastrándose",
        "futuro_esp": "se arrastrará", "cond_esp": "se arrastraría",
        "oraciones": {
            "infinitivo":   {"ing": "I creep downstairs quietly.","esp": "Yo me arrastro escaleras abajo en silencio."},
            "pasadoSimple": {"ing": "You crept up behind me.","esp": "Tú te arrastraste detrás de mí."},
            "participio":   {"ing": "The vine has crept up the wall.","esp": "La enredadera se ha arrastrado por la pared."},
            "gerundio":     {"ing": "They are creeping through the forest.","esp": "Ellos se están arrastrando por el bosque."},
            "futuro":       {"ing": "We will creep forward slowly.","esp": "Nosotros nos arrastraremos lentamente."},
            "condicional":  {"ing": "That sound would creep anyone out.","esp": "Ese sonido pondría nervioso a cualquiera."}
        }
    }
]


BLOQUE_IRREGULARES_5 = [
    {
        "ing_inf": "dwell", "esp_inf": "residir",
        "pasado_ing": "dwelt", "pasado_esp": "residió",
        "participio_ing": "dwelt", "participio_esp": "residido",
        "gerundio_ing": "dwelling", "gerundio_esp": "residiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I dwell on the past too much.","esp": "Yo me quedo pensando en el pasado demasiado."},
            "pasadoSimple": {"ing": "You dwelt on that point.","esp": "Tú insististe en ese punto."},
            "participio":   {"ing": "She has dwelt on negative thoughts.","esp": "Ella se ha quedado pensando en pensamientos negativos."},
            "gerundio":     {"ing": "They are dwelling on the issue.","esp": "Ellos están insistiendo en el tema."},
            "futuro":       {"ing": "We will dwell in peace.","esp": "Nosotros viviremos en paz."},
            "condicional":  {"ing": "That memory would dwell forever.","esp": "Ese recuerdo perduraría para siempre."}
        }
    },
    {
        "ing_inf": "feed", "esp_inf": "alimentar",
        "pasado_ing": "fed", "pasado_esp": "alimentó",
        "participio_ing": "fed", "participio_esp": "alimentado",
        "gerundio_ing": "feeding", "gerundio_esp": "alimentando",
        "oraciones": {
            "infinitivo":   {"ing": "I feed my dog twice daily.","esp": "Yo alimento a mi perro dos veces al día."},
            "pasadoSimple": {"ing": "You fed the baby at midnight.","esp": "Tú alimentaste al bebé a medianoche."},
            "participio":   {"ing": "She has fed the hungry.","esp": "Ella ha alimentado a los hambrientos."},
            "gerundio":     {"ing": "They are feeding the animals.","esp": "Ellos están alimentando a los animales."},
            "futuro":       {"ing": "We will feed the family.","esp": "Nosotros alimentaremos a la familia."},
            "condicional":  {"ing": "That data would feed the model.","esp": "Esos datos alimentarían el modelo."}
        }
    },
    {
        "ing_inf": "fling", "esp_inf": "lanzar",
        "pasado_ing": "flung", "pasado_esp": "lanzó",
        "participio_ing": "flung", "participio_esp": "lanzado",
        "gerundio_ing": "flinging", "gerundio_esp": "lanzando",
        "oraciones": {
            "infinitivo":   {"ing": "I fling myself into work.","esp": "Yo me lanzo al trabajo."},
            "pasadoSimple": {"ing": "You flung the door open.","esp": "Tú lanzaste la puerta abierta."},
            "participio":   {"ing": "She has flung caution aside.","esp": "Ella ha dejado la prudencia de lado."},
            "gerundio":     {"ing": "They are flinging stones.","esp": "Ellos están lanzando piedras."},
            "futuro":       {"ing": "We will fling the frisbee.","esp": "Nosotros lanzaremos el frisbee."},
            "condicional":  {"ing": "That catapult would fling far.","esp": "Esa catapulta lanzaría lejos."}
        }
    },
    {
        "ing_inf": "forsake", "esp_inf": "abandonar",
        "pasado_ing": "forsook", "pasado_esp": "abandonó",
        "participio_ing": "forsaken", "participio_esp": "abandonado",
        "gerundio_ing": "forsaking", "gerundio_esp": "abandonando",
        "oraciones": {
            "infinitivo":   {"ing": "I forsake bad habits yearly.","esp": "Yo abandono malos hábitos cada año."},
            "pasadoSimple": {"ing": "You forsook your old ways.","esp": "Tú abandonaste tus viejas costumbres."},
            "participio":   {"ing": "She has forsaken her fears.","esp": "Ella ha abandonado sus miedos."},
            "gerundio":     {"ing": "They are forsaking tradition.","esp": "Ellos están abandonando la tradición."},
            "futuro":       {"ing": "We will forsake nothing.","esp": "Nosotros no abandonaremos nada."},
            "condicional":  {"ing": "That would forsake all hope.","esp": "Eso abandonaría toda esperanza."}
        }
    },
    {
        "ing_inf": "grind", "esp_inf": "moler",
        "pasado_ing": "ground", "pasado_esp": "molió",
        "participio_ing": "ground", "participio_esp": "molido",
        "gerundio_ing": "grinding", "gerundio_esp": "moliendo",
        "oraciones": {
            "infinitivo":   {"ing": "I grind coffee beans daily.","esp": "Yo muelo granos de café a diario."},
            "pasadoSimple": {"ing": "You ground the spices.","esp": "Tú moliste las especias."},
            "participio":   {"ing": "She has ground the wheat.","esp": "Ella ha molido el trigo."},
            "gerundio":     {"ing": "They are grinding the meat.","esp": "Ellos están moliendo la carne."},
            "futuro":       {"ing": "We will grind the corn.","esp": "Nosotros moleremos el maíz."},
            "condicional":  {"ing": "That mill would grind quickly.","esp": "Ese molino molería rápido."}
        }
    },
    {
        "ing_inf": "heave", "esp_inf": "empujar",
        "pasado_ing": "heaved", "pasado_esp": "empujó",
        "participio_ing": "heaved", "participio_esp": "empujado",
        "gerundio_ing": "heaving", "gerundio_esp": "empujando",
        "oraciones": {
            "infinitivo":   {"ing": "I heave a sigh of relief.","esp": "Yo suspiro de alivio."},
            "pasadoSimple": {"ing": "You heaved the box up.","esp": "Tú levantaste la caja."},
            "participio":   {"ing": "She has heaved the anchor.","esp": "Ella ha levantado el ancla."},
            "gerundio":     {"ing": "They are heaving bags around.","esp": "Ellos están moviendo bolsas."},
            "futuro":       {"ing": "We will heave the trash out.","esp": "Nosotros sacaremos la basura."},
            "condicional":  {"ing": "That wave would heave the boat.","esp": "Esa ola zarandearía el barco."}
        }
    },
    {
        "ing_inf": "knit", "esp_inf": "tejer",
        "pasado_ing": "knitted", "pasado_esp": "tejió",
        "participio_ing": "knitted", "participio_esp": "tejido",
        "gerundio_ing": "knitting", "gerundio_esp": "tejiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I knit scarves for gifts.","esp": "Yo tejo bufandas para regalos."},
            "pasadoSimple": {"ing": "You knitted that sweater.","esp": "Tú tejiste ese suéter."},
            "participio":   {"ing": "She has knitted baby clothes.","esp": "Ella ha tejido ropa de bebé."},
            "gerundio":     {"ing": "They are knitting together.","esp": "Ellos están tejiendo juntos."},
            "futuro":       {"ing": "We will knit all winter.","esp": "Nosotros tejeremos todo el invierno."},
            "condicional":  {"ing": "That yarn would knit beautifully.","esp": "Ese hilo tejería hermosamente."}
        }
    },
    {
        "ing_inf": "leap", "esp_inf": "saltar",
        "pasado_ing": "leapt", "pasado_esp": "saltó",
        "participio_ing": "leapt", "participio_esp": "saltado",
        "gerundio_ing": "leaping", "gerundio_esp": "saltando",
        "oraciones": {
            "infinitivo":   {"ing": "I leap at new opportunities.","esp": "Yo aprovecho nuevas oportunidades."},
            "pasadoSimple": {"ing": "You leapt over the puddle.","esp": "Tú saltaste el charco."},
            "participio":   {"ing": "The frog has leapt into the pond.","esp": "La rana ha saltado al estanque."},
            "gerundio":     {"ing": "They are leaping for joy.","esp": "Ellos están saltando de alegría."},
            "futuro":       {"ing": "We will leap at the chance.","esp": "Nosotros aprovecharemos la oportunidad."},
            "condicional":  {"ing": "That deer would leap high.","esp": "Ese ciervo saltaría alto."}
        }
    },
    {
        "ing_inf": "lean", "esp_inf": "apoyarse",
        "pasado_ing": "leant/leaned", "pasado_esp": "se apoyó",
        "participio_ing": "leant/leaned", "participio_esp": "apoyado",
        "gerundio_ing": "leaning", "gerundio_esp": "apoyándose",
        "futuro_esp": "se apoyará", "cond_esp": "se apoyaría",
        "oraciones": {
            "infinitivo":   {"ing": "I lean toward the left politically.","esp": "Yo me inclino hacia la izquierda políticamente."},
            "pasadoSimple": {"ing": "You leant against the wall.","esp": "Tú te apoyaste contra la pared."},
            "participio":   {"ing": "She has leant on her family.","esp": "Ella se ha apoyado en su familia."},
            "gerundio":     {"ing": "They are leaning out the window.","esp": "Ellos se están asomando por la ventana."},
            "futuro":       {"ing": "We will lean into the curve.","esp": "Nosotros nos inclinaremos en la curva."},
            "condicional":  {"ing": "That ladder would lean dangerously.","esp": "Esa escalera se inclinaría peligrosamente."}
        }
    },
    {
        "ing_inf": "learn", "esp_inf": "aprender",
        "pasado_ing": "learned/learnt", "pasado_esp": "aprendió",
        "participio_ing": "learned/learnt", "participio_esp": "aprendido",
        "gerundio_ing": "learning", "gerundio_esp": "aprendiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I learn something new daily.","esp": "Yo aprendo algo nuevo cada día."},
            "pasadoSimple": {"ing": "You learned to cook last year.","esp": "Tú aprendiste a cocinar el año pasado."},
            "participio":   {"ing": "She has learned three languages.","esp": "Ella ha aprendido tres idiomas."},
            "gerundio":     {"ing": "They are learning quickly.","esp": "Ellos están aprendiendo rápido."},
            "futuro":       {"ing": "We will learn from mistakes.","esp": "Nosotros aprenderemos de los errores."},
            "condicional":  {"ing": "That experience would teach anyone to learn.","esp": "Esa experiencia enseñaría a cualquiera a aprender."}
        }
    },
    {
        "ing_inf": "leave", "esp_inf": "dejar",
        "pasado_ing": "left", "pasado_esp": "dejó",
        "participio_ing": "left", "participio_esp": "dejado",
        "gerundio_ing": "leaving", "gerundio_esp": "dejando",
        "oraciones": {
            "infinitivo":   {"ing": "I leave work at six.","esp": "Yo salgo del trabajo a las seis."},
            "pasadoSimple": {"ing": "You left your keys behind.","esp": "Tú dejaste tus llaves atrás."},
            "participio":   {"ing": "She has left for the day.","esp": "Ella se ha ido por hoy."},
            "gerundio":     {"ing": "They are leaving now.","esp": "Ellos se están yendo ahora."},
            "futuro":       {"ing": "We will leave early.","esp": "Nosotros saldremos temprano."},
            "condicional":  {"ing": "That would leave a mark.","esp": "Eso dejaría una marca."}
        }
    },
    {
        "ing_inf": "lend", "esp_inf": "prestar",
        "pasado_ing": "lent", "pasado_esp": "prestó",
        "participio_ing": "lent", "participio_esp": "prestado",
        "gerundio_ing": "lending", "gerundio_esp": "prestando",
        "oraciones": {
            "infinitivo":   {"ing": "I lend books to neighbors.","esp": "Yo presto libros a vecinos."},
            "pasadoSimple": {"ing": "You lent me your car.","esp": "Tú me prestaste tu coche."},
            "participio":   {"ing": "She has lent her support.","esp": "Ella ha prestado su apoyo."},
            "gerundio":     {"ing": "They are lending money.","esp": "Ellos están prestando dinero."},
            "futuro":       {"ing": "We will lend a hand.","esp": "Nosotros echaremos una mano."},
            "condicional":  {"ing": "That bank would lend easily.","esp": "Ese banco prestaría fácilmente."}
        }
    },
    {
        "ing_inf": "mislead", "esp_inf": "engañar",
        "pasado_ing": "misled", "pasado_esp": "engañó",
        "participio_ing": "misled", "participio_esp": "engañado",
        "gerundio_ing": "misleading", "gerundio_esp": "engañando",
        "oraciones": {
            "infinitivo":   {"ing": "I mislead no one intentionally.","esp": "Yo no engaño a nadie a propósito."},
            "pasadoSimple": {"ing": "You misled me yesterday.","esp": "Tú me engañaste ayer."},
            "participio":   {"ing": "She has misled the public.","esp": "Ella ha engañado al público."},
            "gerundio":     {"ing": "They are misleading voters.","esp": "Ellos están engañando a los votantes."},
            "futuro":       {"ing": "We will mislead no one.","esp": "Nosotros no engañaremos a nadie."},
            "condicional":  {"ing": "That label would mislead anyone.","esp": "Esa etiqueta engañaría a cualquiera."}
        }
    },
    {
        "ing_inf": "mistake", "esp_inf": "confundir",
        "pasado_ing": "mistook", "pasado_esp": "confundió",
        "participio_ing": "mistaken", "participio_esp": "confundido",
        "gerundio_ing": "mistaking", "gerundio_esp": "confundiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I mistake her for her sister.","esp": "Yo la confundo con su hermana."},
            "pasadoSimple": {"ing": "You mistook the address.","esp": "Tú confundiste la dirección."},
            "participio":   {"ing": "She has mistaken the date.","esp": "Ella ha confundido la fecha."},
            "gerundio":     {"ing": "They are mistaking noise for music.","esp": "Ellos están confundiendo ruido con música."},
            "futuro":       {"ing": "We will not mistake kindness for weakness.","esp": "Nosotros no confundiremos amabilidad con debilidad."},
            "condicional":  {"ing": "That shadow would mistake anyone.","esp": "Esa sombra confundiría a cualquiera."}
        }
    },
    {
        "ing_inf": "outgrow", "esp_inf": "superar",
        "pasado_ing": "outgrew", "pasado_esp": "superó",
        "participio_ing": "outgrown", "participio_esp": "superado",
        "gerundio_ing": "outgrowing", "gerundio_esp": "superando",
        "oraciones": {
            "infinitivo":   {"ing": "I outgrow clothes quickly.","esp": "Yo supero la ropa rápidamente."},
            "pasadoSimple": {"ing": "You outgrew your fears.","esp": "Tú superaste tus miedos."},
            "participio":   {"ing": "She has outgrown the hobby.","esp": "Ella ha superado el pasatiempo."},
            "gerundio":     {"ing": "They are outgrowing the house.","esp": "Ellos están quedándose sin espacio en la casa."},
            "futuro":       {"ing": "We will outgrow this phase.","esp": "Nosotros superaremos esta fase."},
            "condicional":  {"ing": "That trend would outgrow itself.","esp": "Esa tendencia se extinguiría sola."}
        }
    },
    {
        "ing_inf": "overdo", "esp_inf": "exagerar",
        "pasado_ing": "overdid", "pasado_esp": "exageró",
        "participio_ing": "overdone", "participio_esp": "exagerado",
        "gerundio_ing": "overdoing", "gerundio_esp": "exagerando",
        "oraciones": {
            "infinitivo":   {"ing": "I overdo it at the gym sometimes.","esp": "Yo me exijo demasiado en el gimnasio a veces."},
            "pasadoSimple": {"ing": "You overdid the spices.","esp": "Tú te excediste con las especias."},
            "participio":   {"ing": "She has overdone the workout.","esp": "Ella se ha excedido con el ejercicio."},
            "gerundio":     {"ing": "They are overdoing the celebrations.","esp": "Ellos están exagerando las celebraciones."},
            "futuro":       {"ing": "We will not overdo the decorations.","esp": "Nosotros no exageraremos las decoraciones."},
            "condicional":  {"ing": "That joke would overdo it.","esp": "Esa broma exageraría."}
        }
    },
    {
        "ing_inf": "overcome", "esp_inf": "superar",
        "pasado_ing": "overcame", "pasado_esp": "superó",
        "participio_ing": "overcome", "participio_esp": "superado",
        "gerundio_ing": "overcoming", "gerundio_esp": "superando",
        "oraciones": {
            "infinitivo":   {"ing": "I overcome challenges daily.","esp": "Yo supero retos a diario."},
            "pasadoSimple": {"ing": "You overcame your fear.","esp": "Tú superaste tu miedo."},
            "participio":   {"ing": "She has overcome the obstacles.","esp": "Ella ha superado los obstáculos."},
            "gerundio":     {"ing": "They are overcoming difficulties.","esp": "Ellos están superando dificultades."},
            "futuro":       {"ing": "We will overcome this together.","esp": "Nosotros superaremos esto juntos."},
            "condicional":  {"ing": "That obstacle would overcome anyone.","esp": "Ese obstáculo superaría a cualquiera."}
        }
    },
    {
        "ing_inf": "overeat", "esp_inf": "atracarse",
        "pasado_ing": "overate", "pasado_esp": "se atracó",
        "participio_ing": "overeaten", "participio_esp": "atracado",
        "gerundio_ing": "overeating", "gerundio_esp": "atracándose",
        "futuro_esp": "se atracará", "cond_esp": "se atracaría",
        "oraciones": {
            "infinitivo":   {"ing": "I overeat on holidays sometimes.","esp": "Yo como de más en las fiestas a veces."},
            "pasadoSimple": {"ing": "You overate at the buffet.","esp": "Tú comiste de más en el bufé."},
            "participio":   {"ing": "She has overeaten badly.","esp": "Ella ha comido demasiado."},
            "gerundio":     {"ing": "They are overeating constantly.","esp": "Ellos están comiendo en exceso constantemente."},
            "futuro":       {"ing": "We will overeat at dinner.","esp": "Nosotros comeremos de más en la cena."},
            "condicional":  {"ing": "That feast would overeat anyone.","esp": "Esa fiesta haría que cualquiera comiera de más."}
        }
    },
    {
        "ing_inf": "overhear", "esp_inf": "oír",
        "pasado_ing": "overheard", "pasado_esp": "oyó",
        "participio_ing": "overheard", "participio_esp": "oído",
        "gerundio_ing": "overhearing", "gerundio_esp": "oyendo",
        "oraciones": {
            "infinitivo":   {"ing": "I overhear conversations on the bus.","esp": "Yo oigo conversaciones en el autobús."},
            "pasadoSimple": {"ing": "You overheard their secret.","esp": "Tú oíste su secreto por casualidad."},
            "participio":   {"ing": "She has overheard the gossip.","esp": "Ella ha oído el chisme por casualidad."},
            "gerundio":     {"ing": "They are overhearing the meeting.","esp": "Ellos están oyendo la reunión sin querer."},
            "futuro":       {"ing": "We will overhear their conversation.","esp": "Nosotros oiremos su conversación sin querer."},
            "condicional":  {"ing": "That microphone would overhear everything.","esp": "Ese micrófono oiría todo."}
        }
    },
    {
        "ing_inf": "overlay", "esp_inf": "superponer",
        "pasado_ing": "overlaid", "pasado_esp": "superpuso",
        "participio_ing": "overlaid", "participio_esp": "superpuesto",
        "gerundio_ing": "overlaying", "gerundio_esp": "superponiendo",
        "futuro_esp": "superpondrá", "cond_esp": "superpondría",
        "oraciones": {
            "infinitivo":   {"ing": "I overlay text on images.","esp": "Yo superpongo texto en imágenes."},
            "pasadoSimple": {"ing": "You overlaid the maps yesterday.","esp": "Tú superpusiste los mapas ayer."},
            "participio":   {"ing": "She has overlaid the patterns.","esp": "Ella ha superpuesto los patrones."},
            "gerundio":     {"ing": "They are overlaying the videos.","esp": "Ellos están superponiendo los videos."},
            "futuro":       {"ing": "We will overlay the images later.","esp": "Nosotros superpondremos las imágenes después."},
            "condicional":  {"ing": "That texture would overlay nicely.","esp": "Esa textura se superpondría bien."}
        }
    },
    {
        "ing_inf": "override", "esp_inf": "anular",
        "pasado_ing": "overrode", "pasado_esp": "anuló",
        "participio_ing": "overridden", "participio_esp": "anulado",
        "gerundio_ing": "overriding", "gerundio_esp": "anulando",
        "oraciones": {
            "infinitivo":   {"ing": "I override the default settings.","esp": "Yo anulo la configuración predeterminada."},
            "pasadoSimple": {"ing": "You overrode my decision.","esp": "Tú anulaste mi decisión."},
            "participio":   {"ing": "She has overridden the system.","esp": "Ella ha anulado el sistema."},
            "gerundio":     {"ing": "They are overriding the rules.","esp": "Ellos están anulando las reglas."},
            "futuro":       {"ing": "We will override the veto.","esp": "Nosotros anularremos el veto."},
            "condicional":  {"ing": "That command would override everything.","esp": "Ese comando anularía todo."}
        }
    },
    {
        "ing_inf": "oversleep", "esp_inf": "dormirse de más",
        "pasado_ing": "overslept", "pasado_esp": "se durmió de más",
        "participio_ing": "overslept", "participio_esp": "dormido de más",
        "gerundio_ing": "oversleeping", "gerundio_esp": "durmiéndose de más",
        "futuro_esp": "se dormirá de más", "cond_esp": "se dormiría de más",
        "oraciones": {
            "infinitivo":   {"ing": "I oversleep on weekends sometimes.","esp": "Yo duermo de más los fines de semana a veces."},
            "pasadoSimple": {"ing": "You overslept and missed class.","esp": "Tú dormiste de más y perdiste clase."},
            "participio":   {"ing": "She has overslept three times.","esp": "Ella ha dormido de más tres veces."},
            "gerundio":     {"ing": "They are oversleeping the meeting.","esp": "Ellos están durmiendo de más para la reunión."},
            "futuro":       {"ing": "We will oversleep if tired.","esp": "Nosotros dormiremos de más si estamos cansados."},
            "condicional":  {"ing": "That alarm would oversleep anyone.","esp": "Esa alarma haría que cualquiera duerma de más."}
        }
    },
    {
        "ing_inf": "overtake", "esp_inf": "adelantar",
        "pasado_ing": "overtook", "pasado_esp": "adelantó",
        "participio_ing": "overtaken", "participio_esp": "adelantado",
        "gerundio_ing": "overtaking", "gerundio_esp": "adelantando",
        "oraciones": {
            "infinitivo":   {"ing": "I overtake slower cars carefully.","esp": "Yo adelanto coches más lentos con cuidado."},
            "pasadoSimple": {"ing": "You overtook the truck.","esp": "Tú adelantaste al camión."},
            "participio":   {"ing": "She has overtaken the competition.","esp": "Ella ha sobrepasado a la competencia."},
            "gerundio":     {"ing": "They are overtaking us fast.","esp": "Ellos nos están adelantando rápido."},
            "futuro":       {"ing": "We will overtake the leader.","esp": "Nosotros adelantaremos al líder."},
            "condicional":  {"ing": "That wave would overtake the boat.","esp": "Esa ola sobrepasaría el barco."}
        }
    },
    {
        "ing_inf": "overthrow", "esp_inf": "derrocar",
        "pasado_ing": "overthrew", "pasado_esp": "derrocó",
        "participio_ing": "overthrown", "participio_esp": "derrocado",
        "gerundio_ing": "overthrowing", "gerundio_esp": "derrocando",
        "oraciones": {
            "infinitivo":   {"ing": "I overthrow old habits yearly.","esp": "Yo derrocó viejas costumbres cada año."},
            "pasadoSimple": {"ing": "You overthrew the dictator.","esp": "Tú derrocaste al dictador."},
            "participio":   {"ing": "She has overthrown the regime.","esp": "Ella ha derrocado al régimen."},
            "gerundio":     {"ing": "They are overthrowing the king.","esp": "Ellos están derrocando al rey."},
            "futuro":       {"ing": "We will overthrow the corrupt leader.","esp": "Nosotros derrocaremos al líder corrupto."},
            "condicional":  {"ing": "That revolution would overthrow everything.","esp": "Esa revolución derrocaría todo."}
        }
    },
    {
        "ing_inf": "partake", "esp_inf": "participar",
        "pasado_ing": "partook", "pasado_esp": "participó",
        "participio_ing": "partaken", "participio_esp": "participado",
        "gerundio_ing": "partaking", "gerundio_esp": "participando",
        "oraciones": {
            "infinitivo":   {"ing": "I partake in family dinners.","esp": "Yo participo en cenas familiares."},
            "pasadoSimple": {"ing": "You partook in the feast.","esp": "Tú participaste en el festín."},
            "participio":   {"ing": "She has partaken of the meal.","esp": "Ella ha participado de la comida."},
            "gerundio":     {"ing": "They are partaking in the ceremony.","esp": "Ellos están participando en la ceremonia."},
            "futuro":       {"ing": "We will partake in the workshop.","esp": "Nosotros participaremos en el taller."},
            "condicional":  {"ing": "That wine would partake of refinement.","esp": "Ese vino participaría de refinamiento."}
        }
    },
    {
        "ing_inf": "pay", "esp_inf": "pagar",
        "pasado_ing": "paid", "pasado_esp": "pagó",
        "participio_ing": "paid", "participio_esp": "pagado",
        "gerundio_ing": "paying", "gerundio_esp": "pagando",
        "oraciones": {
            "infinitivo":   {"ing": "I pay my bills on time.","esp": "Yo pago mis cuentas a tiempo."},
            "pasadoSimple": {"ing": "You paid too much.","esp": "Tú pagaste demasiado."},
            "participio":   {"ing": "She has paid off the loan.","esp": "Ella ha pagado el préstamo."},
            "gerundio":     {"ing": "They are paying attention.","esp": "Ellos están prestando atención."},
            "futuro":       {"ing": "We will pay in cash.","esp": "Nosotros pagaremos en efectivo."},
            "condicional":  {"ing": "That investment would pay off.","esp": "Esa inversión valdría la pena."}
        }
    },
    {
        "ing_inf": "plead", "esp_inf": "suplicar",
        "pasado_ing": "pleaded/pled", "pasado_esp": "suplicó",
        "participio_ing": "pleaded/pled", "participio_esp": "suplicado",
        "gerundio_ing": "pleading", "gerundio_esp": "suplicando",
        "oraciones": {
            "infinitivo":   {"ing": "I plead for mercy sometimes.","esp": "Yo suplico clemencia a veces."},
            "pasadoSimple": {"ing": "You pleaded your case well.","esp": "Tú defendiste tu caso bien."},
            "participio":   {"ing": "She has pleaded not guilty.","esp": "Ella ha declarado no culpable."},
            "gerundio":     {"ing": "They are pleading for help.","esp": "Ellos están suplicando ayuda."},
            "futuro":       {"ing": "We will plead with the judge.","esp": "Nosotros rogaremos al juez."},
            "condicional":  {"ing": "That attorney would plead well.","esp": "Ese abogado defendería bien."}
        }
    },
    {
        "ing_inf": "preset", "esp_inf": "preestablecer",
        "pasado_ing": "preset", "pasado_esp": "preestableció",
        "participio_ing": "preset", "participio_esp": "preestablecido",
        "gerundio_ing": "presetting", "gerundio_esp": "preestableciendo",
        "futuro_esp": "preestablecerá", "cond_esp": "preestablecería",
        "oraciones": {
            "infinitivo":   {"ing": "I preset the alarm clock nightly.","esp": "Yo preestablezco la alarma cada noche."},
            "pasadoSimple": {"ing": "You preset the temperature.","esp": "Tú preestableciste la temperatura."},
            "participio":   {"ing": "She has preset the options.","esp": "Ella ha preestablecido las opciones."},
            "gerundio":     {"ing": "They are presetting the controls.","esp": "Ellos están preestableciendo los controles."},
            "futuro":       {"ing": "We will preset the defaults.","esp": "Nosotros preestableceremos los predeterminados."},
            "condicional":  {"ing": "That timer would preset automatically.","esp": "Ese temporizador se preestablecería automáticamente."}
        }
    },
    {
        "ing_inf": "prove", "esp_inf": "probar",
        "pasado_ing": "proved", "pasado_esp": "probó",
        "participio_ing": "proven", "participio_esp": "probado",
        "gerundio_ing": "proving", "gerundio_esp": "probando",
        "oraciones": {
            "infinitivo":   {"ing": "I prove theorems in math.","esp": "Yo pruebo teoremas en matemáticas."},
            "pasadoSimple": {"ing": "You proved your point.","esp": "Tú probaste tu punto."},
            "participio":   {"ing": "She has proven herself.","esp": "Ella se ha demostrado a sí misma."},
            "gerundio":     {"ing": "They are proving their theory.","esp": "Ellos están probando su teoría."},
            "futuro":       {"ing": "We will prove the hypothesis.","esp": "Nosotros probaremos la hipótesis."},
            "condicional":  {"ing": "That evidence would prove anything.","esp": "Esa evidencia probaría cualquier cosa."}
        }
    },
    {
        "ing_inf": "quit", "esp_inf": "dejar",
        "pasado_ing": "quit", "pasado_esp": "dejó",
        "participio_ing": "quit", "participio_esp": "dejado",
        "gerundio_ing": "quitting", "gerundio_esp": "dejando",
        "oraciones": {
            "infinitivo":   {"ing": "I quit smoking last year.","esp": "Yo dejé de fumar el año pasado."},
            "pasadoSimple": {"ing": "You quit the job.","esp": "Tú renunciaste al trabajo."},
            "participio":   {"ing": "She has quit smoking.","esp": "Ella ha dejado de fumar."},
            "gerundio":     {"ing": "They are quitting early today.","esp": "Ellos están saliendo temprano hoy."},
            "futuro":       {"ing": "We will quit when tired.","esp": "Nosotros pararemos cuando estemos cansados."},
            "condicional":  {"ing": "That habit would quit easily.","esp": "Ese hábito se dejaría fácilmente."}
        }
    }
]


BLOQUE_IRREGULARES_6 = [
    {
        "ing_inf": "rebuild", "esp_inf": "reconstruir",
        "pasado_ing": "rebuilt", "pasado_esp": "reconstruyó",
        "participio_ing": "rebuilt", "participio_esp": "reconstruido",
        "gerundio_ing": "rebuilding", "gerundio_esp": "reconstruyendo",
        "oraciones": {
            "infinitivo":   {"ing": "I rebuild old furniture as a hobby.","esp": "Yo reconstruyo muebles viejos como pasatiempo."},
            "pasadoSimple": {"ing": "You rebuilt the engine.","esp": "Tú reconstruiste el motor."},
            "participio":   {"ing": "She has rebuilt her life.","esp": "Ella ha reconstruido su vida."},
            "gerundio":     {"ing": "They are rebuilding the bridge.","esp": "Ellos están reconstruyendo el puente."},
            "futuro":       {"ing": "We will rebuild after the storm.","esp": "Nosotros reconstruiremos después de la tormenta."},
            "condicional":  {"ing": "That trust would rebuild slowly.","esp": "Esa confianza se reconstruiría lentamente."}
        }
    },
    {
        "ing_inf": "recast", "esp_inf": "redistribuir",
        "pasado_ing": "recast", "pasado_esp": "redistribuyó",
        "participio_ing": "recast", "participio_esp": "redistribuido",
        "gerundio_ing": "recasting", "gerundio_esp": "redistribuyendo",
        "oraciones": {
            "infinitivo":   {"ing": "I recast the vote to another candidate.","esp": "Yo redistribuyo el voto a otro candidato."},
            "pasadoSimple": {"ing": "You recast your ballot yesterday.","esp": "Tú redistribuiste tu papeleta ayer."},
            "participio":   {"ing": "She has recast the role.","esp": "Ella ha redistribuido el papel."},
            "gerundio":     {"ing": "They are recasting the play.","esp": "Ellos están redistribuyendo la obra."},
            "futuro":       {"ing": "We will recast the decision.","esp": "Nosotros redistribuiremos la decisión."},
            "condicional":  {"ing": "That would recast the vote.","esp": "Eso redistribuiría el voto."}
        }
    },
    {
        "ing_inf": "redo", "esp_inf": "rehacer",
        "pasado_ing": "redid", "pasado_esp": "rehízo",
        "participio_ing": "redone", "participio_esp": "rehecho",
        "gerundio_ing": "redoing", "gerundio_esp": "rehaciendo",
        "futuro_esp": "rehará", "cond_esp": "reharía",
        "oraciones": {
            "infinitivo":   {"ing": "I redo my homework until perfect.","esp": "Yo rehago mi tarea hasta que quede perfecta."},
            "pasadoSimple": {"ing": "You redid the test.","esp": "Tú rehiciste el examen."},
            "participio":   {"ing": "She has redone the work.","esp": "Ella ha rehecho el trabajo."},
            "gerundio":     {"ing": "They are redoing the kitchen.","esp": "Ellos están rehaciendo la cocina."},
            "futuro":       {"ing": "We will redo the budget.","esp": "Nosotros reharemos el presupuesto."},
            "condicional":  {"ing": "That would redo the entire project.","esp": "Eso rehará todo el proyecto."}
        }
    },
    {
        "ing_inf": "relay", "esp_inf": "transmitir",
        "pasado_ing": "relayed", "pasado_esp": "transmitió",
        "participio_ing": "relayed", "participio_esp": "transmitido",
        "gerundio_ing": "relaying", "gerundio_esp": "transmitiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I relay messages at work.","esp": "Yo transmito mensajes en el trabajo."},
            "pasadoSimple": {"ing": "You relayed the information.","esp": "Tú transmitiste la información."},
            "participio":   {"ing": "She has relayed the news.","esp": "Ella ha transmitido la noticia."},
            "gerundio":     {"ing": "They are relaying signals.","esp": "Ellos están transmitiendo señales."},
            "futuro":       {"ing": "We will relay the message.","esp": "Nosotros transmitiremos el mensaje."},
            "condicional":  {"ing": "That station would relay signals.","esp": "Esa estación transmitiría señales."}
        }
    },
    {
        "ing_inf": "remake", "esp_inf": "rehacer",
        "pasado_ing": "remade", "pasado_esp": "rehízo",
        "participio_ing": "remade", "participio_esp": "rehecho",
        "gerundio_ing": "remaking", "gerundio_esp": "rehaciendo",
        "futuro_esp": "rehará", "cond_esp": "reharía",
        "oraciones": {
            "infinitivo":   {"ing": "I remake recipes with healthier ingredients.","esp": "Yo rehago recetas con ingredientes más sanos."},
            "pasadoSimple": {"ing": "You remade the movie.","esp": "Tú rehiciste la película."},
            "participio":   {"ing": "She has remade the dress.","esp": "Ella ha rehecho el vestido."},
            "gerundio":     {"ing": "They are remaking the classic film.","esp": "Ellos están rehaciendo la película clásica."},
            "futuro":       {"ing": "We will remake the recipe.","esp": "Nosotros reharemos la receta."},
            "condicional":  {"ing": "That sequel would remake the success.","esp": "Esa secuela replicaría el éxito."}
        }
    },
    {
        "ing_inf": "repay", "esp_inf": "reembolsar",
        "pasado_ing": "repaid", "pasado_esp": "reembolsó",
        "participio_ing": "repaid", "participio_esp": "reembolsado",
        "gerundio_ing": "repaying", "gerundio_esp": "reembolsando",
        "oraciones": {
            "infinitivo":   {"ing": "I repay loans on time.","esp": "Yo reembolso préstamos a tiempo."},
            "pasadoSimple": {"ing": "You repaid the debt.","esp": "Tú reembolsaste la deuda."},
            "participio":   {"ing": "She has repaid her kindness.","esp": "Ella ha reembolsado su amabilidad."},
            "gerundio":     {"ing": "They are repaying the favor.","esp": "Ellos están reembolsando el favor."},
            "futuro":       {"ing": "We will repay the favor.","esp": "Nosotros reembolsaremos el favor."},
            "condicional":  {"ing": "That kindness would repay itself.","esp": "Esa amabilidad se pagaría sola."}
        }
    },
    {
        "ing_inf": "reset", "esp_inf": "restablecer",
        "pasado_ing": "reset", "pasado_esp": "restableció",
        "participio_ing": "reset", "participio_esp": "restablecido",
        "gerundio_ing": "resetting", "gerundio_esp": "restableciendo",
        "futuro_esp": "restablecerá", "cond_esp": "restablecería",
        "oraciones": {
            "infinitivo":   {"ing": "I reset the alarm every night.","esp": "Yo restablezco la alarma cada noche."},
            "pasadoSimple": {"ing": "You reset the device.","esp": "Tú restableciste el dispositivo."},
            "participio":   {"ing": "She has reset the counter.","esp": "Ella ha restablecido el contador."},
            "gerundio":     {"ing": "They are resetting the system.","esp": "Ellos están restableciendo el sistema."},
            "futuro":       {"ing": "We will reset the defaults.","esp": "Nosotros restableceremos los valores predeterminados."},
            "condicional":  {"ing": "That button would reset everything.","esp": "Ese botón restablecería todo."}
        }
    },
    {
        "ing_inf": "retell", "esp_inf": "recontar",
        "pasado_ing": "retold", "pasado_esp": "recontó",
        "participio_ing": "retold", "participio_esp": "recontado",
        "gerundio_ing": "retelling", "gerundio_esp": "recontando",
        "oraciones": {
            "infinitivo":   {"ing": "I retell stories to my kids.","esp": "Yo reconto historias a mis hijos."},
            "pasadoSimple": {"ing": "You retold the joke.","esp": "Tú recontaste el chiste."},
            "participio":   {"ing": "She has retold the tale.","esp": "Ella ha recontado el cuento."},
            "gerundio":     {"ing": "They are retelling the legend.","esp": "Ellos están recontando la leyenda."},
            "futuro":       {"ing": "We will retell the story.","esp": "Nosotros recontaremos la historia."},
            "condicional":  {"ing": "That tale would retell well.","esp": "Ese cuento se recontaría bien."}
        }
    },
    {
        "ing_inf": "rewrite", "esp_inf": "reescribir",
        "pasado_ing": "rewrote", "pasado_esp": "reescribió",
        "participio_ing": "rewritten", "participio_esp": "reescrito",
        "gerundio_ing": "rewriting", "gerundio_esp": "reescribiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I rewrite my drafts multiple times.","esp": "Yo reescribo mis borradores varias veces."},
            "pasadoSimple": {"ing": "You rewrote the essay.","esp": "Tú reescribiste el ensayo."},
            "participio":   {"ing": "She has rewritten the chapter.","esp": "Ella ha reescrito el capítulo."},
            "gerundio":     {"ing": "They are rewriting the rules.","esp": "Ellos están reescribiendo las reglas."},
            "futuro":       {"ing": "We will rewrite the code.","esp": "Nosotros reescribiremos el código."},
            "condicional":  {"ing": "That law would rewrite history.","esp": "Esa ley reescribiría la historia."}
        }
    },
    {
        "ing_inf": "rid", "esp_inf": "librar",
        "pasado_ing": "rid", "pasado_esp": "libró",
        "participio_ing": "rid", "participio_esp": "librado",
        "gerundio_ing": "ridding", "gerundio_esp": "librando",
        "oraciones": {
            "infinitivo":   {"ing": "I rid the house of pests.","esp": "Yo libro la casa de plagas."},
            "pasadoSimple": {"ing": "You rid yourself of doubts.","esp": "Tú te libraste de dudas."},
            "participio":   {"ing": "She has rid herself of bad habits.","esp": "Ella se ha librado de malos hábitos."},
            "gerundio":     {"ing": "They are ridding the garden of weeds.","esp": "Ellos están librando el jardín de maleza."},
            "futuro":       {"ing": "We will rid the city of pollution.","esp": "Nosotros libraremos la ciudad de contaminación."},
            "condicional":  {"ing": "That move would rid the problem.","esp": "Esa medida libraría del problema."}
        }
    },
    {
        "ing_inf": "rot", "esp_inf": "pudrirse",
        "pasado_ing": "rotted", "pasado_esp": "se pudrió",
        "participio_ing": "rotted", "participio_esp": "podrido",
        "gerundio_ing": "rotting", "gerundio_esp": "pudriéndose",
        "futuro_esp": "se pudrirá", "cond_esp": "se pudriría",
        "oraciones": {
            "infinitivo":   {"ing": "I let the wood rot for compost.","esp": "Yo dejo que la madera se pudra para compost."},
            "pasadoSimple": {"ing": "You let the food rot.","esp": "Tú dejaste que la comida se pudriera."},
            "participio":   {"ing": "The apple has rotted.","esp": "La manzana se ha podrido."},
            "gerundio":     {"ing": "They are rotting in jail.","esp": "Ellos se están pudriendo en la cárcel."},
            "futuro":       {"ing": "We will rot without exercise.","esp": "Nosotros nos pudriremos sin ejercicio."},
            "condicional":  {"ing": "That food would rot quickly.","esp": "Esa comida se pudriría rápido."}
        }
    },
    {
        "ing_inf": "saw", "esp_inf": "serrar",
        "pasado_ing": "sawed", "pasado_esp": "serrjó",
        "participio_ing": "sawed", "participio_esp": "serrado",
        "gerundio_ing": "sawing", "gerundio_esp": "serrando",
        "oraciones": {
            "infinitivo":   {"ing": "I saw wood for the fireplace.","esp": "Yo serrucho madera para la chimenea."},
            "pasadoSimple": {"ing": "You sawed the log yesterday.","esp": "Tú serrast el tronco ayer."},
            "participio":   {"ing": "She has sawed the boards.","esp": "Ella ha serrado las tablas."},
            "gerundio":     {"ing": "They are sawing the tree.","esp": "Ellos están serrando el árbol."},
            "futuro":       {"ing": "We will saw the wood later.","esp": "Nosotros serrremos la madera después."},
            "condicional":  {"ing": "That saw would cut easily.","esp": "Esa sierra cortaría fácilmente."}
        }
    },
    {
        "ing_inf": "send", "esp_inf": "enviar",
        "pasado_ing": "sent", "pasado_esp": "envió",
        "participio_ing": "sent", "participio_esp": "enviado",
        "gerundio_ing": "sending", "gerundio_esp": "enviando",
        "oraciones": {
            "infinitivo":   {"ing": "I send postcards from trips.","esp": "Yo envío postales desde viajes."},
            "pasadoSimple": {"ing": "You sent the documents.","esp": "Tú enviaste los documentos."},
            "participio":   {"ing": "She has sent the parcel.","esp": "Ella ha enviado el paquete."},
            "gerundio":     {"ing": "They are sending troops.","esp": "Ellos están enviando tropas."},
            "futuro":       {"ing": "We will send a reply.","esp": "Nosotros enviaremos una respuesta."},
            "condicional":  {"ing": "That satellite would send signals.","esp": "Ese satélite enviaría señales."}
        }
    },
    {
        "ing_inf": "set", "esp_inf": "establecer",
        "pasado_ing": "set", "pasado_esp": "estableció",
        "participio_ing": "set", "participio_esp": "establecido",
        "gerundio_ing": "setting", "gerundio_esp": "estableciendo",
        "futuro_esp": "establecerá", "cond_esp": "establecería",
        "oraciones": {
            "infinitivo":   {"ing": "I set goals every January.","esp": "Yo establezco metas cada enero."},
            "pasadoSimple": {"ing": "You set the time.","esp": "Tú estableciste el tiempo."},
            "participio":   {"ing": "She has set the record straight.","esp": "Ella ha aclarado el asunto."},
            "gerundio":     {"ing": "They are setting up the equipment.","esp": "Ellos están instalando el equipo."},
            "futuro":       {"ing": "We will set the rules.","esp": "Nosotros estableceremos las reglas."},
            "condicional":  {"ing": "That rule would set the standard.","esp": "Esa regla establecería el estándar."}
        }
    },
    {
        "ing_inf": "sew", "esp_inf": "coser",
        "pasado_ing": "sewed", "pasado_esp": "cosió",
        "participio_ing": "sewn", "participio_esp": "cosido",
        "gerundio_ing": "sewing", "gerundio_esp": "cosiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I sew buttons on shirts.","esp": "Yo cose botones en las camisas."},
            "pasadoSimple": {"ing": "You sewed the dress yourself.","esp": "Tú cosiste el vestido tú misma."},
            "participio":   {"ing": "She has sewn a quilt.","esp": "Ella ha cosido una colcha."},
            "gerundio":     {"ing": "They are sewing costumes.","esp": "Ellos están cosiendo disfraces."},
            "futuro":       {"ing": "We will sew the patches on.","esp": "Nosotros coseremos los parches."},
            "condicional":  {"ing": "That machine would sew quickly.","esp": "Esa máquina cosería rápido."}
        }
    },
    {
        "ing_inf": "shed", "esp_inf": "derramar",
        "pasado_ing": "shed", "pasado_esp": "derramó",
        "participio_ing": "shed", "participio_esp": "derramado",
        "gerundio_ing": "shedding", "gerundio_esp": "derramando",
        "oraciones": {
            "infinitivo":   {"ing": "I shed a tear at the ending.","esp": "Yo derramo una lágrima al final."},
            "pasadoSimple": {"ing": "You shed the old skin.","esp": "Tú derramaste la piel vieja."},
            "participio":   {"ing": "The tree has shed its leaves.","esp": "El árbol ha derramado sus hojas."},
            "gerundio":     {"ing": "They are shedding weight.","esp": "Ellos están perdiendo peso."},
            "futuro":       {"ing": "We will shed light on this.","esp": "Nosotros aclararemos esto."},
            "condicional":  {"ing": "That snake would shed soon.","esp": "Esa serpiente mudaría pronto."}
        }
    },
    {
        "ing_inf": "shine", "esp_inf": "brillar",
        "pasado_ing": "shone", "pasado_esp": "brilló",
        "participio_ing": "shone", "participio_esp": "brillado",
        "gerundio_ing": "shining", "gerundio_esp": "brillando",
        "oraciones": {
            "infinitivo":   {"ing": "I shine my shoes for work.","esp": "Yo brillo mis zapatos para el trabajo."},
            "pasadoSimple": {"ing": "You shone the flashlight.","esp": "Tú enfocaste la linterna."},
            "participio":   {"ing": "The sun has shone today.","esp": "El sol ha brillado hoy."},
            "gerundio":     {"ing": "They are shining at school.","esp": "Ellos están brillando en la escuela."},
            "futuro":       {"ing": "We will shine tomorrow.","esp": "Nosotros brillaremos mañana."},
            "condicional":  {"ing": "That star would shine bright.","esp": "Esa estrella brillaría intensamente."}
        }
    },
    {
        "ing_inf": "shoe", "esp_inf": "calzar",
        "pasado_ing": "shod", "pasado_esp": "calzó",
        "participio_ing": "shod", "participio_esp": "calzado",
        "gerundio_ing": "shoeing", "gerundio_esp": "calzando",
        "oraciones": {
            "infinitivo":   {"ing": "I shoe my horse before riding.","esp": "Yo calzo mi caballo antes de montarlo."},
            "pasadoSimple": {"ing": "You shod the horse yesterday.","esp": "Tú calzaste al caballo ayer."},
            "participio":   {"ing": "The farrier has shod the horses.","esp": "El herrador ha calzado a los caballos."},
            "gerundio":     {"ing": "They are shoeing the horses now.","esp": "Ellos están calzando a los caballos ahora."},
            "futuro":       {"ing": "We will shoe all the horses.","esp": "Nosotros calzaremos a todos los caballos."},
            "condicional":  {"ing": "That horse would shoe easily.","esp": "Ese caballo se calzaría fácilmente."}
        }
    },
    {
        "ing_inf": "shoot", "esp_inf": "disparar",
        "pasado_ing": "shot", "pasado_esp": "disparó",
        "participio_ing": "shot", "participio_esp": "disparado",
        "gerundio_ing": "shooting", "gerundio_esp": "disparando",
        "oraciones": {
            "infinitivo":   {"ing": "I shoot photos for fun.","esp": "Yo tomo fotos por diversión."},
            "pasadoSimple": {"ing": "You shot the arrow.","esp": "Tú disparaste la flecha."},
            "participio":   {"ing": "She has shot a short film.","esp": "Ella ha filmado un cortometraje."},
            "gerundio":     {"ing": "They are shooting baskets.","esp": "Ellos están encestando."},
            "futuro":       {"ing": "We will shoot the movie next week.","esp": "Nosotros filmaremos la película la próxima semana."},
            "condicional":  {"ing": "That camera would shoot in HD.","esp": "Esa cámara filmaría en HD."}
        }
    },
    {
        "ing_inf": "shrink", "esp_inf": "encoger",
        "pasado_ing": "shrank", "pasado_esp": "encogió",
        "participio_ing": "shrunk", "participio_esp": "encogido",
        "gerundio_ing": "shrinking", "gerundio_esp": "encogiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I shrink from conflict.","esp": "Yo me echo atrás ante el conflicto."},
            "pasadoSimple": {"ing": "You shrank the sweater.","esp": "Tú encogiste el suéter."},
            "participio":   {"ing": "The fabric has shrunk in the wash.","esp": "La tela se ha encogido al lavarse."},
            "gerundio":     {"ing": "They are shrinking the budget.","esp": "Ellos están recortando el presupuesto."},
            "futuro":       {"ing": "We will shrink the image.","esp": "Nosotros encogeremos la imagen."},
            "condicional":  {"ing": "That market would shrink soon.","esp": "Ese mercado se encogería pronto."}
        }
    },
    {
        "ing_inf": "shut", "esp_inf": "cerrar",
        "pasado_ing": "shut", "pasado_esp": "cerró",
        "participio_ing": "shut", "participio_esp": "cerrado",
        "gerundio_ing": "shutting", "gerundio_esp": "cerrando",
        "oraciones": {
            "infinitivo":   {"ing": "I shut the door quietly.","esp": "Yo cierro la puerta en silencio."},
            "pasadoSimple": {"ing": "You shut the laptop.","esp": "Tú cerraste el portátil."},
            "participio":   {"ing": "She has shut the door on him.","esp": "Ella le ha cerrado la puerta."},
            "gerundio":     {"ing": "They are shutting down the server.","esp": "Ellos están cerrando el servidor."},
            "futuro":       {"ing": "We will shut up and listen.","esp": "Nosotros nos callaremos y escucharemos."},
            "condicional":  {"ing": "That window would shut tight.","esp": "Esa ventana se cerraría herméticamente."}
        }
    },
    {
        "ing_inf": "slay", "esp_inf": "asesinar",
        "pasado_ing": "slew/slain", "pasado_esp": "asesinó",
        "participio_ing": "slain", "participio_esp": "asesinado",
        "gerundio_ing": "slaying", "gerundio_esp": "asesinando",
        "oraciones": {
            "infinitivo":   {"ing": "I slay dragons in video games.","esp": "Yo asesino dragones en videojuegos."},
            "pasadoSimple": {"ing": "You slew the boss.","esp": "Tú asesinaste al jefe final."},
            "participio":   {"ing": "The hero has slain the dragon.","esp": "El héroe ha asesinado al dragón."},
            "gerundio":     {"ing": "They are slaying the enemy.","esp": "Ellos están asesinando al enemigo."},
            "futuro":       {"ing": "We will slay the competition.","esp": "Nosotros venceremos a la competencia."},
            "condicional":  {"ing": "That dragon would slay anyone.","esp": "Ese dragón mataría a cualquiera."}
        }
    },
    {
        "ing_inf": "slide", "esp_inf": "deslizar",
        "pasado_ing": "slid", "pasado_esp": "deslizó",
        "participio_ing": "slid", "participio_esp": "deslizado",
        "gerundio_ing": "sliding", "gerundio_esp": "deslizando",
        "oraciones": {
            "infinitivo":   {"ing": "I slide into DMs sometimes.","esp": "Yo me deslizo a los mensajes directos a veces."},
            "pasadoSimple": {"ing": "You slid down the hill.","esp": "Tú te deslizaste colina abajo."},
            "participio":   {"ing": "She has slid the door closed.","esp": "Ella ha deslizado la puerta para cerrarla."},
            "gerundio":     {"ing": "They are sliding on the ice.","esp": "Ellos se están deslizando sobre el hielo."},
            "futuro":       {"ing": "We will slide the card through.","esp": "Nosotros deslizaremos la tarjeta."},
            "condicional":  {"ing": "That drawer would slide smoothly.","esp": "Ese cajón se deslizaría suavemente."}
        }
    },
    {
        "ing_inf": "slit", "esp_inf": "rasgar",
        "pasado_ing": "slit", "pasado_esp": "rasgó",
        "participio_ing": "slit", "participio_esp": "rasgado",
        "gerundio_ing": "slitting", "gerundio_esp": "rasgando",
        "oraciones": {
            "infinitivo":   {"ing": "I slit the envelope open.","esp": "Yo rasgo el sobre para abrirlo."},
            "pasadoSimple": {"ing": "You slit his throat.","esp": "Tú le cortaste la garganta."},
            "participio":   {"ing": "She has slit the fabric.","esp": "Ella ha rasgado la tela."},
            "gerundio":     {"ing": "They are slitting the paper.","esp": "Ellos están cortando el papel."},
            "futuro":       {"ing": "We will slit the envelope.","esp": "Nosotros cortaremos el sobre."},
            "condicional":  {"ing": "That blade would slit easily.","esp": "Esa cuchilla cortaría fácilmente."}
        }
    },
    {
        "ing_inf": "sneak", "esp_inf": "escabullirse",
        "pasado_ing": "sneaked/snuck", "pasado_esp": "se escabulló",
        "participio_ing": "snuck", "participio_esp": "escabullido",
        "gerundio_ing": "sneaking", "gerundio_esp": "escabulléndose",
        "futuro_esp": "se escabullirá", "cond_esp": "se escabulliría",
        "oraciones": {
            "infinitivo":   {"ing": "I sneak snacks after bedtime.","esp": "Yo me escabullo a buscar botanas después de dormir."},
            "pasadoSimple": {"ing": "You snuck out last night.","esp": "Tú te escabulliste anoche."},
            "participio":   {"ing": "She has snuck into the party.","esp": "Ella se ha escabullido en la fiesta."},
            "gerundio":     {"ing": "They are sneaking up on us.","esp": "Ellos se nos están acercando sigilosamente."},
            "futuro":       {"ing": "We will sneak away quietly.","esp": "Nosotros nos escabulliremos en silencio."},
            "condicional":  {"ing": "That cat would sneak anywhere.","esp": "Ese gato se escabulliría en cualquier parte."}
        }
    },
    {
        "ing_inf": "sow", "esp_inf": "sembrar",
        "pasado_ing": "sowed", "pasado_esp": "sembró",
        "participio_ing": "sown", "participio_esp": "sembrado",
        "gerundio_ing": "sowing", "gerundio_esp": "sembrando",
        "oraciones": {
            "infinitivo":   {"ing": "I sow seeds in spring.","esp": "Yo siembro semillas en primavera."},
            "pasadoSimple": {"ing": "You sowed doubt in their minds.","esp": "Tú sembraste duda en sus mentes."},
            "participio":   {"ing": "She has sown the seeds.","esp": "Ella ha sembrado las semillas."},
            "gerundio":     {"ing": "They are sowing wildflowers.","esp": "Ellos están sembrando flores silvestres."},
            "futuro":       {"ing": "We will sow the field tomorrow.","esp": "Nosotros sembraremos el campo mañana."},
            "condicional":  {"ing": "That rumor would sow discord.","esp": "Ese rumor sembraría discordia."}
        }
    },
    {
        "ing_inf": "speed", "esp_inf": "acelerar",
        "pasado_ing": "sped", "pasado_esp": "aceleró",
        "participio_ing": "sped", "participio_esp": "acelerado",
        "gerundio_ing": "speeding", "gerundio_esp": "acelerando",
        "oraciones": {
            "infinitivo":   {"ing": "I speed through homework.","esp": "Yo termino la tarea rápidamente."},
            "pasadoSimple": {"ing": "You sped past the school.","esp": "Tú pasaste rápido por la escuela."},
            "participio":   {"ing": "She has sped up the process.","esp": "Ella ha acelerado el proceso."},
            "gerundio":     {"ing": "They are speeding down the highway.","esp": "Ellos están acelerando por la autopista."},
            "futuro":       {"ing": "We will speed up production.","esp": "Nosotros aceleraremos la producción."},
            "condicional":  {"ing": "That car would speed dangerously.","esp": "Ese coche aceleraría peligrosamente."}
        }
    },
    {
        "ing_inf": "spell", "esp_inf": "deletrear",
        "pasado_ing": "spelled/spelt", "pasado_esp": "deletreó",
        "participio_ing": "spelled/spelt", "participio_esp": "deletreado",
        "gerundio_ing": "spelling", "gerundio_esp": "deletreando",
        "oraciones": {
            "infinitivo":   {"ing": "I spell my name clearly.","esp": "Yo deletreo mi nombre con claridad."},
            "pasadoSimple": {"ing": "You spelled the word wrong.","esp": "Tú deletreaste la palabra mal."},
            "participio":   {"ing": "She has spelled disaster.","esp": "Ella ha significado desastre."},
            "gerundio":     {"ing": "They are spelling the test.","esp": "Ellos están haciendo el examen de deletreo."},
            "futuro":       {"ing": "We will spell out the rules.","esp": "Nosotros deletrearemos las reglas."},
            "condicional":  {"ing": "That move would spell trouble.","esp": "Ese movimiento significaría problemas."}
        }
    },
    {
        "ing_inf": "spill", "esp_inf": "derramar",
        "pasado_ing": "spilled/spilt", "pasado_esp": "derramó",
        "participio_ing": "spilled/spilt", "participio_esp": "derramado",
        "gerundio_ing": "spilling", "gerundio_esp": "derramando",
        "oraciones": {
            "infinitivo":   {"ing": "I spill coffee on my desk.","esp": "Yo derramo café en mi escritorio."},
            "pasadoSimple": {"ing": "You spilled the orange juice.","esp": "Tú derramaste el jugo de naranja."},
            "participio":   {"ing": "She has spilled the beans.","esp": "Ella ha revelado el secreto."},
            "gerundio":     {"ing": "They are spilling oil.","esp": "Ellos están derramando petróleo."},
            "futuro":       {"ing": "We will spill the paint.","esp": "Nosotros derramaremos la pintura."},
            "condicional":  {"ing": "That drink would spill easily.","esp": "Esa bebida se derramaría fácilmente."}
        }
    },
    {
        "ing_inf": "spin", "esp_inf": "girar",
        "pasado_ing": "spun", "pasado_esp": "giró",
        "participio_ing": "spun", "participio_esp": "girado",
        "gerundio_ing": "spinning", "gerundio_esp": "girando",
        "oraciones": {
            "infinitivo":   {"ing": "I spin yarn for fun.","esp": "Yo hilo lana por diversión."},
            "pasadoSimple": {"ing": "You spun the wheel.","esp": "Tú giraste la rueda."},
            "participio":   {"ing": "She has spun the story.","esp": "Ella ha dado un giro a la historia."},
            "gerundio":     {"ing": "They are spinning the top.","esp": "Ellos están girando la peonza."},
            "futuro":       {"ing": "We will spin the dreidel.","esp": "Nosotros giraremos la peonza."},
            "condicional":  {"ing": "That wheel would spin forever.","esp": "Esa rueda giraría para siempre."}
        }
    }
]


BLOQUE_IRREGULARES_7 = [
    {
        "ing_inf": "spit", "esp_inf": "escupir",
        "pasado_ing": "spat/spit", "pasado_esp": "escupió",
        "participio_ing": "spat/spit", "participio_esp": "escupido",
        "gerundio_ing": "spitting", "gerundio_esp": "escupiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I spit out the seeds.","esp": "Yo escupo las semillas."},
            "pasadoSimple": {"ing": "You spat at the bus.","esp": "Tú escupiste al autobús."},
            "participio":   {"ing": "She has spit on the ground.","esp": "Ella ha escupido al suelo."},
            "gerundio":     {"ing": "They are spitting seeds at each other.","esp": "Ellos se están escupiendo semillas."},
            "futuro":       {"ing": "We will spit out the gum.","esp": "Nosotros escupiremos el chicle."},
            "condicional":  {"ing": "That camel would spit far.","esp": "Ese camello escupiría lejos."}
        }
    },
    {
        "ing_inf": "split", "esp_inf": "dividir",
        "pasado_ing": "split", "pasado_esp": "dividió",
        "participio_ing": "split", "participio_esp": "dividido",
        "gerundio_ing": "splitting", "gerundio_esp": "dividiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I split the bill evenly.","esp": "Yo divido la cuenta en partes iguales."},
            "pasadoSimple": {"ing": "You split the log.","esp": "Tú partiste el tronco."},
            "participio":   {"ing": "She has split up with him.","esp": "Ella ha terminado con él."},
            "gerundio":     {"ing": "They are splitting the costs.","esp": "Ellos están dividiendo los costos."},
            "futuro":       {"ing": "We will split the work.","esp": "Nosotros dividiremos el trabajo."},
            "condicional":  {"ing": "That decision would split the party.","esp": "Esa decisión dividiría al partido."}
        }
    },
    {
        "ing_inf": "spoil", "esp_inf": "arruinar",
        "pasado_ing": "spoiled/spoilt", "pasado_esp": "arruinó",
        "participio_ing": "spoiled/spoilt", "participio_esp": "arruinado",
        "gerundio_ing": "spoiling", "gerundio_esp": "arruinando",
        "oraciones": {
            "infinitivo":   {"ing": "I spoil my pets often.","esp": "Yo consiento a mis mascotas a menudo."},
            "pasadoSimple": {"ing": "You spoiled the surprise.","esp": "Tú arruinaste la sorpresa."},
            "participio":   {"ing": "She has spoiled the children.","esp": "Ella ha malcriado a los niños."},
            "gerundio":     {"ing": "They are spoiling the food.","esp": "Ellos están echando a perder la comida."},
            "futuro":       {"ing": "We will spoil the broth.","esp": "Nosotros arruinaremos el caldo."},
            "condicional":  {"ing": "That rain would spoil the picnic.","esp": "Esa lluvia arruinaría el picnic."}
        }
    },
    {
        "ing_inf": "spread", "esp_inf": "extender",
        "pasado_ing": "spread", "pasado_esp": "extendió",
        "participio_ing": "spread", "participio_esp": "extendido",
        "gerundio_ing": "spreading", "gerundio_esp": "extendiendo",
        "oraciones": {
            "infinitivo":   {"ing": "I spread butter on toast.","esp": "Yo unto mantequilla al pan tostado."},
            "pasadoSimple": {"ing": "You spread the news quickly.","esp": "Tú difundiste la noticia rápidamente."},
            "participio":   {"ing": "She has spread the tablecloth.","esp": "Ella ha extendido el mantel."},
            "gerundio":     {"ing": "They are spreading rumors.","esp": "Ellos están difundiendo rumores."},
            "futuro":       {"ing": "We will spread out later.","esp": "Nosotros nos dispersaremos después."},
            "condicional":  {"ing": "That rumor would spread fast.","esp": "Ese rumor se difundiría rápido."}
        }
    },
    {
        "ing_inf": "spring", "esp_inf": "saltar",
        "pasado_ing": "sprang", "pasado_esp": "saltó",
        "participio_ing": "sprung", "participio_esp": "saltado",
        "gerundio_ing": "springing", "gerundio_esp": "saltando",
        "oraciones": {
            "infinitivo":   {"ing": "I spring out of bed early.","esp": "Yo salto de la cama temprano."},
            "pasadoSimple": {"ing": "You sprang into action.","esp": "Tú saltaste a la acción."},
            "participio":   {"ing": "She has sprung a leak.","esp": "Ella ha tenido una fuga."},
            "gerundio":     {"ing": "They are springing a trap.","esp": "Ellos están tendiendo una trampa."},
            "futuro":       {"ing": "We will spring for dinner.","esp": "Nosotros pagaremos la cena."},
            "condicional":  {"ing": "That trap would spring easily.","esp": "Esa trampa se activaría fácilmente."}
        }
    },
    {
        "ing_inf": "stand", "esp_inf": "pararse",
        "pasado_ing": "stood", "pasado_esp": "se paró",
        "participio_ing": "stood", "participio_esp": "parado",
        "gerundio_ing": "standing", "gerundio_esp": "parándose",
        "futuro_esp": "se parará", "cond_esp": "se pararía",
        "oraciones": {
            "infinitivo":   {"ing": "I stand by my principles.","esp": "Yo defiendo mis principios."},
            "pasadoSimple": {"ing": "You stood up for her.","esp": "Tú te pusiste de pie por ella."},
            "participio":   {"ing": "She has stood the test of time.","esp": "Ella ha resistido la prueba del tiempo."},
            "gerundio":     {"ing": "They are standing in line.","esp": "Ellos están haciendo cola."},
            "futuro":       {"ing": "We will stand together.","esp": "Nosotros nos mantendremos unidos."},
            "condicional":  {"ing": "That building would stand forever.","esp": "Ese edificio permanecería en pie para siempre."}
        }
    },
    {
        "ing_inf": "stave", "esp_inf": "evitar",
        "pasado_ing": "staved/stove", "pasado_esp": "evitó",
        "participio_ing": "staved/stove", "participio_esp": "evitado",
        "gerundio_ing": "staving", "gerundio_esp": "evitando",
        "oraciones": {
            "infinitivo":   {"ing": "I stave off hunger with snacks.","esp": "Yo evito el hambre con botanas."},
            "pasadoSimple": {"ing": "You staved off the disaster.","esp": "Tú evitaste el desastre."},
            "participio":   {"ing": "She has staved off bankruptcy.","esp": "Ella ha evitado la bancarrota."},
            "gerundio":     {"ing": "They are staving off sleep.","esp": "Ellos están evitando dormir."},
            "futuro":       {"ing": "We will stave off the cold.","esp": "Nosotros evitaremos el frío."},
            "condicional":  {"ing": "That would stave off disaster.","esp": "Eso evitaría el desastre."}
        }
    },
    {
        "ing_inf": "steal", "esp_inf": "robar",
        "pasado_ing": "stole", "pasado_esp": "robó",
        "participio_ing": "stolen", "participio_esp": "robado",
        "gerundio_ing": "stealing", "gerundio_esp": "robando",
        "oraciones": {
            "infinitivo":   {"ing": "I steal glances at my phone.","esp": "Yo robo miradas a mi teléfono."},
            "pasadoSimple": {"ing": "You stole my heart.","esp": "Tú robaste mi corazón."},
            "participio":   {"ing": "She has stolen the show.","esp": "Ella ha robado el show."},
            "gerundio":     {"ing": "They are stealing bases.","esp": "Ellos están robando bases."},
            "futuro":       {"ing": "We will steal a march on them.","esp": "Nosotros nos adelantaremos a ellos."},
            "condicional":  {"ing": "That thief would steal anything.","esp": "Ese ladrón robaría cualquier cosa."}
        }
    },
    {
        "ing_inf": "stick", "esp_inf": "pegar",
        "pasado_ing": "stuck", "pasado_esp": "pegó",
        "participio_ing": "stuck", "participio_esp": "pegado",
        "gerundio_ing": "sticking", "gerundio_esp": "pegando",
        "oraciones": {
            "infinitivo":   {"ing": "I stick to my routine.","esp": "Yo me apego a mi rutina."},
            "pasadoSimple": {"ing": "You stuck the note on the fridge.","esp": "Tú pegaste la nota en el refrigerador."},
            "participio":   {"ing": "She has stuck with the plan.","esp": "Ella se ha mantenido en el plan."},
            "gerundio":     {"ing": "They are sticking around.","esp": "Ellos se están quedando."},
            "futuro":       {"ing": "We will stick together.","esp": "Nosotros nos mantendremos unidos."},
            "condicional":  {"ing": "That label would stick easily.","esp": "Esa etiqueta pegaría fácilmente."}
        }
    },
    {
        "ing_inf": "sting", "esp_inf": "picar",
        "pasado_ing": "stung", "pasado_esp": "picó",
        "participio_ing": "stung", "participio_esp": "picado",
        "gerundio_ing": "stinging", "gerundio_esp": "picando",
        "oraciones": {
            "infinitivo":   {"ing": "I sting easily with criticism.","esp": "Yo me siento atacado fácilmente con críticas."},
            "pasadoSimple": {"ing": "You stung me with your words.","esp": "Tú me lastimaste con tus palabras."},
            "participio":   {"ing": "The wasp has stung the child.","esp": "La avispa ha picado al niño."},
            "gerundio":     {"ing": "They are stinging from defeat.","esp": "Ellos están sufriendo por la derrota."},
            "futuro":       {"ing": "We will sting the attackers.","esp": "Nosotros contraatacaremos."},
            "condicional":  {"ing": "That jellyfish would sting badly.","esp": "Esa medusa picaría mucho."}
        }
    },
    {
        "ing_inf": "stink", "esp_inf": "apestar",
        "pasado_ing": "stank/stunk", "pasado_esp": "apestó",
        "participio_ing": "stunk", "participio_esp": "apestado",
        "gerundio_ing": "stinking", "gerundio_esp": "apestando",
        "oraciones": {
            "infinitivo":   {"ing": "I stink at dancing.","esp": "Yo soy malísimo bailando."},
            "pasadoSimple": {"ing": "You stank up the bathroom.","esp": "Tú apestaste el baño."},
            "participio":   {"ing": "The trash has stunk all day.","esp": "La basura ha apestado todo el día."},
            "gerundio":     {"ing": "They are stinking up the room.","esp": "Ellos están apestando el cuarto."},
            "futuro":       {"ing": "We will stink after practice.","esp": "Nosotros oleremos mal después de la práctica."},
            "condicional":  {"ing": "That fish would stink quickly.","esp": "Ese pez apestaría rápido."}
        }
    },
    {
        "ing_inf": "stride", "esp_inf": "avanzar",
        "pasado_ing": "strode", "pasado_esp": "avanzó",
        "participio_ing": "stridden", "participio_esp": "avanzado",
        "gerundio_ing": "striding", "gerundio_esp": "avanzando",
        "oraciones": {
            "infinitivo":   {"ing": "I stride confidently into meetings.","esp": "Yo entro con confianza a las reuniones."},
            "pasadoSimple": {"ing": "You strode across the stage.","esp": "Tú cruzaste el escenario con zancadas."},
            "participio":   {"ing": "She has stridden into history.","esp": "Ella ha entrado en la historia."},
            "gerundio":     {"ing": "They are striding forward.","esp": "Ellos están avanzando."},
            "futuro":       {"ing": "We will stride into the future.","esp": "Nosotros avanzaremos al futuro."},
            "condicional":  {"ing": "That leader would stride confidently.","esp": "Ese líder avanzaría con confianza."}
        }
    },
    {
        "ing_inf": "strike", "esp_inf": "golpear",
        "pasado_ing": "struck", "pasado_esp": "golpeó",
        "participio_ing": "struck/stricken", "participio_esp": "golpeado",
        "gerundio_ing": "striking", "gerundio_esp": "golpeando",
        "oraciones": {
            "infinitivo":   {"ing": "I strike a balance daily.","esp": "Yo encuentro un equilibrio a diario."},
            "pasadoSimple": {"ing": "You struck the ball hard.","esp": "Tú golpeaste la pelota con fuerza."},
            "participio":   {"ing": "She has struck a chord.","esp": "Ella ha tocado la fibra sensible."},
            "gerundio":     {"ing": "They are striking for better pay.","esp": "Ellos están en huelga por mejor salario."},
            "futuro":       {"ing": "We will strike at midnight.","esp": "Nosotros atacaremos a medianoche."},
            "condicional":  {"ing": "That clock would strike twelve.","esp": "Ese reloj daría las doce."}
        }
    },
    {
        "ing_inf": "string", "esp_inf": "ensartar",
        "pasado_ing": "strung", "pasado_esp": "ensartó",
        "participio_ing": "strung", "participio_esp": "ensartado",
        "gerundio_ing": "stringing", "gerundio_esp": "ensartando",
        "oraciones": {
            "infinitivo":   {"ing": "I string beads for jewelry.","esp": "Yo ensarto cuentas para joyería."},
            "pasadoSimple": {"ing": "You strung the popcorn.","esp": "Tú ensartaste las palomitas."},
            "participio":   {"ing": "She has strung the lights.","esp": "Ella ha ensartado las luces."},
            "gerundio":     {"ing": "They are stringing the tennis racket.","esp": "Ellos están encordando la raqueta."},
            "futuro":       {"ing": "We will string the lanterns.","esp": "Nosotros ensartaremos las linternas."},
            "condicional":  {"ing": "That garland would string nicely.","esp": "Esa guirnalda ensartaría bien."}
        }
    },
    {
        "ing_inf": "strive", "esp_inf": "esforzarse",
        "pasado_ing": "strove/strived", "pasado_esp": "se esforzó",
        "participio_ing": "striven/strived", "participio_esp": "esforzado",
        "gerundio_ing": "striving", "gerundio_esp": "esforzándose",
        "futuro_esp": "se esforzará", "cond_esp": "se esforzaría",
        "oraciones": {
            "infinitivo":   {"ing": "I strive for excellence daily.","esp": "Yo me esfuerzo por la excelencia a diario."},
            "pasadoSimple": {"ing": "You strove to be the best.","esp": "Tú te esforzaste por ser el mejor."},
            "participio":   {"ing": "She has striven for perfection.","esp": "Ella se ha esforzado por la perfección."},
            "gerundio":     {"ing": "They are striving to succeed.","esp": "Ellos se están esforzando por tener éxito."},
            "futuro":       {"ing": "We will strive harder.","esp": "Nosotros nos esforzaremos más."},
            "condicional":  {"ing": "That goal would make anyone strive.","esp": "Ese objetivo haría que cualquiera se esforzara."}
        }
    },
    {
        "ing_inf": "swear", "esp_inf": "jurar",
        "pasado_ing": "swore", "pasado_esp": "juró",
        "participio_ing": "sworn", "participio_esp": "jurado",
        "gerundio_ing": "swearing", "gerundio_esp": "jurando",
        "oraciones": {
            "infinitivo":   {"ing": "I swear on my life.","esp": "Yo juro por mi vida."},
            "pasadoSimple": {"ing": "You swore loyalty.","esp": "Tú juraste lealtad."},
            "participio":   {"ing": "She has sworn revenge.","esp": "Ella ha jurado venganza."},
            "gerundio":     {"ing": "They are swearing at each other.","esp": "Ellos se están maldiciendo."},
            "futuro":       {"ing": "We will swear in the president.","esp": "Nosotros tomaremos juramento al presidente."},
            "condicional":  {"ing": "That oath would swear anyone in.","esp": "Ese juramento investiría a cualquiera."}
        }
    },
    {
        "ing_inf": "sweat", "esp_inf": "sudar",
        "pasado_ing": "sweated", "pasado_esp": "sudó",
        "participio_ing": "sweated", "participio_esp": "sudado",
        "gerundio_ing": "sweating", "gerundio_esp": "sudando",
        "oraciones": {
            "infinitivo":   {"ing": "I sweat when I exercise.","esp": "Yo sudo cuando hago ejercicio."},
            "pasadoSimple": {"ing": "You sweated a lot yesterday.","esp": "Tú sudaste mucho ayer."},
            "participio":   {"ing": "She has sweated through her shirt.","esp": "Ella ha empapado su camisa de sudor."},
            "gerundio":     {"ing": "They are sweating bullets.","esp": "Ellos están sudando la gota gorda."},
            "futuro":       {"ing": "We will sweat it out.","esp": "Nosotros sudaremos la fiebre."},
            "condicional":  {"ing": "That effort would sweat anyone.","esp": "Ese esfuerzo haría sudar a cualquiera."}
        }
    },
    {
        "ing_inf": "sweep", "esp_inf": "barrer",
        "pasado_ing": "swept", "pasado_esp": "barrió",
        "participio_ing": "swept", "participio_esp": "barrido",
        "gerundio_ing": "sweeping", "gerundio_esp": "barriendo",
        "oraciones": {
            "infinitivo":   {"ing": "I sweep the floor daily.","esp": "Yo barro el piso a diario."},
            "pasadoSimple": {"ing": "You swept the garage.","esp": "Tú barriste el garaje."},
            "participio":   {"ing": "She has swept the awards.","esp": "Ella ha arrasado en los premios."},
            "gerundio":     {"ing": "They are sweeping the leaves.","esp": "Ellos están barriendo las hojas."},
            "futuro":       {"ing": "We will sweep the deck.","esp": "Nosotros barreremos la cubierta."},
            "condicional":  {"ing": "That broom would sweep easily.","esp": "Esa escoba barrería fácilmente."}
        }
    },
    {
        "ing_inf": "swell", "esp_inf": "hinchar",
        "pasado_ing": "swelled", "pasado_esp": "hinchó",
        "participio_ing": "swelled/swollen", "participio_esp": "hinchado",
        "gerundio_ing": "swelling", "gerundio_esp": "hinchando",
        "oraciones": {
            "infinitivo":   {"ing": "I swell with pride sometimes.","esp": "Yo me hincho de orgullo a veces."},
            "pasadoSimple": {"ing": "You swelled the ranks.","esp": "Tú hinchaste las filas."},
            "participio":   {"ing": "Her ankle has swollen badly.","esp": "Su tobillo se ha hinchado mucho."},
            "gerundio":     {"ing": "They are swelling the crowd.","esp": "Ellos están haciendo crecer la multitud."},
            "futuro":       {"ing": "We will swell the numbers.","esp": "Nosotros inflaremos los números."},
            "condicional":  {"ing": "That river would swell dangerously.","esp": "Ese río se hincharía peligrosamente."}
        }
    },
    {
        "ing_inf": "swim", "esp_inf": "nadar",
        "pasado_ing": "swam", "pasado_esp": "nadó",
        "participio_ing": "swum", "participio_esp": "nadado",
        "gerundio_ing": "swimming", "gerundio_esp": "nadando",
        "oraciones": {
            "infinitivo":   {"ing": "I swim laps every morning.","esp": "Yo nado largos cada mañana."},
            "pasadoSimple": {"ing": "You swam in the ocean.","esp": "Tú nadaste en el océano."},
            "participio":   {"ing": "She has swum competitively.","esp": "Ella ha nadado competitivamente."},
            "gerundio":     {"ing": "They are swimming with dolphins.","esp": "Ellos están nadando con delfines."},
            "futuro":       {"ing": "We will swim at the lake.","esp": "Nosotros nadaremos en el lago."},
            "condicional":  {"ing": "That fish would swim away.","esp": "Ese pez nadaría lejos."}
        }
    },
    {
        "ing_inf": "swing", "esp_inf": "columpiarse",
        "pasado_ing": "swung", "pasado_esp": "se columpió",
        "participio_ing": "swung", "participio_esp": "columpiado",
        "gerundio_ing": "swinging", "gerundio_esp": "columpiándose",
        "futuro_esp": "se columpiará", "cond_esp": "se columpiaría",
        "oraciones": {
            "infinitivo":   {"ing": "I swing at the park with my kids.","esp": "Yo me columpio en el parque con mis hijos."},
            "pasadoSimple": {"ing": "You swung the bat hard.","esp": "Tú balanceaste el bate con fuerza."},
            "participio":   {"ing": "The door has swung open.","esp": "La puerta se ha abierto de golpe."},
            "gerundio":     {"ing": "They are swinging on the vines.","esp": "Ellos están columpiándose en las vides."},
            "futuro":       {"ing": "We will swing by your house.","esp": "Nosotros pasaremos por tu casa."},
            "condicional":  {"ing": "That pendulum would swing forever.","esp": "Ese péndulo oscilaría para siempre."}
        }
    },
    {
        "ing_inf": "take", "esp_inf": "tomar",
        "pasado_ing": "took", "pasado_esp": "tomó",
        "participio_ing": "taken", "participio_esp": "tomado",
        "gerundio_ing": "taking", "gerundio_esp": "tomando",
        "oraciones": {
            "infinitivo":   {"ing": "I take the train to work.","esp": "Yo tomo el tren al trabajo."},
            "pasadoSimple": {"ing": "You took the test yesterday.","esp": "Tú tomaste el examen ayer."},
            "participio":   {"ing": "She has taken a break.","esp": "Ella ha tomado un descanso."},
            "gerundio":     {"ing": "They are taking photos.","esp": "Ellos están tomando fotos."},
            "futuro":       {"ing": "We will take the trip next month.","esp": "Nosotros haremos el viaje el próximo mes."},
            "condicional":  {"ing": "That medicine would take effect soon.","esp": "Esa medicina haría efecto pronto."}
        }
    },
    {
        "ing_inf": "teach", "esp_inf": "enseñar",
        "pasado_ing": "taught", "pasado_esp": "enseñó",
        "participio_ing": "taught", "participio_esp": "enseñado",
        "gerundio_ing": "teaching", "gerundio_esp": "enseñando",
        "oraciones": {
            "infinitivo":   {"ing": "I teach math at the high school.","esp": "Yo enseño matemáticas en la secundaria."},
            "pasadoSimple": {"ing": "You taught me to drive.","esp": "Tú me enseñaste a manejar."},
            "participio":   {"ing": "She has taught for twenty years.","esp": "Ella ha enseñado durante veinte años."},
            "gerundio":     {"ing": "They are teaching yoga.","esp": "Ellos están enseñando yoga."},
            "futuro":       {"ing": "We will teach next week.","esp": "Nosotros enseñaremos la próxima semana."},
            "condicional":  {"ing": "That class would teach anyone.","esp": "Esa clase enseñaría a cualquiera."}
        }
    },
    {
        "ing_inf": "tear", "esp_inf": "rasgar",
        "pasado_ing": "tore", "pasado_esp": "rasgó",
        "participio_ing": "torn", "participio_esp": "rasgado",
        "gerundio_ing": "tearing", "gerundio_esp": "rasgando",
        "oraciones": {
            "infinitivo":   {"ing": "I tear up at the ending.","esp": "Yo lloro al final."},
            "pasadoSimple": {"ing": "You tore the photo.","esp": "Tú rasgaste la foto."},
            "participio":   {"ing": "She has torn her dress.","esp": "Ella ha roto su vestido."},
            "gerundio":     {"ing": "They are tearing down the old building.","esp": "Ellos están demoliendo el edificio viejo."},
            "futuro":       {"ing": "We will tear up the agreement.","esp": "Nosotros romperemos el acuerdo."},
            "condicional":  {"ing": "That paper would tear easily.","esp": "Ese papel se rasgaría fácilmente."}
        }
    },
    {
        "ing_inf": "tell", "esp_inf": "decir",
        "pasado_ing": "told", "pasado_esp": "dijo",
        "participio_ing": "told", "participio_esp": "dicho",
        "gerundio_ing": "telling", "gerundio_esp": "diciendo",
        "futuro_esp": "dirá", "cond_esp": "diría",
        "oraciones": {
            "infinitivo":   {"ing": "I tell stories to my kids.","esp": "Yo cuento historias a mis hijos."},
            "pasadoSimple": {"ing": "You told me the truth.","esp": "Tú me dijiste la verdad."},
            "participio":   {"ing": "She has told everyone.","esp": "Ella ha contado a todos."},
            "gerundio":     {"ing": "They are telling jokes.","esp": "Ellos están contando chistes."},
            "futuro":       {"ing": "We will tell you tomorrow.","esp": "Nosotros te diremos mañana."},
            "condicional":  {"ing": "That look would tell everything.","esp": "Esa mirada lo diría todo."}
        }
    },
    {
        "ing_inf": "think", "esp_inf": "pensar",
        "pasado_ing": "thought", "pasado_esp": "pensó",
        "participio_ing": "thought", "participio_esp": "pensado",
        "gerundio_ing": "thinking", "gerundio_esp": "pensando",
        "oraciones": {
            "infinitivo":   {"ing": "I think deeply about life.","esp": "Yo pienso profundamente sobre la vida."},
            "pasadoSimple": {"ing": "You thought it through.","esp": "Tú lo pensaste bien."},
            "participio":   {"ing": "She has thought about quitting.","esp": "Ella ha pensado en renunciar."},
            "gerundio":     {"ing": "They are thinking creatively.","esp": "Ellos están pensando creativamente."},
            "futuro":       {"ing": "We will think about your offer.","esp": "Nosotros pensaremos en tu oferta."},
            "condicional":  {"ing": "That would make anyone think.","esp": "Eso haría pensar a cualquiera."}
        }
    },
    {
        "ing_inf": "thrive", "esp_inf": "prosperar",
        "pasado_ing": "thrived/throve", "pasado_esp": "prosperó",
        "participio_ing": "thrived/thriven", "participio_esp": "prosperado",
        "gerundio_ing": "thriving", "gerundio_esp": "prosperando",
        "oraciones": {
            "infinitivo":   {"ing": "I thrive under pressure.","esp": "Yo prospero bajo presión."},
            "pasadoSimple": {"ing": "You thrived in the new job.","esp": "Tú prosperaste en el trabajo nuevo."},
            "participio":   {"ing": "She has thrived since the move.","esp": "Ella ha prosperado desde la mudanza."},
            "gerundio":     {"ing": "They are thriving at the new school.","esp": "Ellos están prosperando en la escuela nueva."},
            "futuro":       {"ing": "We will thrive with effort.","esp": "Nosotros prosperaremos con esfuerzo."},
            "condicional":  {"ing": "That business would thrive anywhere.","esp": "Ese negocio prosperaría en cualquier lugar."}
        }
    },
    {
        "ing_inf": "throw", "esp_inf": "lanzar",
        "pasado_ing": "threw", "pasado_esp": "lanzó",
        "participio_ing": "thrown", "participio_esp": "lanzado",
        "gerundio_ing": "throwing", "gerundio_esp": "lanzando",
        "oraciones": {
            "infinitivo":   {"ing": "I throw the ball far.","esp": "Yo lanzo la pelota lejos."},
            "pasadoSimple": {"ing": "You threw a party.","esp": "Tú lanzaste una fiesta."},
            "participio":   {"ing": "She has thrown out the trash.","esp": "Ella ha sacado la basura."},
            "gerundio":     {"ing": "They are throwing stones.","esp": "Ellos están lanzando piedras."},
            "futuro":       {"ing": "We will throw a surprise.","esp": "Nosotros haremos una sorpresa."},
            "condicional":  {"ing": "That rock would throw far.","esp": "Esa roca volaría lejos."}
        }
    },
    {
        "ing_inf": "thrust", "esp_inf": "empujar",
        "pasado_ing": "thrust", "pasado_esp": "empujó",
        "participio_ing": "thrust", "participio_esp": "empujado",
        "gerundio_ing": "thrusting", "gerundio_esp": "empujando",
        "oraciones": {
            "infinitivo":   {"ing": "I thrust my hand into the fire.","esp": "Yo metí la mano en el fuego."},
            "pasadoSimple": {"ing": "You thrust the door open.","esp": "Tú empujaste la puerta para abrirla."},
            "participio":   {"ing": "She has thrust herself into work.","esp": "Ella se ha lanzado al trabajo."},
            "gerundio":     {"ing": "They are thrusting forward.","esp": "Ellos están avanzando con fuerza."},
            "futuro":       {"ing": "We will thrust ahead.","esp": "Nosotros nos abriremos paso."},
            "condicional":  {"ing": "That sword would thrust deep.","esp": "Esa espada atravesaría profundo."}
        }
    },
    {
        "ing_inf": "tread", "esp_inf": "pisar",
        "pasado_ing": "trod", "pasado_esp": "pisó",
        "participio_ing": "trodden/trod", "participio_esp": "pisado",
        "gerundio_ing": "treading", "gerundio_esp": "pisando",
        "oraciones": {
            "infinitivo":   {"ing": "I tread carefully around the boss.","esp": "Yo piso con cuidado alrededor del jefe."},
            "pasadoSimple": {"ing": "You trod on the snake.","esp": "Tú pisaste la serpiente."},
            "participio":   {"ing": "She has trodden this path before.","esp": "Ella ha pisado este camino antes."},
            "gerundio":     {"ing": "They are treading water.","esp": "Ellos están pisando el agua (manteniéndose a flote)."},
            "futuro":       {"ing": "We will tread carefully.","esp": "Nosotros pisaremos con cuidado."},
            "condicional":  {"ing": "That path would tread lightly.","esp": "Ese camino se pisaría suavemente."}
        }
    }
]


if __name__ == "__main__":
    procesar_bloque(BLOQUE_IRREGULARES_7, "irregulares", 180)
    aplicar_correcciones(CORRECCIONES, "simples")

    with open(RUTA_JSON, "r", encoding="utf-8") as f:
        check = json.load(f)
    print("\nVerbo #595 (strive) muestra:")
    print(json.dumps(check["generales"]["irregulares"][15], indent=2, ensure_ascii=False))