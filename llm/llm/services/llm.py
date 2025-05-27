import logging
import time
import asyncio
import httpx
from fastapi import HTTPException

from .settings import Settings
from .models import ChatRequest, ChatResponse

logger = logging.getLogger(__name__)

class TokenBucket:
    def __init__(self, rate: float, capacity: int):
        self.rate = rate  # tokens per second
        self.capacity = capacity  # maximum tokens
        self.tokens = capacity  # current tokens
        self.last_update = time.time()
        self._lock = asyncio.Lock()

    async def acquire(self) -> bool:
        async with self._lock:
            now = time.time()
            # Add new tokens based on time passed
            time_passed = now - self.last_update
            new_tokens = time_passed * self.rate
            self.tokens = min(self.capacity, self.tokens + new_tokens)
            self.last_update = now

            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False

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
        # Initialize rate limiter
        requests_per_second = settings.RATE_LIMIT_REQUESTS_PER_MINUTE / 60
        self.rate_limiter = TokenBucket(
            rate=requests_per_second,
            capacity=settings.RATE_LIMIT_BURST_SIZE
        )

    async def generate_response(self, request: ChatRequest) -> ChatResponse:
        """Generate a response using OpenRouter API."""
        # Check rate limit
        if not await self.rate_limiter.acquire():
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again later."
            )

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
