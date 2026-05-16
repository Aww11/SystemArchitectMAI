from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, products, cart
from app.redis_client import close_redis

app = FastAPI(
    title="Online Store API with MongoDB",
    description="REST API for online store using MongoDB with caching and rate limiting",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    swagger_ui_parameters={"persistAuthorization": True}
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(products.router)
app.include_router(cart.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Online Store API with MongoDB",
        "version": "3.0.0",
        "features": ["caching", "rate_limiting"],
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.on_event("shutdown")
async def shutdown_event():
    await close_redis()