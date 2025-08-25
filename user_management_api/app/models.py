"""
Pydantic models for User Management API
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict


class UserBase(BaseModel):
    """Base user model with common fields"""
    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    email: EmailStr = Field(..., description="User's email address")
    age: Optional[int] = Field(None, gt=0, le=150, description="User's age (optional)")


class UserCreate(UserBase):
    """Model for creating a new user (input validation)"""
    pass


class UserUpdate(BaseModel):
    """Model for updating user information (all fields optional)"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, gt=0, le=150)


class User(UserBase):
    """Complete user model with auto-generated fields (response model)"""
    id: int = Field(..., description="Unique user identifier")
    created_at: datetime = Field(..., description="User creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )


class UserList(BaseModel):
    """Model for paginated user list response"""
    users: list[User] = Field(..., description="List of users")
    total: int = Field(..., description="Total number of users")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Page size")
    has_next: bool = Field(..., description="Whether there are more pages")


class ErrorResponse(BaseModel):
    """Standard error response model"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional error details")
    status_code: int = Field(..., description="HTTP status code")


class SuccessResponse(BaseModel):
    """Standard success response model"""
    message: str = Field(..., description="Success message")
    data: Optional[dict] = Field(None, description="Response data")
