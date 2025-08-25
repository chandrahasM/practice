"""
Custom exceptions for User Management API
"""
from fastapi import HTTPException, status


class UserNotFoundError(HTTPException):
    """Exception raised when a user is not found"""
    def __init__(self, user_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )


class UserAlreadyExistsError(HTTPException):
    """Exception raised when trying to create a user with existing email"""
    def __init__(self, email: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email {email} already exists"
        )


class InvalidUserDataError(HTTPException):
    """Exception raised when user data is invalid"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )


class DatabaseError(HTTPException):
    """Exception raised when database operations fail"""
    def __init__(self, detail: str = "Database operation failed"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )
