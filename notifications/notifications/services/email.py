import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import aiosmtplib
from fastapi import HTTPException
from pydantic import EmailStr

from .settings import Settings

logger = logging.getLogger(__name__)

class NotificationMessage:
    def __init__(self, to_email: EmailStr, subject: str, body: str):
        self.to_email = to_email
        self.subject = subject
        self.body = body

class EmailService:
    def __init__(self, settings: Settings):
        self.settings = settings

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
