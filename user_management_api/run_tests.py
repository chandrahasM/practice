#!/usr/bin/env python3
"""
Test runner for User Management API
"""
import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🚀 {description}")
    print(f"Running: {command}")
    print("-" * 50)
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✅ Success!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False

def main():
    """Main test runner"""
    print("🧪 User Management API Test Runner")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("app/main.py"):
        print("❌ Error: Please run this script from the user_management_api directory")
        sys.exit(1)
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Run model tests
    if not run_command("python -m pytest tests/test_models.py -v", "Running model tests"):
        print("❌ Model tests failed")
        sys.exit(1)
    
    # Run service tests
    if not run_command("python -m pytest tests/test_services.py -v", "Running service tests"):
        print("❌ Service tests failed")
        sys.exit(1)
    
    # Run API tests
    if not run_command("python -m pytest tests/test_api.py -v", "Running API tests"):
        print("❌ API tests failed")
        sys.exit(1)
    
    # Run all tests together
    if not run_command("python -m pytest tests/ -v", "Running all tests"):
        print("❌ Some tests failed")
        sys.exit(1)
    
    print("\n🎉 All tests completed successfully!")
    print("\nTo run the API server:")
    print("  uvicorn app.main:app --reload")
    print("\nTo access the API documentation:")
    print("  http://localhost:8000/docs")

if __name__ == "__main__":
    main()
