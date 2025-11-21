"""
Shared User Entity

This module defines the User entity used across all slices.
In MVP 0.9, this is a simple Pydantic model.
In production, this would be a SQLAlchemy model with database mapping.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class User(BaseModel):
    """
    Shared User entity.

    Used by slices that need user information.
    This is a read-only representation (no password).

    Attributes:
        id: Unique user identifier
        email: User's email address (validated)
        name: User's display name
        is_active: Whether user account is active
        created_at: When user was created (optional for MVP)
    """
    id: int = Field(..., description="Unique user ID", gt=0)
    email: EmailStr = Field(..., description="User email address")
    name: str = Field(..., description="User display name", min_length=1, max_length=100)
    is_active: bool = Field(default=True, description="Account active status")
    created_at: Optional[datetime] = Field(default=None, description="Account creation timestamp")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "demo@vibecodiq.com",
                "name": "Demo User",
                "is_active": True,
                "created_at": "2025-11-20T12:00:00Z"
            }
        }


class UserInDB(User):
    """
    User model with password hash.

    This extends User with sensitive fields that should never be exposed via API.
    Used internally by authentication slices.

    Attributes:
        password_hash: Hashed password (never send to client!)
    """
    password_hash: str = Field(..., description="Hashed password (internal only)")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "demo@vibecodiq.com",
                "name": "Demo User",
                "is_active": True,
                "password_hash": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
            }
        }


class UserCreate(BaseModel):
    """
    Schema for creating new users.

    Used by registration slices.
    """
    email: EmailStr = Field(..., description="User email")
    name: str = Field(..., min_length=1, max_length=100, description="User name")
    password: str = Field(..., min_length=8, max_length=100, description="Plain password")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "newuser@vibecodiq.com",
                "name": "New User",
                "password": "securepassword123"
            }
        }


class UserUpdate(BaseModel):
    """
    Schema for updating user information.

    All fields are optional.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Updated Name",
                "email": "newemail@vibecodiq.com"
            }
        }
