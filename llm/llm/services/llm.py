import logging
import httpx
from fastapi import HTTPException

from .settings import Settings
from .models import ChatRequest, ChatResponse

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = httpx.AsyncClient(
            base_url=settings.OPENROUTER_BASE_URL,
            headers={
                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                "HTTP-Referer": "http://localhost:8000",  # Required by OpenRouter
                "X-Title": "Capslock LLM Service",  # Optional, but helpful for OpenRouter
            },
            timeout=30.0,
        )

    async def generate_response(self, request: ChatRequest) -> ChatResponse:
        """Generate a response using OpenRouter API."""
        try:
            response = await self.client.post(
                "/chat/completions",
                json={
                    "model": self.settings.MODEL,
                    "messages": [msg.dict() for msg in request.messages],
                    "temperature": request.temperature,
                    "max_tokens": request.max_tokens,
                    "stream": request.stream,
                },
            )
            logger.info(f"Response: {response}")
            response.raise_for_status()
            data = response.json()
            
            return ChatResponse(
                response=data["choices"][0]["message"]["content"],
                model=data["model"],
            )
        except httpx.HTTPError as e:
            logger.error(f"OpenRouter API error: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Error communicating with OpenRouter API: {str(e)}",
            )
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error: {str(e)}",
            )

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
