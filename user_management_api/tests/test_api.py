"""
Tests for API endpoints using FastAPI TestClient
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestHealthEndpoint:
    """Test health check endpoint"""
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "User Management API"


class TestRootEndpoint:
    """Test root endpoint"""
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "User Management API"
        assert data["version"] == "1.0.0"
        assert "/docs" in data["docs"]


class TestUserEndpoints:
    """Test user CRUD endpoints"""
    
    def setup_method(self):
        """Reset database before each test"""
        from app.database import user_db
        user_db.clear()
    
    def test_create_user_success(self):
        """Test successful user creation"""
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30
        }
        
        response = client.post("/users/", json=user_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "John Doe"
        assert data["email"] == "john@example.com"
        assert data["age"] == 30
        assert "created_at" in data
        assert "updated_at" in data
    
    def test_create_user_without_age(self):
        """Test user creation without optional age field"""
        user_data = {
            "name": "Jane Doe",
            "email": "jane@example.com"
        }
        
        response = client.post("/users/", json=user_data)
        assert response.status_code == 201
        
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "Jane Doe"
        assert data["email"] == "jane@example.com"
        assert data["age"] is None
    
    def test_create_user_duplicate_email(self):
        """Test user creation with duplicate email"""
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30
        }
        
        # Create first user
        response1 = client.post("/users/", json=user_data)
        assert response1.status_code == 201
        
        # Try to create second user with same email
        response2 = client.post("/users/", json=user_data)
        assert response2.status_code == 409
        
        data = response2.json()
        assert data["error"] == "User already exists"
        assert "john@example.com" in data["detail"]
    
    def test_create_user_invalid_email(self):
        """Test user creation with invalid email"""
        user_data = {
            "name": "John Doe",
            "email": "invalid-email",
            "age": 30
        }
        
        response = client.post("/users/", json=user_data)
        assert response.status_code == 422
    
    def test_create_user_invalid_age(self):
        """Test user creation with invalid age"""
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "age": -5
        }
        
        response = client.post("/users/", json=user_data)
        assert response.status_code == 422
    
    def test_get_user_success(self):
        """Test successful user retrieval"""
        # Create user first
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30
        }
        create_response = client.post("/users/", json=user_data)
        created_user = create_response.json()
        
        # Retrieve user
        response = client.get(f"/users/{created_user['id']}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == created_user["id"]
        assert data["name"] == created_user["name"]
        assert data["email"] == created_user["email"]
    
    def test_get_user_not_found(self):
        """Test user retrieval for non-existent user"""
        response = client.get("/users/999")
        assert response.status_code == 404
        
        data = response.json()
        assert data["error"] == "User not found"
        assert "999" in data["detail"]
    
    def test_get_users_empty(self):
        """Test getting users when database is empty"""
        response = client.get("/users/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total"] == 0
        assert len(data["users"]) == 0
        assert data["page"] == 1
        assert data["size"] == 100
        assert data["has_next"] is False
    
    def test_get_users_with_data(self):
        """Test getting users with data"""
        # Create multiple users
        users_data = [
            {"name": "John Doe", "email": "john@example.com", "age": 30},
            {"name": "Jane Doe", "email": "jane@example.com", "age": 25},
            {"name": "Bob Smith", "email": "bob@example.com", "age": 35}
        ]
        
        for user_data in users_data:
            client.post("/users/", json=user_data)
        
        response = client.get("/users/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total"] == 3
        assert len(data["users"]) == 3
        assert data["page"] == 1
        assert data["size"] == 100
        assert data["has_next"] is False
    
    def test_get_users_pagination(self):
        """Test user pagination"""
        # Create multiple users
        for i in range(25):
            user_data = {
                "name": f"User {i}",
                "email": f"user{i}@example.com",
                "age": 20 + i
            }
            client.post("/users/", json=user_data)
        
        # Test first page
        response1 = client.get("/users/?skip=0&limit=10")
        assert response1.status_code == 200
        
        data1 = response1.json()
        assert data1["total"] == 25
        assert len(data1["users"]) == 10
        assert data1["page"] == 1
        assert data1["has_next"] is True
        
        # Test second page
        response2 = client.get("/users/?skip=10&limit=10")
        assert response2.status_code == 200
        
        data2 = response2.json()
        assert data2["total"] == 25
        assert len(data2["users"]) == 10
        assert data2["page"] == 2
        assert data2["has_next"] is True
    
    def test_update_user_success(self):
        """Test successful user update"""
        # Create user first
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30
        }
        create_response = client.post("/users/", json=user_data)
        created_user = create_response.json()
        
        # Update user
        update_data = {
            "name": "John Updated",
            "age": 31
        }
        
        response = client.put(f"/users/{created_user['id']}", json=update_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == created_user["id"]
        assert data["name"] == "John Updated"
        assert data["email"] == "john@example.com"  # Unchanged
        assert data["age"] == 31
    
    def test_update_user_not_found(self):
        """Test user update for non-existent user"""
        update_data = {"name": "John Updated"}
        
        response = client.put("/users/999", json=update_data)
        assert response.status_code == 404
        
        data = response.json()
        assert data["error"] == "User not found"
    
    def test_update_user_duplicate_email(self):
        """Test user update with duplicate email"""
        # Create two users
        user1_data = {"name": "John Doe", "email": "john@example.com", "age": 30}
        user2_data = {"name": "Jane Doe", "email": "jane@example.com", "age": 25}
        
        user1_response = client.post("/users/", json=user1_data)
        client.post("/users/", json=user2_data)
        
        user1 = user1_response.json()
        
        # Try to update user1 with user2's email
        update_data = {"email": "jane@example.com"}
        
        response = client.put(f"/users/{user1['id']}", json=update_data)
        assert response.status_code == 409
        
        data = response.json()
        assert data["error"] == "User already exists"
    
    def test_delete_user_success(self):
        """Test successful user deletion"""
        # Create user first
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30
        }
        create_response = client.post("/users/", json=user_data)
        created_user = create_response.json()
        
        # Delete user
        response = client.delete(f"/users/{created_user['id']}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["message"] == f"User with ID {created_user['id']} deleted successfully"
        
        # Verify user is deleted
        get_response = client.get(f"/users/{created_user['id']}")
        assert get_response.status_code == 404
    
    def test_delete_user_not_found(self):
        """Test user deletion for non-existent user"""
        response = client.delete("/users/999")
        assert response.status_code == 404
        
        data = response.json()
        assert data["error"] == "User not found"


class TestSearchEndpoints:
    """Test search and statistics endpoints"""
    
    def setup_method(self):
        """Reset database before each test"""
        from app.database import user_db
        user_db.clear()
    
    def test_search_users_success(self):
        """Test successful user search"""
        # Create users with different names
        users_data = [
            {"name": "John Doe", "email": "john@example.com", "age": 30},
            {"name": "Jane Doe", "email": "jane@example.com", "age": 25},
            {"name": "Bob Smith", "email": "bob@example.com", "age": 35}
        ]
        
        for user_data in users_data:
            client.post("/users/", json=user_data)
        
        # Search by name
        response = client.get("/users/search/?q=Doe")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total"] == 2
        assert len(data["users"]) == 2
        
        # Search by email
        response = client.get("/users/search/?q=john@")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total"] == 1
        assert len(data["users"]) == 1
    
    def test_search_users_empty_query(self):
        """Test user search with empty query"""
        # Create a user
        user_data = {"name": "John Doe", "email": "john@example.com", "age": 30}
        client.post("/users/", json=user_data)
        
        # Search with empty query should return all users
        response = client.get("/users/search/?q=")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total"] == 1
    
    def test_search_users_short_query(self):
        """Test user search with query too short returns all users"""
        # Create a user
        user_data = {"name": "John Doe", "email": "john@example.com", "age": 30}
        client.post("/users/", json=user_data)
        
        # Search with short query should return all users (new behavior)
        response = client.get("/users/search/?q=a")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total"] == 1
    
    def test_get_user_stats_empty(self):
        """Test user statistics when database is empty"""
        response = client.get("/users/stats/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total_users"] == 0
        assert data["average_age"] == 0
        assert data["age_distribution"] == {}
        assert data["email_domains"] == {}
    
    def test_get_user_stats_with_data(self):
        """Test user statistics with data"""
        # Create users with different ages and email domains
        users_data = [
            {"name": "John Doe", "email": "john@gmail.com", "age": 30},
            {"name": "Jane Doe", "email": "jane@yahoo.com", "age": 25},
            {"name": "Bob Smith", "email": "bob@gmail.com", "age": 35}
        ]
        
        for user_data in users_data:
            client.post("/users/", json=user_data)
        
        response = client.get("/users/stats/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total_users"] == 3
        assert data["average_age"] == 30.0
        assert "20-29" in data["age_distribution"]
        assert "30-39" in data["age_distribution"]
        assert data["email_domains"]["gmail.com"] == 2
        assert data["email_domains"]["yahoo.com"] == 1
