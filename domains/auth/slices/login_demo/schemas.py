"""
Login Demo Schemas
"""
from pydantic import BaseModel, EmailStr, Field
from shared.entities import User


class LoginRequest(BaseModel):
    """
    Login request schema.

    Attributes:
        email: User email address
        password: Plain text password
    """
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=1, description="User password")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "demo@vibecodiq.com",
                "password": "demo123"
            }
        }


class LoginResponse(BaseModel):
    """
    Login response schema.

    Attributes:
        access_token: JWT access token
        token_type: Token type (always "bearer")
        user: User information
    """
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    user: User = Field(..., description="User information")

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "mock_jwt_token_demo@vibecodiq.com_1234567890",
                "token_type": "bearer",
                "user": {
                    "id": 1,
                    "email": "demo@vibecodiq.com",
                    "name": "Demo User",
                    "is_active": True
                }
            }
        }
