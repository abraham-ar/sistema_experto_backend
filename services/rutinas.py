import json
from pathlib import Path
from typing import List, Optional

RUTA_RUTINAS = Path("rutinas.json")
RUTA_EJERCICIOS = Path("ejercicios.json")


# =======================================================
#   LECTURA / ESCRITURA JSON
# =======================================================

def load_json(path: Path) -> List[dict]:
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path: Path, data: List[dict]):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# =======================================================
#   GET RUTINAS COMPLETAS CON EJERCICIOS
# =======================================================

def get_rutinas() -> List[dict]:
    rutinas = load_json(RUTA_RUTINAS)
    ejercicios = load_json(RUTA_EJERCICIOS)

    ejercicios_map = {e["id"]: e for e in ejercicios}

    resultado = []
    for r in rutinas:
        datos = {
            "clasificacion": r["clasificacion"],
            "genero": r["genero"],
            "rutina": r["rutina"],
            "tipo": r["tipo"],
            "ejercicios": [ejercicios_map[id] for id in r.get("ejercicios", []) if id in ejercicios_map]
        }
        resultado.append(datos)

    return resultado


# =======================================================
#   GET UNA RUTINA POR NOMBRE
# =======================================================

def get_rutina(nombre: str) -> Optional[dict]:
    rutinas = load_json(RUTA_RUTINAS)
    for r in rutinas:
        if r["rutina"].lower() == nombre.lower():
            return r
    return None


# =======================================================
#   VALIDAR NOMBRE ÚNICO
# =======================================================

def validate_rutina(nombre: str) -> bool:
    return get_rutina(nombre) is None


# =======================================================
#   AÑADIR RUTINA NUEVA
# =======================================================

def add_rutina(rutina: dict) -> dict:
    rutinas = load_json(RUTA_RUTINAS)

    rutina["ejercicios"] = rutina.get("ejercicios", [])

    rutinas.append(rutina)
    save_json(RUTA_RUTINAS, rutinas)

    return rutina


# =======================================================
#   ACTUALIZAR RUTINA
# =======================================================

def update_rutina(nombre: str, cambios: dict) -> Optional[dict]:
    rutinas = load_json(RUTA_RUTINAS)

    for i, r in enumerate(rutinas):
        if r["rutina"].lower() == nombre.lower():
            rutinas[i].update({k: v for k, v in cambios.items() if v is not None})
            save_json(RUTA_RUTINAS, rutinas)
            return rutinas[i]

    return None


# =======================================================
#   ELIMINAR RUTINA
# =======================================================

def delete_rutina(nombre: str) -> bool:
    rutinas = load_json(RUTA_RUTINAS)

    nueva_lista = [r for r in rutinas if r["rutina"].lower() != nombre.lower()]

    if len(nueva_lista) == len(rutinas):
        return False

    save_json(RUTA_RUTINAS, nueva_lista)
    return True

#============================================================
#METODOS PARA LOS ENDPOINTS DE /routine/{rutina}/exercises
#===========================================================
def add_ejercicio_rutina(nombre: str, ejercicio_id: int):
    rutinas = load_json(RUTA_RUTINAS)

    for r in rutinas:
        if r["rutina"].lower() == nombre.lower():
            if ejercicio_id not in r["ejercicios"]:
                r["ejercicios"].append(ejercicio_id)
                save_json(RUTA_RUTINAS, rutinas)
                return True
            return False
    return False


def delete_ejercicio_from_rutina(nombre: str, ejercicio_id: int):
    rutinas = load_json(RUTA_RUTINAS)

    for r in rutinas:
        if r["rutina"].lower() == nombre.lower():
            if ejercicio_id in r["ejercicios"]:
                r["ejercicios"].remove(ejercicio_id)
                save_json(RUTA_RUTINAS, rutinas)
                return True

            return False
    return False


def ejercicio_usado_en_otras_rutinas(nombre_rutina: str, ejercicio_id: int) -> bool:
    rutinas = load_json(RUTA_RUTINAS)

    for r in rutinas:
        if r["rutina"].lower() != nombre_rutina.lower():
            if ejercicio_id in r["ejercicios"]:
                return True

    return False
