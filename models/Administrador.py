from sqlalchemy import Column, Integer, String
from .base import Base


class Administrador(Base):
    __tablename__ = 'administrador'

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    nombre = Column(String(100), nullable=False)

    def __repr__(self):
        return f"<Administrador(id={self.id}, usuario={self.usuario})>"
