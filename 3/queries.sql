-- SQL запросы для API операций (вариант #2 - магазин)

-- Создание нового пользователя (POST /api/users/register)
INSERT INTO users (username, email, first_name, last_name, hashed_password)
VALUES ('new_user', 'new@example.com', 'Иван', 'Петров', 'hashed_password_here')
RETURNING id, username, email, first_name, last_name, created_at, is_active;

-- Поиск пользователя по логину (GET /api/users/{username})
-- Использует индекс idx_users_username
SELECT id, username, email, first_name, last_name, created_at, is_active
FROM users
WHERE username = 'ivan_88';

-- Поиск пользователя по маске имени (GET /api/users/search?first_name=...)
-- Использует индекс idx_users_first_name с text_pattern_ops
SELECT id, username, email, first_name, last_name
FROM users
WHERE first_name LIKE 'Иван%';

-- Поиск пользователя по маске фамилии (GET /api/users/search?last_name=...)
SELECT id, username, email, first_name, last_name
FROM users
WHERE last_name LIKE 'Пет%';

-- Поиск по маске имени и фамилии вместе
-- Использует составной индекс idx_users_full_name
SELECT id, username, email, first_name, last_name
FROM users
WHERE first_name LIKE 'Иван%' AND last_name LIKE 'Пет%';

-- Создание товара (POST /api/products)
INSERT INTO products (name, description, price, stock, category)
VALUES ('Новый смартфон', 'Мощный смартфон с отличной камерой', 599.99, 100, 'Electronics')
RETURNING id, name, price, stock, category, created_at;

-- Получение списка товаров с фильтром по категории (GET /api/products?category=...)
-- Использует индекс idx_products_category
SELECT id, name, description, price, stock, category, created_at
FROM products
WHERE category = 'Electronics'
ORDER BY id
LIMIT 100 OFFSET 0;

-- Получение всех товаров без фильтра
SELECT id, name, description, price, stock, category, created_at
FROM products
ORDER BY id
LIMIT 100 OFFSET 0;

-- Получение товаров с сортировкой по цене
-- Использует индекс idx_products_price
SELECT id, name, price, category
FROM products
ORDER BY price DESC
LIMIT 20;

-- Добавление товара в корзину (POST /api/cart/items)
-- Сначала проверяем остаток (можно и в одном запросе, но для наглядности отдельно)
SELECT id, name, stock FROM products WHERE id = 1;

-- Добавляем в корзину (FOREIGN KEY сам проверит существование user_id и product_id)
INSERT INTO cart_items (user_id, product_id, quantity)
VALUES (1, 1, 2)
RETURNING id, user_id, product_id, quantity, added_at;

-- Если товар уже есть в корзине - обновляем количество
INSERT INTO cart_items (user_id, product_id, quantity)
VALUES (1, 1, 2)
ON CONFLICT (user_id, product_id) 
DO UPDATE SET quantity = cart_items.quantity + EXCLUDED.quantity, added_at = CURRENT_TIMESTAMP
RETURNING id, user_id, product_id, quantity, added_at;

-- Обновление количества товара в корзине (PUT /api/cart/items/{product_id})
UPDATE cart_items
SET quantity = 5, added_at = CURRENT_TIMESTAMP
WHERE user_id = 1 AND product_id = 1
RETURNING id, user_id, product_id, quantity, added_at;

-- Удаление товара из корзины (DELETE /api/cart/items/{product_id})
DELETE FROM cart_items
WHERE user_id = 1 AND product_id = 1
RETURNING id, user_id, product_id, quantity;

-- Очистка всей корзины (DELETE /api/cart)
DELETE FROM cart_items
WHERE user_id = 1
RETURNING id, user_id, product_id, quantity;

-- Получение корзины пользователя с деталями товаров (GET /api/cart)
-- Использует индексы idx_cart_items_user_id и products_pkey
SELECT 
    ci.user_id,
    ci.product_id,
    ci.quantity,
    ci.added_at,
    p.name AS product_name,
    p.price AS product_price,
    p.category AS product_category,
    (p.price * ci.quantity) AS subtotal
FROM cart_items ci
JOIN products p ON ci.product_id = p.id
WHERE ci.user_id = 1
ORDER BY ci.added_at DESC;

-- Подсчёт общей суммы корзины
SELECT 
    ci.user_id,
    COALESCE(SUM(p.price * ci.quantity), 0) AS total
FROM cart_items ci
JOIN products p ON ci.product_id = p.id
WHERE ci.user_id = 1
GROUP BY ci.user_id;

-- Обновление товара (PUT /api/products/{product_id})
UPDATE products
SET price = 899.99, stock = 45
WHERE id = 1
RETURNING id, name, price, stock, category;

-- Удаление товара (DELETE /api/products/{product_id})
-- ON DELETE CASCADE в cart_items удалит все связанные записи в корзине
DELETE FROM products
WHERE id = 15
RETURNING id, name;

-- Проверка работы FOREIGN KEY (вызовет ошибку - товара нет)
-- INSERT INTO cart_items (user_id, product_id, quantity) VALUES (1, 999, 1);

-- Получение статистики по корзинам (дополнительный полезный запрос)
SELECT 
    u.username,
    COUNT(ci.id) AS items_count,
    COALESCE(SUM(p.price * ci.quantity), 0) AS cart_total
FROM users u
LEFT JOIN cart_items ci ON u.id = ci.user_id
LEFT JOIN products p ON ci.product_id = p.id
WHERE u.is_active = TRUE
GROUP BY u.id, u.username
ORDER BY cart_total DESC;

-- Поиск товаров по названию (частичное совпадение)
-- Использует индекс idx_products_name с text_pattern_ops
SELECT id, name, price, category
FROM products
WHERE name LIKE '%iPhone%';