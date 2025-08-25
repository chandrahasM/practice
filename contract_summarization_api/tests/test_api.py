import pytest
import json
from fastapi.testclient import TestClient
from app.main import app
from app.utils import load_json_file, get_project_root

# Create test client
client = TestClient(app)


class TestHealthEndpoint:
    """Test cases for the health check endpoint."""
    
    def test_health_endpoint(self):
        """Test that health endpoint returns correct response."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "status" in data
        assert "timestamp" in data
        assert "version" in data
        assert data["status"] == "healthy"
        assert data["version"] == "1.0.0"
    
    def test_health_endpoint_response_structure(self):
        """Test that health endpoint response has correct structure."""
        response = client.get("/health")
        data = response.json()
        
        # Check all required fields exist
        required_fields = ["status", "timestamp", "version"]
        for field in required_fields:
            assert field in data
            assert data[field] is not None


class TestRootEndpoint:
    """Test cases for the root endpoint."""
    
    def test_root_endpoint(self):
        """Test that root endpoint returns API information."""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "message" in data
        assert "version" in data
        assert "endpoints" in data
        assert "description" in data
        
        assert data["message"] == "AI-Powered Contract Summarization API"
        assert data["version"] == "1.0.0"
    
    def test_root_endpoint_available_endpoints(self):
        """Test that root endpoint lists all available endpoints."""
        response = client.get("/")
        data = response.json()
        
        endpoints = data["endpoints"]
        assert "health" in endpoints
        assert "summarize" in endpoints
        assert "documentation" in endpoints


class TestSummarizeEndpoint:
    """Test cases for the contract summarization endpoint."""
    
    def test_summarize_single_contract(self):
        """Test summarizing a single contract."""
        request_data = {
            "contracts": [
                {
                    "contract_id": "CONTRACT_001",
                    "text": "This is a single contract to summarize."
                }
            ]
        }
        
        response = client.post("/summarize", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "summaries" in data
        assert len(data["summaries"]) == 1
        
        summary = data["summaries"][0]
        assert summary["contract_id"] == "CONTRACT_001"
        assert summary["summary"] == "This is a single contract to summarize."
    
    def test_summarize_multiple_contracts(self):
        """Test summarizing multiple contracts."""
        request_data = {
            "contracts": [
                {
                    "contract_id": "CONTRACT_001",
                    "text": "First contract text."
                },
                {
                    "contract_id": "CONTRACT_002",
                    "text": "Second contract text."
                },
                {
                    "contract_id": "CONTRACT_003",
                    "text": "Third contract text."
                }
            ]
        }
        
        response = client.post("/summarize", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert "summaries" in data
        assert len(data["summaries"]) == 3
        
        # Check all summaries are present
        contract_ids = [s["contract_id"] for s in data["summaries"]]
        assert "CONTRACT_001" in contract_ids
        assert "CONTRACT_002" in contract_ids
        assert "CONTRACT_003" in contract_ids
    
    def test_summarize_with_long_text(self):
        """Test summarizing contracts with long text."""
        long_text = "This is a very long first sentence that contains more than twenty-five words and should be truncated appropriately to maintain readability and conciseness in the summary output. This is the second sentence that should not be included in the summary."
        
        request_data = {
            "contracts": [
                {
                    "contract_id": "CONTRACT_LONG",
                    "text": long_text
                }
            ]
        }
        
        response = client.post("/summarize", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        summary = data["summaries"][0]
        assert summary["contract_id"] == "CONTRACT_LONG"
        # Should be truncated to first 25 words + "..."
        assert summary["summary"].endswith("...")
        assert len(summary["summary"].split()) <= 26  # 25 words + "..."
    
    def test_summarize_with_special_characters(self):
        """Test summarizing contracts with special characters."""
        special_text = "Contract with special chars: @#$%^&*()_+-=[]{}|;':\",./<>?`~"
        
        request_data = {
            "contracts": [
                {
                    "contract_id": "CONTRACT_SPECIAL",
                    "text": special_text
                }
            ]
        }
        
        response = client.post("/summarize", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        
        summary = data["summaries"][0]
        assert summary["contract_id"] == "CONTRACT_SPECIAL"
        assert "Contract with special chars" in summary["summary"]


class TestSummarizeEndpointValidation:
    """Test cases for input validation in the summarize endpoint."""
    
    def test_missing_contracts_field(self):
        """Test that missing contracts field returns 422 error."""
        request_data = {}
        
        response = client.post("/summarize", json=request_data)
        
        assert response.status_code == 422
    
    def test_empty_contracts_list(self):
        """Test that empty contracts list returns 400 error."""
        request_data = {
            "contracts": []
        }
        
        response = client.post("/summarize", json=request_data)
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "At least one contract must be provided" in data["detail"]
    
    def test_missing_contract_id(self):
        """Test that missing contract_id returns 422 error."""
        request_data = {
            "contracts": [
                {
                    "text": "Contract text without ID."
                }
            ]
        }
        
        response = client.post("/summarize", json=request_data)
        
        assert response.status_code == 422
    
    def test_missing_text(self):
        """Test that missing text returns 422 error."""
        request_data = {
            "contracts": [
                {
                    "contract_id": "CONTRACT_001"
                }
            ]
        }
        
        response = client.post("/summarize", json=request_data)
        
        assert response.status_code == 422
    
    def test_empty_text(self):
        """Test that empty text returns 400 error."""
        request_data = {
            "contracts": [
                {
                    "contract_id": "CONTRACT_001",
                    "text": ""
                }
            ]
        }
        
        response = client.post("/summarize", json=request_data)
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "Contract text cannot be empty" in data["detail"]
    
    def test_whitespace_only_text(self):
        """Test that whitespace-only text returns 400 error."""
        request_data = {
            "contracts": [
                {
                    "contract_id": "CONTRACT_001",
                    "text": "   \n\t   "
                }
            ]
        }
        
        response = client.post("/summarize", json=request_data)
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "Contract text cannot be empty" in data["detail"]


class TestJSONTestCases:
    """Test cases using the provided JSON test data files."""
    
    def test_input_json_against_expected_output(self):
        """Test that the API correctly processes the input.json file."""
        try:
            # Load test data
            project_root = get_project_root()
            input_file = project_root / "test_data" / "input.json"
            expected_file = project_root / "test_data" / "expected_output.json"
            
            input_data = load_json_file(str(input_file))
            expected_data = load_json_file(str(expected_file))
            
            # Submit request to API
            response = client.post("/summarize", json=input_data)
            
            assert response.status_code == 200
            actual_data = response.json()
            
            # Verify response structure
            assert "summaries" in actual_data
            assert len(actual_data["summaries"]) == len(expected_data["summaries"])
            
            # Verify each summary matches expected
            for i, expected_summary in enumerate(expected_data["summaries"]):
                actual_summary = actual_data["summaries"][i]
                assert actual_summary["contract_id"] == expected_summary["contract_id"]
                assert actual_summary["summary"] == expected_summary["summary"]
                
        except FileNotFoundError:
            pytest.skip("Test data files not found")
    
    def test_edge_cases_json(self):
        """Test edge cases from the edge_cases.json file."""
        try:
            # Load edge cases data
            project_root = get_project_root()
            edge_cases_file = project_root / "test_data" / "edge_cases.json"
            edge_cases_data = load_json_file(str(edge_cases_file))
            
            for test_case in edge_cases_data["test_cases"]:
                test_name = test_case["name"]
                input_data = test_case["input"]
                
                if "expected_error" in test_case:
                    # Test case expects an error
                    response = client.post("/summarize", json=input_data)
                    assert response.status_code in [400, 422]
                    
                elif "expected_output" in test_case:
                    # Test case expects successful output
                    response = client.post("/summarize", json=input_data)
                    assert response.status_code == 200
                    
                    actual_data = response.json()
                    expected_data = test_case["expected_output"]
                    
                    assert len(actual_data["summaries"]) == len(expected_data["summaries"])
                    
                    for i, expected_summary in enumerate(expected_data["summaries"]):
                        actual_summary = actual_data["summaries"][i]
                        assert actual_summary["contract_id"] == expected_summary["contract_id"]
                        assert actual_summary["summary"] == expected_summary["summary"]
                        
        except FileNotFoundError:
            pytest.skip("Edge cases test data file not found")


class TestErrorHandling:
    """Test cases for error handling scenarios."""
    
    def test_invalid_json_request(self):
        """Test that invalid JSON returns 422 error."""
        response = client.post(
            "/summarize",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 422
    
    def test_malformed_request_structure(self):
        """Test that malformed request structure returns appropriate error."""
        request_data = {
            "contracts": [
                {
                    "contract_id": "CONTRACT_001",
                    "text": "Valid text",
                    "extra_field": "should not be here"
                }
            ]
        }
        
        response = client.post("/summarize", json=request_data)
        
        # Should still process successfully, ignoring extra fields
        assert response.status_code == 200
    
    def test_large_request_handling(self):
        """Test that large requests are handled appropriately."""
        # Create a large request with many contracts
        contracts = []
        for i in range(100):
            contracts.append({
                "contract_id": f"CONTRACT_{i:03d}",
                "text": f"This is contract number {i} with some text content."
            })
        
        request_data = {"contracts": contracts}
        
        response = client.post("/summarize", json=request_data)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["summaries"]) == 100


class TestAPIDocumentation:
    """Test cases for API documentation endpoints."""
    
    def test_swagger_docs_available(self):
        """Test that Swagger documentation is available."""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_redoc_available(self):
        """Test that ReDoc documentation is available."""
        response = client.get("/redoc")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_openapi_schema_available(self):
        """Test that OpenAPI schema is available."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        
        # Check basic OpenAPI structure
        assert "openapi" in data
        assert "info" in data
        assert "paths" in data
        
        # Check that our endpoints are documented
        paths = data["paths"]
        assert "/health" in paths
        assert "/summarize" in paths
        assert "/" in paths
