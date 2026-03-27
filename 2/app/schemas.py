from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# User schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserResponse(UserBase):
    id: int
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Product schemas
class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., max_length=500)
    price: Decimal = Field(..., gt=0, decimal_places=2)
    stock: int = Field(..., ge=0)
    category: str = Field(..., min_length=1, max_length=50)

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    stock: Optional[int] = Field(None, ge=0)
    category: Optional[str] = Field(None, min_length=1, max_length=50)

# Cart schemas
class CartItemAdd(BaseModel):
    product_id: int
    quantity: int = Field(..., ge=1)

class CartItemUpdate(BaseModel):
    quantity: int = Field(..., ge=0)

class CartItemResponse(BaseModel):
    id: int
    product: ProductResponse
    quantity: int
    added_at: datetime
    subtotal: Decimal

class CartResponse(BaseModel):
    user_id: int
    items: List[CartItemResponse]
    total: Decimal
    item_count: int

class ErrorResponse(BaseModel):
    """Схема для ошибок API"""
    detail: str
    status_code: int