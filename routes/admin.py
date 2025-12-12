from fastapi import APIRouter, Depends, HTTPException, status, Query, Header
from sqlalchemy.orm import Session
from config.db import get_db
from typing import List
from schemas import RuleResponse, RuleCreate, RuleUpdate
from schemas import EjercicioResponse, EjercicioCreate, EjercicioUpdate
from schemas import RutinaResponse, RutinaCreate, RutinaUpdate
from services import get_reglas, get_regla, validate_regla, add_regla, update_regla, delete_regla
from services import get_ejercicios, get_ejercicio, validate_ejercicio, add_ejercicio, update_ejercicio, delete_ejercicio, add_ejercicio_rutina, ejercicio_repetido
from services import get_rutinas, get_rutina, validate_rutina, add_rutina, update_rutina, delete_rutina, delete_ejercicio_from_rutina, ejercicio_usado_en_otras_rutinas, get_rutinas_raw, delete_ejercicio_from_all_rutinas


admin = APIRouter(prefix="/admin", tags=["admin"])

# ============================================
#   VALIDAR QUE ADMIN EXISTE POR HEADERS
# ============================================

def validar_admin(admin_id: str = Header(...), admin_user: str = Header(...)):
    # Aquí no hay JWT: solo verificas si vienen los headers
    if not admin_id or not admin_user:
        raise HTTPException(status_code=403, detail="Acceso no autorizado (admin headers faltantes)")


# ============================================
#   GET /admin/rules
# ============================================

@admin.get("/rules", response_model=List[RuleResponse])
def listar_reglas(admin_id: str = Header(...), admin_user: str = Header(...)):
    validar_admin(admin_id, admin_user)
    return get_reglas()


# ============================================
#   POST /admin/rules
# ============================================

@admin.post("/rules", response_model=RuleResponse)
def crear_regla(data: RuleCreate, admin_id: str = Header(...), admin_user: str = Header(...)):
    validar_admin(admin_id, admin_user)

    nueva = data.dict()

    if not validate_regla(nueva):
        raise HTTPException(status_code=400, detail="La regla ya existe o está duplicada")

    regla_creada = add_regla(nueva)
    return regla_creada


# ============================================
#   PUT /admin/rules/{id}
# ============================================

@admin.put("/rules/{id}", response_model=RuleResponse)
def modificar_regla(id: int, datos: RuleUpdate, admin_id: str = Header(...), admin_user: str = Header(...)):
    validar_admin(admin_id, admin_user)

    existente = get_regla(id)
    if not existente:
        raise HTTPException(status_code=404, detail="Regla no encontrada")

    actualizada = update_regla(id, datos.dict())
    return actualizada


# ============================================
#   DELETE /admin/rules/{id}
# ============================================

@admin.delete("/rules/{id}")
def eliminar_regla(id: int, admin_id: str = Header(...), admin_user: str = Header(...)):
    validar_admin(admin_id, admin_user)

    if not get_regla(id):
        raise HTTPException(status_code=404, detail="Regla no encontrada")

    if not delete_regla(id):
        raise HTTPException(status_code=400, detail="No se pudo eliminar la regla")

    return {"message": "Regla eliminada correctamente"}

# =======================================================
#   GET /admin/exercises
# =======================================================

@admin.get("/exercises", response_model=List[EjercicioResponse])
def listar_ejercicios(admin_id: str = Header(...), admin_user: str = Header(...)):
    validar_admin(admin_id, admin_user)
    return get_ejercicios()


# =======================================================
#   POST /admin/exercises
# =======================================================

@admin.post("/exercises", response_model=EjercicioResponse)
def crear_ejercicio(data: EjercicioCreate, admin_id: str = Header(...), admin_user: str = Header(...)):
    validar_admin(admin_id, admin_user)

    nuevo = data.dict()

    if not validate_ejercicio(nuevo):
        raise HTTPException(status_code=400, detail="El ejercicio ya existe")

    nuevo_id = add_ejercicio(nuevo)["id"]

    #=====MODIFICACION DEL ENDPOINT=======
    # 3. Cargar rutinas
    rutinas = get_rutinas_raw()  # función que solo lee rutinas.json

    # 4. Buscar una rutina con coincidencia de tipo y genero
    rutina_encontrada = None
    for r in rutinas:
        if (
            r["tipo"].lower() == nuevo["objetivo"].lower()
            and r["genero"].lower() == nuevo["genero"].lower()
        ):
            rutina_encontrada = r["rutina"]
            break

    if not rutina_encontrada:
        raise HTTPException(
            status_code=404,
            detail="No existe ninguna rutina con el mismo tipo y género del ejercicio"
        )

    # 5. Agregar ejercicio a la rutina
    add_ejercicio_rutina(rutina_encontrada, nuevo_id)

    # 6. Respuesta final
    return {
        "id": nuevo_id,
        **nuevo,
        "asignado_a": rutina_encontrada
    }


# =======================================================
#   PUT /admin/exercises/{id}
# =======================================================

@admin.put("/exercises/{id}", response_model=EjercicioResponse)
def modificar_ejercicio(id: int, datos: EjercicioUpdate, admin_id: str = Header(...), admin_user: str = Header(...)):
    validar_admin(admin_id, admin_user)

    existente = get_ejercicio(id)
    if not existente:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

    actualizado = update_ejercicio(id, datos.dict())
    return actualizado


# =======================================================
#   DELETE /admin/exercises/{id}
# =======================================================

@admin.delete("/exercises/{id}")
def eliminar_ejercicio(id: int, admin_id: str = Header(...), admin_user: str = Header(...)):
    validar_admin(admin_id, admin_user)

    if not get_ejercicio(id):
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

    # 1. elimina el ejercicio de TODAS las rutinas
    eliminadas = delete_ejercicio_from_all_rutinas(id)

    # 2. elimina el ejercicio globalmente
    if not delete_ejercicio(id):
        raise HTTPException(status_code=400, detail="No se pudo eliminar")

    return {
        "message": "Ejercicio eliminado correctamente",
        "eliminado_de_rutinas": eliminadas
    }

# =======================================================
#   GET /admin/routines
# =======================================================

@admin.get("/routines", response_model=List[RutinaResponse])
def listar_rutinas(admin_id: str = Header(...), admin_user: str = Header(...)):
    validar_admin(admin_id, admin_user)
    return get_rutinas()


# =======================================================
#   POST /admin/routines
# =======================================================

@admin.post("/routines", response_model=RutinaResponse)
def crear_rutina(data: RutinaCreate, admin_id: str = Header(...), admin_user: str = Header(...)):
    validar_admin(admin_id, admin_user)

    if not validate_rutina(data.rutina):
        raise HTTPException(status_code=400, detail="Ya existe una rutina con ese nombre")

    rutina_obj = data.dict()
    rutina_obj["ejercicios"] = []  # se crea vacía

    nueva = add_rutina(rutina_obj)

    # devolvemos versión expandida (ejercicios completos)
    return {
        **nueva,
        "ejercicios": []
    }


# =======================================================
#   PUT /admin/routines/{rutina}
# =======================================================

@admin.put("/routines/{rutina}", response_model=RutinaResponse)
def modificar_rutina(rutina: str, cambios: RutinaUpdate, admin_id: str = Header(...), admin_user: str = Header(...)):
    validar_admin(admin_id, admin_user)

    existente = get_rutina(rutina)
    if not existente:
        raise HTTPException(status_code=404, detail="Rutina no encontrada")

    modificada = update_rutina(rutina, cambios.dict())

    # reconstruir ejercicios completos
    from services.ejercicios import load_ejercicios
    ejercicios = load_ejercicios()
    ejercicios_map = {e["id"]: e for e in ejercicios}

    return {
        **modificada,
        "ejercicios": [ejercicios_map[id] for id in modificada.get("ejercicios", []) if id in ejercicios_map]
    }


# =======================================================
#   DELETE /admin/routines/{rutina}
# =======================================================

@admin.delete("/routines/{rutina}")
def eliminar_rutina(rutina: str, admin_id: str = Header(...), admin_user: str = Header(...)):
    validar_admin(admin_id, admin_user)

    if not get_rutina(rutina):
        raise HTTPException(status_code=404, detail="Rutina no encontrada")

    if not delete_rutina(rutina):
        raise HTTPException(status_code=400, detail="No se pudo borrar la rutina")

    return {"message": "Rutina eliminada correctamente"}

# =====================================================
# POST /admin/routines/{rutina}/exercises
# =====================================================

@admin.post("/routines/{rutina}/exercises")
def agregar_ejercicio(
    rutina: str,
    data: EjercicioCreate,
    admin_id: str = Header(...),
    admin_user: str = Header(...)
):
    validar_admin(admin_id, admin_user)

    # 1. validar que la rutina exista
    rutina_obj = get_rutina(rutina)
    if not rutina_obj:
        raise HTTPException(404, "La rutina no existe")

    # 2. validar que el ejercicio no esté repetido
    if ejercicio_repetido(data.dict()):
        raise HTTPException(400, "Este ejercicio ya existe con los mismos datos")

    # 3. crear ejercicio nuevo
    new_id = add_ejercicio(data.dict())

    # 4. asignarlo a la rutina
    add_ejercicio_rutina(rutina, new_id)

    return {"message": "Ejercicio agregado a la rutina", "id": new_id}


# =====================================================
# DELETE /admin/routines/{rutina}/exercises/{exercise_id}
# =====================================================

@admin.delete("/routines/{rutina}/exercises/{exercise_id}")
def eliminar_ejercicio(
    rutina: str,
    exercise_id: int,
    admin_id: str = Header(...),
    admin_user: str = Header(...)
):
    validar_admin(admin_id, admin_user)

    # 1. validar rutina
    rutina_obj = get_rutina(rutina)
    if not rutina_obj:
        raise HTTPException(404, "La rutina no existe")

    # 2. validar ejercicio
    ejercicio_obj = get_ejercicio(exercise_id)
    if not ejercicio_obj:
        raise HTTPException(404, "El ejercicio no existe")

    # 3. eliminar ejercicio de la rutina
    ok = delete_ejercicio_from_rutina(rutina, exercise_id)
    if not ok:
        raise HTTPException(400, "El ejercicio no está asignado a esta rutina")

    # 4. si ninguna otra rutina lo usa → borrarlo del sistema
    if not ejercicio_usado_en_otras_rutinas(rutina, exercise_id):
        delete_ejercicio(exercise_id)

    return {"message": "Ejercicio eliminado de la rutina correctamente"}