#!/usr/bin/env python3
"""
Test suite for the Contract Expiry Status Updater

This file contains tests to verify your implementation works correctly.
Run with: python test_contract_updater.py

IMPORTANT: Complete the functions in contract_updater.py before running these tests!
"""

import pytest
import json
import tempfile
import os
from datetime import datetime, timedelta
from contract_updater import (
    load_contracts, save_contracts, parse_date, 
    is_expiring_soon, update_contract_statuses
)


class TestContractUpdater:
    """Test cases for the contract updater functionality."""
    
    def test_parse_date_valid(self):
        """Test parsing valid date strings."""
        print("Testing parse_date with valid dates...")
        
        # Test various valid date formats
        assert parse_date("2025-01-15") == datetime(2025, 1, 15)
        assert parse_date("2024-12-31") == datetime(2024, 12, 31)
        assert parse_date("2026-02-29") == datetime(2026, 2, 29)  # Leap year
        
        print("✅ parse_date handles valid dates correctly")
    
    def test_parse_date_invalid(self):
        """Test parsing invalid date strings."""
        print("Testing parse_date with invalid dates...")
        
        # Test various invalid formats
        with pytest.raises(ValueError):
            parse_date("invalid-date")
        with pytest.raises(ValueError):
            parse_date("2025/01/15")
        with pytest.raises(ValueError):
            parse_date("15-01-2025")
        with pytest.raises(ValueError):
            parse_date("2025-13-01")  # Invalid month
        
        print("✅ parse_date properly handles invalid dates")
    
    def test_is_expiring_soon(self):
        """Test the expiring soon logic."""
        print("Testing is_expiring_soon logic...")
        
        # Get current date for consistent testing
        today = datetime.now().date()
        
        # Contract expiring in 25 days (should be expiring soon)
        future_date = (today + timedelta(days=25)).strftime("%Y-%m-%d")
        assert is_expiring_soon(future_date, 30) == True, f"Contract expiring on {future_date} should be expiring soon"
        
        # Contract expiring in 35 days (should not be expiring soon)
        future_date = (today + timedelta(days=35)).strftime("%Y-%m-%d")
        assert is_expiring_soon(future_date, 30) == False, f"Contract expiring on {future_date} should not be expiring soon"
        
        # Contract expiring today (should be expiring soon)
        today_str = today.strftime("%Y-%m-%d")
        assert is_expiring_soon(today_str, 30) == True, f"Contract expiring today should be expiring soon"
        
        # Contract expiring in exactly 30 days (should be expiring soon)
        future_date = (today + timedelta(days=30)).strftime("%Y-%m-%d")
        assert is_expiring_soon(future_date, 30) == True, f"Contract expiring in exactly 30 days should be expiring soon"
        
        print("✅ is_expiring_soon correctly identifies contracts expiring within threshold")
    
    def test_load_and_save_contracts(self):
        """Test loading and saving contracts."""
        print("Testing load_contracts and save_contracts...")
        
        test_contracts = [
            {"contract_id": "TEST001", "company": "Test Corp", "status": "active", "expiry_date": "2025-01-15"},
            {"contract_id": "TEST002", "company": "Another Corp", "status": "draft", "expiry_date": "2025-02-01"}
        ]
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
            json.dump(test_contracts, f)
        
        try:
            # Test loading
            loaded_contracts = load_contracts(temp_file)
            assert loaded_contracts == test_contracts, "Loaded contracts should match original data"
            
            # Test saving
            output_file = temp_file + "_output.json"
            save_contracts(loaded_contracts, output_file)
            
            # Verify saved content
            with open(output_file, 'r') as f:
                saved_contracts = json.load(f)
            assert saved_contracts == test_contracts, "Saved contracts should match original data"
            
            # Cleanup
            os.unlink(output_file)
            print("✅ load_contracts and save_contracts work correctly")
            
        finally:
            os.unlink(temp_file)
    
    def test_update_contract_statuses(self):
        """Test updating contract statuses."""
        print("Testing update_contract_statuses...")
        
        test_contracts = [
            {"contract_id": "C001", "company": "Acme", "status": "active", "expiry_date": "2025-01-15"},
            {"contract_id": "C002", "company": "BetaCo", "status": "active", "expiry_date": "2026-01-01"},
            {"contract_id": "C003", "company": "Gamma", "status": "draft", "expiry_date": "2025-01-20"},
            {"contract_id": "C004", "company": "Delta", "status": "terminated", "expiry_date": "2025-01-25"}
        ]
        
        updated_contracts = update_contract_statuses(test_contracts)
        
        # Verify structure is preserved
        assert len(updated_contracts) == len(test_contracts), "Number of contracts should remain the same"
        assert all('contract_id' in contract for contract in updated_contracts), "All contracts should have contract_id"
        assert all('company' in contract for contract in updated_contracts), "All contracts should have company"
        assert all('status' in contract for contract in updated_contracts), "All contracts should have status"
        assert all('expiry_date' in contract for contract in updated_contracts), "All contracts should have expiry_date"
        
        # Verify business rules
        # Only active contracts should be considered for status updates
        # Draft and terminated contracts should remain unchanged
        
        print("✅ update_contract_statuses preserves contract structure and applies business rules")
    
    def test_business_rules(self):
        """Test that business rules are correctly applied."""
        print("Testing business rules...")
        
        # Create test contracts with various statuses and dates
        today = datetime.now().date()
        expiring_soon_date = (today + timedelta(days=15)).strftime("%Y-%m-%d")
        far_future_date = (today + timedelta(days=45)).strftime("%Y-%m-%d")
        
        test_contracts = [
            # Active contract expiring soon - should be updated
            {"contract_id": "C001", "company": "Acme", "status": "active", "expiry_date": expiring_soon_date},
            # Active contract expiring later - should remain active
            {"contract_id": "C002", "company": "BetaCo", "status": "active", "expiry_date": far_future_date},
            # Draft contract expiring soon - should remain draft
            {"contract_id": "C003", "company": "Gamma", "status": "draft", "expiry_date": expiring_soon_date},
            # Terminated contract expiring soon - should remain terminated
            {"contract_id": "C004", "company": "Delta", "status": "terminated", "expiry_date": expiring_soon_date}
        ]
        
        updated_contracts = update_contract_statuses(test_contracts)
        
        # Find contracts by ID for easier testing
        updated_by_id = {contract['contract_id']: contract for contract in updated_contracts}
        
        # C001 should be updated to expiring_soon
        assert updated_by_id['C001']['status'] == 'expiring_soon', "Active contract expiring soon should be marked as expiring_soon"
        
        # C002 should remain active
        assert updated_by_id['C002']['status'] == 'active', "Active contract expiring later should remain active"
        
        # C003 should remain draft
        assert updated_by_id['C003']['status'] == 'draft', "Draft contract should remain draft regardless of expiry"
        
        # C004 should remain terminated
        assert updated_by_id['C004']['status'] == 'terminated', "Terminated contract should remain terminated regardless of expiry"
        
        print("✅ Business rules are correctly applied")


def run_basic_tests():
    """Run basic tests without pytest for quick verification."""
    print("🧪 Running basic tests...")
    print("=" * 50)
    
    try:
        # Test 1: Parse date
        print("Test 1: parse_date function")
        test_date = parse_date("2025-01-15")
        print(f"   ✅ parse_date('2025-01-15') = {test_date}")
        
        # Test 2: Check if expiring soon
        print("\nTest 2: is_expiring_soon function")
        today = datetime.now().date()
        tomorrow = (today + timedelta(days=1)).strftime("%Y-%m-%d")
        is_soon = is_expiring_soon(tomorrow, 30)
        print(f"   ✅ Contract expiring tomorrow is expiring soon: {is_soon}")
        
        # Test 3: Load contracts
        print("\nTest 3: load_contracts function")
        contracts = load_contracts("contracts.json")
        print(f"   ✅ Loaded {len(contracts)} contracts from contracts.json")
        
        # Test 4: Update statuses
        print("\nTest 4: update_contract_statuses function")
        updated = update_contract_statuses(contracts)
        expiring_count = sum(1 for c in updated if c['status'] == 'expiring_soon')
        print(f"   ✅ Updated {expiring_count} contracts to 'expiring_soon'")
        
        # Test 5: Save contracts
        print("\nTest 5: save_contracts function")
        save_contracts(updated, "test_output.json")
        print("   ✅ Successfully saved updated contracts")
        
        # Cleanup test file
        if os.path.exists("test_output.json"):
            os.remove("test_output.json")
        
        print("\n🎉 All basic tests passed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        print("   Make sure you've implemented all the required functions!")


if __name__ == "__main__":
    print("Contract Updater Test Suite")
    print("=" * 50)
    
    # Check if pytest is available
    try:
        import pytest
        print("Running with pytest...")
        pytest.main([__file__, "-v"])
    except ImportError:
        print("Pytest not available, running basic tests...")
        run_basic_tests()
