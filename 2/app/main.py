from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routers import users, products, cart
from app.schemas import ErrorResponse
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Online Store API",
    description="REST API для интернет-магазина (аналог Ozon)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Сохраняем оригинальную функцию openapi
original_openapi = app.openapi

def custom_openapi():
    # Если уже сгенерировали, возвращаем сохраненную схему
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = original_openapi()
    
    # Добавляем Bearer auth схему
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Введите токен: Bearer <token>"
        }
    }
    
    # Добавляем security ко всем эндпоинтам по умолчанию
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    
    # Убираем security с публичных эндпоинтов
    public_endpoints = [
        ("/api/users/register", "post"),
        ("/api/users/login", "post"),
        ("/", "get"),
        ("/health", "get"),
    ]
    
    for path, method in public_endpoints:
        if path in openapi_schema["paths"]:
            if method in openapi_schema["paths"][path]:
                openapi_schema["paths"][path][method]["security"] = []
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# CORS настройки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(users.router)
app.include_router(products.router)
app.include_router(cart.router)

@app.get("/")
async def root():
    return {
        "message": "Добро пожаловать в Online Store API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "users": "/api/users",
            "products": "/api/products",
            "cart": "/api/cart"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Глобальный обработчик ошибок
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            detail=exc.detail,
            status_code=exc.status_code
        ).dict()
    )