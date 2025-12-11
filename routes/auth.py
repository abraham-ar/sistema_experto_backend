from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from config.db import get_db
from models import Administrador, Usuario
from schemas import (
    AdminLoginRequest,
    AdminLoginResponse,
    UsuarioLoginRequest,
    UsuarioLoginResponse,
    UsuarioRegisterRequest,
    UsuarioRegisterResponse,
)
import services as _services
from passlib.context import CryptContext

auth = APIRouter()

# Configuración de hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash una contraseña"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica una contraseña contra su hash"""
    return pwd_context.verify(plain_password, hashed_password)


# ===========================
#  LOGIN ADMINISTRADOR
# ===========================
@auth.post("/auth/login/admin", response_model=AdminLoginResponse)
async def login_admin(
    credentials: AdminLoginRequest,
    db: Session = Depends(get_db)
):
    """
    Endpoint para login de administrador.
    Retorna datos del admin + token JWT
    """
    # Buscar administrador por usuario
    admin = db.query(Administrador).filter(
        Administrador.usuario == credentials.usuario
    ).first()

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de administrador no válidas"
        )

    # Verificar contraseña
    if not verify_password(credentials.password, admin.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de administrador no válidas"
        )

    return AdminLoginResponse(
        id=admin.id,
        usuario=admin.usuario,
        nombre=admin.nombre
        #token=token_data.get("access_token")
    )


# ===========================
#  LOGIN USUARIO
# ===========================
@auth.post("/auth/login/usuario", response_model=UsuarioLoginResponse)
async def login_usuario(
    credentials: UsuarioLoginRequest,
    db: Session = Depends(get_db)
):
    """
    Endpoint para login de usuario normal.
    Retorna datos del usuario + token JWT
    """
    # Buscar usuario por correo
    usuario = db.query(Usuario).filter(
        Usuario.correo == credentials.correo
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de usuario no válidas"
        )

    # Verificar contraseña
    if not verify_password(credentials.password, usuario.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de usuario no válidas"
        )

    return UsuarioLoginResponse(
        id=usuario.id,
        nombre=usuario.nombre,
        correo=usuario.correo,
        genero=usuario.genero
        #token=token_data.get("access_token")
    )


# ===========================
#  REGISTRO USUARIO
# ===========================
@auth.post("/auth/register/usuario", response_model=UsuarioRegisterResponse, status_code=status.HTTP_201_CREATED)
async def register_usuario(
    usuario_data: UsuarioRegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Endpoint para registro de usuario nuevo.
    Retorna datos del usuario registrado + token JWT
    """
    # Verificar que el correo no exista
    usuario_existente = db.query(Usuario).filter(
        Usuario.correo == usuario_data.correo
    ).first()

    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya está registrado"
        )

    # Crear nuevo usuario
    nuevo_usuario = Usuario(
        nombre=usuario_data.nombre,
        correo=usuario_data.correo,
        password_hash=hash_password(usuario_data.password),
    )

    try:
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al registrar el usuario. Verifica los datos"
        )


    return UsuarioRegisterResponse(
        id=nuevo_usuario.id,
        nombre=nuevo_usuario.nombre,
        correo=nuevo_usuario.correo
        #token=token_data.get("access_token")
    )


@auth.get("/auth/me")
async def auth_me(user=Depends(_services.require_user)):
    """Endpoint para obtener datos del usuario autenticado"""
    return user
