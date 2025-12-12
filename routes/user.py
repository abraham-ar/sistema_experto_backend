from fastapi import APIRouter, HTTPException, Header, Depends
from sqlalchemy.orm import Session
from schemas import EngineInput, EngineRutinaResponse, RutinaEjerciciosResponse
from config.db import get_db
from services import clasificar_imc, obtener_rutinas, obtener_ejercicios_por_ids, load_json
from models import Usuario

engine = APIRouter(prefix="/user/run-engine", tags=["Engine"])

def validar_usuario(user_id: str = Header(...), user_email: str = Header(...)):
    # Aquí no hay JWT: solo verificas si vienen los headers
    if not user_id or not user_email:
        raise HTTPException(status_code=403, detail="Acceso no autorizado (admin headers faltantes)")

@engine.post("/rutina", response_model=EngineRutinaResponse)
def run_engine_rutina(data: EngineInput, user_id: str = Header(...), user_email: str = Header(...), db: Session = Depends(get_db)):
    validar_usuario(user_id, user_email)

     # 1. Buscar usuario en BD
    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario:
        raise HTTPException(404, "Usuario no encontrado")

    imc = data.peso / (data.altura ** 2)
    clasificacion = clasificar_imc(imc)

    if not clasificacion:
        raise HTTPException(500, "No se pudo clasificar el IMC")

    rutinas = obtener_rutinas(clasificacion, data.genero)

    if not rutinas:
        rutinas_nombres = []
    else:
        rutinas_nombres = [r["rutina"] for r in rutinas]

    # 4. Guardar en BD los datos del usuario
    usuario.peso = data.peso
    usuario.altura = data.altura
    usuario.genero = data.genero
    usuario.imc = round(imc, 2)
    usuario.categoria_imc = clasificacion

    db.commit()

    return {
        "imc": round(imc, 2),
        "clasificacion": clasificacion,
        "rutinas": rutinas_nombres
    }


@engine.post("/ejercicios/rutina/{rutina}", response_model=RutinaEjerciciosResponse)
def get_ejercicios_rutina(rutina: str, user_id: str = Header(...), user_email: str = Header(...), db: Session = Depends(get_db)):
    validar_usuario(user_id, user_email)

    # 1. Buscar usuario
    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario:
        raise HTTPException(404, "Usuario no encontrado")

    rutinas = load_json("rutinas.json")
    rutina_obj = next((r for r in rutinas if r["rutina"].lower() == rutina.lower()), None)

    if not rutina_obj:
        raise HTTPException(404, "La rutina no existe")

    ejercicios = obtener_ejercicios_por_ids(rutina_obj["ejercicios"])

    # 4. Guardar la rutina seleccionada en BD
    usuario.rutina_asignada = rutina_obj["rutina"]
    db.commit()

    return {
        "rutina": rutina,
        "ejercicios": ejercicios
    }
