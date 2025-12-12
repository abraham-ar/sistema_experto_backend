from fastapi import APIRouter, Depends, HTTPException, status, Query, Header
from sqlalchemy.orm import Session
from config.db import get_db
from schemas import RoutineCreate, RoutineUpdate, RoutineResponse
from typing import List
from schemas import RuleResponse, RuleCreate, RuleUpdate
from services import get_reglas, get_regla, validate_regla, add_regla, update_regla, delete_regla, get_ejercicios, get_ejercicio, validate_ejercicio, add_ejercicio, update_ejercicio, delete_ejercicio
from schemas import EjercicioResponse, EjercicioCreate, EjercicioUpdate

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

@admin.post("rules", response_model=RuleResponse)
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

@admin.put("rules/{id}", response_model=RuleResponse)
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

    return add_ejercicio(nuevo)


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

    if not delete_ejercicio(id):
        raise HTTPException(status_code=400, detail="No se pudo eliminar")

    return {"message": "Ejercicio eliminado correctamente"}