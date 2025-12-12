from config.db import Base, engine
from sqlalchemy.orm import Session, selectinload, joinedload
from models import Administrador, usuario
from datetime import datetime, timedelta, date
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status, Header
from config.db import get_db
from sqlalchemy import func

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

JWT_SECRET = "myjwtsecret"
ACCESS_TOKEN_EXPIRE = 30

def create_database():
    return Base.metadata.create_all(bind=engine)

