from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class MessageCreate(BaseModel):
    """Schema for creating a new message"""
    recipient_id: int = Field(..., description="ID of the user to send message to")
    content: str = Field(..., min_length=1, max_length=5000)


class MessageResponse(BaseModel):
    """Schema for message response"""
    id: int
    chat_room_id: int
    sender_id: Optional[int]
    content: str
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class MessageWithSender(MessageResponse):
    """Schema for message with sender information"""
    sender_username: Optional[str] = None
    sender_full_name: Optional[str] = None