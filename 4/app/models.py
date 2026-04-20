from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class CartItemBase(BaseModel):
    product_id: str
    product_name: str
    quantity: int = Field(ge=1)
    price: float = Field(ge=0)
    added_at: datetime = Field(default_factory=datetime.utcnow)

class CartItemInDB(CartItemBase):
    product_id: str

class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)

class UserCreate(UserBase):
    password: str = Field(min_length=6)

class UserInDB(UserBase):
    id: str = Field(alias="_id")
    hashed_password: str
    created_at: datetime
    is_active: bool = True
    cart: List[CartItemInDB] = []

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class UserResponse(UserBase):
    id: str
    created_at: datetime
    is_active: bool

class ProductBase(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    price: float = Field(ge=0)
    stock: int = Field(ge=0)
    category: str = Field(min_length=1, max_length=50)

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: str
    created_at: datetime

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    stock: Optional[int] = Field(None, ge=0)
    category: Optional[str] = Field(None, min_length=1, max_length=50)

class CartItemAdd(BaseModel):
    product_id: str
    quantity: int = Field(ge=1)

class CartItemUpdate(BaseModel):
    quantity: int = Field(ge=0)

class CartItemResponse(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    price: float
    added_at: datetime
    subtotal: float

class CartResponse(BaseModel):
    user_id: str
    items: List[CartItemResponse]
    total: float
    updated_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str