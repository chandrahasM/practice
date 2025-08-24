#!/usr/bin/env python3
"""
Test suite for the Batch User Update Applier

This file contains tests to verify your implementation works correctly.
Run with: python test_user_updater.py

IMPORTANT: Complete the functions in user_updater.py before running these tests!
"""

import pytest
import json
import tempfile
import os
from user_updater import (
    load_json_file, save_json_file, find_user_by_id, 
    apply_update_to_user, apply_batch_updates
)


class TestUserUpdater:
    """Test cases for the user updater functionality."""
    
    def test_load_json_file(self):
        """Test loading JSON files."""
        print("Testing load_json_file...")
        
        test_data = [
            {"user_id": "TEST001", "name": "Test User", "role": "member"}
        ]
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
            json.dump(test_data, f)
        
        try:
            # Test loading
            loaded_data = load_json_file(temp_file)
            assert loaded_data == test_data, "Loaded data should match original data"
            print("✅ load_json_file works correctly")
            
        finally:
            os.unlink(temp_file)
    
    def test_save_json_file(self):
        """Test saving JSON files."""
        print("Testing save_json_file...")
        
        test_data = [
            {"user_id": "TEST001", "name": "Test User", "role": "member"}
        ]
        
        # Create temporary output file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            # Test saving
            save_json_file(test_data, temp_file)
            
            # Verify saved content
            with open(temp_file, 'r') as f:
                saved_data = json.load(f)
            assert saved_data == test_data, "Saved data should match original data"
            print("✅ save_json_file works correctly")
            
        finally:
            os.unlink(temp_file)
    
    def test_find_user_by_id(self):
        """Test finding users by ID."""
        print("Testing find_user_by_id...")
        
        test_users = [
            {"user_id": "U1", "name": "Alice", "role": "member"},
            {"user_id": "U2", "name": "Bob", "role": "admin"},
            {"user_id": "U3", "name": "Charlie", "role": "member"}
        ]
        
        # Test finding existing user
        user = find_user_by_id(test_users, "U2")
        assert user is not None, "Should find user with ID U2"
        assert user["name"] == "Bob", "Should return correct user data"
        
        # Test finding non-existent user
        user = find_user_by_id(test_users, "U99")
        assert user is None, "Should return None for non-existent user ID"
        
        print("✅ find_user_by_id works correctly")
    
    def test_apply_update_to_user(self):
        """Test applying updates to individual users."""
        print("Testing apply_update_to_user...")
        
        original_user = {
            "user_id": "U1", 
            "name": "Alice", 
            "role": "member", 
            "email": "alice@company.com"
        }
        
        update = {
            "user_id": "U1",  # This should be ignored
            "role": "admin",
            "department": "Management"
        }
        
        updated_user = apply_update_to_user(original_user, update)
        
        # Check that original user is unchanged
        assert original_user["role"] == "member", "Original user should not be modified"
        
        # Check that updated user has new values
        assert updated_user["role"] == "admin", "Role should be updated"
        assert updated_user["department"] == "Management", "Department should be added"
        assert updated_user["name"] == "Alice", "Name should be preserved"
        assert updated_user["email"] == "alice@company.com", "Email should be preserved"
        
        print("✅ apply_update_to_user works correctly")
    
    def test_apply_batch_updates(self):
        """Test applying multiple updates to users."""
        print("Testing apply_batch_updates...")
        
        test_users = [
            {"user_id": "U1", "name": "Alice", "role": "member"},
            {"user_id": "U2", "name": "Bob", "role": "admin"},
            {"user_id": "U3", "name": "Charlie", "role": "member"}
        ]
        
        test_updates = [
            {"user_id": "U1", "role": "admin"},
            {"user_id": "U2", "name": "Robert"},
            {"user_id": "U99", "role": "member"}  # Non-existent user
        ]
        
        updated_users = apply_batch_updates(test_users, test_updates)
        
        # Check that all users are present
        assert len(updated_users) == len(test_users), "Should preserve all users"
        
        # Check specific updates
        user1 = find_user_by_id(updated_users, "U1")
        assert user1["role"] == "admin", "U1 role should be updated to admin"
        assert user1["name"] == "Alice", "U1 name should be preserved"
        
        user2 = find_user_by_id(updated_users, "U2")
        assert user2["name"] == "Robert", "U2 name should be updated"
        assert user2["role"] == "admin", "U2 role should be preserved"
        
        user3 = find_user_by_id(updated_users, "U3")
        assert user3 == test_users[2], "U3 should be unchanged"
        
        print("✅ apply_batch_updates works correctly")
    
    def test_preserve_user_order(self):
        """Test that user order is preserved after updates."""
        print("Testing user order preservation...")
        
        test_users = [
            {"user_id": "U1", "name": "Alice", "role": "member"},
            {"user_id": "U2", "name": "Bob", "role": "admin"},
            {"user_id": "U3", "name": "Charlie", "role": "member"}
        ]
        
        test_updates = [
            {"user_id": "U2", "role": "super_admin"},
            {"user_id": "U1", "name": "Alice Smith"}
        ]
        
        updated_users = apply_batch_updates(test_users, test_updates)
        
        # Check order preservation
        assert updated_users[0]["user_id"] == "U1", "First user should still be U1"
        assert updated_users[1]["user_id"] == "U2", "Second user should still be U2"
        assert updated_users[2]["user_id"] == "U3", "Third user should still be U3"
        
        print("✅ User order is preserved correctly")


def run_basic_tests():
    """Run basic tests without pytest for quick verification."""
    print("🧪 Running basic tests...")
    print("=" * 50)
    
    try:
        # Test 1: Load JSON file
        print("Test 1: load_json_file function")
        users = load_json_file("users.json")
        print(f"   ✅ Loaded {len(users)} users from users.json")
        
        # Test 2: Find user by ID
        print("\nTest 2: find_user_by_id function")
        user = find_user_by_id(users, "U1")
        print(f"   ✅ Found user: {user['name'] if user else 'Not found'}")
        
        # Test 3: Apply update to user
        print("\nTest 3: apply_update_to_user function")
        if user:
            update = {"user_id": "U1", "role": "admin"}
            updated_user = apply_update_to_user(user, update)
            print(f"   ✅ Updated user role to: {updated_user['role']}")
        
        # Test 4: Load updates
        print("\nTest 4: Load updates")
        updates = load_json_file("updates.json")
        print(f"   ✅ Loaded {len(updates)} updates from updates.json")
        
        # Test 5: Apply batch updates
        print("\nTest 5: apply_batch_updates function")
        updated_users = apply_batch_updates(users, updates)
        print(f"   ✅ Applied updates to {len(updated_users)} users")
        
        print("\n🎉 All basic tests passed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        print("   Make sure you've implemented all the required functions!")


if __name__ == "__main__":
    print("User Updater Test Suite")
    print("=" * 50)
    
    # Check if pytest is available
    try:
        import pytest
        print("Running with pytest...")
        pytest.main([__file__, "-v"])
    except ImportError:
        print("Pytest not available, running basic tests...")
        run_basic_tests()
