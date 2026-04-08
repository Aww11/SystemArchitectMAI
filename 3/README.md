```markdown
# ДЗ #3: Проектирование БД для интернет-магазина

**Вариант #2 (магазин, как Ozon)**  
**Студент:** Белякова Евдокия Алексеевна

## Описание схемы БД

### Таблицы

#### users - пользователи
| Колонка | Тип | Ограничения |
|---------|-----|-------------|
| id | SERIAL | PRIMARY KEY |
| username | VARCHAR(50) | NOT NULL, UNIQUE |
| email | VARCHAR(100) | NOT NULL, UNIQUE |
| first_name | VARCHAR(50) | NOT NULL |
| last_name | VARCHAR(50) | NOT NULL |
| hashed_password | VARCHAR(255) | NOT NULL |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |
| is_active | BOOLEAN | DEFAULT TRUE |

#### products - товары
| Колонка | Тип | Ограничения |
|---------|-----|-------------|
| id | SERIAL | PRIMARY KEY |
| name | VARCHAR(200) | NOT NULL |
| description | TEXT | |
| price | DECIMAL(10,2) | NOT NULL, CHECK (price >= 0) |
| stock | INT | NOT NULL, DEFAULT 0, CHECK (stock >= 0) |
| category | VARCHAR(50) | NOT NULL |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

#### cart_items - корзина
| Колонка | Тип | Ограничения |
|---------|-----|-------------|
| id | SERIAL | PRIMARY KEY |
| user_id | INT | NOT NULL, FK → users(id) |
| product_id | INT | NOT NULL, FK → products(id) |
| quantity | INT | NOT NULL, CHECK (quantity > 0) |
| added_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |
| UNIQUE(user_id, product_id) | | |

### Связи между таблицами

users (1) ─────< (N) cart_items (N) >───── (1) products

- Один пользователь может иметь много записей в корзине
- Один товар может быть во многих корзинах
- Связь многие-ко-многим реализована через cart_items

## Индексы

| Таблица | Индекс | Тип | Назначение |
|---------|--------|-----|------------|
| users | idx_users_username | B-tree | Быстрый поиск по логину |
| users | idx_users_first_name | B-tree (text_pattern_ops) | Поиск по маске имени |
| users | idx_users_last_name | B-tree (text_pattern_ops) | Поиск по маске фамилии |
| users | idx_users_full_name | B-tree (составной) | Поиск по имени+фамилии |
| products | idx_products_category | B-tree | Фильтрация по категории |
| products | idx_products_name | B-tree (text_pattern_ops) | Поиск по названию |
| products | idx_products_price | B-tree | Сортировка по цене |
| cart_items | idx_cart_items_user_id | B-tree | JOIN и поиск корзины |
| cart_items | idx_cart_items_product_id | B-tree | JOIN и каскадное удаление |

## Запуск

### Через Docker

```bash
# Клонировать репозиторий
cd SystemArchitectMAI/3

# Запустить контейнеры
docker-compose up --build

# Остановить контейнеры
docker-compose down

# Остановить с удалением томов (очистка БД)
docker-compose down -v
```

### Доступ к сервисам

| Сервис | Адрес | Данные для входа |
|--------|-------|------------------|
| API документация | http://localhost:8000/docs | - |
| PostgreSQL | localhost:5432 | user: store_user, pass: store_pass, db: store_db |

### Проверка работы

```bash
# Проверить количество пользователей в БД
docker exec -it store_postgres psql -U store_user -d store_db -c "SELECT COUNT(*) FROM users;"

# Проверить состояние API
curl http://localhost:8000/health

# Подключиться к БД через psql
docker exec -it store_postgres psql -U store_user -d store_db
```

## Тестовые данные

| Таблица | Количество записей |
|---------|-------------------|
| users | 10 |
| products | 15 |
| cart_items | 22 |

### Примеры запросов

```sql
-- Получить корзину пользователя с деталями товаров
SELECT 
    u.username,
    p.name AS product_name,
    ci.quantity,
    p.price,
    (ci.quantity * p.price) AS subtotal
FROM cart_items ci
JOIN users u ON ci.user_id = u.id
JOIN products p ON ci.product_id = p.id
WHERE ci.user_id = 1;

-- Топ-5 товаров в корзинах
SELECT 
    p.name,
    p.category,
    SUM(ci.quantity) AS total_quantity,
    COUNT(DISTINCT ci.user_id) AS users_count
FROM products p
JOIN cart_items ci ON p.id = ci.product_id
GROUP BY p.id
ORDER BY total_quantity DESC
LIMIT 5;
```

## Структура проекта

```
SystemArchitectMAI/3/
├── app/                    # FastAPI приложение
├── sql/
│   ├── schema.sql         # CREATE TABLE, индексы, FK
│   ├── data.sql           # Тестовые данные
│   └── queries.sql        # SQL запросы для API
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── init_db.py
├── optimization.md
└── README.md
```