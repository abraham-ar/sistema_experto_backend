from pydantic import BaseModel, Field
from typing import Optional, Literal

class EjercicioBase(BaseModel):
    ejercicio: str = Field(..., example="Press de banca")
    series: int = Field(..., example=4)
    repeticiones: str = Field(..., example="8-10")
    objetivo: str = Field(..., example="Ganar Masa Muscular")
    genero: Literal["hombre", "mujer", "mixto"] = Field(..., example="hombre")

class EjercicioCreate(EjercicioBase):
    pass

class EjercicioUpdate(BaseModel):
    ejercicio: Optional[str] = None
    series: Optional[int] = None
    repeticiones: Optional[str] = None
    objetivo: Optional[str] = None
    genero: Optional[str] = None

class EjercicioResponse(EjercicioBase):
    id: int

    class Config:
        orm_mode = True
