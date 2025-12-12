import json
from typing import List, Optional
from pathlib import Path

RUTAS_REGLAS = Path("reglas.json")

# ============================================
#   LECTURA / ESCRITURA JSON
# ============================================

def load_rules() -> List[dict]:
    if not RUTAS_REGLAS.exists():
        return []
    with open(RUTAS_REGLAS, "r", encoding="utf-8") as f:
        return json.load(f)

def save_rules(rules: List[dict]):
    with open(RUTAS_REGLAS, "w", encoding="utf-8") as f:
        json.dump(rules, f, indent=2, ensure_ascii=False)


# ============================================
#   MÉTODOS ESPECÍFICOS DE REGLAS
# ============================================

def get_reglas() -> List[dict]:
    return load_rules()


def get_regla(regla_id: int) -> Optional[dict]:
    reglas = load_rules()
    for r in reglas:
        if r["id"] == regla_id:
            return r
    return None


def validate_regla(nueva: dict) -> bool:
    reglas = load_rules()

    for r in reglas:
        # evitar duplicado exacto (misma condición y clasificación)
        if r["condicion"] == nueva["condicion"] and r["clasificacion"] == nueva["clasificacion"]:
            return False

    return True


def add_regla(regla: dict) -> dict:
    reglas = load_rules()

    # generar ID incremental
    new_id = max([r["id"] for r in reglas], default=0) + 1
    regla["id"] = new_id

    reglas.append(regla)
    save_rules(reglas)

    return regla


def update_regla(regla_id: int, datos: dict) -> Optional[dict]:
    reglas = load_rules()

    for i, r in enumerate(reglas):
        if r["id"] == regla_id:
            reglas[i].update({k: v for k, v in datos.items() if v is not None})
            save_rules(reglas)
            return reglas[i]

    return None


def delete_regla(regla_id: int) -> bool:
    reglas = load_rules()
    nuevas = [r for r in reglas if r["id"] != regla_id]

    if len(reglas) == len(nuevas):
        return False  # no existía

    save_rules(nuevas)
    return True
