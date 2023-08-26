from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import List


from ..database import db
from ..database.models import User
from ..schemas import Token, TokenData
from ..schemas import ContactCreate, ContactListResponse, ContactCreateResponse
from ..repository import users
from ..routes.auth import create_access_token, get_current_user

router = APIRouter()

# Налаштування JWT
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Генерація токена доступу
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire_date = datetime.utcnow() + expire
    to_encode.update({"exp": expire_date})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db.get_db)):
    user = users.get_user_by_email(db, form_data.username)
    if not user or not user.check_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_data = {
        "sub": user.email,
        "scopes": ["me"],
    }
    access_token = create_access_token(access_token_data)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me/", response_model=User)
def read_users_me(user: User = Depends(get_current_user)):
    return user


def get_current_user_from_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = users.get_user_by_email(db, email)
    if user is None:
        raise credentials_exception
    return user


@router.post("/contacts/", response_model=ContactCreateResponse)
def create_contact(contact: ContactCreate, db: Session = Depends(db.get_db), user: User = Depends(get_current_user_from_token)):
    # Ваш код для створення контакту тут
    pass

@router.get("/contacts/", response_model=List[ContactListResponse])
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(db.get_db), user: User = Depends(get_current_user_from_token)):
    # Ваш код для отримання списку контактів тут
    pass



