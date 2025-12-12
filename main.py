from fastapi import FastAPI, Depends
from routes import auth, admin
from config.db import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from models import Administrador
from fastapi.middleware.cors import CORSMiddleware
from services import services
from passlib.hash import bcrypt
import logging

#creación del usuario Admin
def crear_usuario_principal():
    db: Session = SessionLocal()
    try:
        admin = db.query(Administrador).filter(Administrador.usuario == "Admin").first()
        if not admin:
            nuevo_admin = Administrador(
                usuario="Admin",
                password_hash = bcrypt.hash("Admin123"),
                nombre="Administrador Principal"
            )
            db.add(nuevo_admin)
            db.commit()
            logging.info("Administrador principal creado.")
        else:
            logging.info("Administrador principal ya existe.")
    finally:
        db.close()

# Configura los orígenes permitidos en este caso donde se se encuentra el front
origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://127.0.0.1:5501",
    "http://localhost:5501",
]

services.create_database()

crear_usuario_principal()

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Qué orígenes pueden acceder
    allow_credentials=True, #permite envio de tokens JWT
    allow_methods=["*"],    # Qué métodos HTTP se permiten (GET, POST, PUT, etc)
    allow_headers=["*"],    # Qué cabeceras se permiten
)

app.include_router(auth)
app.include_router(admin)