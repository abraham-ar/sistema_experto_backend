from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class RutinaBase(BaseModel):
    clasificacion: str = Field(..., example="Bajo peso")
    genero: Literal["hombre", "mujer", "mixto"] = Field(..., example="hombre")
    rutina: str = Field(..., example="Ganar masa muscular - Hombre") # nombre único
    tipo: str = Field(..., example="Ganar masa muscular")


class RutinaCreate(RutinaBase):
    """
    Al crear rutina NO se envían ejercicios
    """
    pass


class RutinaUpdate(BaseModel):
    clasificacion: Optional[str] = None
    genero: Optional[str] = None
    tipo: Optional[str] = None
    ejercicios: Optional[List[int]] = None


class RutinaResponse(BaseModel):
    clasificacion: str
    genero: str
    rutina: str
    tipo: str
    ejercicios: List[dict]  # ejercicios completos

    class Config:
        orm_mode = True

class RutinaEjerciciosResponse(BaseModel):
    rutina: str
    ejercicios: list[dict]
