# ДЗ #5: Оптимизация производительности через кеширование и rate limiting

**Вариант #2 (магазин, как Ozon)**  
**Студент:** Белякова Евдокия Алексеевна

---

## Реализованные оптимизации
1. **Кеширование (Redis)**
Эндпоинт	TTL	Инвалидация
GET /api/products	60 сек	При создании/обновлении/удалении товара
GET /api/products/{id}	300 сек	При обновлении/удалении товара
GET /api/cart	30 сек	При изменении корзины
2. **Rate limiting (Token Bucket)**
Эндпоинт	Лимит
GET /api/products	100 запросов/мин
GET /api/cart	60 запросов/мин
POST /api/cart/items	30 запросов/мин
POST /api/users/login	10 запросов/мин
POST /api/users/register	5 запросов/мин
Тестирование оптимизаций
Проверка кеширования
bash
# Получить токен
TOKEN=$(curl -s -X POST "http://localhost:8000/api/users/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser6","password":"111111"}' | jq -r '.access_token')

# Первый запрос (кеш пуст)
time curl -s -X GET "http://localhost:8000/api/products" \
  -H "Authorization: Bearer $TOKEN"

# Второй запрос (из кеша)
time curl -s -X GET "http://localhost:8000/api/products" \
  -H "Authorization: Bearer $TOKEN"

# Проверить Redis
docker exec store_redis redis-cli KEYS "*"
Проверка rate limiting
bash
# Быстро 12 запросов логина (должен вернуть 429 на 11-м)
for i in {1..12}; do
  curl -s -o /dev/null -w "%{http_code}\n" \
    -X POST "http://localhost:8000/api/users/login" \
    -H "Content-Type: application/json" \
    -d '{"username":"testuser6","password":"111111"}'
done

Структура проекта
text
SystemArchitectMAI/5/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── auth.py
│   ├── redis_client.py     # Подключение к Redis
│   ├── cache.py            # Функции кеширования
│   ├── rate_limit.py       # Token Bucket реализация
│   └── routers/
│       ├── __init__.py
│       ├── users.py
│       ├── products.py
│       └── cart.py
├── mongo-init/
│   └── data.js
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── performance_design.md
└── README.md