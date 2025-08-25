"""
Business logic services for User Management API
"""
from typing import List, Optional
from app.database import user_db
from app.models import User, UserCreate, UserUpdate, UserList
from app.exceptions import UserNotFoundError, UserAlreadyExistsError, InvalidUserDataError


class UserService:
    """Service class for user-related business logic"""
    
    @staticmethod
    def create_user(user_data: UserCreate) -> User:
        """Create a new user with validation"""
        # Check if email already exists
        if user_db.email_exists(user_data.email):
            raise UserAlreadyExistsError(user_data.email)
        
        # Validate age if provided
        if user_data.age is not None and user_data.age <= 0:
            raise InvalidUserDataError("Age must be a positive number")
        
        try:
            user = user_db.create_user(user_data)
            return user
        except Exception as e:
            raise InvalidUserDataError(f"Failed to create user: {str(e)}")
    
    @staticmethod
    def get_user(user_id: int) -> User:
        """Retrieve a user by ID"""
        user = user_db.get_user(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        return user
    
    @staticmethod
    def get_users(skip: int = 0, limit: int = 100) -> UserList:
        """Retrieve all users with pagination"""
        if skip < 0:
            skip = 0
        if limit <= 0 or limit > 1000:
            limit = 100
        
        users = user_db.get_all_users(skip, limit)
        total = user_db.get_total_users()
        
        return UserList(
            users=users,
            total=total,
            page=(skip // limit) + 1,
            size=limit,
            has_next=(skip + limit) < total
        )
    
    @staticmethod
    def update_user(user_id: int, user_data: UserUpdate) -> User:
        """Update an existing user"""
        # Check if user exists
        if not user_db.user_exists(user_id):
            raise UserNotFoundError(user_id)
        
        # Check email uniqueness if updating email
        if user_data.email is not None:
            if user_db.email_exists(user_data.email, exclude_id=user_id):
                raise UserAlreadyExistsError(user_data.email)
        
        # Validate age if provided
        if user_data.age is not None and user_data.age <= 0:
            raise InvalidUserDataError("Age must be a positive number")
        
        try:
            user = user_db.update_user(user_id, user_data)
            if not user:
                raise UserNotFoundError(user_id)
            return user
        except Exception as e:
            raise InvalidUserDataError(f"Failed to update user: {str(e)}")
    
    @staticmethod
    def delete_user(user_id: int) -> bool:
        """Delete a user by ID"""
        if not user_db.user_exists(user_id):
            raise UserNotFoundError(user_id)
        
        try:
            return user_db.delete_user(user_id)
        except Exception as e:
            raise InvalidUserDataError(f"Failed to delete user: {str(e)}")
    
    @staticmethod
    def search_users(query: str, skip: int = 0, limit: int = 100) -> UserList:
        """Search users by name or email"""
        # If query is empty or just whitespace, return all users
        if not query or not query.strip():
            return UserService.get_users(skip, limit)
        
        # If query is too short, return all users
        if len(query.strip()) < 2:
            return UserService.get_users(skip, limit)
        
        query = query.strip().lower()
        all_users = user_db.get_all_users(0, 10000)  # Get all users for search
        
        # Simple search implementation
        matching_users = []
        for user in all_users:
            if (query in user.name.lower() or 
                query in user.email.lower()):
                matching_users.append(user)
        
        # Apply pagination
        total = len(matching_users)
        paginated_users = matching_users[skip:skip + limit]
        
        return UserList(
            users=paginated_users,
            total=total,
            page=(skip // limit) + 1,
            size=limit,
            has_next=(skip + limit) < total
        )
    
    @staticmethod
    def get_user_stats() -> dict:
        """Get user statistics (bonus feature)"""
        all_users = user_db.get_all_users(0, 10000)
        total_users = len(all_users)
        
        if total_users == 0:
            return {
                "total_users": 0,
                "average_age": 0,
                "age_distribution": {},
                "email_domains": {}
            }
        
        # Calculate statistics
        ages = [user.age for user in all_users if user.age is not None]
        average_age = sum(ages) / len(ages) if ages else 0
        
        # Age distribution
        age_distribution = {}
        for age in ages:
            age_group = f"{(age // 10) * 10}-{(age // 10) * 10 + 9}"
            age_distribution[age_group] = age_distribution.get(age_group, 0) + 1
        
        # Email domain distribution
        email_domains = {}
        for user in all_users:
            domain = user.email.split('@')[1]
            email_domains[domain] = email_domains.get(domain, 0) + 1
        
        return {
            "total_users": total_users,
            "average_age": round(average_age, 2),
            "age_distribution": age_distribution,
            "email_domains": email_domains
        }
