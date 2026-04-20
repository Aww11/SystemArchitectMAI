import os
import sys
import time
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = "postgresql://store_user:store_password@postgres:5432/store_db"

def wait_for_db():
    """Ждем пока БД станет доступной"""
    engine = create_engine(DATABASE_URL)
    for i in range(30):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                logger.info("Database is ready!")
                return True
        except Exception as e:
            logger.info(f"Waiting for database... ({i+1}/30)")
            time.sleep(1)
    logger.error("Database not available after 30 seconds")
    return False

def init_database():
    """Инициализация базы данных"""
    logger.info("Starting database initialization...")
    
    if not wait_for_db():
        sys.exit(1)
    
    engine = create_engine(DATABASE_URL)
    
    # Импортируем модели после проверки соединения
    from app.models import Base, User, Product, CartItem
    from app.auth import get_password_hash
    
    # Создаем таблицы
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Проверяем, есть ли уже данные
        user_count = db.query(User).count()
        if user_count > 0:
            logger.info(f"Database already has {user_count} users, skipping initialization")
            logger.info("Initialization complete!")
            return
        
        # Создаем тестовых пользователей
        logger.info("👥 Creating test users...")
        test_users = [
            {"username": "ivan_petrov", "email": "ivan@example.com", 
             "password": "password123", "first_name": "Иван", "last_name": "Петров"},
            {"username": "maria_sidorova", "email": "maria@example.com", 
             "password": "password123", "first_name": "Мария", "last_name": "Сидорова"},
            {"username": "alexey_smirnov", "email": "alexey@example.com", 
             "password": "password123", "first_name": "Алексей", "last_name": "Смирнов"},
        ]
        
        users = []
        for user_data in test_users:
            hashed_password = get_password_hash(user_data["password"])
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                hashed_password=hashed_password
            )
            db.add(user)
            users.append(user)
        
        db.commit()
        logger.info(f"Created {len(users)} test users")
        
        # Создаем тестовые товары
        logger.info("Creating test products...")
        test_products = [
            {"name": "Ноутбук Lenovo ThinkPad", "description": "Мощный ноутбук для работы и учебы", 
             "price": 89999.99, "stock": 10, "category": "Электроника"},
            {"name": "Смартфон Xiaomi Mi 11", "description": "Современный смартфон с отличной камерой", 
             "price": 34999.99, "stock": 25, "category": "Электроника"},
            {"name": "Наушники Sony WH-1000XM4", "description": "Беспроводные наушники с шумоподавлением", 
             "price": 24999.99, "stock": 15, "category": "Аксессуары"},
            {"name": "Клавиатура Mechanical", "description": "Механическая клавиатура для геймеров", 
             "price": 8999.99, "stock": 30, "category": "Аксессуары"},
            {"name": "Монитор Dell 27\"", "description": "Профессиональный монитор для работы", 
             "price": 29999.99, "stock": 8, "category": "Электроника"},
            {"name": "Мышь Logitech MX Master 3", "description": "Эргономичная беспроводная мышь", 
             "price": 7999.99, "stock": 20, "category": "Аксессуары"},
        ]
        
        products = []
        for product_data in test_products:
            product = Product(**product_data)
            db.add(product)
            products.append(product)
        
        db.commit()
        logger.info(f"Created {len(products)} test products")
        
        # Добавляем товары в корзины
        logger.info("🛒 Adding items to carts...")
        for user in users[:2]:
            for product in products[:3]:
                cart_item = CartItem(
                    user_id=user.id,
                    product_id=product.id,
                    quantity=1
                )
                db.add(cart_item)
        
        db.commit()
        
        logger.info("\n" + "="*60)
        logger.info("DATABASE INITIALIZATION COMPLETE!")
        logger.info("="*60)
        logger.info("Test credentials:")
        for user in users:
            logger.info(f"   {user.username} / password123")
        logger.info("="*60 + "\n")
        
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_database()