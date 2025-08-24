#!/usr/bin/env python3
"""
Batch User Update Applier

This script reads users.json and updates.json, applies updates to matching users,
and writes the result to updated_users.json.

Author: [Your Name]
Date: [Current Date]

PROBLEM: Apply batch updates to user data based on user_id
SOLUTION: Merge update data with existing user data, preserving unchanged fields
"""

import json
from typing import List, Dict, Any


def load_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Load data from a JSON file.
    
    Args:
        file_path (str): Path to the JSON file
        
    Returns:
        List[Dict[str, Any]]: List of dictionaries from the JSON file
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    
    TODO: Implement this function
    - Open and read the JSON file
    - Parse the JSON content
    - Return the parsed data
    - Handle potential errors (file not found, invalid JSON)
    """
    # YOUR CODE HERE
    # Hint: Use json.load() with a file object
    # Hint: Use 'with open()' for proper file handling
    try:
        with open(file_path,'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"User file not found:{file_path}")
    except json.JSONDecodeError:
        raise json.JSONDecodeError(f"Invalid JSON format in file:{file_path}")
    except Exception as e:
        raise Exception(f"Error loading users:{str(e)}")


def save_json_file(data: List[Dict[str, Any]], file_path: str) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data (List[Dict[str, Any]]): Data to save
        file_path (str): Path where to save the JSON file
        
    Raises:
        IOError: If there's an error writing to the file
    
    TODO: Implement this function
    - Open a file for writing
    - Convert the data to JSON format
    - Write the JSON to the file
    - Handle potential I/O errors
    """
    # YOUR CODE HERE
    # Hint: Use json.dump() with a file object
    # Hint: Use 'with open()' for proper file handling
    # Hint: Consider using json.dumps() with indent for pretty formatting
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    except IOError as e:
        raise IOError(f"Error writing to file {file_path}: {str(e)}")
    except Exception as e:
        raise Exception(f"Unexpected error saving users: {str(e)}")


def find_user_by_id(users: List[Dict[str, Any]], user_id: str) -> Dict[str, Any] | None:
    """
    Find a user in the users list by their user_id.
    
    Args:
        users (List[Dict[str, Any]]): List of user dictionaries
        user_id (str): The user_id to search for
        
    Returns:
        Dict[str, Any] | None: The user dictionary if found, None otherwise
    
    TODO: Implement this function
    - Iterate through the users list
    - Check if each user's user_id matches the search user_id
    - Return the matching user or None if not found
    
    Example:
        find_user_by_id(users, "U1") should return the user with user_id "U1"
    """
    # YOUR CODE HERE
    # Hint: Use a for loop to iterate through users
    # Hint: Check if user['user_id'] == user_id
    # Hint: Return the user if found, None if not found
    for user in users:
        if user['user_id'] == user_id:
            return user
    return None


def apply_update_to_user(user: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
    """
    Apply an update to a user, preserving existing fields and adding/updating new ones.
    
    Args:
        user (Dict[str, Any]): The original user dictionary
        update (Dict[str, Any]): The update dictionary (contains user_id and fields to update)
        
    Returns:
        Dict[str, Any]: The updated user dictionary
        
    TODO: Implement this function
    - Create a copy of the original user
    - Update the copy with new values from the update
    - Preserve all existing fields that aren't being updated
    - Return the updated user
    
    Business Rules:
    - Don't modify the original user dictionary
    - Update only the fields specified in the update
    - Keep all other fields unchanged
    """
    # YOUR CODE HERE
    # Hint: Create a copy of the user: updated_user = user.copy()
    # Hint: Use update() method or loop through update fields
    # Hint: Skip the user_id field (it's just for matching)
    # Hint: Return the updated user
    updated_user = user.copy()
    for key, value in update.items():
        if key != 'user_id':
            updated_user[key] = value
    return updated_user


def apply_batch_updates(users: List[Dict[str, Any]], updates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Apply all updates to the users list.
    
    Args:
        users (List[Dict[str, Any]]): List of user dictionaries
        updates (List[Dict[str, Any]]): List of update dictionaries
        
    Returns:
        List[Dict[str, Any]]: List of updated users
        
    TODO: Implement this function
    - Create a new list to store updated users
    - For each update, find the matching user by user_id
    - Apply the update to the user
    - Add the updated user to the new list
    - Handle cases where user_id doesn't exist
    
    Business Rules:
    - Only update users that exist (matching user_id)
    - Skip updates for non-existent users
    - Preserve the order of users
    - Return a new list (don't modify the original)
    """
    # YOUR CODE HERE
    # Hint: Create a new list: updated_users = []
    # Hint: Loop through each update
    # Hint: Use find_user_by_id() to find matching user
    # Hint: Use apply_update_to_user() to apply the update
    # Hint: Add updated user to the new list
    # Hint: Handle cases where user is not found
    updated_users = []
    
    for user in users:
        # Check if this user has any updates
        user_updates = [update for update in updates if update['user_id'] == user['user_id']]
        
        if user_updates:
            # Apply all updates for this user
            updated_user = user.copy()
            for update in user_updates:
                updated_user = apply_update_to_user(updated_user, update)
            updated_users.append(updated_user)
        else:
            # No updates for this user, keep as is
            updated_users.append(user)
    
    return updated_users


def main():
    """
    Main function to execute the batch user update process.
    
    This function orchestrates the entire process:
    1. Load users from users.json
    2. Load updates from updates.json
    3. Apply updates to users
    4. Save updated users to updated_users.json
    5. Provide summary of changes made
    """
    users_file = "users.json"
    updates_file = "updates.json"
    output_file = "updated_users.json"
    
    try:
        # Step 1: Load users
        print(f"📁 Loading users from {users_file}...")
        users = load_json_file(users_file)
        print(f"✅ Loaded {len(users)} users")
        
        # Step 2: Load updates
        print(f"📁 Loading updates from {updates_file}...")
        updates = load_json_file(updates_file)
        print(f"✅ Loaded {len(updates)} updates")
        
        # Step 3: Apply updates
        print("🔄 Applying batch updates...")
        updated_users = apply_batch_updates(users, updates)
        
        # Step 4: Save updated users
        print(f"💾 Saving updated users to {output_file}...")
        save_json_file(updated_users, output_file)
        
        # Step 5: Print summary
        print(f"\n📊 Summary of Changes:")
        print(f"   • Total users processed: {len(users)}")
        print(f"   • Total updates applied: {len(updates)}")
        
        # Count how many users were actually updated
        updated_count = 0
        for i, user in enumerate(users):
            if updated_users[i] != user:
                updated_count += 1
        
        print(f"   • Users updated: {updated_count}")
        print(f"\n🎉 Success! Check {output_file} for updated users.")
        
    except FileNotFoundError as e:
        print(f"❌ Error: File not found - {e}")
        print("   Make sure users.json and updates.json exist in the current directory")
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in input file - {e}")
        print("   Check that your JSON files contain valid JSON format")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("   Check your implementation for bugs")


if __name__ == "__main__":
    main()
