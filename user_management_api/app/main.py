"""
Main FastAPI application for User Management API
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.models import (
    User, UserCreate, UserUpdate, UserList, 
    ErrorResponse, SuccessResponse
)
from app.services import UserService
from app.exceptions import (
    UserNotFoundError, UserAlreadyExistsError, 
    InvalidUserDataError, DatabaseError
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting User Management API...")
    yield
    # Shutdown
    logger.info("Shutting down User Management API...")


# Create FastAPI app
app = FastAPI(
    title="User Management API",
    description="A RESTful API for managing user information with FastAPI and Pydantic",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handlers
@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(request, exc):
    """Handle user not found errors"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error="User not found",
            detail=exc.detail,
            status_code=exc.status_code
        ).model_dump()
    )


@app.exception_handler(UserAlreadyExistsError)
async def user_already_exists_handler(request, exc):
    """Handle user already exists errors"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error="User already exists",
            detail=exc.detail,
            status_code=exc.status_code
        ).model_dump()
    )


@app.exception_handler(InvalidUserDataError)
async def invalid_user_data_handler(request, exc):
    """Handle invalid user data errors"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error="Invalid user data",
            detail=exc.detail,
            status_code=exc.status_code
        ).model_dump()
    )


@app.exception_handler(DatabaseError)
async def database_error_handler(request, exc):
    """Handle database errors"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error="Database error",
            detail=exc.detail,
            status_code=exc.status_code
        ).model_dump()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="Internal server error",
            detail="An unexpected error occurred",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ).model_dump()
    )


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "User Management API"}


# User CRUD endpoints
@app.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED, tags=["Users"])
async def create_user(user_data: UserCreate):
    """
    Create a new user
    
    - **name**: User's full name (required)
    - **email**: User's email address (required, must be unique)
    - **age**: User's age (optional, must be positive)
    """
    try:
        user = UserService.create_user(user_data)
        logger.info(f"Created user with ID: {user.id}")
        return user
    except Exception as e:
        logger.error(f"Failed to create user: {e}")
        raise


@app.get("/users/{user_id}", response_model=User, tags=["Users"])
async def get_user(user_id: int):
    """
    Retrieve a specific user by ID
    
    - **user_id**: The unique identifier of the user
    """
    try:
        user = UserService.get_user(user_id)
        return user
    except Exception as e:
        logger.error(f"Failed to get user {user_id}: {e}")
        raise


@app.get("/users/", response_model=UserList, tags=["Users"])
async def get_users(
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of users to return")
):
    """
    Retrieve all users with pagination
    
    - **skip**: Number of users to skip (for pagination)
    - **limit**: Maximum number of users to return (max 1000)
    """
    try:
        users = UserService.get_users(skip, limit)
        return users
    except Exception as e:
        logger.error(f"Failed to get users: {e}")
        raise


@app.put("/users/{user_id}", response_model=User, tags=["Users"])
async def update_user(user_id: int, user_data: UserUpdate):
    """
    Update an existing user
    
    - **user_id**: The unique identifier of the user to update
    - **user_data**: User data to update (all fields optional)
    """
    try:
        user = UserService.update_user(user_id, user_data)
        logger.info(f"Updated user with ID: {user_id}")
        return user
    except Exception as e:
        logger.error(f"Failed to update user {user_id}: {e}")
        raise


@app.delete("/users/{user_id}", response_model=SuccessResponse, tags=["Users"])
async def delete_user(user_id: int):
    """
    Delete a user by ID
    
    - **user_id**: The unique identifier of the user to delete
    """
    try:
        success = UserService.delete_user(user_id)
        if success:
            logger.info(f"Deleted user with ID: {user_id}")
            return SuccessResponse(
                message=f"User with ID {user_id} deleted successfully",
                data={"user_id": user_id}
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete user"
            )
    except Exception as e:
        logger.error(f"Failed to delete user {user_id}: {e}")
        raise


# Bonus endpoints
@app.get("/users/search/", response_model=UserList, tags=["Search"])
async def search_users(
    q: str = Query("", min_length=0, description="Search query for name or email"),
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of users to return")
):
    """
    Search users by name or email
    
    - **q**: Search query (empty string returns all users)
    - **skip**: Number of users to skip (for pagination)
    - **limit**: Maximum number of users to return (max 1000)
    """
    try:
        users = UserService.search_users(q, skip, limit)
        return users
    except Exception as e:
        logger.error(f"Failed to search users: {e}")
        raise


@app.get("/users/stats/", tags=["Statistics"])
async def get_user_stats():
    """
    Get user statistics including total count, average age, and distributions
    """
    try:
        stats = UserService.get_user_stats()
        return stats
    except Exception as e:
        logger.error(f"Failed to get user stats: {e}")
        raise


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "User Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
