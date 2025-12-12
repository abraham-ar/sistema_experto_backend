from pydantic import BaseModel, Field
from typing import Optional


class RoutineBase(BaseModel):
    clasificacion: str = Field(..., example="normal")
    genero: str = Field(..., example="hombre")
    rutina: str = Field(..., example="mantener_peso_h")

# ======================================================
# Modelo para CREAR rutinas (POST)
# ======================================================
class RoutineCreate(RoutineBase):
    """Modelo para crear una rutina nueva."""
    pass

# ======================================================
# Modelo para ACTUALIZAR rutinas (PUT)
# ======================================================
class RoutineUpdate(BaseModel):
    clasificacion: Optional[str] = Field(None, example="normal")
    genero: Optional[str] = Field(None, example="hombre")
    rutina: Optional[str] = Field(None, example="mantener_peso_h")

# ======================================================
# Modelo para RESPUESTA (lo que devuelves al cliente)
# ======================================================
class RoutineResponse(RoutineBase):
    id: int = Field(..., example=1)

    class Config:
        orm_mode = True