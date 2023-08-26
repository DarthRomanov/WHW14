import cloudinary
from fastapi import Depends, APIRouter, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext

from ..database import db
from ..repository import users
from ..database.models import User
from ...config import CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET, CLOUDINARY_CLOUD_NAME
from ..schemas import Token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

auth_router = APIRouter()


# Налаштування JWT
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Налаштування API для аватарів
cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)
# Функція для створення JWT токена
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Декоратор для перевірки авторизації
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
    user = users.get_user_by_email(db.get_db(), email)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user


@auth_router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db.get_db)):
    user = get_current_user(form_data.username)  # Отримання об'єкту користувача на основі username

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

