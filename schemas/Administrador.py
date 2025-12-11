from pydantic import BaseModel, EmailStr, SecretStr

class Administrador(BaseModel):
    #datos generales
    usuario: str
    password: str