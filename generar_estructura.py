import json

def crear_estructura_vacia():
    return {
        "id": "",
        "imagen": "",
        "infinitivo":   {"esp": "", "ing": ""},
        "pasadoSimple": {"esp": "", "ing": ""},
        "participio":   {"esp": "", "ing": ""},
        "gerundio":     {"esp": "", "ing": ""},
        "futuro":       {"esp": "", "ing": ""},
        "condicional":  {"esp": "", "ing": ""},
        "oraciones": {
            "infinitivo":   {"pronombre": "yo",       "ing": "", "esp": ""},
            "pasadoSimple": {"pronombre": "tu",       "ing": "", "esp": ""},
            "participio":   {"pronombre": "el_ella",  "ing": "", "esp": ""},
            "gerundio":     {"pronombre": "ellos",    "ing": "", "esp": ""},
            "futuro":       {"pronombre": "nosotros", "ing": "", "esp": ""},
            "condicional":  {"pronombre": "eso",      "ing": "", "esp": ""}
        }
    }

data = {
    "generales": {
        "simples":     [crear_estructura_vacia() for _ in range(400)],
        "irregulares": [crear_estructura_vacia() for _ in range(300)],
        "compuestos":  [crear_estructura_vacia() for _ in range(150)]
    },
    "tecnologia": [crear_estructura_vacia() for _ in range(150)]
}

with open("/home/ospinajuanp/proyectos/ospinajuanp-ingles/verbos_estructura.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

total = (
    len(data["generales"]["simples"])
    + len(data["generales"]["irregulares"])
    + len(data["generales"]["compuestos"])
    + len(data["tecnologia"])
)

print("Archivo regenerado con exito")
print(f"  - generales.simples:     {len(data['generales']['simples'])}")
print(f"  - generales.irregulares: {len(data['generales']['irregulares'])}")
print(f"  - generales.compuestos:  {len(data['generales']['compuestos'])}")
print(f"  - tecnologia:            {len(data['tecnologia'])}")
print(f"  - TOTAL:                 {total}")