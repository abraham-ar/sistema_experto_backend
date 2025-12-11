from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/sistema_experto_gimnasio"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db  # Usamos yield para devolver la conexión a la base de datos
    finally:
        db.close()  # Cerramos la sesión cuando terminemos