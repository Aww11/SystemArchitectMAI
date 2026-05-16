## Файл 2: `event_catalog.md`

```markdown
# Каталог событий интернет-магазина

**Вариант #2 (магазин, как Ozon)**  
**Студент:** Белякова Евдокия Алексеевна

---

## 1. События пользователей

### 1.1 user.registered

| Свойство | Значение |
|----------|----------|
| Описание | Пользователь успешно зарегистрировался в системе |
| Производитель | API Users (POST /api/users/register) |
| Потребители | Analytics Consumer, (будущий) Notification Service |
| Routing key | `user.registered` |
| Тип доставки | Persistent, at-least-once |

**Payload структура:**

```json
{
  "user_id": "string - ID пользователя",
  "username": "string - Логин пользователя",
  "email": "string - Email пользователя",
  "first_name": "string - Имя пользователя",
  "last_name": "string - Фамилия пользователя",
  "created_at": "datetime - Дата и время регистрации (ISO 8601)"
}
```

---

### 1.2 user.logged_in

| Свойство | Значение |
|----------|----------|
| Описание | Пользователь успешно вошёл в систему |
| Производитель | API Users (POST /api/users/login) |
| Потребители | Analytics Consumer |
| Routing key | `user.logged_in` |
| Тип доставки | Persistent, at-least-once |

**Payload структура:**

```json
{
  "user_id": "string - ID пользователя",
  "username": "string - Логин пользователя",
  "timestamp": "datetime - Дата и время входа (ISO 8601)"
}
```

---

## 2. События товаров

### 2.1 product.created

| Свойство | Значение |
|----------|----------|
| Описание | Создан новый товар в каталоге |
| Производитель | API Products (POST /api/products) |
| Потребители | Analytics Consumer, (будущий) Search Service |
| Routing key | `product.created` |
| Тип доставки | Persistent, at-least-once |

**Payload структура:**

```json
{
  "product_id": "string - ID товара",
  "name": "string - Название товара",
  "description": "string - Описание товара",
  "price": "float - Цена товара",
  "stock": "int - Количество на складе",
  "category": "string - Категория товара",
  "created_at": "datetime - Дата и время создания (ISO 8601)"
}
```

---

### 2.2 product.updated

| Свойство | Значение |
|----------|----------|
| Описание | Обновлена информация о товаре (цена, остаток, описание) |
| Производитель | API Products (PUT /api/products/{id}) |
| Потребители | Analytics Consumer, Search Service, Cache |
| Routing key | `product.updated` |
| Тип доставки | Persistent, at-least-once |

**Payload структура:**

```json
{
  "product_id": "string - ID товара",
  "updated_fields": "object - Какие поля были изменены",
  "updated_at": "datetime - Дата и время обновления (ISO 8601)"
}
```

---

### 2.3 product.deleted

| Свойство | Значение |
|----------|----------|
| Описание | Товар удалён из каталога |
| Производитель | API Products (DELETE /api/products/{id}) |
| Потребители | Analytics Consumer, Search Service, Cache |
| Routing key | `product.deleted` |
| Тип доставки | Persistent, at-least-once |

**Payload структура:**

```json
{
  "product_id": "string - ID товара",
  "product_name": "string - Название удалённого товара",
  "deleted_at": "datetime - Дата и время удаления (ISO 8601)"
}
```

---

## 3. События корзины

### 3.1 cart.item_added

| Свойство | Значение |
|----------|----------|
| Описание | Товар добавлен в корзину пользователя |
| Производитель | API Cart (POST /api/cart/items) |
| Потребители | Analytics Consumer, Recommendations Service |
| Routing key | `cart.item_added` |
| Тип доставки | Persistent, at-least-once |

**Payload структура:**

```json
{
  "user_id": "string - ID пользователя",
  "username": "string - Логин пользователя",
  "product_id": "string - ID товара",
  "product_name": "string - Название товара",
  "quantity": "int - Количество",
  "price": "float - Цена за единицу",
  "added_at": "datetime - Дата и время добавления (ISO 8601)"
}
```

---

### 3.2 cart.item_removed

| Свойство | Значение |
|----------|----------|
| Описание | Товар удалён из корзины пользователя |
| Производитель | API Cart (DELETE /api/cart/items/{product_id}) |
| Потребители | Analytics Consumer |
| Routing key | `cart.item_removed` |
| Тип доставки | Persistent, at-least-once |

**Payload структура:**

```json
{
  "user_id": "string - ID пользователя",
  "username": "string - Логин пользователя",
  "product_id": "string - ID товара",
  "product_name": "string - Название удалённого товара",
  "removed_at": "datetime - Дата и время удаления (ISO 8601)"
}
```

---

### 3.3 cart.cleared

| Свойство | Значение |
|----------|----------|
| Описание | Корзина пользователя полностью очищена (обычно после оформления заказа) |
| Производитель | API Cart (DELETE /api/cart) |
| Потребители | Analytics Consumer, Orders Service |
| Routing key | `cart.cleared` |
| Тип доставки | Persistent, at-least-once |

**Payload структура:**

```json
{
  "user_id": "string - ID пользователя",
  "username": "string - Логин пользователя",
  "cleared_at": "datetime - Дата и время очистки (ISO 8601)"
}
```

---

## 4. Схема всех событий

| Событие | Производитель | Потребители | Routing Key |
|---------|---------------|-------------|-------------|
| user.registered | API Users | Analytics, Notification | user.registered |
| user.logged_in | API Users | Analytics | user.logged_in |
| product.created | API Products | Analytics, Search | product.created |
| product.updated | API Products | Analytics, Search, Cache | product.updated |
| product.deleted | API Products | Analytics, Search, Cache | product.deleted |
| cart.item_added | API Cart | Analytics, Recommendations | cart.item_added |
| cart.item_removed | API Cart | Analytics | cart.item_removed |
| cart.cleared | API Cart | Analytics, Orders | cart.cleared |

---

## 5. Диаграмма потоков

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              RABBITMQ                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         Exchange: store_events                       │   │
│  │                           (type: topic)                              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│          ┌─────────────┬───────────┼───────────┬─────────────┐             │
│          │             │           │           │             │             │
│          ▼             ▼           ▼           ▼             ▼             │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│   │ user.    │  │ user.    │  │ product. │  │ product. │  │ cart.    │    │
│   │registered│  │logged_in │  │created   │  │updated   │  │item_added│    │
│   └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
│                                                                             │
│                              Queue: analytics_queue                         │
│                              Binding: # (все события)                       │
│                                    │                                        │
└────────────────────────────────────┼────────────────────────────────────────┘
                                     │
                                     ▼
                    ┌─────────────────────────────────────┐
                    │         Analytics Consumer          │
                    │    (логирование, метрики, аналитика) │
                    └─────────────────────────────────────┘
```

---

## 6. Пример использования для аналитики

Consumer, подписанный на все события, может собирать метрики:

| Метрика | События |
|---------|---------|
| Количество регистраций в день | user.registered |
| Количество активных пользователей | user.logged_in |
| Популярные товары | cart.item_added |
| Конверсия (очистка корзины) | cart.cleared |
| Товары с падением остатка | product.updated (stock) |
```