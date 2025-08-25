#!/usr/bin/env python3
"""
Test runner script for the Contract Summarization API.

This script runs all tests and provides detailed output including:
- Unit tests for models and services
- Integration tests for API endpoints
- JSON test case validation
- Test coverage and performance metrics
"""

import os
import sys
import time
import subprocess
import json
from pathlib import Path

def run_command(command, description):
    """Run a command and return the result."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print('='*60)
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        
        execution_time = time.time() - start_time
        
        print(f"Exit Code: {result.returncode}")
        print(f"Execution Time: {execution_time:.2f} seconds")
        
        if result.stdout:
            print("\nSTDOUT:")
            print(result.stdout)
        
        if result.stderr:
            print("\nSTDERR:")
            print(result.stderr)
        
        return result.returncode == 0, execution_time
        
    except Exception as e:
        print(f"Error running command: {e}")
        return False, 0

def check_dependencies():
    """Check if required dependencies are installed."""
    print("Checking dependencies...")
    
    required_packages = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "pytest",
        "httpx"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Install them with: pip install -r requirements.txt")
        return False
    
    print("All dependencies are installed!")
    return True

def run_unit_tests():
    """Run unit tests for models and services."""
    return run_command(
        "python -m pytest tests/test_models.py tests/test_services.py -v",
        "Unit Tests (Models & Services)"
    )

def run_api_tests():
    """Run API integration tests."""
    return run_command(
        "python -m pytest tests/test_api.py -v",
        "API Integration Tests"
    )

def run_all_tests():
    """Run all tests together."""
    return run_command(
        "python -m pytest tests/ -v",
        "All Tests"
    )

def run_tests_with_coverage():
    """Run tests with coverage reporting."""
    return run_command(
        "python -m pytest tests/ --cov=app --cov-report=term-missing --cov-report=html",
        "Tests with Coverage"
    )

def validate_test_data():
    """Validate that test data files exist and are valid JSON."""
    print("\nValidating test data files...")
    
    test_data_dir = Path("test_data")
    if not test_data_dir.exists():
        print("✗ test_data directory not found")
        return False
    
    required_files = ["input.json", "expected_output.json", "edge_cases.json"]
    all_valid = True
    
    for filename in required_files:
        file_path = test_data_dir / filename
        if not file_path.exists():
            print(f"✗ {filename} not found")
            all_valid = False
            continue
        
        try:
            with open(file_path, 'r') as f:
                json.load(f)
            print(f"✓ {filename} - Valid JSON")
        except json.JSONDecodeError as e:
            print(f"✗ {filename} - Invalid JSON: {e}")
            all_valid = False
    
    return all_valid

def run_quick_api_test():
    """Run a quick test to ensure the API can start and respond."""
    print("\nRunning quick API test...")
    
    # Start the API in the background
    try:
        import uvicorn
        from app.main import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        
        # Test health endpoint
        response = client.get("/health")
        if response.status_code == 200:
            print("✓ API health check passed")
            return True
        else:
            print(f"✗ API health check failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ Quick API test failed: {e}")
        return False

def main():
    """Main test runner function."""
    print("Contract Summarization API - Test Runner")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("app").exists() or not Path("tests").exists():
        print("Error: Please run this script from the project root directory")
        print("Expected structure: app/, tests/, test_data/")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        print("\nDependencies check failed. Please install missing packages.")
        sys.exit(1)
    
    # Validate test data
    if not validate_test_data():
        print("\nTest data validation failed.")
        sys.exit(1)
    
    # Run quick API test
    if not run_quick_api_test():
        print("\nQuick API test failed.")
        sys.exit(1)
    
    # Run tests
    test_results = []
    
    print("\n" + "="*60)
    print("STARTING TEST EXECUTION")
    print("="*60)
    
    # Run unit tests
    success, time_taken = run_unit_tests()
    test_results.append(("Unit Tests", success, time_taken))
    
    # Run API tests
    success, time_taken = run_api_tests()
    test_results.append(("API Tests", success, time_taken))
    
    # Run all tests together
    success, time_taken = run_all_tests()
    test_results.append(("All Tests", success, time_taken))
    
    # Run tests with coverage (optional)
    print("\nWould you like to run tests with coverage? (y/n): ", end="")
    try:
        user_input = input().lower().strip()
        if user_input in ['y', 'yes']:
            success, time_taken = run_tests_with_coverage()
            test_results.append(("Tests with Coverage", success, time_taken))
    except KeyboardInterrupt:
        print("\nCoverage test skipped.")
    
    # Print summary
    print("\n" + "="*60)
    print("TEST EXECUTION SUMMARY")
    print("="*60)
    
    total_time = 0
    passed_tests = 0
    
    for test_name, success, time_taken in test_results:
        status = "PASSED" if success else "FAILED"
        total_time += time_taken
        if success:
            passed_tests += 1
        
        print(f"{test_name:<25} {status:<10} {time_taken:.2f}s")
    
    print("-" * 60)
    print(f"Total Execution Time: {total_time:.2f}s")
    print(f"Tests Passed: {passed_tests}/{len(test_results)}")
    
    if passed_tests == len(test_results):
        print("\n🎉 All tests passed successfully!")
        return 0
    else:
        print(f"\n❌ {len(test_results) - passed_tests} test suite(s) failed!")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nTest execution interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)
