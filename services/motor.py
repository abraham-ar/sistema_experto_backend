import json

def load_json(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)


# ============================
# 1) CLASIFICAR IMC
# ============================
def clasificar_imc(imc: float):
    reglas = load_json("reglas.json")

    for r in reglas:
        if eval(r["condicion"], {}, {"imc": imc}):
            return r["clasificacion"]
    return None


# ============================
# 2) OBTENER RUTINAS
# ============================
def obtener_rutinas(clasificacion: str, genero: str):
    rutinas = load_json("rutinas.json")
    return [
        r for r in rutinas
        if r["clasificacion"].lower() == clasificacion.lower()
        and r["genero"].lower() == genero.lower()
    ]


# ============================
# 3) OBTENER EJERCICIOS
# ============================
def obtener_ejercicios_por_ids(ids: list[int]):
    ejercicios = load_json("ejercicios.json")
    mapa = {e["id"]: e for e in ejercicios}
    return [mapa[i] for i in ids if i in mapa]
