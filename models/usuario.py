from sqlalchemy import Column, Integer, String, Numeric, Enum, CheckConstraint
from .base import Base


class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    peso = Column(Numeric(5, 2), nullable=False)
    altura = Column(Numeric(4, 2), nullable=False)
    genero = Column(Enum('hombre', 'mujer', name='genero_enum'), nullable=False)
    imc = Column(Numeric(5, 2), nullable=True)
    categoria_imc = Column(String(30), nullable=True)
    rutina_asignada = Column(String(50), nullable=True)

    __table_args__ = (
        CheckConstraint('peso > 0', name='ck_usuario_peso_positive'),
        CheckConstraint('altura > 0 AND altura < 3', name='ck_usuario_altura_range'),
    )

    def calcular_imc(self):
        if self.altura and self.peso:
            try:
                imc_value = float(self.peso) / (float(self.altura) ** 2)
            except Exception:
                return None
            self.imc = round(imc_value, 2)
            if self.imc < 18.5:
                self.categoria_imc = 'bajo peso'
            elif self.imc < 25:
                self.categoria_imc = 'normal'
            elif self.imc < 30:
                self.categoria_imc = 'sobrepeso'
            else:
                self.categoria_imc = 'obesidad'
            return self.imc
        return None

    def __repr__(self):
        return f"<Usuario(id={self.id}, correo={self.correo})>"
