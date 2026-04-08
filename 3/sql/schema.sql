-- Таблица пользователей
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    
    CONSTRAINT check_name_length CHECK (LENGTH(first_name) >= 1 AND LENGTH(last_name) >= 1)
);

-- Таблица товаров (без партиционирования)
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0),
    category VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица корзины (с FOREIGN KEY на обе таблицы)
CREATE TABLE cart_items (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- FOREIGN KEY - всё правильно, без костылей
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    
    -- Один пользователь не может добавить один товар дважды
    UNIQUE(user_id, product_id)
);

-- Индексы для ускорения запросов
-- Для users: поиск по логину и по маске имени/фамилии
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_first_name ON users(first_name text_pattern_ops);
CREATE INDEX idx_users_last_name ON users(last_name text_pattern_ops);
CREATE INDEX idx_users_full_name ON users(first_name, last_name);

-- Для products: фильтрация и поиск
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_name ON products(name text_pattern_ops);
CREATE INDEX idx_products_price ON products(price);

-- Для cart_items: быстрые JOIN и поиск по пользователю
CREATE INDEX idx_cart_items_user_id ON cart_items(user_id);
CREATE INDEX idx_cart_items_product_id ON cart_items(product_id);