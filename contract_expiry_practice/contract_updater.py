#!/usr/bin/env python3
"""
Contract Expiry Status Updater

This script updates contract statuses to "expiring_soon" for contracts
that expire within the next 30 days.

Author: [Your Name]
Date: [Current Date]

PROBLEM: Update contract statuses based on expiry dates
SOLUTION: Identify contracts expiring within 30 days and mark them as "expiring_soon"
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict, Any


def load_contracts(file_path: str) -> List[Dict[str, Any]]:
    """
    Load contracts from a JSON file.
    
    Args:
        file_path (str): Path to the JSON file containing contracts
        
    Returns:
        List[Dict[str, Any]]: List of contract dictionaries
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    
    TODO: Implement this function
    - Open and read the JSON file
    - Parse the JSON content
    - Return the list of contracts
    - Handle potential errors (file not found, invalid JSON)
    """
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Contract file not found: {file_path}")
    except json.JSONDecodeError:
        raise json.JSONDecodeError(f"Invalid JSON format in file: {file_path}")
    except Exception as e:
        raise Exception(f"Error loading contracts: {str(e)}")


def save_contracts(contracts: List[Dict[str, Any]], file_path: str) -> None:
    """
    Save contracts to a JSON file.
    
    Args:
        contracts (List[Dict[str, Any]]): List of contract dictionaries to save
        file_path (str): Path where to save the JSON file
        
    Raises:
        IOError: If there's an error writing to the file
    
    TODO: Implement this function
    - Open a file for writing
    - Convert the contracts list to JSON format
    - Write the JSON to the file
    - Handle potential I/O errors
    """
    try:
        with open(file_path, 'w') as f:
            json.dump(contracts, f, indent=2)
    except IOError as e:
        raise IOError(f"Error writing contracts to file {file_path}: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error saving contracts: {str(e)}")
        


def parse_date(date_string: str) -> datetime:
    """
    Parse a date string in ISO format (YYYY-MM-DD).
    
    Args:
        date_string (str): Date string in YYYY-MM-DD format
        
    Returns:
        datetime: Parsed datetime object
        
    Raises:
        ValueError: If the date string is not in valid format
    
    TODO: Implement this function
    - Convert the date string to a datetime object
    - Handle invalid date formats
    - Return the parsed datetime
    
    Example:
        parse_date("2025-01-15") should return datetime(2025, 1, 15)
    """
    # YOUR CODE HERE
    # Hint: Use datetime.strptime() with format string "%Y-%m-%d"
    # Hint: This will raise ValueError if the format is wrong
    return datetime.strptime(date_string, "%Y-%m-%d")


def is_expiring_soon(expiry_date: str, days_threshold: int = 30) -> bool:
    """
    Check if a contract expires within the specified number of days.
    
    Args:
        expiry_date (str): Contract expiry date in YYYY-MM-DD format
        days_threshold (int): Number of days to check (default: 30)
        
    Returns:
        bool: True if contract expires within threshold, False otherwise
    
    TODO: Implement this function
    - Parse the expiry date string
    - Get today's date
    - Calculate the difference in days
    - Return True if within threshold, False otherwise
    
    Business Rules:
    - Include the current day (0 days remaining = expiring soon)
    - Use the days_threshold parameter (default 30)
    """
    # YOUR CODE HERE
    # Hint: Use parse_date() to convert string to datetime
    # Hint: Use datetime.now().date() to get today's date
    # Hint: Calculate difference: (expiry_date - today).days
    # Hint: Return True if difference <= days_threshold
    expiry_date = parse_date(expiry_date).date()
    today = datetime.now().date()
    return 0<=(expiry_date - today).days <= days_threshold


def update_contract_statuses(contracts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Update contract statuses to "expiring_soon" for contracts expiring within 30 days.
    
    Args:
        contracts (List[Dict[str, Any]]): List of contract dictionaries
        
    Returns:
        List[Dict[str, Any]]: Updated list of contracts
    
    TODO: Implement this function
    - Create a new list to store updated contracts
    - Iterate through each contract
    - For each contract, check if it's expiring soon
    - Update status to "expiring_soon" if conditions are met
    - Preserve all other contract data
    
    Business Rules:
    - Only update contracts with status "active"
    - Only update contracts expiring within 30 days
    - Change status to "expiring_soon" for qualifying contracts
    - Leave all other contracts unchanged
    """
    # YOUR CODE HERE
    # Hint: Create a new list: updated_contracts = []
    # Hint: Use a for loop to iterate through contracts
    # Hint: Check contract['status'] == "active" first
    # Hint: Use is_expiring_soon() to check expiry
    # Hint: Create a copy of the contract and update status if needed
    # Hint: Append each contract (original or updated) to the new list
    updated_contracts = []
    for contract in contracts:
        if contract['status'] == "active" and is_expiring_soon(contract['expiry_date']):
            contract['status'] = "expiring_soon"
            updated_contract = contract.copy()  # ✅ CREATE COPY FIRST
            updated_contract['status'] = "expiring_soon"
        updated_contracts.append(contract)
    return updated_contracts


def main():
    """
    Main function to execute the contract status update process.
    
    This function orchestrates the entire process:
    1. Load contracts from input file
    2. Update contract statuses based on business rules
    3. Save updated contracts to output file
    4. Provide summary of changes made
    """
    input_file = "contracts.json"
    output_file = "updated_contracts.json"
    
    try:
        # Step 1: Load contracts
        print(f"📁 Loading contracts from {input_file}...")
        contracts = load_contracts(input_file)
        print(f"✅ Loaded {len(contracts)} contracts")
        
        # Step 2: Update contract statuses
        print("🔄 Updating contract statuses...")
        updated_contracts = update_contract_statuses(contracts)
        
        
        # Step 3: Save updated contracts
        print(f"💾 Saving updated contracts to {output_file}...")
        save_contracts(updated_contracts, output_file)
        
        # Step 4: Print summary
        expiring_soon_count = sum(1 for contract in updated_contracts 
                                if contract.get('status') == 'expiring_soon')
        active_count = sum(1 for contract in updated_contracts 
                          if contract.get('status') == 'active')
        
        print(f"\n📊 Summary of Changes:")
        print(f"   • Contracts marked as 'expiring_soon': {expiring_soon_count}")
        print(f"   • Contracts remaining 'active': {active_count}")
        print(f"   • Total contracts processed: {len(updated_contracts)}")
        print(f"\n🎉 Success! Check {output_file} for updated contracts.")
        
    except FileNotFoundError as e:
        print(f"❌ Error: File not found - {e}")
        print("   Make sure contracts.json exists in the current directory")
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in input file - {e}")
        print("   Check that contracts.json contains valid JSON format")
    except ValueError as e:
        print(f"❌ Error: Invalid date format - {e}")
        print("   Ensure all dates are in YYYY-MM-DD format")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("   Check your implementation for bugs")


if __name__ == "__main__":
    main()
