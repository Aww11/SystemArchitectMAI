import json
from typing import Any, Dict
import aio_pika
from aio_pika import Message, Connection
import os

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")

rabbit_connection: Connection = None

async def get_rabbit_connection():
    global rabbit_connection
    if rabbit_connection is None or rabbit_connection.is_closed:
        rabbit_connection = await aio_pika.connect_robust(RABBITMQ_URL)
    return rabbit_connection

async def publish_event(event_name: str, payload: Dict[str, Any], routing_key: str = None):
    try:
        connection = await get_rabbit_connection()
        channel = await connection.channel()
        
        exchange = await channel.declare_exchange(
            "store_events",
            aio_pika.ExchangeType.TOPIC,
            durable=True
        )
        
        event = {
            "event_name": event_name,
            "payload": payload,
            "timestamp": None
        }
        import datetime
        event["timestamp"] = datetime.datetime.utcnow().isoformat()
        
        message_body = json.dumps(event, default=str).encode()
        message = Message(message_body, delivery_mode=aio_pika.DeliveryMode.PERSISTENT)
        
        if routing_key is None:
            routing_key = event_name
        
        await exchange.publish(message, routing_key=routing_key)
        print(f"Event published: {event_name}")
        
    except Exception as e:
        print(f"Failed to publish event {event_name}: {e}")