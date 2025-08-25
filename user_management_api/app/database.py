"""
In-memory database for User Management API
"""
import threading
from datetime import datetime, timezone
from typing import Dict, List, Optional
from app.models import User, UserCreate, UserUpdate


class InMemoryUserDB:
    """Thread-safe in-memory user database"""
    
    def __init__(self):
        self._users: Dict[int, User] = {}
        self._next_id: int = 1
        self._lock = threading.Lock()
    
    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user with auto-generated fields"""
        with self._lock:
            user_id = self._next_id
            self._next_id += 1
            
            now = datetime.now(timezone.utc)
            user = User(
                id=user_id,
                name=user_data.name,
                email=user_data.email,
                age=user_data.age,
                created_at=now,
                updated_at=now
            )
            
            self._users[user_id] = user
            return user
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Retrieve a user by ID"""
        with self._lock:
            return self._users.get(user_id)
    
    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Retrieve all users with pagination"""
        with self._lock:
            user_list = list(self._users.values())
            return user_list[skip:skip + limit]
    
    def get_total_users(self) -> int:
        """Get total number of users"""
        with self._lock:
            return len(self._users)
    
    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Update an existing user"""
        with self._lock:
            if user_id not in self._users:
                return None
            
            user = self._users[user_id]
            
            # Update only provided fields
            if user_data.name is not None:
                user.name = user_data.name
            if user_data.email is not None:
                user.email = user_data.email
            if user_data.age is not None:
                user.age = user_data.age
            
            user.updated_at = datetime.now(timezone.utc)
            return user
    
    def delete_user(self, user_id: int) -> bool:
        """Delete a user by ID"""
        with self._lock:
            if user_id in self._users:
                del self._users[user_id]
                return True
            return False
    
    def user_exists(self, user_id: int) -> bool:
        """Check if a user exists"""
        with self._lock:
            return user_id in self._users
    
    def email_exists(self, email: str, exclude_id: Optional[int] = None) -> bool:
        """Check if an email already exists (for uniqueness validation)"""
        with self._lock:
            for user_id, user in self._users.items():
                if exclude_id and user_id == exclude_id:
                    continue
                if user.email == email:
                    return True
            return False
    
    def clear(self):
        """Clear all users (useful for testing)"""
        with self._lock:
            self._users.clear()
            self._next_id = 1


# Global database instance
user_db = InMemoryUserDB()
