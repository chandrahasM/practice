import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


def load_json_file(file_path: str) -> Dict[str, Any]:
    """
    Load and parse a JSON file.
    
    Args:
        file_path (str): Path to the JSON file
        
    Returns:
        Dict[str, Any]: Parsed JSON data
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            logger.info(f"Successfully loaded JSON file: {file_path}")
            return data
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in file {file_path}: {str(e)}")
        raise


def save_json_file(file_path: str, data: Dict[str, Any]) -> None:
    """
    Save data to a JSON file.
    
    Args:
        file_path (str): Path to save the JSON file
        data (Dict[str, Any]): Data to save
        
    Raises:
        IOError: If there's an error writing the file
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
            logger.info(f"Successfully saved JSON file: {file_path}")
    except IOError as e:
        logger.error(f"Error writing to file {file_path}: {str(e)}")
        raise


def get_current_timestamp() -> str:
    """
    Get current timestamp in ISO format.
    
    Returns:
        str: Current timestamp in ISO format
    """
    return datetime.now().isoformat()


def format_error_response(error_message: str, detail: Optional[str] = None, status_code: int = 400) -> Dict[str, Any]:
    """
    Format a standardized error response.
    
    Args:
        error_message (str): Main error message
        detail (Optional[str]): Additional error details
        status_code (int): HTTP status code
        
    Returns:
        Dict[str, Any]: Formatted error response
    """
    return {
        "error": error_message,
        "detail": detail,
        "status_code": status_code,
        "timestamp": get_current_timestamp()
    }


def validate_test_data_structure(data: Dict[str, Any], expected_keys: list) -> bool:
    """
    Validate that test data has the expected structure.
    
    Args:
        data (Dict[str, Any]): Data to validate
        expected_keys (list): List of expected top-level keys
        
    Returns:
        bool: True if validation passes, False otherwise
    """
    if not isinstance(data, dict):
        logger.error("Test data must be a dictionary")
        return False
    
    for key in expected_keys:
        if key not in data:
            logger.error(f"Missing required key in test data: {key}")
            return False
    
    return True


def get_project_root() -> Path:
    """
    Get the project root directory.
    
    Returns:
        Path: Path to the project root
    """
    return Path(__file__).parent.parent


def setup_logging(log_level: str = "INFO") -> None:
    """
    Setup logging configuration.
    
    Args:
        log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('contract_api.log')
        ]
    )
