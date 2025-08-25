# AI-Powered Contract Summarization API

A FastAPI-based backend service that simulates AI-powered contract summarization for legal document processing.

## Problem Statement

Modern businesses process large volumes of legal contracts. Legal teams benefit from quickly understanding key terms, parties, and dates in contracts, but manual review is time-consuming. This API simulates "AI-powered contract summarization," processing contracts and returning a short summary for each.

## Features

- **Contract Summarization**: Extract summaries from contract text
- **Batch Processing**: Handle multiple contracts in a single request
- **Input Validation**: Robust error handling with Pydantic models
- **Comprehensive Testing**: Automated tests with JSON test cases
- **API Documentation**: OpenAPI/Swagger docs with FastAPI
- **Health Monitoring**: Health check endpoint

## API Endpoints

### POST /summarize
Process one or more contracts and return summaries.

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
Health check endpoint returning service status.

## Project Structure

```
contract_summarization_api/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── models.py        # Pydantic models
│   ├── services.py      # Business logic
│   └── utils.py         # Utility functions
├── tests/
│   ├── __init__.py
│   ├── test_api.py      # API tests
│   ├── test_models.py   # Model tests
│   └── test_services.py # Service tests
├── test_data/
│   ├── input.json       # Sample input contracts
│   ├── expected_output.json  # Expected API responses
│   └── edge_cases.json  # Edge case test data
├── requirements.txt      # Python dependencies
├── run_tests.py         # Test runner script
└── README.md            # This file
```

## Quick Start

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the API:**
   ```bash
   uvicorn app.main:app --reload
   ```

3. **Run Tests:**
   ```bash
   python run_tests.py
   ```

4. **Access API Documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Testing

The project includes comprehensive testing with:
- Unit tests for models and services
- Integration tests for API endpoints
- JSON test case validation
- Edge case handling

## Technical Details

- **Framework**: FastAPI with Pydantic validation
- **Python Version**: 3.8+
- **Testing**: pytest with FastAPI TestClient
- **Documentation**: OpenAPI 3.0 specification

## Future Enhancements

- Real AI/ML model integration
- Caching and rate limiting
- Database persistence
- Authentication and authorization
- Containerization with Docker
- Cloud deployment (GCP, AWS)
