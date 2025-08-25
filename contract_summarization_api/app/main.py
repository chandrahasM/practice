from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import time
from typing import Dict, Any

from .models import (
    ContractSummaryRequest, 
    ContractSummaryResponse, 
    HealthResponse,
    ErrorResponse
)
from .services import ContractSummarizationService
from .utils import get_current_timestamp, setup_logging

# Setup logging
setup_logging()

# Create FastAPI app
app = FastAPI(
    title="AI-Powered Contract Summarization API",
    description="A FastAPI service that simulates AI-powered contract summarization for legal document processing",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log request details
    logging.info(f"Request: {request.method} {request.url}")
    
    response = await call_next(request)
    
    # Log response details
    process_time = time.time() - start_time
    logging.info(f"Response: {response.status_code} - Processed in {process_time:.3f}s")
    
    return response


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify service status.
    
    Returns:
        HealthResponse: Service status information
    """
    return HealthResponse(
        status="healthy",
        timestamp=get_current_timestamp(),
        version="1.0.0"
    )


@app.post("/summarize", response_model=ContractSummaryResponse, tags=["Contracts"])
async def summarize_contracts(request: ContractSummaryRequest):
    """
    Summarize multiple contracts using AI-powered text analysis.
    
    This endpoint simulates AI summarization by extracting the first sentence
    or the first 25 words from each contract, whichever comes first.
    
    Args:
        request (ContractSummaryRequest): Request containing contracts to summarize
        
    Returns:
        ContractSummaryResponse: Summaries for all contracts
        
    Raises:
        HTTPException: If validation fails or processing errors occur
    """
    try:
        logging.info(f"Received request to summarize {len(request.contracts)} contracts")
        
        # Validate input data
        if not ContractSummarizationService.validate_contract_data(request.contracts):
            raise HTTPException(
                status_code=400,
                detail="Invalid contract data provided"
            )
        
        # Process contracts
        summaries = ContractSummarizationService.summarize_contracts(request.contracts)
        
        logging.info(f"Successfully generated summaries for {len(summaries)} contracts")
        
        return ContractSummaryResponse(summaries=summaries)
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logging.error(f"Unexpected error in summarize_contracts: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Custom exception handler for HTTP exceptions.
    
    Args:
        request (Request): The request that caused the exception
        exc (HTTPException): The HTTP exception
        
    Returns:
        JSONResponse: Formatted error response
    """
    error_response = ErrorResponse(
        error="HTTP Exception",
        detail=exc.detail,
        status_code=exc.status_code
    )
    
    logging.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.dict()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    General exception handler for unexpected errors.
    
    Args:
        request (Request): The request that caused the exception
        exc (Exception): The unexpected exception
        
    Returns:
        JSONResponse: Formatted error response
    """
    error_response = ErrorResponse(
        error="Internal Server Error",
        detail="An unexpected error occurred",
        status_code=500
    )
    
    logging.error(f"Unexpected error: {str(exc)}")
    
    return JSONResponse(
        status_code=500,
        content=error_response.dict()
    )


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint providing API information.
    
    Returns:
        Dict[str, Any]: API information and available endpoints
    """
    return {
        "message": "AI-Powered Contract Summarization API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "summarize": "/summarize",
            "documentation": "/docs"
        },
        "description": "A FastAPI service for contract summarization"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
