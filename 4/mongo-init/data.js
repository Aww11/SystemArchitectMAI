db.users.drop();
db.products.drop();

db.products.insertMany([
  {
    _id: ObjectId("000000000000000000000001"),
    name: "iPhone 15 Pro",
    description: "Смартфон Apple с A17 Pro",
    price: 999.99,
    stock: 50,
    category: "Electronics",
    created_at: ISODate("2024-01-01T00:00:00Z")
  },
  {
    _id: ObjectId("000000000000000000000002"),
    name: "Samsung TV 55\"",
    description: "4K телевизор с Smart TV",
    price: 699.99,
    stock: 20,
    category: "Electronics",
    created_at: ISODate("2024-01-02T00:00:00Z")
  },
  {
    _id: ObjectId("000000000000000000000003"),
    name: "Sony WH-1000XM5",
    description: "Беспроводные наушники с шумодавом",
    price: 349.99,
    stock: 100,
    category: "Electronics",
    created_at: ISODate("2024-01-03T00:00:00Z")
  },
  {
    _id: ObjectId("000000000000000000000004"),
    name: "MacBook Air M2",
    description: "Ноутбук Apple 13\"",
    price: 1199.99,
    stock: 30,
    category: "Electronics",
    created_at: ISODate("2024-01-04T00:00:00Z")
  },
  {
    _id: ObjectId("000000000000000000000005"),
    name: "Nike Air Max",
    description: "Кроссовки белые",
    price: 129.99,
    stock: 200,
    category: "Clothing",
    created_at: ISODate("2024-01-05T00:00:00Z")
  },
  {
    _id: ObjectId("000000000000000000000006"),
    name: "Adidas Hoodie",
    description: "Толстовка черная",
    price: 89.99,
    stock: 150,
    category: "Clothing",
    created_at: ISODate("2024-01-06T00:00:00Z")
  },
  {
    _id: ObjectId("000000000000000000000007"),
    name: "Levis Jeans 501",
    description: "Джинсы классические синие",
    price: 79.99,
    stock: 80,
    category: "Clothing",
    created_at: ISODate("2024-01-07T00:00:00Z")
  },
  {
    _id: ObjectId("000000000000000000000008"),
    name: "The North Face Jacket",
    description: "Пуховик зимний",
    price: 299.99,
    stock: 40,
    category: "Clothing",
    created_at: ISODate("2024-01-08T00:00:00Z")
  },
  {
    _id: ObjectId("000000000000000000000009"),
    name: "Python Programming",
    description: "Учебник по Python для начинающих",
    price: 49.99,
    stock: 30,
    category: "Books",
    created_at: ISODate("2024-01-09T00:00:00Z")
  },
  {
    _id: ObjectId("000000000000000000000010"),
    name: "The Hobbit",
    description: "Фэнтези роман Толкина",
    price: 19.99,
    stock: 45,
    category: "Books",
    created_at: ISODate("2024-01-10T00:00:00Z")
  },
  {
    _id: ObjectId("000000000000000000000011"),
    name: "Clean Code",
    description: "Роберт Мартин. Идеальный код",
    price: 39.99,
    stock: 25,
    category: "Books",
    created_at: ISODate("2024-01-11T00:00:00Z")
  },
  {
    _id: ObjectId("000000000000000000000012"),
    name: "IKEA Floor Lamp",
    description: "Напольная лампа с регулировкой",
    price: 59.99,
    stock: 300,
    category: "Home",
    created_at: ISODate("2024-01-12T00:00:00Z")
  },
  {
    _id: ObjectId("000000000000000000000013"),
    name: "DeLonghi Coffee Maker",
    description: "Кофеварка капельная",
    price: 129.99,
    stock: 40,
    category: "Home",
    created_at: ISODate("2024-01-13T00:00:00Z")
  },
  {
    _id: ObjectId("000000000000000000000014"),
    name: "Yoga Mat",
    description: "Коврик для йоги 6мм",
    price: 25.99,
    stock: 120,
    category: "Sports",
    created_at: ISODate("2024-01-14T00:00:00Z")
  },
  {
    _id: ObjectId("000000000000000000000015"),
    name: "Dumbbell Set 20kg",
    description: "Набор гантелей с блинами",
    price: 89.99,
    stock: 35,
    category: "Sports",
    created_at: ISODate("2024-01-15T00:00:00Z")
  }
]);

// =====================================================
// 2. Пользователи с корзинами (10 документов)
// =====================================================
db.users.insertMany([
  {
    _id: ObjectId("100000000000000000000001"),
    username: "ivan_88",
    email: "ivan@mail.ru",
    first_name: "Иван",
    last_name: "Петров",
    hashed_password: "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VTtYrTe3mGjYzS",
    created_at: ISODate("2024-01-15T10:30:00Z"),
    is_active: true,
    cart: [
      {
        product_id: ObjectId("000000000000000000000001"),
        product_name: "iPhone 15 Pro",
        quantity: 1,
        price: 999.99,
        added_at: ISODate("2024-02-01T10:00:00Z")
      },
      {
        product_id: ObjectId("000000000000000000000005"),
        product_name: "Nike Air Max",
        quantity: 2,
        price: 129.99,
        added_at: ISODate("2024-02-01T10:05:00Z")
      },
      {
        product_id: ObjectId("000000000000000000000010"),
        product_name: "The Hobbit",
        quantity: 1,
        price: 19.99,
        added_at: ISODate("2024-02-01T10:10:00Z")
      }
    ]
  },
  {
    _id: ObjectId("100000000000000000000002"),
    username: "maria_s",
    email: "maria@yandex.ru",
    first_name: "Мария",
    last_name: "Сидорова",
    hashed_password: "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VTtYrTe3mGjYzS",
    created_at: ISODate("2024-01-20T14:20:00Z"),
    is_active: true,
    cart: [
      {
        product_id: ObjectId("000000000000000000000009"),
        product_name: "Python Programming",
        quantity: 1,
        price: 49.99,
        added_at: ISODate("2024-02-02T11:00:00Z")
      },
      {
        product_id: ObjectId("000000000000000000000012"),
        product_name: "IKEA Floor Lamp",
        quantity: 1,
        price: 59.99,
        added_at: ISODate("2024-02-02T11:15:00Z")
      }
    ]
  },
  {
    _id: ObjectId("100000000000000000000003"),
    username: "alex_k",
    email: "alex@google.com",
    first_name: "Алексей",
    last_name: "Кузнецов",
    hashed_password: "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VTtYrTe3mGjYzS",
    created_at: ISODate("2024-02-01T09:15:00Z"),
    is_active: true,
    cart: [
      {
        product_id: ObjectId("000000000000000000000002"),
        product_name: "Samsung TV 55\"",
        quantity: 1,
        price: 699.99,
        added_at: ISODate("2024-02-03T09:00:00Z")
      },
      {
        product_id: ObjectId("000000000000000000000006"),
        product_name: "Adidas Hoodie",
        quantity: 1,
        price: 89.99,
        added_at: ISODate("2024-02-03T09:20:00Z")
      }
    ]
  },
  {
    _id: ObjectId("100000000000000000000004"),
    username: "olga_n",
    email: "olga@mail.ru",
    first_name: "Ольга",
    last_name: "Новикова",
    hashed_password: "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VTtYrTe3mGjYzS",
    created_at: ISODate("2024-02-10T16:45:00Z"),
    is_active: false,
    cart: [
      {
        product_id: ObjectId("000000000000000000000014"),
        product_name: "Yoga Mat",
        quantity: 2,
        price: 25.99,
        added_at: ISODate("2024-02-04T14:00:00Z")
      },
      {
        product_id: ObjectId("000000000000000000000015"),
        product_name: "Dumbbell Set 20kg",
        quantity: 1,
        price: 89.99,
        added_at: ISODate("2024-02-04T14:05:00Z")
      }
    ]
  },
  {
    _id: ObjectId("100000000000000000000005"),
    username: "dmitry99",
    email: "dmitry@bk.ru",
    first_name: "Дмитрий",
    last_name: "Морозов",
    hashed_password: "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VTtYrTe3mGjYzS",
    created_at: ISODate("2024-03-05T11:20:00Z"),
    is_active: true,
    cart: [
      {
        product_id: ObjectId("000000000000000000000003"),
        product_name: "Sony WH-1000XM5",
        quantity: 1,
        price: 349.99,
        added_at: ISODate("2024-02-05T16:30:00Z")
      },
      {
        product_id: ObjectId("000000000000000000000008"),
        product_name: "The North Face Jacket",
        quantity: 1,
        price: 299.99,
        added_at: ISODate("2024-02-05T16:45:00Z")
      }
    ]
  },
  {
    _id: ObjectId("100000000000000000000006"),
    username: "ekaterina_p",
    email: "ekaterina@mail.ru",
    first_name: "Екатерина",
    last_name: "Павлова",
    hashed_password: "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VTtYrTe3mGjYzS",
    created_at: ISODate("2024-03-10T13:40:00Z"),
    is_active: true,
    cart: [
      {
        product_id: ObjectId("000000000000000000000004"),
        product_name: "MacBook Air M2",
        quantity: 1,
        price: 1199.99,
        added_at: ISODate("2024-02-06T12:00:00Z")
      },
      {
        product_id: ObjectId("000000000000000000000011"),
        product_name: "Clean Code",
        quantity: 1,
        price: 39.99,
        added_at: ISODate("2024-02-06T12:20:00Z")
      }
    ]
  },
  {
    _id: ObjectId("100000000000000000000007"),
    username: "sergey_n",
    email: "sergey@yandex.ru",
    first_name: "Сергей",
    last_name: "Николаев",
    hashed_password: "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VTtYrTe3mGjYzS",
    created_at: ISODate("2024-03-15T08:30:00Z"),
    is_active: true,
    cart: [
      {
        product_id: ObjectId("000000000000000000000007"),
        product_name: "Levis Jeans 501",
        quantity: 2,
        price: 79.99,
        added_at: ISODate("2024-02-07T08:30:00Z")
      },
      {
        product_id: ObjectId("000000000000000000000013"),
        product_name: "DeLonghi Coffee Maker",
        quantity: 1,
        price: 129.99,
        added_at: ISODate("2024-02-07T08:45:00Z")
      }
    ]
  },
  {
    _id: ObjectId("100000000000000000000008"),
    username: "anna_s",
    email: "anna@google.com",
    first_name: "Анна",
    last_name: "Соколова",
    hashed_password: "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VTtYrTe3mGjYzS",
    created_at: ISODate("2024-03-20T17:15:00Z"),
    is_active: true,
    cart: [
      {
        product_id: ObjectId("000000000000000000000005"),
        product_name: "Nike Air Max",
        quantity: 1,
        price: 129.99,
        added_at: ISODate("2024-02-08T19:00:00Z")
      },
      {
        product_id: ObjectId("000000000000000000000006"),
        product_name: "Adidas Hoodie",
        quantity: 1,
        price: 89.99,
        added_at: ISODate("2024-02-08T19:10:00Z")
      },
      {
        product_id: ObjectId("000000000000000000000007"),
        product_name: "Levis Jeans 501",
        quantity: 1,
        price: 79.99,
        added_at: ISODate("2024-02-08T19:15:00Z")
      }
    ]
  },
  {
    _id: ObjectId("100000000000000000000009"),
    username: "pavel_r",
    email: "pavel@bk.ru",
    first_name: "Павел",
    last_name: "Романов",
    hashed_password: "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VTtYrTe3mGjYzS",
    created_at: ISODate("2024-03-25T12:00:00Z"),
    is_active: true,
    cart: [
      {
        product_id: ObjectId("000000000000000000000001"),
        product_name: "iPhone 15 Pro",
        quantity: 1,
        price: 999.99,
        added_at: ISODate("2024-02-09T20:00:00Z")
      },
      {
        product_id: ObjectId("000000000000000000000014"),
        product_name: "Yoga Mat",
        quantity: 1,
        price: 25.99,
        added_at: ISODate("2024-02-09T20:30:00Z")
      }
    ]
  },
  {
    _id: ObjectId("100000000000000000000010"),
    username: "tatyana_l",
    email: "tatyana@mail.ru",
    first_name: "Татьяна",
    last_name: "Лебедева",
    hashed_password: "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VTtYrTe3mGjYzS",
    created_at: ISODate("2024-03-30T19:45:00Z"),
    is_active: true,
    cart: [
      {
        product_id: ObjectId("000000000000000000000002"),
        product_name: "Samsung TV 55\"",
        quantity: 1,
        price: 699.99,
        added_at: ISODate("2024-02-10T22:00:00Z")
      },
      {
        product_id: ObjectId("000000000000000000000003"),
        product_name: "Sony WH-1000XM5",
        quantity: 1,
        price: 349.99,
        added_at: ISODate("2024-02-10T22:15:00Z")
      }
    ]
  }
]);

// Проверка
print("Users count: " + db.users.count());
print("Products count: " + db.products.count());