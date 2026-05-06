from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DB = os.getenv("MONGODB_DB", "store_db")

client = AsyncIOMotorClient(MONGODB_URL)
db = client[MONGODB_DB]

users_collection = db.users
products_collection = db.products

def get_db():
    return db