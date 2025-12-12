from pydantic import BaseModel, Field
from typing import Optional

class RuleBase(BaseModel):
    condicion: str = Field(..., example="imc < 18.5")
    clasificacion: str = Field(..., example="Bajo peso")

class RuleCreate(RuleBase):
    pass

class RuleUpdate(RuleBase):
    id: int

class RuleResponse(RuleBase):
    id: int

    class Config:
        orm_mode = True
