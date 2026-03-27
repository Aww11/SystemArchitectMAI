from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
import logging
from app.schemas import UserCreate, UserResponse, UserLogin, Token
from app.database import get_db
from app.models import User
from app.auth import authenticate_user, create_access_token, get_password_hash, get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Создание нового пользователя (публичный эндпоинт)"""
    logger.info(f"POST /api/users/register - Регистрация пользователя: {user_data.username}")
    
    # Проверка существующего логина
    existing_user = db.query(User).filter(
        User.username == user_data.username,
        User.is_deleted == False
    ).first()
    if existing_user:
        logger.warning(f"POST /api/users/register - Логин уже существует: {user_data.username}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Проверка существующего email
    existing_email = db.query(User).filter(
        User.email == user_data.email,
        User.is_deleted == False
    ).first()
    if existing_email:
        logger.warning(f"POST /api/users/register - Email уже существует: {user_data.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Создание пользователя
    hashed_password = get_password_hash(user_data.password)
    user = User(
        username=user_data.username,
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        hashed_password=hashed_password
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    logger.info(f"POST /api/users/register - Пользователь создан с ID: {user.id}")
    return user

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Вход в систему (публичный эндпоинт)"""
    logger.info(f"POST /api/users/login - Попытка входа: {user_data.username}")
    
    user = authenticate_user(db, user_data.username, user_data.password)
    if not user:
        logger.warning(f"POST /api/users/login - Неудачная попытка входа: {user_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    logger.info(f"POST /api/users/login - Успешный вход: {user.username}")
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/search", response_model=List[UserResponse])
def search_users(
    login: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Поиск пользователей по маске логина, имени и фамилии (требует авторизацию)"""
    logger.info(f"GET /api/users/search - Поиск: login={login}, first_name={first_name}, last_name={last_name}")
    
    query = db.query(User).filter(User.is_deleted == False)
    
    if login:
        login_pattern = login.replace('%', '%%')
        if '%' not in login_pattern:
            login_pattern = f"%{login_pattern}%"
        query = query.filter(User.username.like(login_pattern))
    
    if first_name:
        first_name_pattern = first_name.replace('%', '%%')
        if '%' not in first_name_pattern:
            first_name_pattern = f"%{first_name_pattern}%"
        query = query.filter(User.first_name.like(first_name_pattern))
    
    if last_name:
        last_name_pattern = last_name.replace('%', '%%')
        if '%' not in last_name_pattern:
            last_name_pattern = f"%{last_name_pattern}%"
        query = query.filter(User.last_name.like(last_name_pattern))
    
    users = query.all()
    logger.info(f"GET /api/users/search - Найдено {len(users)} пользователей")
    return users

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user = Depends(get_current_active_user)):
    """Получение информации о текущем пользователе (требует авторизацию)"""
    logger.info(f"GET /api/users/me - Информация о пользователе: {current_user.username}")
    return current_user

@router.get("/by-login/{login}", response_model=UserResponse)
def get_user_by_login(
    login: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Получение пользователя по логину (требует авторизацию)"""
    logger.info(f"GET /api/users/by-login/{login} - Поиск пользователя")
    
    user = db.query(User).filter(
        User.username == login,
        User.is_deleted == False
    ).first()
    
    if not user:
        logger.warning(f"GET /api/users/by-login/{login} - Пользователь не найден")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    logger.info(f"GET /api/users/by-login/{login} - Найден пользователь: {user.username}")
    return user