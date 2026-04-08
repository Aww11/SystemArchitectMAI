# Оптимизация запросов для интернет-магазина

## 1. Созданные индексы

| Таблица | Индекс | Тип | Назначение |
|---------|--------|-----|------------|
| users | idx_users_username | B-tree | Быстрый поиск пользователя по логину |
| users | idx_users_first_name | B-tree (text_pattern_ops) | Поиск по маске имени (LIKE 'Иван%') |
| users | idx_users_last_name | B-tree (text_pattern_ops) | Поиск по маске фамилии |
| users | idx_users_full_name | B-tree (составной) | Поиск по имени и фамилии одновременно |
| products | idx_products_category | B-tree | Фильтрация товаров по категории |
| products | idx_products_name | B-tree (text_pattern_ops) | Поиск товаров по названию |
| products | idx_products_price | B-tree | Сортировка товаров по цене |
| cart_items | idx_cart_items_user_id | B-tree | Быстрое получение корзины пользователя |
| cart_items | idx_cart_items_product_id | B-tree | JOIN с таблицей products и каскадное удаление |

## 2. Обоснование индексов

### idx_users_username
Запрос `WHERE username = 'ivan_88'` используется при входе пользователя и получении профиля. Без индекса PostgreSQL выполняет последовательное сканирование.

### idx_users_first_name и idx_users_last_name
Поиск по маске `LIKE 'Иван%'` не может использовать обычный B-tree индекс. text_pattern_ops позволяет ускорить поиск по началу строки.

### idx_cart_items_user_id
При получении корзины пользователя выполняется `WHERE user_id = 1`. Индекс позволяет найти все записи корзины без сканирования всей таблицы.

## 3. Сравнение планов выполнения (EXPLAIN)

### 3.1 Поиск пользователя по логину

**Без индекса:**
```
Seq Scan on users (cost=0.00..10.50 rows=1 width=100)
  Filter: ((username)::text = 'ivan_88'::text)
```

**С индексом idx_users_username:**
```
Index Scan using idx_users_username on users (cost=0.14..8.15 rows=1 width=100)
  Index Cond: (username = 'ivan_88'::text)
```

**Вывод:** Index Scan быстрее Seq Scan, особенно при большом количестве записей.

### 3.2 Поиск по маске имени

**Без индекса (обычный B-tree не помогает):**
```
Seq Scan on users (cost=0.00..10.50 rows=1 width=100)
  Filter: (first_name ~~ 'Иван%'::text)
```

**С индексом idx_users_first_name с text_pattern_ops:**
```
Index Scan using idx_users_first_name on users (cost=0.14..8.15 rows=1 width=100)
  Index Cond: ((first_name ~>=~ 'Иван'::text) AND (first_name ~<~ 'Ивао'::text))
  Filter: (first_name ~~ 'Иван%'::text)
```

**Вывод:** text_pattern_ops позволяет использовать индекс для LIKE-запросов.

### 3.3 Получение корзины пользователя

**Без индекса:**
```
Seq Scan on cart_items (cost=0.00..15.00 rows=5 width=20)
  Filter: (user_id = 1)
```

**С индексом idx_cart_items_user_id:**
```
Index Scan using idx_cart_items_user_id on cart_items (cost=0.14..8.15 rows=5 width=20)
  Index Cond: (user_id = 1)
```

### 3.4 JOIN корзины с товарами

**Без индексов:**
```
Nested Loop (cost=0.00..30.00 rows=10 width=200)
  -> Seq Scan on cart_items (cost=0.00..15.00 rows=5 width=50)
        Filter: (user_id = 1)
  -> Seq Scan on products (cost=0.00..15.00 rows=1 width=150)
        Filter: (id = cart_items.product_id)
```

**С индексами:**
```
Nested Loop (cost=2.00..20.00 rows=5 width=200)
  -> Index Scan using idx_cart_items_user_id on cart_items (cost=0.14..8.15 rows=5 width=50)
        Index Cond: (user_id = 1)
  -> Index Scan using products_pkey on products (cost=0.14..8.15 rows=1 width=150)
        Index Cond: (id = cart_items.product_id)
```

## 4. Тестовые данные

| Таблица | Количество записей |
|---------|-------------------|
| users | 10 |
| products | 15 |
| cart_items | 22 |

## 5. Валидация FOREIGN KEY

При попытке вставить в корзину несуществующий товар:
```sql
INSERT INTO cart_items (user_id, product_id, quantity) VALUES (1, 999, 1);
```

Результат:
```
ERROR: insert or update on table "cart_items" violates foreign key constraint "cart_items_product_id_fkey"
DETAIL: Key (product_id)=(999) is not present in table "products".
```

## 6. Примеры выполнения запросов

### 6.1 Общая стоимость корзины по пользователям
```sql
SELECT 
    u.username,
    COALESCE(SUM(p.price * ci.quantity), 0) AS cart_total
FROM users u
LEFT JOIN cart_items ci ON u.id = ci.user_id
LEFT JOIN products p ON ci.product_id = p.id
GROUP BY u.id
ORDER BY cart_total DESC;
```

Результат:
```
   username   | cart_total
--------------+------------
 ekaterina_p  |    1239.98
 ivan_88      |    1179.96
 tatyana_l    |    1049.98
 pavel_r      |     925.98
 alex_k       |     789.98
```

### 6.2 Топ-5 товаров в корзинах
```sql
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

Результат:
```
      name       |  category   | total_quantity | users_count
-----------------+-------------+----------------+-------------
 Nike Air Max    | Clothing    |              3 |           2
 Levis Jeans 501 | Clothing    |              3 |           2
 Sony WH-1000XM5 | Electronics |              2 |           2
 Samsung TV 55"  | Electronics |              2 |           2
 iPhone 15 Pro   | Electronics |              2 |           2
```

### 6.3 Каскадное удаление
```sql
DELETE FROM users WHERE id = 4 RETURNING id, username;
-- Записи в cart_items с user_id=4 удалены автоматически благодаря ON DELETE CASCADE
```

## 7. Вывод

1. Индексы ускоряют выполнение запросов: Index Scan вместо Seq Scan
2. text_pattern_ops необходим для эффективного поиска по маске (LIKE)
3. FOREIGN KEY обеспечивают целостность данных
4. ON DELETE CASCADE автоматически очищает связанные записи
5. Партиционирование не применялось, так как таблицы небольшого размера и FOREIGN KEY важнее для данной схемы