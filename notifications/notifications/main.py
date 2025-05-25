import asyncio
import json
import logging
from typing import Any

import aio_pika
from aio_pika.abc import AbstractConnection, AbstractChannel
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from pydantic_settings import BaseSettings
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # RabbitMQ settings
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_QUEUE: str

    # Email settings
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_FROM: str

    # API settings
    API_HOST: str
    API_PORT: int
    DEBUG: bool = False

    class Config:
        env_file = ".envs/.local/.notifications"

class NotificationMessage(BaseModel):
    to_email: EmailStr
    subject: str
    body: str

class NotificationService:
    def __init__(self, settings: Settings):
        self.settings = settings
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

    async def send_email(self, message: NotificationMessage):
        """Send an email using the configured SMTP server."""
        msg = MIMEMultipart()
        msg["From"] = self.settings.EMAIL_FROM
        msg["To"] = message.to_email
        msg["Subject"] = message.subject

        msg.attach(MIMEText(message.body, "plain"))

        try:
            async with aiosmtplib.SMTP(
                hostname=self.settings.SMTP_HOST,
                port=self.settings.SMTP_PORT,
                use_tls=False,
            ) as smtp:
                if self.settings.SMTP_USER and self.settings.SMTP_PASSWORD:
                    await smtp.login(self.settings.SMTP_USER, self.settings.SMTP_PASSWORD)
                await smtp.send_message(msg)
                logger.info(f"Email sent to {message.to_email}")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            raise HTTPException(status_code=500, detail="Failed to send email")

    async def process_message(self, message: aio_pika.IncomingMessage):
        """Process incoming RabbitMQ message."""
        async with message.process():
            try:
                data = json.loads(message.body.decode())
                notification = NotificationMessage(**data)
                await self.send_email(notification)
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

# Initialize FastAPI app and settings
app = FastAPI(title="Notifications Service")
settings = Settings()
notification_service = NotificationService(settings)

@app.on_event("startup")
async def startup():
    """Initialize services on startup."""
    await notification_service.connect()
    asyncio.create_task(notification_service.start_consuming())

@app.on_event("shutdown")
async def shutdown():
    """Cleanup on shutdown."""
    await notification_service.close()

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
