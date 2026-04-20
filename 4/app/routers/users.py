from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from app.database import users_collection
from app.auth import (
    authenticate_user, create_access_token, get_password_hash,
    get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.models import (
    UserCreate, UserResponse, Token, UserLogin
)
from datetime import timedelta

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate):
    if await users_collection.find_one({"username": user_data.username}):
        raise HTTPException(status_code=400, detail="Username already registered")
    if await users_collection.find_one({"email": user_data.email}):
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user_data.password)
    user_doc = {
        "username": user_data.username,
        "email": user_data.email,
        "first_name": user_data.first_name,
        "last_name": user_data.last_name,
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow(),
        "is_active": True,
        "cart": []
    }
    result = await users_collection.insert_one(user_doc)
    user_doc["id"] = str(result.inserted_id)
    return user_doc

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin):
    user = await authenticate_user(user_data.username, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/search", response_model=List[UserResponse])
async def search_users(
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    current_user = Depends(get_current_active_user)
):
    query = {}
    if first_name:
        query["first_name"] = {"$regex": f"^{first_name}", "$options": "i"}
    if last_name:
        query["last_name"] = {"$regex": f"^{last_name}", "$options": "i"}
    cursor = users_collection.find(query)
    users = await cursor.to_list(length=100)
    for u in users:
        u["id"] = str(u["_id"])
        del u["_id"]
    return users

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user = Depends(get_current_active_user)):
    current_user["id"] = str(current_user["_id"])
    del current_user["_id"]
    return current_user

@router.get("/{username}", response_model=UserResponse)
async def get_user_by_username(
    username: str,
    current_user = Depends(get_current_active_user)
):
    user = await users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user["id"] = str(user["_id"])
    del user["_id"]
    return user