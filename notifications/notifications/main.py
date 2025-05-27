import asyncio
import logging
from fastapi import FastAPI

from .services.settings import Settings
from .services.email import EmailService
from .services.rabbitmq import RabbitMQService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app and services
app = FastAPI(title="Notifications Service")
settings = Settings()
email_service = EmailService(settings)
rabbitmq_service = RabbitMQService(settings, email_service)

@app.on_event("startup")
async def startup():
    """Initialize services on startup."""
    await rabbitmq_service.connect()
    asyncio.create_task(rabbitmq_service.start_consuming())

@app.on_event("shutdown")
async def shutdown():
    """Cleanup on shutdown."""
    await rabbitmq_service.close()

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
