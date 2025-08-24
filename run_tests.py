#!/usr/bin/env python3
"""
Simple Test Runner for Contract Updater

This script runs basic tests without requiring pytest.
Useful for quick verification of your implementation.
"""

import sys
import os

def main():
    print("🚀 Contract Updater - Simple Test Runner")
    print("=" * 50)
    
    # Check if the main script exists
    if not os.path.exists("contract_updater.py"):
        print("❌ Error: contract_updater.py not found!")
        print("   Make sure you're in the correct directory.")
        return
    
    # Check if contracts.json exists
    if not os.path.exists("contracts.json"):
        print("❌ Error: contracts.json not found!")
        print("   Make sure the sample data file exists.")
        return
    
    print("📁 Files found:")
    print("   ✅ contract_updater.py")
    print("   ✅ contracts.json")
    print()
    
    try:
        # Import the functions to test
        print("🧪 Testing function imports...")
        from contract_updater import (
            load_contracts, save_contracts, parse_date, 
            is_expiring_soon, update_contract_statuses
        )
        print("   ✅ All functions imported successfully")
        
        # Test 1: Parse a simple date
        print("\n🧪 Test 1: parse_date function")
        try:
            test_date = parse_date("2025-01-15")
            print(f"   ✅ parse_date('2025-01-15') = {test_date}")
        except Exception as e:
            print(f"   ❌ parse_date failed: {e}")
            return
        
        # Test 2: Check if expiring soon
        print("\n🧪 Test 2: is_expiring_soon function")
        try:
            from datetime import datetime, timedelta
            today = datetime.now().date()
            tomorrow = (today + timedelta(days=1)).strftime("%Y-%m-%d")
            is_soon = is_expiring_soon(tomorrow, 30)
            print(f"   ✅ Contract expiring tomorrow is expiring soon: {is_soon}")
        except Exception as e:
            print(f"   ❌ is_expiring_soon failed: {e}")
            return
        
        # Test 3: Load contracts
        print("\n🧪 Test 3: load_contracts function")
        try:
            contracts = load_contracts("contracts.json")
            print(f"   ✅ Loaded {len(contracts)} contracts from contracts.json")
        except Exception as e:
            print(f"   ❌ load_contracts failed: {e}")
            return
        
        # Test 4: Update statuses
        print("\n🧪 Test 4: update_contract_statuses function")
        try:
            updated = update_contract_statuses(contracts)
            expiring_count = sum(1 for c in updated if c['status'] == 'expiring_soon')
            print(f"   ✅ Updated {expiring_count} contracts to 'expiring_soon'")
        except Exception as e:
            print(f"   ❌ update_contract_statuses failed: {e}")
            return
        
        # Test 5: Save contracts
        print("\n🧪 Test 5: save_contracts function")
        try:
            save_contracts(updated, "test_output.json")
            print("   ✅ Successfully saved updated contracts")
            
            # Cleanup test file
            if os.path.exists("test_output.json"):
                os.remove("test_output.json")
                print("   ✅ Cleaned up test output file")
        except Exception as e:
            print(f"   ❌ save_contracts failed: {e}")
            return
        
        print("\n🎉 All tests passed! Your implementation is working correctly.")
        print("\n💡 Next steps:")
        print("   1. Run the main script: python contract_updater.py")
        print("   2. Check the generated updated_contracts.json file")
        print("   3. Review the changes made to contract statuses")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure you've implemented all the required functions!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("   Check your implementation for bugs")


if __name__ == "__main__":
    main()
