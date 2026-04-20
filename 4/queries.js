db.users.insertOne({
  username: "new_user",
  email: "new@example.com",
  first_name: "Новый",
  last_name: "Пользователь",
  hashed_password: "hashed_password_here",
  created_at: new Date(),
  is_active: true,
  cart: []
});

db.products.insertOne({
  name: "Новый смартфон",
  description: "Мощный смартфон с отличной камерой",
  price: 599.99,
  stock: 100,
  category: "Electronics",
  created_at: new Date()
});

db.users.find({ username: { $eq: "ivan_88" } });

db.users.find({ first_name: { $regex: "^Иван", $options: "i" } });

db.users.find({ last_name: { $regex: "^Пет", $options: "i" } });

db.users.find({
  $and: [
    { first_name: { $regex: "^Иван", $options: "i" } },
    { last_name: { $regex: "^Пет", $options: "i" } }
  ]
});

db.products.find({});

db.products.find({ category: "Electronics" });

db.products.find({ price: { $gt: 500 } });

db.products.find({ price: { $gte: 50, $lte: 200 } });

db.products.find({ category: { $in: ["Electronics", "Books"] } });

db.users.find({ is_active: true });

db.users.find(
  { username: "ivan_88" },
  { username: 1, cart: 1, _id: 0 }
);

db.users.find({ cart: { $ne: [] } });

db.products.find({ stock: { $lt: 30 } });

db.users.updateOne(
  { username: "new_user" },
  {
    $push: {
      cart: {
        product_id: ObjectId("000000000000000000000001"),
        product_name: "iPhone 15 Pro",
        quantity: 1,
        price: 999.99,
        added_at: new Date()
      }
    }
  }
);

db.users.updateOne(
  { username: "new_user", "cart.product_id": ObjectId("000000000000000000000001") },
  { $inc: { "cart.$.quantity": 1 } }
);

db.products.updateOne(
  { name: "iPhone 15 Pro" },
  { $set: { price: 899.99 } }
);

db.products.updateOne(
  { name: "iPhone 15 Pro" },
  { $set: { stock: 45 } }
);

db.users.updateOne(
  { username: "new_user" },
  { $set: { first_name: "Измененный", last_name: "Имя" } }
);

db.users.updateOne(
  { username: "new_user" },
  { $pull: { cart: { product_id: ObjectId("000000000000000000000001") } } }
);

db.users.updateOne(
  { username: "new_user" },
  { $set: { cart: [] } }
);

db.users.updateOne(
  { username: "new_user", "cart.product_id": ObjectId("000000000000000000000005") },
  { $inc: { "cart.$.quantity": 2 } }
);

db.users.updateOne(
  { username: "new_user" },
  { $set: { cart_updated_at: new Date() } }
);

db.products.updateMany(
  { category: "Electronics" },
  { $mul: { price: 0.9 } }
);

db.users.updateOne(
  { username: "ivan_88" },
  { $pull: { cart: { product_id: ObjectId("000000000000000000000010") } } }
);

db.users.deleteOne({ username: "new_user" });

db.products.deleteOne({ name: "Dumbbell Set 20kg" });

db.users.deleteMany({ is_active: false });

db.users.aggregate([
  { $match: { username: "ivan_88" } },
  { $unwind: "$cart" },
  {
    $group: {
      _id: "$username",
      total: { $sum: { $multiply: ["$cart.quantity", "$cart.price"] } }
    }
  }
]);

db.users.aggregate([
  { $match: { cart: { $ne: [] } } },
  { $unwind: "$cart" },
  {
    $group: {
      _id: "$_id",
      username: { $first: "$username" },
      total: { $sum: { $multiply: ["$cart.quantity", "$cart.price"] } }
    }
  },
  { $match: { total: { $gt: 1000 } } },
  { $sort: { total: -1 } }
]);

db.users.aggregate([
  { $unwind: "$cart" },
  {
    $group: {
      _id: "$cart.product_id",
      name: { $first: "$cart.product_name" },
      total_quantity: { $sum: "$cart.quantity" },
      users_count: { $addToSet: "$_id" }
    }
  },
  {
    $project: {
      name: 1,
      total_quantity: 1,
      users_count: { $size: "$users_count" }
    }
  },
  { $sort: { total_quantity: -1 } },
  { $limit: 5 }
]);

db.users.aggregate([
  { $unwind: "$cart" },
  {
    $lookup: {
      from: "products",
      localField: "cart.product_id",
      foreignField: "_id",
      as: "product_info"
    }
  },
  { $unwind: "$product_info" },
  {
    $group: {
      _id: "$product_info.category",
      total_items: { $sum: "$cart.quantity" },
      total_value: { $sum: { $multiply: ["$cart.quantity", "$cart.price"] } }
    }
  },
  { $sort: { total_value: -1 } }
]);

db.users.find(
  { "cart.product_id": ObjectId("000000000000000000000001") },
  { username: 1, first_name: 1, last_name: 1, _id: 0 }
);