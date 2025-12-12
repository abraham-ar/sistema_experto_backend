from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# ===========================
#  ADMINISTRADOR - LOGIN
# ===========================
class AdminLoginRequest(BaseModel):
    """Schema para login de administrador"""
    usuario: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=1)


class AdminLoginResponse(BaseModel):
    """Response después de login de administrador"""
    id: int
    usuario: str
    nombre: str
    token: Optional[str] = None  # JWT token si aplica

    model_config = {"from_attributes": True}


# ===========================
#  USUARIO - LOGIN
# ===========================
class UsuarioLoginRequest(BaseModel):
    """Schema para login de usuario normal"""
    correo: EmailStr
    password: str = Field(..., min_length=1)


class UsuarioLoginResponse(BaseModel):
    """Response después de login de usuario"""
    id: int
    nombre: str
    correo: EmailStr
    token: Optional[str] = None  # JWT token si aplica

    model_config = {"from_attributes": True}


# ===========================
#  USUARIO - REGISTRO
# ===========================
class UsuarioRegisterRequest(BaseModel):
    """Schema para registro de usuario nuevo"""
    nombre: str = Field(..., min_length=1, max_length=100)
    correo: EmailStr
    password: str = Field(..., min_length=6)  # Mínimo 6 caracteres


class UsuarioRegisterResponse(BaseModel):
    """Response después de registro de usuario"""
    id: int
    nombre: str
    correo: EmailStr
    token: Optional[str] = None  # JWT token si aplica

    model_config = {"from_attributes": True}


# ===========================
#  USUARIO - PERFIL COMPLETO
# ===========================
class UsuarioProfile(BaseModel):
    """Schema completo del usuario para consultas"""
    id: int
    nombre: str
    correo: EmailStr
    peso: Optional[float] = None
    altura: Optional[float] = None
    genero: Optional[str] = None
    imc: Optional[float] = None
    categoria_imc: Optional[str] = None
    rutina_asignada: Optional[str] = None

    model_config = {"from_attributes": True}
