from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_
import logging
from decimal import Decimal
from app.schemas import CartItemAdd, CartItemUpdate, CartResponse, CartItemResponse
from app.database import get_db
from app.models import CartItem, Product
from app.auth import get_current_active_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/cart", tags=["cart"])

@router.get("/", response_model=CartResponse)
def get_cart(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Получение корзины текущего пользователя"""
    cart_items = db.query(CartItem).filter(
        CartItem.user_id == current_user.id
    ).all()
    
    items_response = []
    total = Decimal('0')
    
    for item in cart_items:
        if item.product and not item.product.is_deleted:
            subtotal = item.product.price * item.quantity
            total += subtotal
            
            items_response.append(CartItemResponse(
                id=item.id,
                product=item.product,
                quantity=item.quantity,
                added_at=item.added_at,
                subtotal=subtotal
            ))
    
    return CartResponse(
        user_id=current_user.id,
        items=items_response,
        total=total,
        item_count=sum(item.quantity for item in cart_items)
    )

@router.post("/items", response_model=CartResponse, status_code=status.HTTP_201_CREATED)
def add_to_cart(
    item: CartItemAdd,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Добавление товара в корзину"""
    # Проверка наличия товара
    product = db.query(Product).filter(
        Product.id == item.product_id,
        Product.is_deleted == False
    ).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    if product.stock < item.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not enough stock. Available: {product.stock}"
        )
    
    # Проверка наличия товара в корзине
    existing_item = db.query(CartItem).filter(
        and_(
            CartItem.user_id == current_user.id,
            CartItem.product_id == item.product_id
        )
    ).first()
    
    if existing_item:
        existing_item.quantity += item.quantity
    else:
        cart_item = CartItem(
            user_id=current_user.id,
            product_id=item.product_id,
            quantity=item.quantity
        )
        db.add(cart_item)
    
    db.commit()
    return get_cart(db, current_user)

@router.put("/items/{product_id}", response_model=CartResponse)
def update_cart_item(
    product_id: int,
    item: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Обновление количества товара в корзине"""
    cart_item = db.query(CartItem).filter(
        and_(
            CartItem.user_id == current_user.id,
            CartItem.product_id == product_id
        )
    ).first()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found in cart"
        )
    
    if item.quantity <= 0:
        db.delete(cart_item)
    else:
        cart_item.quantity = item.quantity
    
    db.commit()
    return get_cart(db, current_user)

@router.delete("/items/{product_id}", response_model=CartResponse)
def remove_from_cart(
    product_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Удаление товара из корзины"""
    cart_item = db.query(CartItem).filter(
        and_(
            CartItem.user_id == current_user.id,
            CartItem.product_id == product_id
        )
    ).first()
    
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found in cart"
        )
    
    db.delete(cart_item)
    db.commit()
    return get_cart(db, current_user)

@router.delete("/", response_model=CartResponse)
def clear_cart(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Очистка всей корзины"""
    db.query(CartItem).filter(
        CartItem.user_id == current_user.id
    ).delete()
    
    db.commit()
    
    return CartResponse(
        user_id=current_user.id,
        items=[],
        total=Decimal('0'),
        item_count=0
    )