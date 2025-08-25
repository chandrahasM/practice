#!/usr/bin/env python3
"""
Simple test runner for the current User Management API
"""
import subprocess
import sys
import os

def run_tests():
    """Run the current API tests"""
    print("🧪 Running User Management API Tests...")
    print("=" * 50)
    
    # Change to the API directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        # Run the tests with pytest
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/test_current_api.py", 
            "-v",  # Verbose output
            "--tb=short"  # Short traceback format
        ], capture_output=True, text=True)
        
        # Print output
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print("Errors/Warnings:")
            print(result.stderr)
        
        # Print summary
        print("=" * 50)
        if result.returncode == 0:
            print("✅ All tests passed!")
        else:
            print("❌ Some tests failed!")
            print(f"Exit code: {result.returncode}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def run_specific_test(test_name):
    """Run a specific test by name"""
    print(f"🧪 Running specific test: {test_name}")
    print("=" * 50)
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/test_current_api.py", 
            "-v",
            "-k", test_name,  # Run only tests matching this name
            "--tb=short"
        ], capture_output=True, text=True)
        
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print("Errors/Warnings:")
            print(result.stderr)
        
        print("=" * 50)
        if result.returncode == 0:
            print("✅ Test completed!")
        else:
            print("❌ Test failed!")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error running test: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run specific test
        test_name = sys.argv[1]
        success = run_specific_test(test_name)
    else:
        # Run all tests
        success = run_tests()
    
    sys.exit(0 if success else 1) 