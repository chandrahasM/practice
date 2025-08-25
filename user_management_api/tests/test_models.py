"""
Tests for Pydantic models
"""
import pytest
from datetime import datetime, timezone
from pydantic import ValidationError, EmailStr

from app.models import UserBase, UserCreate, UserUpdate, User, UserList


class TestUserBase:
    """Test UserBase model validation"""
    
    def test_valid_user_base(self):
        """Test valid user base data"""
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30
        }
        user = UserBase(**user_data)
        assert user.name == "John Doe"
        assert user.email == "john@example.com"
        assert user.age == 30
    
    def test_user_base_without_age(self):
        """Test user base without optional age field"""
        user_data = {
            "name": "Jane Doe",
            "email": "jane@example.com"
        }
        user = UserBase(**user_data)
        assert user.name == "Jane Doe"
        assert user.email == "jane@example.com"
        assert user.age is None
    
    def test_invalid_email(self):
        """Test invalid email format"""
        user_data = {
            "name": "John Doe",
            "email": "invalid-email",
            "age": 30
        }
        with pytest.raises(ValidationError):
            UserBase(**user_data)
    
    def test_empty_name(self):
        """Test empty name validation"""
        user_data = {
            "name": "",
            "email": "john@example.com",
            "age": 30
        }
        with pytest.raises(ValidationError):
            UserBase(**user_data)
    
    def test_name_too_long(self):
        """Test name length validation"""
        user_data = {
            "name": "A" * 101,  # 101 characters
            "email": "john@example.com",
            "age": 30
        }
        with pytest.raises(ValidationError):
            UserBase(**user_data)
    
    def test_invalid_age_negative(self):
        """Test negative age validation"""
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "age": -5
        }
        with pytest.raises(ValidationError):
            UserBase(**user_data)
    
    def test_invalid_age_zero(self):
        """Test zero age validation"""
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "age": 0
        }
        with pytest.raises(ValidationError):
            UserBase(**user_data)
    
    def test_invalid_age_too_high(self):
        """Test age upper bound validation"""
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "age": 151
        }
        with pytest.raises(ValidationError):
            UserBase(**user_data)


class TestUserCreate:
    """Test UserCreate model validation"""
    
    def test_valid_user_create(self):
        """Test valid user creation data"""
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30
        }
        user = UserCreate(**user_data)
        assert user.name == "John Doe"
        assert user.email == "john@example.com"
        assert user.age == 30


class TestUserUpdate:
    """Test UserUpdate model validation"""
    
    def test_valid_user_update_all_fields(self):
        """Test valid user update with all fields"""
        user_data = {
            "name": "John Updated",
            "email": "john.updated@example.com",
            "age": 31
        }
        user = UserUpdate(**user_data)
        assert user.name == "John Updated"
        assert user.email == "john.updated@example.com"
        assert user.age == 31
    
    def test_valid_user_update_partial(self):
        """Test valid user update with partial fields"""
        user_data = {
            "name": "John Updated"
        }
        user = UserUpdate(**user_data)
        assert user.name == "John Updated"
        assert user.email is None
        assert user.age is None
    
    def test_user_update_empty_dict(self):
        """Test user update with empty dictionary"""
        user = UserUpdate()
        assert user.name is None
        assert user.email is None
        assert user.age is None


class TestUser:
    """Test User model validation"""
    
    def test_valid_user(self):
        """Test valid complete user data"""
        now = datetime.now(timezone.utc)
        user_data = {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30,
            "created_at": now,
            "updated_at": now
        }
        user = User(**user_data)
        assert user.id == 1
        assert user.name == "John Doe"
        assert user.email == "john@example.com"
        assert user.age == 30
        assert user.created_at == now
        assert user.updated_at == now


class TestUserList:
    """Test UserList model validation"""
    
    def test_valid_user_list(self):
        """Test valid user list data"""
        now = datetime.now(timezone.utc)
        user_data = {
            "users": [
                {
                    "id": 1,
                    "name": "John Doe",
                    "email": "john@example.com",
                    "age": 30,
                    "created_at": now,
                    "updated_at": now
                }
            ],
            "total": 1,
            "page": 1,
            "size": 10,
            "has_next": False
        }
        user_list = UserList(**user_data)
        assert len(user_list.users) == 1
        assert user_list.total == 1
        assert user_list.page == 1
        assert user_list.size == 10
        assert user_list.has_next is False
