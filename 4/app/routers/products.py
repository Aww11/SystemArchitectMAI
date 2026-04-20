from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from app.database import products_collection
from app.auth import get_current_active_user
from app.models import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(prefix="/api/products", tags=["products"])

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    current_user = Depends(get_current_active_user)
):
    product_doc = {
        "name": product_data.name,
        "description": product_data.description,
        "price": product_data.price,
        "stock": product_data.stock,
        "category": product_data.category,
        "created_at": datetime.utcnow()
    }
    result = await products_collection.insert_one(product_doc)
    product_doc["id"] = str(result.inserted_id)
    del product_doc["_id"]
    return product_doc

@router.get("/", response_model=List[ProductResponse])
async def get_products(
    category: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_active_user)
):
    query = {}
    if category:
        query["category"] = {"$regex": f"^{category}$", "$options": "i"}
    cursor = products_collection.find(query).skip(skip).limit(limit)
    products = await cursor.to_list(length=limit)
    for p in products:
        p["id"] = str(p["_id"])
        del p["_id"]
    return products

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: str,
    current_user = Depends(get_current_active_user)
):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")
    product = await products_collection.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product["id"] = str(product["_id"])
    del product["_id"]
    return product

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: str,
    product_data: ProductUpdate,
    current_user = Depends(get_current_active_user)
):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")
    update_data = {k: v for k, v in product_data.dict().items() if v is not None}
    if not update_data:
        product = await products_collection.find_one({"_id": ObjectId(product_id)})
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        product["id"] = str(product["_id"])
        del product["_id"]
        return product
    result = await products_collection.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    product = await products_collection.find_one({"_id": ObjectId(product_id)})
    product["id"] = str(product["_id"])
    del product["_id"]
    return product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: str,
    current_user = Depends(get_current_active_user)
):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")
    result = await products_collection.delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")