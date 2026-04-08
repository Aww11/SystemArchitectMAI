from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os

# Получаем DATABASE_URL из переменных окружения
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://store_user:store_pass@localhost:5432/store_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()