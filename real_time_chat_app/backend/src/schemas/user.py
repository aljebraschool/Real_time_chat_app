from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    """Base user schema with common fields"""
    username: str
    email: EmailStr
    full_name: Optional[str] = None

    
class UserResponse(UserBase):
    """Schema for user response (without sensitive data)"""
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True  # Allows conversion from ORM models


class UserUpdate(BaseModel):
    """Schema for updating user profile"""
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None