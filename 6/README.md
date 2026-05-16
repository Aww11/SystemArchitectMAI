# ДЗ #6: Проектирование Event-Driven архитектуры

**Вариант #2 (магазин, как Ozon)**  
**Студент:** Белякова Евдокия Алексеевна

---

## Описание проекта

REST API для интернет-магазина с Event-Driven архитектурой.  
При каждом действии в системе публикуются события в RabbitMQ, которые обрабатываются асинхронным consumer'ом.

### Компоненты системы

| Компонент | Назначение | Технология |
|-----------|------------|------------|
| API | Основной сервер, обрабатывает запросы | FastAPI + MongoDB + Redis |
| Producer | Публикует события при каждом действии | aio-pika |
| Broker | Маршрутизация событий | RabbitMQ |
| Consumer | Асинхронная обработка событий (логирование, аналитика) | aio-pika |
| Cache | Кеширование данных для ускорения ответов | Redis |

---

## События системы

| Событие | Когда публикуется |
|---------|-------------------|
| user.registered | При регистрации нового пользователя |
| user.logged_in | При входе пользователя |
| product.created | При создании нового товара |
| product.updated | При обновлении товара |
| product.deleted | При удалении товара |
| cart.item_added | При добавлении товара в корзину |
| cart.item_removed | При удалении товара из корзины |
| cart.cleared | При очистке корзины |

---

## Запуск проекта

Должны быть:
- `store_mongodb` (healthy)
- `store_redis` (healthy)
- `store_rabbitmq` (healthy)
- `store_api` (running)
- `store_consumer` (running)

### 4. Доступ к сервисам

| Сервис | Адрес | Данные для входа |
|--------|-------|------------------|
| API документация | http://localhost:8000/docs | - |
| RabbitMQ Management | http://localhost:15672 | guest / guest |
| PostgreSQL (если используется) | localhost:5432 | store_user / store_pass |
| Redis | localhost:6379 | - |
| MongoDB | localhost:27017 | - |

---

## API Эндпоинты

### Пользователи

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| POST | `/api/users/register` | Регистрация пользователя |
| POST | `/api/users/login` | Вход (получение JWT токена) |
| GET | `/api/users/me` | Текущий пользователь |
| GET | `/api/users/search` | Поиск по маске |
| GET | `/api/users/{username}` | Получить пользователя по логину |

### Товары

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| POST | `/api/products` | Создать товар (публикует `product.created`) |
| GET | `/api/products` | Список товаров |
| GET | `/api/products/{id}` | Товар по ID |
| PUT | `/api/products/{id}` | Обновить товар (публикует `product.updated`) |
| DELETE | `/api/products/{id}` | Удалить товар (публикует `product.deleted`) |

### Корзина

| Метод | Эндпоинт | Описание |
|-------|----------|----------|
| GET | `/api/cart` | Корзина пользователя |
| POST | `/api/cart/items` | Добавить товар (публикует `cart.item_added`) |
| PUT | `/api/cart/items/{id}` | Изменить количество |
| DELETE | `/api/cart/items/{id}` | Удалить товар (публикует `cart.item_removed`) |
| DELETE | `/api/cart` | Очистить корзину (публикует `cart.cleared`) |

---


## Мониторинг

### RabbitMQ Management UI

- Открой http://localhost:15672
- Логин: guest, Пароль: guest
- Вкладки:
  - **Queues** — просмотр очередей и сообщений
  - **Exchanges** — просмотр exchange `store_events`
  - **Connections** — активные подключения

---