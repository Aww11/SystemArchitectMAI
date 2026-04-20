from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime
from bson import ObjectId
from app.database import users_collection, products_collection
from app.auth import get_current_active_user
from app.models import CartItemAdd, CartItemUpdate, CartResponse, CartItemResponse

router = APIRouter(prefix="/api/cart", tags=["cart"])

@router.get("/", response_model=CartResponse)
async def get_cart(current_user = Depends(get_current_active_user)):
    user_id = current_user["_id"]
    user = await users_collection.find_one({"_id": user_id})
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
    return CartResponse(
        user_id=str(user_id),
        items=items_response,
        total=total,
        updated_at=datetime.utcnow()
    )

@router.post("/items", response_model=CartResponse, status_code=status.HTTP_201_CREATED)
async def add_to_cart(
    item: CartItemAdd,
    current_user = Depends(get_current_active_user)
):
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
    return await get_cart(current_user)

@router.put("/items/{product_id}", response_model=CartResponse)
async def update_cart_item(
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
    return await get_cart(current_user)

@router.delete("/items/{product_id}", response_model=CartResponse)
async def remove_from_cart(
    product_id: str,
    current_user = Depends(get_current_active_user)
):
    user_id = current_user["_id"]
    user = await users_collection.find_one({"_id": user_id})
    cart = user.get("cart", [])
    new_cart = [item for item in cart if item["product_id"] != product_id]
    if len(new_cart) == len(cart):
        raise HTTPException(status_code=404, detail="Item not found in cart")
    await users_collection.update_one(
        {"_id": user_id},
        {"$set": {"cart": new_cart}}
    )
    return await get_cart(current_user)

@router.delete("/", response_model=CartResponse)
async def clear_cart(current_user = Depends(get_current_active_user)):
    user_id = current_user["_id"]
    await users_collection.update_one(
        {"_id": user_id},
        {"$set": {"cart": []}}
    )
    return await get_cart(current_user)