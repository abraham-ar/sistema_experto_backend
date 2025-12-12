from pydantic import BaseModel

class EngineInput(BaseModel):
    peso: float
    altura: float
    genero: str   # "hombre" | "mujer"


class EngineRutinaResponse(BaseModel):
    imc: float
    clasificacion: str
    rutinas: list[str]
