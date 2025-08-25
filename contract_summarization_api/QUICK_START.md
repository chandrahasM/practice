# Quick Start Guide

Get the AI-Powered Contract Summarization API running in under 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. **Navigate to the project directory:**
   ```bash
   cd contract_summarization_api
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the API

1. **Start the FastAPI server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Access the API:**
   - API Base URL: http://localhost:8000
   - Interactive Docs (Swagger): http://localhost:8000/docs
   - Alternative Docs (ReDoc): http://localhost:8000/redoc

## Quick Test

1. **Health Check:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Test Contract Summarization:**
   ```bash
   curl -X POST "http://localhost:8000/summarize" \
        -H "Content-Type: application/json" \
        -d '{
          "contracts": [
            {
              "contract_id": "TEST_001",
              "text": "This is a test contract that should be summarized."
            }
          ]
        }'
   ```

## Running Tests

1. **Run all tests:**
   ```bash
   python run_tests.py
   ```

2. **Run specific test categories:**
   ```bash
   # Unit tests only
   python -m pytest tests/test_models.py tests/test_services.py -v
   
   # API tests only
   python -m pytest tests/test_api.py -v
   
   # All tests with coverage
   python -m pytest tests/ --cov=app --cov-report=term-missing
   ```

## API Endpoints

### POST /summarize
Process contracts and return summaries.

**Request Body:**
```json
{
  "contracts": [
    {
      "contract_id": "string",
      "text": "string"
    }
  ]
}
```

**Response:**
```json
{
  "summaries": [
    {
      "contract_id": "string",
      "summary": "string"
    }
  ]
}
```

### GET /health
Health check endpoint.

### GET /
API information and available endpoints.

## Test Data

The project includes sample test data in the `test_data/` directory:
- `input.json` - Sample contract inputs
- `expected_output.json` - Expected API responses
- `edge_cases.json` - Edge case test scenarios

## Development

- **Project Structure:**
  - `app/` - Main application code
  - `tests/` - Test files
  - `test_data/` - JSON test data
  - `requirements.txt` - Python dependencies

- **Key Files:**
  - `app/main.py` - FastAPI application
  - `app/models.py` - Pydantic data models
  - `app/services.py` - Business logic
  - `run_tests.py` - Test runner script

## Troubleshooting

### Common Issues

1. **Import errors:**
   - Ensure you're in the project root directory
   - Check that all dependencies are installed

2. **Port already in use:**
   - Change the port: `uvicorn app.main:app --port 8001`
   - Or kill the process using port 8000

3. **Test failures:**
   - Run `python run_tests.py` to see detailed output
   - Check that test data files exist and are valid JSON

### Getting Help

- Check the comprehensive README.md for detailed documentation
- Review test files for usage examples
- Use the interactive API documentation at `/docs`

## Next Steps

- Customize the summarization logic in `app/services.py`
- Add new endpoints in `app/main.py`
- Extend the data models in `app/models.py`
- Add more test cases in the `tests/` directory

Happy coding! 🚀
