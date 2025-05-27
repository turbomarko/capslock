import json
import logging
from typing import Any

import aio_pika
from aio_pika.abc import AbstractConnection, AbstractChannel
from aio_pika import IncomingMessage

from .settings import Settings
from .email import EmailService, NotificationMessage

logger = logging.getLogger(__name__)

class RabbitMQService:
    def __init__(self, settings: Settings, email_service: EmailService):
        self.settings = settings
        self.email_service = email_service
        self.connection: AbstractConnection | None = None
        self.channel: AbstractChannel | None = None

    async def connect(self):
        """Connect to RabbitMQ."""
        self.connection = await aio_pika.connect_robust(
            f"amqp://{self.settings.RABBITMQ_USER}:{self.settings.RABBITMQ_PASSWORD}@"
            f"{self.settings.RABBITMQ_HOST}:{self.settings.RABBITMQ_PORT}/"
        )
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=10)

    async def process_message(self, message: IncomingMessage):
        """Process incoming RabbitMQ message."""
        async with message.process():
            try:
                data = json.loads(message.body.decode())
                notification = NotificationMessage(**data)
                await self.email_service.send_email(notification)
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                # In a production environment, you might want to implement a dead letter queue
                raise

    async def start_consuming(self):
        """Start consuming messages from RabbitMQ."""
        queue = await self.channel.declare_queue(
            self.settings.RABBITMQ_QUEUE,
            durable=True
        )
        await queue.consume(self.process_message)
        logger.info(f"Started consuming from queue: {self.settings.RABBITMQ_QUEUE}")

    async def close(self):
        """Close RabbitMQ connection."""
        if self.connection:
            await self.connection.close()
