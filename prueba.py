import json

def leer_json(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)

imc_rules = leer_json("reglas.json")

def clasificar_imc(imc):
    for regla in imc_rules:
        if eval(regla["condicion"], {}, {"imc": imc}):
            return regla["clasificacion"]
    return None

routine_rules = leer_json("rutinas.json")

def obtener_rutinas(clasificacion, genero):
    posibles = []
    for regla in routine_rules:
        if regla["clasificacion"] == clasificacion and regla["genero"] == genero:
            posibles.append(regla["rutina"])
    return posibles


exercises = leer_json("ejercicios.json")

def obtener_ejercicios(rutina):
    return exercises.get(rutina, [])

def generar_plan(peso, altura, genero):
    imc = peso / (altura ** 2)

    clasificacion = clasificar_imc(imc)
    print(f"Clasificacion: {clasificacion}")
    rutina = obtener_rutinas(clasificacion, genero)
    print(f"Rutina: {rutina}")
    rutina = rutina[0] if rutina else None
    ejercicios = obtener_ejercicios(rutina)
    print(f"Ejercicios: {ejercicios}")

    return {
        "imc": round(imc, 2),
        "clasificacion": clasificacion,
        "rutina": rutina,
        "ejercicios": ejercicios
    }

print(generar_plan(85, 1.74, "hombre"))