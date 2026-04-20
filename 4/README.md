# ДЗ #4: Проектирование и работа с MongoDB

**Вариант #2 (магазин, как Ozon)**  
**Студент:** Белякова Евдокия Алексеевна

---

## Запуск проекта

### 1. Запустить через Docker Compose

```bash
cd SystemArchitectMAI/4
docker-compose up --build
```

### 2. Проверить что база данных заполнилась

```bash
docker exec -it store_mongodb mongosh store_db --eval "db.users.countDocuments()"
docker exec -it store_mongodb mongosh store_db --eval "db.products.countDocuments()"
```

Ожидается: 10 пользователей, 15 товаров.

### 3. Открыть API документацию

```
http://localhost:8000/docs
```

---

## API Эндпоинты

### Пользователи

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| POST | `/api/users/register` | Создание пользователя |
| POST | `/api/users/login` | Вход (получение JWT токена) |
| GET | `/api/users/me` | Текущий пользователь |
| GET | `/api/users/search?first_name=&last_name=` | Поиск по маске |
| GET | `/api/users/{username}` | Получить пользователя по логину |

### Товары

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| POST | `/api/products` | Создать товар |
| GET | `/api/products` | Список товаров |
| GET | `/api/products/{product_id}` | Товар по ID |
| PUT | `/api/products/{product_id}` | Обновить товар |
| DELETE | `/api/products/{product_id}` | Удалить товар |

### Корзина

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/api/cart` | Корзина пользователя |
| POST | `/api/cart/items` | Добавить товар |
| PUT | `/api/cart/items/{product_id}` | Изменить количество |
| DELETE | `/api/cart/items/{product_id}` | Удалить товар из корзины |
| DELETE | `/api/cart` | Очистить корзину |

---

## Тестовые данные

| Логин | Пароль |
|-------|--------|
| ivan_88 | password123 |
| maria_s | password123 |
| alex_k | password123 |

---

## Выполнение MongoDB запросов

### Подключиться к MongoDB Shell

```bash
docker exec -it store_mongodb mongosh store_db
```

### Выполнить все CRUD операции

```bash
Get-Content queries.js | docker exec -i store_mongodb mongosh store_db
```

### Протестировать валидацию схемы

```bash
Get-Content validation.js | docker exec -i store_mongodb mongosh store_db
```

### Выйти из Shell

```javascript
exit
```

---

## Остановка контейнеров

```bash
docker-compose down

# Полная очистка (удаление томов с данными)
docker-compose down -v
```

---

## Структура проекта

```
SystemArchitectMAI/4/
├── app/                    # FastAPI приложение
├── mongo-init/
│   └── data.js            # Тестовые данные
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── queries.js             # CRUD операции
├── validation.js          # Валидация схемы
├── schema_design.md       # Проектирование модели
└── README.md
```