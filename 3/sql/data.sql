-- Тестовые данные для интернет-магазина

TRUNCATE TABLE cart_items CASCADE;
TRUNCATE TABLE products CASCADE;
TRUNCATE TABLE users CASCADE;

-- Пользователи (10 записей)
INSERT INTO users (username, email, first_name, last_name, hashed_password, created_at, is_active) VALUES
('ivan_88', 'ivan@mail.ru', 'Иван', 'Петров', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VTtYrTe3mGjYzS', '2024-01-15 10:30:00', TRUE),
('maria_s', 'maria@yandex.ru', 'Мария', 'Сидорова', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VTtYrTe3mGjYzS', '2024-01-20 14:20:00', TRUE),
('alex_k', 'alex@google.com', 'Алексей', 'Кузнецов', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VTtYrTe3mGjYzS', '2024-02-01 09:15:00', TRUE),
('olga_n', 'olga@mail.ru', 'Ольга', 'Новикова', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VTtYrTe3mGjYzS', '2024-02-10 16:45:00', FALSE),
('dmitry99', 'dmitry@bk.ru', 'Дмитрий', 'Морозов', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VTtYrTe3mGjYzS', '2024-03-05 11:20:00', TRUE),
('ekaterina_p', 'ekaterina@mail.ru', 'Екатерина', 'Павлова', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VTtYrTe3mGjYzS', '2024-03-10 13:40:00', TRUE),
('sergey_n', 'sergey@yandex.ru', 'Сергей', 'Николаев', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VTtYrTe3mGjYzS', '2024-03-15 08:30:00', TRUE),
('anna_s', 'anna@google.com', 'Анна', 'Соколова', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VTtYrTe3mGjYzS', '2024-03-20 17:15:00', TRUE),
('pavel_r', 'pavel@bk.ru', 'Павел', 'Романов', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VTtYrTe3mGjYzS', '2024-03-25 12:00:00', TRUE),
('tatyana_l', 'tatyana@mail.ru', 'Татьяна', 'Лебедева', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VTtYrTe3mGjYzS', '2024-03-30 19:45:00', TRUE);

-- Товары (15 записей, разные категории)
INSERT INTO products (name, description, price, stock, category, created_at) VALUES
-- Электроника
('iPhone 15 Pro', 'Смартфон Apple с A17 Pro', 999.99, 50, 'Electronics', '2024-01-01'),
('Samsung TV 55"', '4K телевизор с Smart TV', 699.99, 20, 'Electronics', '2024-01-02'),
('Sony WH-1000XM5', 'Беспроводные наушники с шумодавом', 349.99, 100, 'Electronics', '2024-01-03'),
('MacBook Air M2', 'Ноутбук Apple 13"', 1199.99, 30, 'Electronics', '2024-01-04'),

-- Одежда
('Nike Air Max', 'Кроссовки белые', 129.99, 200, 'Clothing', '2024-01-05'),
('Adidas Hoodie', 'Толстовка черная', 89.99, 150, 'Clothing', '2024-01-06'),
('Levis Jeans 501', 'Джинсы классические синие', 79.99, 80, 'Clothing', '2024-01-07'),
('The North Face Jacket', 'Пуховик зимний', 299.99, 40, 'Clothing', '2024-01-08'),

-- Книги
('Python Programming', 'Учебник по Python для начинающих', 49.99, 30, 'Books', '2024-01-09'),
('The Hobbit', 'Фэнтези роман Толкина', 19.99, 45, 'Books', '2024-01-10'),
('Clean Code', 'Роберт Мартин. Идеальный код', 39.99, 25, 'Books', '2024-01-11'),

-- Товары для дома
('IKEA Floor Lamp', 'Напольная лампа с регулировкой', 59.99, 300, 'Home', '2024-01-12'),
('DeLonghi Coffee Maker', 'Кофеварка капельная', 129.99, 40, 'Home', '2024-01-13'),

-- Спорт
('Yoga Mat', 'Коврик для йоги 6мм', 25.99, 120, 'Sports', '2024-01-14'),
('Dumbbell Set 20kg', 'Набор гантелей с блинами', 89.99, 35, 'Sports', '2024-01-15');

-- Корзина пользователей (20 записей, чтобы было достаточно)
INSERT INTO cart_items (user_id, product_id, quantity, added_at) VALUES
(1, 1, 1, '2024-02-01 10:00:00'),   -- Иван: iPhone
(1, 5, 2, '2024-02-01 10:05:00'),   -- Иван: кроссовки
(1, 10, 1, '2024-02-01 10:10:00'),  -- Иван: Хоббит

(2, 9, 1, '2024-02-02 11:00:00'),   -- Мария: Python книга
(2, 12, 1, '2024-02-02 11:15:00'),  -- Мария: лампа

(3, 2, 1, '2024-02-03 09:00:00'),   -- Алексей: телевизор
(3, 6, 1, '2024-02-03 09:20:00'),   -- Алексей: толстовка

(4, 14, 2, '2024-02-04 14:00:00'),  -- Ольга (неактивная, но корзина есть)
(4, 15, 1, '2024-02-04 14:05:00'),  -- Ольга: гантели

(5, 3, 1, '2024-02-05 16:30:00'),   -- Дмитрий: наушники Sony
(5, 8, 1, '2024-02-05 16:45:00'),   -- Дмитрий: пуховик

(6, 4, 1, '2024-02-06 12:00:00'),   -- Екатерина: MacBook
(6, 11, 1, '2024-02-06 12:20:00'),  -- Екатерина: Clean Code

(7, 7, 2, '2024-02-07 08:30:00'),   -- Сергей: джинсы Levi's
(7, 13, 1, '2024-02-07 08:45:00'),  -- Сергей: кофеварка

(8, 5, 1, '2024-02-08 19:00:00'),   -- Анна: кроссовки
(8, 6, 1, '2024-02-08 19:10:00'),   -- Анна: толстовка
(8, 7, 1, '2024-02-08 19:15:00'),   -- Анна: джинсы

(9, 1, 1, '2024-02-09 20:00:00'),   -- Павел: iPhone
(9, 14, 1, '2024-02-09 20:30:00'),  -- Павел: коврик

(10, 2, 1, '2024-02-10 22:00:00'),  -- Татьяна: телевизор
(10, 3, 1, '2024-02-10 22:15:00');  -- Татьяна: наушники

-- Проверка целостности данных
-- Эта вставка вызовет ошибку FOREIGN KEY (товара с id=99 нет)
-- INSERT INTO cart_items (user_id, product_id, quantity) VALUES (1, 99, 1);

-- Эта вставка вызовет ошибку FOREIGN KEY (пользователя с id=99 нет)
-- INSERT INTO cart_items (user_id, product_id, quantity) VALUES (99, 1, 1);