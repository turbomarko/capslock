import logging
from typing import List, Optional

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # API settings
    API_HOST: str
    API_PORT: int
    DEBUG: bool = False

    # OpenRouter settings
    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str
    MODEL: str

    class Config:
        env_file = ".envs/.local/.llm"

class Message(BaseModel):
    role: str = Field(..., description="The role of the message sender (system, user, or assistant)")
    content: str = Field(..., description="The content of the message")

class ChatRequest(BaseModel):
    messages: List[Message] = Field(..., description="List of messages in the conversation")
    temperature: Optional[float] = Field(0.7, description="Sampling temperature between 0 and 2")
    max_tokens: Optional[int] = Field(None, description="Maximum number of tokens to generate")
    stream: Optional[bool] = Field(False, description="Whether to stream the response")

class ChatResponse(BaseModel):
    response: str = Field(..., description="The generated response")
    model: str = Field(..., description="The model used for generation")

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

# Initialize FastAPI app and settings
app = FastAPI(title="LLM Service")
settings = Settings()
llm_service = LLMService(settings)

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Generate a chat completion using OpenRouter."""
    return await llm_service.generate_response(request)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.on_event("shutdown")
async def shutdown():
    """Cleanup on shutdown."""
    await llm_service.close()
