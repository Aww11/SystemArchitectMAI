db.createCollection("users_validated", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["username", "email", "first_name", "last_name", "hashed_password"],
      properties: {
        username: {
          bsonType: "string",
          description: "Логин должен быть строкой и обязателен",
          minLength: 3,
          maxLength: 50
        },
        email: {
          bsonType: "string",
          description: "Email должен быть строкой и обязателен",
          pattern: "^[^@\\s]+@([^@\\s]+\\.)+[^@\\s]+$"
        },
        first_name: {
          bsonType: "string",
          description: "Имя должно быть строкой и обязателено",
          minLength: 1,
          maxLength: 50
        },
        last_name: {
          bsonType: "string",
          description: "Фамилия должна быть строкой и обязателена",
          minLength: 1,
          maxLength: 50
        },
        hashed_password: {
          bsonType: "string",
          description: "Пароль должен быть строкой и обязателен",
          minLength: 8
        },
        created_at: {
          bsonType: "date",
          description: "Дата создания должна быть датой"
        },
        is_active: {
          bsonType: "bool",
          description: "Статус активности должен быть булевым"
        },
        cart: {
          bsonType: "array",
          description: "Корзина должна быть массивом",
          items: {
            bsonType: "object",
            required: ["product_id", "product_name", "quantity", "price"],
            properties: {
              product_id: {
                bsonType: "objectId",
                description: "ID товара должен быть ObjectId"
              },
              product_name: {
                bsonType: "string",
                description: "Название товара должно быть строкой",
                minLength: 1
              },
              quantity: {
                bsonType: "int",
                description: "Количество должно быть целым положительным числом",
                minimum: 1
              },
              price: {
                bsonType: "double",
                description: "Цена должна быть положительным числом",
                minimum: 0
              },
              added_at: {
                bsonType: "date",
                description: "Дата добавления должна быть датой"
              }
            }
          }
        }
      }
    }
  },
  validationLevel: "strict",
  validationAction: "error"
});

print("=== Тестирование валидации ===");

try {
  db.users_validated.insertOne({
    username: "valid_user",
    email: "valid@example.com",
    first_name: "Валидный",
    last_name: "Пользователь",
    hashed_password: "secure_password_123",
    created_at: new Date(),
    is_active: true,
    cart: [
      {
        product_id: ObjectId("000000000000000000000001"),
        product_name: "Test Product",
        quantity: NumberInt(2),
        price: 99.99,
        added_at: new Date()
      }
    ]
  });
  print("Валидный документ вставлен успешно");
} catch (e) {
  print("Ошибка: " + e);
}

try {
  db.users_validated.insertOne({
    email: "no_username@example.com",
    first_name: "Тест",
    last_name: "Тестов",
    hashed_password: "password123"
  });
  print("Ошибка: документ без username не должен был вставиться");
} catch (e) {
  print("Валидация сработала: " + e.message);
}

try {
  db.users_validated.insertOne({
    username: "bad_email_user",
    email: "not-an-email",
    first_name: "Тест",
    last_name: "Тестов",
    hashed_password: "password123"
  });
  print("Ошибка: неверный email не должен был вставиться");
} catch (e) {
  print("Валидация email сработала: " + e.message);
}

try {
  db.users_validated.insertOne({
    username: "bad_quantity",
    email: "valid@example.com",
    first_name: "Тест",
    last_name: "Тестов",
    hashed_password: "password123",
    cart: [
      {
        product_id: ObjectId("000000000000000000000001"),
        product_name: "Test",
        quantity: NumberInt(-5),
        price: 99.99
      }
    ]
  });
  print("Ошибка: отрицательное количество не должно было вставиться");
} catch (e) {
  print("алидация quantity сработала: " + e.message);
}

try {
  db.users_validated.insertOne({
    username: "short_pass",
    email: "valid@example.com",
    first_name: "Тест",
    last_name: "Тестов",
    hashed_password: "short"
  });
  print("Ошибка: короткий пароль не должен был вставиться");
} catch (e) {
  print("Валидация длины пароля сработала: " + e.message);
}