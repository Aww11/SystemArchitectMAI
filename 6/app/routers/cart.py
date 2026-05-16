from fastapi import APIRouter, HTTPException, status, Depends, Request
from datetime import datetime
from bson import ObjectId
from app.database import users_collection, products_collection
from app.auth import get_current_active_user
from app.models import CartItemAdd, CartItemUpdate, CartResponse, CartItemResponse
from app.cache import invalidate_user_cart_cache
from app.rate_limit import rate_limit
from app.redis_client import get_redis
from app.event_publisher import publish_event
import json

router = APIRouter(prefix="/api/cart", tags=["cart"])

@router.get("/", response_model=CartResponse)
async def get_cart(
    request: Request,
    current_user = Depends(get_current_active_user)
):
    await rate_limit(request, "cart")
    
    user_id = str(current_user["_id"])
    redis = await get_redis()
    cache_key = f"cart:user_id={user_id}"
    
    cached = await redis.get(cache_key)
    if cached:
        return json.loads(cached)
    
    user = await users_collection.find_one({"_id": current_user["_id"]})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    cart_items = user.get("cart", [])
    items_response = []
    total = 0.0
    for item in cart_items:
        subtotal = item["quantity"] * item["price"]
        total += subtotal
        items_response.append(CartItemResponse(
            product_id=item["product_id"],
            product_name=item["product_name"],
            quantity=item["quantity"],
            price=item["price"],
            added_at=item.get("added_at", datetime.utcnow()),
            subtotal=subtotal
        ))
    result = CartResponse(
        user_id=user_id,
        items=items_response,
        total=total,
        updated_at=datetime.utcnow()
    )
    
    await redis.setex(cache_key, 30, json.dumps(result.dict(), default=str))
    return result

@router.post("/items", response_model=CartResponse, status_code=status.HTTP_201_CREATED)
async def add_to_cart(
    request: Request,
    item: CartItemAdd,
    current_user = Depends(get_current_active_user)
):
    await rate_limit(request, "cart_write")
    
    user_id = current_user["_id"]
    if not ObjectId.is_valid(item.product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")
    product = await products_collection.find_one({"_id": ObjectId(item.product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product["stock"] < item.quantity:
        raise HTTPException(status_code=400, detail=f"Not enough stock. Available: {product['stock']}")
    user = await users_collection.find_one({"_id": user_id})
    cart = user.get("cart", [])
    found = False
    for i, cart_item in enumerate(cart):
        if cart_item["product_id"] == item.product_id:
            cart[i]["quantity"] += item.quantity
            found = True
            break
    if not found:
        cart.append({
            "product_id": item.product_id,
            "product_name": product["name"],
            "quantity": item.quantity,
            "price": product["price"],
            "added_at": datetime.utcnow()
        })
    await users_collection.update_one(
        {"_id": user_id},
        {"$set": {"cart": cart}}
    )
    
    await invalidate_user_cart_cache(str(user_id))
    
    await publish_event("cart.item_added", {
        "user_id": str(user_id),
        "username": current_user.get("username"),
        "product_id": item.product_id,
        "product_name": product["name"],
        "quantity": item.quantity,
        "price": product["price"],
        "added_at": datetime.utcnow().isoformat()
    })
    
    return await get_cart(request, current_user)

@router.put("/items/{product_id}", response_model=CartResponse)
async def update_cart_item(
    request: Request,
    product_id: str,
    item: CartItemUpdate,
    current_user = Depends(get_current_active_user)
):
    user_id = current_user["_id"]
    user = await users_collection.find_one({"_id": user_id})
    cart = user.get("cart", [])
    found = False
    for i, cart_item in enumerate(cart):
        if cart_item["product_id"] == product_id:
            if item.quantity <= 0:
                cart.pop(i)
            else:
                cart[i]["quantity"] = item.quantity
            found = True
            break
    if not found:
        raise HTTPException(status_code=404, detail="Item not found in cart")
    await users_collection.update_one(
        {"_id": user_id},
        {"$set": {"cart": cart}}
    )
    
    await invalidate_user_cart_cache(str(user_id))
    return await get_cart(request, current_user)

@router.delete("/items/{product_id}", response_model=CartResponse)
async def remove_from_cart(
    request: Request,
    product_id: str,
    current_user = Depends(get_current_active_user)
):
    user_id = current_user["_id"]
    user = await users_collection.find_one({"_id": user_id})
    cart = user.get("cart", [])
    product_name = None
    for item in cart:
        if item["product_id"] == product_id:
            product_name = item.get("product_name")
            break
    
    new_cart = [item for item in cart if item["product_id"] != product_id]
    if len(new_cart) == len(cart):
        raise HTTPException(status_code=404, detail="Item not found in cart")
    await users_collection.update_one(
        {"_id": user_id},
        {"$set": {"cart": new_cart}}
    )
    
    await invalidate_user_cart_cache(str(user_id))
    
    await publish_event("cart.item_removed", {
        "user_id": str(user_id),
        "username": current_user.get("username"),
        "product_id": product_id,
        "product_name": product_name,
        "removed_at": datetime.utcnow().isoformat()
    })
    
    return await get_cart(request, current_user)

@router.delete("/", response_model=CartResponse)
async def clear_cart(
    request: Request,
    current_user = Depends(get_current_active_user)
):
    user_id = current_user["_id"]
    await users_collection.update_one(
        {"_id": user_id},
        {"$set": {"cart": []}}
    )
    
    await invalidate_user_cart_cache(str(user_id))
    
    await publish_event("cart.cleared", {
        "user_id": str(user_id),
        "username": current_user.get("username"),
        "cleared_at": datetime.utcnow().isoformat()
    })
    
    return await get_cart(request, current_user)