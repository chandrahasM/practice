import pytest
from pydantic import ValidationError
from app.models import (
    ContractInput, 
    ContractSummaryRequest, 
    ContractSummary, 
    ContractSummaryResponse,
    HealthResponse,
    ErrorResponse
)


class TestContractInput:
    """Test cases for ContractInput model."""
    
    def test_valid_contract_input(self):
        """Test valid contract input creation."""
        contract = ContractInput(
            contract_id="CONTRACT_001",
            text="This is a valid contract text."
        )
        assert contract.contract_id == "CONTRACT_001"
        assert contract.text == "This is a valid contract text."
    
    def test_empty_text_validation(self):
        """Test that empty text raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            ContractInput(
                contract_id="CONTRACT_002",
                text=""
            )
        assert "Contract text cannot be empty" in str(exc_info.value)
    
    def test_whitespace_only_text_validation(self):
        """Test that whitespace-only text raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            ContractInput(
                contract_id="CONTRACT_003",
                text="   \n\t   "
            )
        assert "Contract text cannot be empty" in str(exc_info.value)
    
    def test_text_stripping(self):
        """Test that text is properly stripped of leading/trailing whitespace."""
        contract = ContractInput(
            contract_id="CONTRACT_004",
            text="  This text has whitespace  "
        )
        assert contract.text == "This text has whitespace"


class TestContractSummaryRequest:
    """Test cases for ContractSummaryRequest model."""
    
    def test_valid_request(self):
        """Test valid request creation."""
        request = ContractSummaryRequest(
            contracts=[
                ContractInput(
                    contract_id="CONTRACT_001",
                    text="First contract text."
                ),
                ContractInput(
                    contract_id="CONTRACT_002",
                    text="Second contract text."
                )
            ]
        )
        assert len(request.contracts) == 2
        assert request.contracts[0].contract_id == "CONTRACT_001"
        assert request.contracts[1].contract_id == "CONTRACT_002"
    
    def test_empty_contracts_list_validation(self):
        """Test that empty contracts list raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            ContractSummaryRequest(contracts=[])
        assert "At least one contract must be provided" in str(exc_info.value)
    
    def test_single_contract_request(self):
        """Test request with single contract."""
        request = ContractSummaryRequest(
            contracts=[
                ContractInput(
                    contract_id="CONTRACT_001",
                    text="Single contract text."
                )
            ]
        )
        assert len(request.contracts) == 1
        assert request.contracts[0].contract_id == "CONTRACT_001"


class TestContractSummary:
    """Test cases for ContractSummary model."""
    
    def test_valid_summary(self):
        """Test valid summary creation."""
        summary = ContractSummary(
            contract_id="CONTRACT_001",
            summary="This is the extracted summary."
        )
        assert summary.contract_id == "CONTRACT_001"
        assert summary.summary == "This is the extracted summary."


class TestContractSummaryResponse:
    """Test cases for ContractSummaryResponse model."""
    
    def test_valid_response(self):
        """Test valid response creation."""
        response = ContractSummaryResponse(
            summaries=[
                ContractSummary(
                    contract_id="CONTRACT_001",
                    summary="First summary."
                ),
                ContractSummary(
                    contract_id="CONTRACT_002",
                    summary="Second summary."
                )
            ]
        )
        assert len(response.summaries) == 2
        assert response.summaries[0].contract_id == "CONTRACT_001"
        assert response.summaries[1].contract_id == "CONTRACT_002"
    
    def test_empty_summaries_list(self):
        """Test response with empty summaries list."""
        response = ContractSummaryResponse(summaries=[])
        assert len(response.summaries) == 0


class TestHealthResponse:
    """Test cases for HealthResponse model."""
    
    def test_valid_health_response(self):
        """Test valid health response creation."""
        response = HealthResponse(
            status="healthy",
            timestamp="2024-01-01T00:00:00",
            version="1.0.0"
        )
        assert response.status == "healthy"
        assert response.timestamp == "2024-01-01T00:00:00"
        assert response.version == "1.0.0"


class TestErrorResponse:
    """Test cases for ErrorResponse model."""
    
    def test_valid_error_response(self):
        """Test valid error response creation."""
        response = ErrorResponse(
            error="Validation Error",
            detail="Invalid input data",
            status_code=400
        )
        assert response.error == "Validation Error"
        assert response.detail == "Invalid input data"
        assert response.status_code == 400
    
    def test_error_response_without_detail(self):
        """Test error response without optional detail field."""
        response = ErrorResponse(
            error="Internal Error",
            status_code=500
        )
        assert response.error == "Internal Error"
        assert response.detail is None
        assert response.status_code == 500


class TestModelSerialization:
    """Test cases for model serialization and deserialization."""
    
    def test_contract_input_serialization(self):
        """Test ContractInput model serialization."""
        contract = ContractInput(
            contract_id="CONTRACT_001",
            text="Test contract text."
        )
        
        # Test serialization to dict
        contract_dict = contract.dict()
        assert contract_dict["contract_id"] == "CONTRACT_001"
        assert contract_dict["text"] == "Test contract text."
        
        # Test serialization to JSON
        contract_json = contract.json()
        assert "CONTRACT_001" in contract_json
        assert "Test contract text." in contract_json
    
    def test_request_response_serialization(self):
        """Test full request-response cycle serialization."""
        # Create request
        request = ContractSummaryRequest(
            contracts=[
                ContractInput(
                    contract_id="CONTRACT_001",
                    text="Test contract text."
                )
            ]
        )
        
        # Create response
        response = ContractSummaryResponse(
            summaries=[
                ContractSummary(
                    contract_id="CONTRACT_001",
                    summary="Test summary."
                )
            ]
        )
        
        # Test serialization
        request_dict = request.dict()
        response_dict = response.dict()
        
        assert "contracts" in request_dict
        assert "summaries" in response_dict
        assert len(request_dict["contracts"]) == 1
        assert len(response_dict["summaries"]) == 1
