import json
from pathlib import Path
from typing import List, Optional

RUTA_EJERCICIOS = Path("ejercicios.json")

# =======================================================
#   LECTURA / ESCRITURA JSON
# =======================================================

def load_ejercicios() -> List[dict]:
    if not RUTA_EJERCICIOS.exists():
        return []
    with open(RUTA_EJERCICIOS, "r", encoding="utf-8") as f:
        return json.load(f)

def save_ejercicios(data: List[dict]):
    with open(RUTA_EJERCICIOS, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# =======================================================
#   MÉTODOS ESPECÍFICOS
# =======================================================

def get_ejercicios() -> List[dict]:
    return load_ejercicios()


def get_ejercicio(ej_id: int) -> Optional[dict]:
    ejercicios = load_ejercicios()
    for e in ejercicios:
        if e["id"] == ej_id:
            return e
    return None


def validate_ejercicio(nuevo: dict) -> bool:
    ejercicios = load_ejercicios()
    for e in ejercicios:
        # evitar duplicado exacto
        if (
            e["ejercicio"].lower() == nuevo["ejercicio"].lower() and
            e["series"] == nuevo["series"] and
            e["repeticiones"] == nuevo["repeticiones"] and
            e["objetivo"].lower() == nuevo["objetivo"].lower() and
            e["genero"].lower() == nuevo["genero"].lower()
        ):
            return False
    return True


def add_ejercicio(ejercicio: dict) -> dict:
    ejercicios = load_ejercicios()

    new_id = max([e["id"] for e in ejercicios], default=0) + 1
    ejercicio["id"] = new_id

    ejercicios.append(ejercicio)
    save_ejercicios(ejercicios)

    return ejercicio


def update_ejercicio(ej_id: int, datos: dict) -> Optional[dict]:
    ejercicios = load_ejercicios()

    for i, e in enumerate(ejercicios):
        if e["id"] == ej_id:
            ejercicios[i].update({k: v for k, v in datos.items() if v is not None})
            save_ejercicios(ejercicios)
            return ejercicios[i]

    return None


def delete_ejercicio(ej_id: int) -> bool:
    ejercicios = load_ejercicios()
    nuevos = [e for e in ejercicios if e["id"] != ej_id]

    if len(nuevos) == len(ejercicios):
        return False

    save_ejercicios(nuevos)
    return True

#========================================================
#Metodo para verificar que no haya ejercicios repetidos
#=======================================================
def ejercicio_repetido(nuevo: dict) -> bool:
    ejercicios = load_ejercicios()

    for e in ejercicios:
        if (
            e["ejercicio"].lower() == nuevo["ejercicio"].lower()
            and e["series"] == nuevo["series"]
            and e["repeticiones"] == nuevo["repeticiones"]
            and e["objetivo"].lower() == nuevo["objetivo"].lower()
            and e["genero"].lower() == nuevo["genero"].lower()
        ):
            return True

    return False
