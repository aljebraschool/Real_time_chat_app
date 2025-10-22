from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserRegister(BaseModel):
    """Schema for user registration"""
    username : str = Field(..., min_length=3, max_length=50)
    email : EmailStr
    password : str = Field(..., min_length=8, max_length=100)
    full_name : Optional[str] = Field(None, max_length=100)

class UserLogin(BaseModel):
    """Schema for user login"""
    username : str
    password : str

class TokenResponse(BaseModel):
    """Schema for token response"""
    access_token : str
    refresh_token : str
    token_type : str = "bearer"

class TokenRefresh(BaseModel):
    """Schema for refreshing access token"""
    refresh_token: str


class PasswordReset(BaseModel):
    """Schema for password reset request"""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Schema for confirming password reset"""
    token: str
    new_password: str = Field(..., min_length=8, max_length=100)


class ChangePassword(BaseModel):
    """Schema for changing password"""
    old_password: str
    new_password: str = Field(..., min_length=8, max_length=100)
