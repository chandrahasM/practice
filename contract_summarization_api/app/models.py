from pydantic import BaseModel, Field, validator
from typing import List, Optional


class ContractInput(BaseModel):
    """Input model for a single contract."""
    contract_id: str = Field(..., description="Unique identifier for the contract")
    text: str = Field(..., description="Full text content of the contract")
    
    @validator('text')
    def text_cannot_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Contract text cannot be empty')
        return v.strip()


class ContractSummaryRequest(BaseModel):
    """Request model for contract summarization endpoint."""
    contracts: List[ContractInput] = Field(..., description="List of contracts to summarize")
    
    @validator('contracts')
    def contracts_cannot_be_empty(cls, v):
        if not v:
            raise ValueError('At least one contract must be provided')
        return v


class ContractSummary(BaseModel):
    """Output model for a single contract summary."""
    contract_id: str = Field(..., description="Unique identifier for the contract")
    summary: str = Field(..., description="Generated summary of the contract")


class ContractSummaryResponse(BaseModel):
    """Response model for contract summarization endpoint."""
    summaries: List[ContractSummary] = Field(..., description="List of contract summaries")


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    status: str = Field(..., description="Service status")
    timestamp: str = Field(..., description="Current timestamp")
    version: str = Field(..., description="API version")


class ErrorResponse(BaseModel):
    """Standard error response model."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional error details")
    status_code: int = Field(..., description="HTTP status code")
