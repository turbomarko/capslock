from typing import List, Optional
from pydantic import BaseModel, Field

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
