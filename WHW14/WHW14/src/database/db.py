from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from decouple import config

DATABASE_URL = config("DATABASE_URL")


#DATABASE_URL = "postgresql://postgres:567234@localhost:5432/rest_app"  

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# З'єднання до бази даних та інші налаштування
from .models import Base, engine

# Створення таблиці для токенів скидання паролю
Base.metadata.create_all(bind=engine)