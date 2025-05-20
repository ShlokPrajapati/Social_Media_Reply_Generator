"""
Pydantic models for request and response validation.
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone

from app.config import SUPPORTED_PLATFORMS


class ReplyRequest(BaseModel):
    """Request model for generating social media replies."""
    platform: str = Field(
        ..., 
        description="Social media platform (e.g., twitter, linkedin)"
    )
    post_text: str = Field(
        ..., 
        description="The text of the social media post",
        min_length=3
    )
    context: Optional[str] = Field(
        None, 
        description="Optional additional context about the post"
    )
    include_analysis: Optional[bool] = Field(
        False, 
        description="Whether to include post analysis in the response"
    )
    
    @field_validator("platform")
    def validate_platform(cls, v):
        """Validate that the platform is supported."""
        if v.lower() not in SUPPORTED_PLATFORMS:
            raise ValueError(f"Platform must be one of: {', '.join(SUPPORTED_PLATFORMS)}")
        return v.lower()


class PostAnalysis(BaseModel):
    """Model for post analysis data."""
    intent: str = Field(..., description="Detected intent of the post")
    sentiment: str = Field(..., description="Detected sentiment of the post")
    topics: List[str] = Field(..., description="Key topics detected in the post")
    response_type: str = Field(..., description="Recommended type of response")


class ReplyResponse(BaseModel):
    """Response model for generated replies."""
    reply_text: str = Field(..., description="Generated reply text")
    platform: str = Field(..., description="Platform the reply is for")
    post_text: str = Field(..., description="Original post text")
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    analysis: Optional[PostAnalysis] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        """Configuration for the model."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }