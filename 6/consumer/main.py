import json
import asyncio
import aio_pika
from aio_pika import IncomingMessage
import os

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")

async def process_event(message: IncomingMessage):
    async with message.process():
        try:
            body = json.loads(message.body.decode())
            event_name = body.get("event_name")
            payload = body.get("payload")
            timestamp = body.get("timestamp")
            
            print(f"    Received event: {event_name}")
            print(f"    Payload: {payload}")
            print(f"    Timestamp: {timestamp}")
            
            if event_name == "user.registered":
                print(f"    -> Новый пользователь зарегистрирован: {payload.get('username')}")
                
            elif event_name == "user.logged_in":
                print(f"    -> Пользователь {payload.get('username')} вошёл в систему")
                
            elif event_name == "product.created":
                print(f"    -> Новый товар: {payload.get('name')}")
                
            elif event_name == "product.updated":
                print(f"    -> Товар {payload.get('product_id')} обновлён")
                
            elif event_name == "product.deleted":
                print(f"    -> Товар {payload.get('product_id')} удалён")
                
            elif event_name == "cart.item_added":
                print(f"    -> Пользователь {payload.get('user_id')} добавил {payload.get('quantity')} x {payload.get('product_name')}")
                
            elif event_name == "cart.item_removed":
                print(f"    -> Пользователь {payload.get('user_id')} удалил товар {payload.get('product_id')}")
                
            elif event_name == "cart.cleared":
                print(f"    -> Пользователь {payload.get('user_id')} очистил корзину")
                
        except Exception as e:
            print(f"Error processing event: {e}")

async def main():
    print("Starting Analytics Consumer...")
    
    while True:
        try:
            print("Attempting to connect to RabbitMQ...")
            connection = await aio_pika.connect_robust(RABBITMQ_URL)
            print("Connected to RabbitMQ!")
            
            channel = await connection.channel()
            
            exchange = await channel.declare_exchange(
                "store_events",
                aio_pika.ExchangeType.TOPIC,
                durable=True
            )
            
            queue = await channel.declare_queue("analytics_queue", durable=True)
            
            await queue.bind(exchange, routing_key="#")
            
            print("Waiting for events. To exit press CTRL+C")
            
            await queue.consume(process_event)
            
            try:
                await asyncio.Future()
            finally:
                await connection.close()
                
        except Exception as e:
            print(f"Connection failed: {e}. Retrying in 5 seconds...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())