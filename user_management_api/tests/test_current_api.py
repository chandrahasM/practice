"""
Comprehensive tests for the current User Management API implementation
"""
import pytest
import json
import tempfile
import os
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app, users_db, next_id, rate_limit_store

# Create a test client
client = TestClient(app)


class TestCreateUserEndpoint:
    """Test the create user endpoint (/users)"""
    
    def setup_method(self):
        """Reset the database and rate limiting before each test"""
        # Clear the users database
        users_db.clear()
        
        # Reset the next_id counter
        global next_id
        next_id = 1
        
        # Clear rate limiting data
        rate_limit_store.clear()
        
        # Create a temporary sample_data.json for testing
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
        
        # Create empty sample data
        with open("sample_data.json", "w") as f:
            json.dump({"users": []}, f)
    
    def teardown_method(self):
        """Clean up after each test"""
        # Restore original working directory
        os.chdir(self.original_cwd)
        
        # Clean up temporary directory
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_create_user_success(self):
        """
        Test successful user creation
        
        This test verifies:
        1. User is created with correct data
        2. Auto-generated ID is assigned
        3. Response status is 200 (not 201 as in some APIs)
        4. All user fields are returned correctly
        """
        # Test data
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "age": 30
        }
        
        # Make the request
        response = client.post("/users", json=user_data)
        
        # Assertions
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Check response data
        data = response.json()
        assert data["id"] == 1, f"Expected ID 1, got {data['id']}"
        assert data["name"] == "John Doe"
        assert data["email"] == "john@example.com"
        assert data["age"] == 30
        
        # Verify user was added to database
        assert len(users_db) == 1
        assert users_db[0]["id"] == 1
        assert users_db[0]["name"] == "John Doe"
        
        # Verify output file was created
        assert os.path.exists("output_users.json")
        with open("output_users.json", "r") as f:
            output_data = json.load(f)
            assert len(output_data["users"]) == 1
            assert output_data["users"][0]["id"] == 1
    
    def test_create_user_without_age(self):
        """
        Test user creation without optional age field
        
        This test verifies:
        1. User can be created without age
        2. Age field is set to None
        3. Other required fields work correctly
        """
        user_data = {
            "name": "Jane Doe",
            "email": "jane@example.com"
            # age field is omitted
        }
        
        response = client.post("/users", json=user_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "Jane Doe"
        assert data["email"] == "jane@example.com"
        assert data["age"] is None
        
        # Verify in database
        assert users_db[0]["age"] is None
    
    def test_create_user_sequential_ids(self):
        """
        Test that multiple users get sequential IDs
        
        This test verifies:
        1. First user gets ID 1
        2. Second user gets ID 2
        3. IDs are unique and sequential
        """
        # Create first user
        user1_data = {"name": "User 1", "email": "user1@example.com"}
        response1 = client.post("/users", json=user1_data)
        assert response1.status_code == 200
        assert response1.json()["id"] == 1
        
        # Create second user
        user2_data = {"name": "User 2", "email": "user2@example.com"}
        response2 = client.post("/users", json=user2_data)
        assert response2.status_code == 200
        assert response2.json()["id"] == 2
        
        # Verify database state
        assert len(users_db) == 2
        assert users_db[0]["id"] == 1
        assert users_db[1]["id"] == 2
        
        # Verify output file
        with open("output_users.json", "r") as f:
            output_data = json.load(f)
            assert len(output_data["users"]) == 2
            assert output_data["users"][0]["id"] == 1
            assert output_data["users"][1]["id"] == 2
    
    def test_create_user_missing_required_fields(self):
        """
        Test user creation with missing required fields
        
        This test verifies:
        1. Missing name returns validation error
        2. Missing email returns validation error
        3. Proper error status codes
        """
        # Test missing name
        user_data_no_name = {"email": "test@example.com", "age": 25}
        response = client.post("/users", json=user_data_no_name)
        assert response.status_code == 422  # Validation error
        
        # Test missing email
        user_data_no_email = {"name": "Test User", "age": 25}
        response = client.post("/users", json=user_data_no_email)
        assert response.status_code == 422  # Validation error
    
    def test_create_user_invalid_data_types(self):
        """
        Test user creation with invalid data types
        
        This test verifies:
        1. Invalid age type returns validation error
        2. Invalid email format returns validation error
        3. Proper error handling
        """
        # Test invalid age type
        user_data_invalid_age = {
            "name": "Test User",
            "email": "test@example.com",
            "age": "not_a_number"
        }
        response = client.post("/users", json=user_data_invalid_age)
        assert response.status_code == 422
        
        # Test invalid email format
        user_data_invalid_email = {
            "name": "Test User",
            "email": "invalid_email_format",
            "age": 25
        }
        response = client.post("/users", json=user_data_invalid_email)
        assert response.status_code == 422
    
    def test_create_user_empty_strings(self):
        """
        Test user creation with empty strings
        
        This test verifies:
        1. Empty name is rejected
        2. Empty email is rejected
        3. Proper validation
        """
        # Test empty name
        user_data_empty_name = {"name": "", "email": "test@example.com"}
        response = client.post("/users", json=user_data_empty_name)
        assert response.status_code == 422
        
        # Test empty email
        user_data_empty_email = {"name": "Test User", "email": ""}
        response = client.post("/users", json=user_data_empty_email)
        assert response.status_code == 422


class TestRateLimiting:
    """Test rate limiting functionality"""
    
    def setup_method(self):
        """Reset rate limiting before each test"""
        rate_limit_store.clear()
    
    def test_rate_limit_not_exceeded(self):
        """Test that rate limiting allows requests within limits"""
        # Make a request
        user_data = {"name": "Test User", "email": "test@example.com"}
        response = client.post("/users", json=user_data)
        assert response.status_code == 200
        
        # Check rate limit status
        status_response = client.get("/rate-limit-status")
        assert status_response.status_code == 200
        status_data = status_response.json()
        assert status_data["requests_in_window"] == 1
        assert status_data["remaining_requests"] == 99  # 100 - 1
    
    def test_rate_limit_exceeded(self):
        """Test that rate limiting blocks requests when exceeded"""
        # Make 100 requests to hit the limit
        user_data = {"name": "Test User", "email": "test@example.com"}
        
        for i in range(100):
            response = client.post("/users", json=user_data)
            if response.status_code != 200:
                break
        
        # The 101st request should be blocked
        response = client.post("/users", json=user_data)
        assert response.status_code == 429  # Too Many Requests
        
        # Check error message
        error_data = response.json()
        assert "Rate limit exceeded" in error_data["detail"]


class TestHealthEndpoints:
    """Test health and monitoring endpoints"""
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "users_count" in data
        assert "rate_limit_window" in data
        assert "max_requests_per_window" in data
    
    def test_rate_limit_status(self):
        """Test rate limit status endpoint"""
        response = client.get("/rate-limit-status")
        assert response.status_code == 200
        
        data = response.json()
        assert "ip" in data
        assert "requests_in_window" in data
        assert "max_requests" in data
        assert "window_seconds" in data
        assert "remaining_requests" in data


# Example of how to run specific tests
if __name__ == "__main__":
    # Run specific test class
    pytest.main([__file__, "-v", "-k", "TestCreateUserEndpoint"])
    
    # Run specific test method
    pytest.main([__file__, "-v", "-k", "test_create_user_success"]) 