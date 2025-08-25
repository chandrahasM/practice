"""
Main FastAPI application for User Management API
"""
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any
import json
import os
import asyncio
import time
import logging
from datetime import datetime, timedelta
from collections import defaultdict
from app.models import User, UserCreate
from pydantic import BaseModel, Field

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="User Management API",
    description="A production-ready API with rate limiting and logging",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create asyncio locks for thread-safe operations
users_lock = asyncio.Lock()  # Protects users_db operations
file_lock = asyncio.Lock()   # Protects file I/O operations
id_lock = asyncio.Lock()     # Protects ID generation

# Rate limiting storage
rate_limit_store = defaultdict(list)  # IP -> list of request timestamps
RATE_LIMIT_WINDOW = 60  # 1 minute window
MAX_REQUESTS_PER_WINDOW = 100  # Max requests per IP per minute

# Load existing users from sample_data.json and create output file
def load_users():
    try:
        with open("sample_data.json", "r") as f:
            data = json.load(f)
            users = data.get("users", [])
            # Add IDs to existing users
            for i, user in enumerate(users):
                user["id"] = i + 1
            
            # Save to output file
            output_data = {"users": users}
            with open("output_users.json", "w") as output_f:
                json.dump(output_data, output_f, indent=2)
            
            logger.info(f"Loaded {len(users)} users from sample_data.json")
            return users
    except FileNotFoundError:
        logger.warning("sample_data.json not found, starting with empty database")
        return []

# In-memory storage for users
users_db = load_users()
next_id = len(users_db) + 1

class UserUpdate(BaseModel):
    """Model for updating user with current values shown as examples"""
    name: Optional[str] = Field(
        None, 
        description="User's name",
        example="John Doe"
    )
    email: Optional[str] = Field(
        None, 
        description="User's email address",
        example="john.doe@example.com"
    )
    age: Optional[int] = Field(
        None, 
        description="User's age (must be positive)",
        example=30,
        ge=1
    )

# Rate limiting dependency
async def check_rate_limit(request: Request):
    """Check if request is within rate limits"""
    client_ip = request.client.host
    current_time = time.time()
    
    # Clean old timestamps outside the window
    rate_limit_store[client_ip] = [
        ts for ts in rate_limit_store[client_ip] 
        if current_time - ts < RATE_LIMIT_WINDOW
    ]
    
    # Check if limit exceeded
    if len(rate_limit_store[client_ip]) >= MAX_REQUESTS_PER_WINDOW:
        logger.warning(f"Rate limit exceeded for IP: {client_ip}")
        raise HTTPException(
            status_code=429, 
            detail=f"Rate limit exceeded. Maximum {MAX_REQUESTS_PER_WINDOW} requests per {RATE_LIMIT_WINDOW} seconds."
        )
    
    # Add current request timestamp
    rate_limit_store[client_ip].append(current_time)
    
    # Log request
    logger.info(f"Request from {client_ip}: {request.method} {request.url.path}")

# Logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests and responses"""
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url.path} from {request.client.host}")
    
    # Process request
    response = await call_next(request)
    
    # Log response
    process_time = time.time() - start_time
    logger.info(f"Response: {response.status_code} in {process_time:.3f}s")
    
    return response

@app.get("/")
async def read_root():
    """Root endpoint with API information"""
    logger.info("Root endpoint accessed")
    return {
        "message": "User Management API",
        "version": "1.0.0",
        "features": ["rate_limiting", "logging", "async_locks"],
        "docs": "/docs"
    }

@app.post("/users", response_model=User)
async def create_user(user: UserCreate, request: Request, rate_limit: None = Depends(check_rate_limit)):
    """Create a new user with rate limiting and logging"""
    start_time = time.time()
    
    try:
        global next_id
        
        # Use locks to ensure thread-safe operations
        async with users_lock:  # Protect users_db operations
            async with id_lock:  # Protect ID generation
                new_user = user.dict()
                new_user["id"] = next_id
                next_id += 1
                users_db.append(new_user)
            
            # Use file lock to prevent concurrent file writes
            async with file_lock:
                # Update output file with new user
                output_data = {"users": users_db}
                with open("output_users.json", "w") as f:
                    json.dump(output_data, f, indent=2)
        
        process_time = time.time() - start_time
        logger.info(f"User created successfully: ID={new_user['id']}, name={new_user['name']}, time={process_time:.3f}s")
        
        return new_user
        
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/users", response_model=List[User])
async def get_users(request: Request, rate_limit: None = Depends(check_rate_limit)):
    """Get all users with rate limiting and logging"""
    try:
        # Read operation - use lock to ensure consistent data
        async with users_lock:
            users = users_db.copy()  # Return a copy to prevent external modification
        
        logger.info(f"Retrieved {len(users)} users")
        return users
        
    except Exception as e:
        logger.error(f"Error retrieving users: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int, request: Request, rate_limit: None = Depends(check_rate_limit)):
    """Get a specific user by ID with rate limiting and logging"""
    try:
        async with users_lock:
            user = next((user for user in users_db if user["id"] == user_id), None)
            if user is None:
                logger.warning(f"User not found: ID={user_id}")
                raise HTTPException(status_code=404, detail="User not found")
            
            logger.info(f"User retrieved: ID={user_id}, name={user['name']}")
            return user
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.patch("/users/{user_id}", response_model=User)
async def update_user(
    user_id: int, 
    user_update: UserUpdate, 
    request: Request, 
    rate_limit: None = Depends(check_rate_limit)
):
    """
    Update user information (partial update) with rate limiting and logging
    
    Only the fields you provide will be updated. Other fields remain unchanged.
    """
    start_time = time.time()
    
    try:
        async with users_lock:
            # Find user by ID
            user_index = next((i for i, u in enumerate(users_db) if u["id"] == user_id), None)
            if user_index is None:
                logger.warning(f"User not found for update: ID={user_id}")
                raise HTTPException(status_code=404, detail="User not found")
            
            # Get existing user data
            existing_user = users_db[user_index]
            old_name = existing_user.get("name")
            
            # Update only the provided fields (partial update)
            update_data = user_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                existing_user[field] = value
            
            # Preserve the ID
            existing_user["id"] = user_id
            
            # Use file lock to prevent concurrent file writes
            async with file_lock:
                # Update output file
                output_data = {"users": users_db}
                with open("output_users.json", "w") as f:
                    json.dump(output_data, f, indent=2)
            
            process_time = time.time() - start_time
            logger.info(f"User updated: ID={user_id}, old_name={old_name}, new_name={existing_user.get('name')}, time={process_time:.3f}s")
            
            return existing_user
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.delete("/users/{user_id}")
async def delete_user(user_id: int, request: Request, rate_limit: None = Depends(check_rate_limit)):
    """Delete a user by ID with rate limiting and logging"""
    start_time = time.time()
    
    try:
        async with users_lock:
            # Find user by ID
            user_index = next((i for i, u in enumerate(users_db) if u["id"] == user_id), None)
            if user_index is None:
                logger.warning(f"User not found for deletion: ID={user_id}")
                raise HTTPException(status_code=404, detail="User not found")
            
            # Get user info before deletion for logging
            deleted_user = users_db[user_index]
            deleted_name = deleted_user.get("name")
            
            # Remove user
            users_db.pop(user_index)
            
            # Use file lock to prevent concurrent file writes
            async with file_lock:
                # Update output file
                output_data = {"users": users_db}
                with open("output_users.json", "w") as f:
                    json.dump(output_data, f, indent=2)
            
            process_time = time.time() - start_time
            logger.info(f"User deleted: ID={user_id}, name={deleted_name}, time={process_time:.3f}s")
            
            return {"message": f"User {user_id} deleted successfully"}
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "users_count": len(users_db),
        "rate_limit_window": RATE_LIMIT_WINDOW,
        "max_requests_per_window": MAX_REQUESTS_PER_WINDOW
    }

# Rate limit status endpoint
@app.get("/rate-limit-status")
async def get_rate_limit_status(request: Request):
    """Get current rate limit status for the requesting IP"""
    client_ip = request.client.host
    current_time = time.time()
    
    # Clean old timestamps
    rate_limit_store[client_ip] = [
        ts for ts in rate_limit_store[client_ip] 
        if current_time - ts < RATE_LIMIT_WINDOW
    ]
    
    return {
        "ip": client_ip,
        "requests_in_window": len(rate_limit_store[client_ip]),
        "max_requests": MAX_REQUESTS_PER_WINDOW,
        "window_seconds": RATE_LIMIT_WINDOW,
        "remaining_requests": max(0, MAX_REQUESTS_PER_WINDOW - len(rate_limit_store[client_ip]))
    }