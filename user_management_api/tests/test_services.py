"""
Tests for business logic services
"""
import pytest
import time
from app.services import UserService
from app.models import UserCreate, UserUpdate
from app.exceptions import UserNotFoundError, UserAlreadyExistsError, InvalidUserDataError
from pydantic import ValidationError


class TestUserService:
    """Test UserService business logic"""
    
    def setup_method(self):
        """Reset database before each test"""
        from app.database import user_db
        user_db.clear()
    
    def test_create_user_success(self):
        """Test successful user creation"""
        user_data = UserCreate(
            name="John Doe",
            email="john@example.com",
            age=30
        )
        
        user = UserService.create_user(user_data)
        
        assert user.id == 1
        assert user.name == "John Doe"
        assert user.email == "john@example.com"
        assert user.age == 30
        assert user.created_at is not None
        assert user.updated_at is not None
    
    def test_create_user_without_age(self):
        """Test user creation without optional age field"""
        user_data = UserCreate(
            name="Jane Doe",
            email="jane@example.com"
        )
        
        user = UserService.create_user(user_data)
        
        assert user.id == 1
        assert user.name == "Jane Doe"
        assert user.email == "jane@example.com"
        assert user.age is None
    
    def test_create_user_duplicate_email(self):
        """Test user creation with duplicate email"""
        # Create first user
        user_data1 = UserCreate(
            name="John Doe",
            email="john@example.com",
            age=30
        )
        UserService.create_user(user_data1)
        
        # Try to create second user with same email
        user_data2 = UserCreate(
            name="John Smith",
            email="john@example.com",
            age=25
        )
        
        with pytest.raises(UserAlreadyExistsError):
            UserService.create_user(user_data2)
    
    def test_create_user_invalid_age(self):
        """Test user creation with invalid age - Pydantic validation error"""
        # Pydantic now validates this before it reaches our service
        with pytest.raises(ValidationError):
            user_data = UserCreate(
                name="John Doe",
                email="john@example.com",
                age=0
            )
    
    def test_get_user_success(self):
        """Test successful user retrieval"""
        # Create user first
        user_data = UserCreate(
            name="John Doe",
            email="john@example.com",
            age=30
        )
        created_user = UserService.create_user(user_data)
        
        # Retrieve user
        retrieved_user = UserService.get_user(created_user.id)
        
        assert retrieved_user.id == created_user.id
        assert retrieved_user.name == created_user.name
        assert retrieved_user.email == created_user.email
    
    def test_get_user_not_found(self):
        """Test user retrieval for non-existent user"""
        with pytest.raises(UserNotFoundError):
            UserService.get_user(999)
    
    def test_get_users_empty(self):
        """Test getting users when database is empty"""
        users = UserService.get_users()
        
        assert users.total == 0
        assert len(users.users) == 0
        assert users.page == 1
        assert users.size == 100
        assert users.has_next is False
    
    def test_get_users_with_data(self):
        """Test getting users with data"""
        # Create multiple users
        user_data1 = UserCreate(name="John Doe", email="john@example.com", age=30)
        user_data2 = UserCreate(name="Jane Doe", email="jane@example.com", age=25)
        user_data3 = UserCreate(name="Bob Smith", email="bob@example.com", age=35)
        
        UserService.create_user(user_data1)
        UserService.create_user(user_data2)
        UserService.create_user(user_data3)
        
        users = UserService.get_users()
        
        assert users.total == 3
        assert len(users.users) == 3
        assert users.page == 1
        assert users.size == 100
        assert users.has_next is False
    
    def test_get_users_pagination(self):
        """Test user pagination"""
        # Create multiple users
        for i in range(25):
            user_data = UserCreate(
                name=f"User {i}",
                email=f"user{i}@example.com",
                age=20 + i
            )
            UserService.create_user(user_data)
        
        # Test first page
        users_page1 = UserService.get_users(skip=0, limit=10)
        assert users_page1.total == 25
        assert len(users_page1.users) == 10
        assert users_page1.page == 1
        assert users_page1.has_next is True
        
        # Test second page
        users_page2 = UserService.get_users(skip=10, limit=10)
        assert users_page2.total == 25
        assert len(users_page2.users) == 10
        assert users_page2.page == 2
        assert users_page2.has_next is True
        
        # Test last page
        users_page3 = UserService.get_users(skip=20, limit=10)
        assert users_page3.total == 25
        assert len(users_page3.users) == 5
        assert users_page3.page == 3
        assert users_page3.has_next is False
    
    def test_update_user_success(self):
        """Test successful user update"""
        # Create user first
        user_data = UserCreate(
            name="John Doe",
            email="john@example.com",
            age=30
        )
        created_user = UserService.create_user(user_data)
        
        # Add a small delay to ensure timestamp difference
        time.sleep(0.001)
        
        # Update user
        update_data = UserUpdate(
            name="John Updated",
            age=31
        )
        
        updated_user = UserService.update_user(created_user.id, update_data)
        
        assert updated_user.id == created_user.id
        assert updated_user.name == "John Updated"
        assert updated_user.email == "john@example.com"  # Unchanged
        assert updated_user.age == 31
        assert updated_user.updated_at >= created_user.updated_at
    
    def test_update_user_not_found(self):
        """Test user update for non-existent user"""
        update_data = UserUpdate(name="John Updated")
        
        with pytest.raises(UserNotFoundError):
            UserService.update_user(999, update_data)
    
    def test_update_user_duplicate_email(self):
        """Test user update with duplicate email"""
        # Create two users
        user1_data = UserCreate(name="John Doe", email="john@example.com", age=30)
        user2_data = UserCreate(name="Jane Doe", email="jane@example.com", age=25)
        
        user1 = UserService.create_user(user1_data)
        UserService.create_user(user2_data)
        
        # Try to update user1 with user2's email
        update_data = UserUpdate(email="jane@example.com")
        
        with pytest.raises(UserAlreadyExistsError):
            UserService.update_user(user1.id, update_data)
    
    def test_delete_user_success(self):
        """Test successful user deletion"""
        # Create user first
        user_data = UserCreate(
            name="John Doe",
            email="john@example.com",
            age=30
        )
        created_user = UserService.create_user(user_data)
        
        # Delete user
        result = UserService.delete_user(created_user.id)
        
        assert result is True
        
        # Verify user is deleted
        with pytest.raises(UserNotFoundError):
            UserService.get_user(created_user.id)
    
    def test_delete_user_not_found(self):
        """Test user deletion for non-existent user"""
        with pytest.raises(UserNotFoundError):
            UserService.delete_user(999)
    
    def test_search_users_success(self):
        """Test successful user search"""
        # Create users with different names
        user_data1 = UserCreate(name="John Doe", email="john@example.com", age=30)
        user_data2 = UserCreate(name="Jane Doe", email="jane@example.com", age=25)
        user_data3 = UserCreate(name="Bob Smith", email="bob@example.com", age=35)
        
        UserService.create_user(user_data1)
        UserService.create_user(user_data2)
        UserService.create_user(user_data3)
        
        # Search by name
        search_results = UserService.search_users("Doe")
        assert search_results.total == 2
        assert len(search_results.users) == 2
        
        # Search by email
        search_results = UserService.search_users("john@")
        assert search_results.total == 1
        assert len(search_results.users) == 1
    
    def test_search_users_empty_query(self):
        """Test user search with empty query"""
        # Create a user
        user_data = UserCreate(name="John Doe", email="john@example.com", age=30)
        UserService.create_user(user_data)
        
        # Search with empty query should return all users
        search_results = UserService.search_users("")
        assert search_results.total == 1
    
    def test_get_user_stats_empty(self):
        """Test user statistics when database is empty"""
        stats = UserService.get_user_stats()
        
        assert stats["total_users"] == 0
        assert stats["average_age"] == 0
        assert stats["age_distribution"] == {}
        assert stats["email_domains"] == {}
    
    def test_get_user_stats_with_data(self):
        """Test user statistics with data"""
        # Create users with different ages and email domains
        user_data1 = UserCreate(name="John Doe", email="john@gmail.com", age=30)
        user_data2 = UserCreate(name="Jane Doe", email="jane@yahoo.com", age=25)
        user_data3 = UserCreate(name="Bob Smith", email="bob@gmail.com", age=35)
        
        UserService.create_user(user_data1)
        UserService.create_user(user_data2)
        UserService.create_user(user_data3)
        
        stats = UserService.get_user_stats()
        
        assert stats["total_users"] == 3
        assert stats["average_age"] == 30.0
        assert "20-29" in stats["age_distribution"]
        assert "30-39" in stats["age_distribution"]
        assert stats["email_domains"]["gmail.com"] == 2
        assert stats["email_domains"]["yahoo.com"] == 1
