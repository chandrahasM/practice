# Batch User Update Applier - Practice Problem

## 🎯 Problem Statement

You are building a **User Management System** that needs to apply batch updates to user records. Your task is to implement a script that reads user data and update instructions, then applies those updates while preserving all existing data.

### What You Need to Build

Create a Python script that:
1. **Reads** a JSON file containing user data (`users.json`)
2. **Reads** a JSON file containing update instructions (`updates.json`)
3. **Applies updates** to matching users based on `user_id`
4. **Preserves** all existing user data that isn't being updated
5. **Writes** the updated user list to a new file (`updated_users.json`)

### Why This Matters

In real user management systems, you often need to:
- **Bulk update** user roles, permissions, or contact information
- **Sync data** from external systems (HR, LDAP, etc.)
- **Apply configuration changes** across multiple users
- **Maintain data integrity** while updating specific fields

---

## 📋 Sample Data

### Input: `users.json`
```json
[
  {"user_id": "U1", "name": "Alice", "role": "member", "email": "alice@company.com", "department": "Engineering"},
  {"user_id": "U2", "name": "Bob", "role": "admin", "email": "bob@company.com", "department": "Management"}
]
```

### Input: `updates.json`
```json
[
  {"user_id": "U1", "role": "admin", "department": "Management"},
  {"user_id": "U2", "name": "Robert", "email": "robert@company.com"}
]
```

### Expected Output: `updated_users.json`
```json
[
  {"user_id": "U1", "name": "Alice", "role": "admin", "email": "alice@company.com", "department": "Management"},
  {"user_id": "U2", "name": "Robert", "role": "admin", "email": "robert@company.com", "department": "Management"}
]
```

---

## 🤔 Implementation Questions to Think About

### 1. Data Merging
- How will you combine existing user data with update data?
- What happens if an update contains a field that doesn't exist in the user?
- How do you ensure the original user data isn't modified?

### 2. Key-Based Lookup
- How will you find the correct user to update?
- What if a user_id in updates.json doesn't exist in users.json?
- How do you handle duplicate user_ids?

### 3. Data Preservation
- How do you preserve fields that aren't being updated?
- What happens to the order of users in the list?
- How do you handle nested data structures?

### 4. Error Handling
- What if the JSON files are corrupted or missing?
- What if a user_id is missing from an update?
- How do you handle malformed update data?

---

## 🚀 Getting Started

### Step 1: Understand the Requirements
- Updates are applied based on `user_id` matching
- Only specified fields are updated; others remain unchanged
- Original user data must be preserved (no mutation)
- Handle cases where user_id doesn't exist

### Step 2: Plan Your Approach
1. **Load data** from both JSON files
2. **Find users** by user_id for each update
3. **Apply updates** while preserving existing data
4. **Save results** to new JSON file

### Step 3: Implement Step by Step
- Start with the simplest function (like `load_json_file`)
- Test each function individually
- Build up to the complete solution

---

## 📁 File Structure

```
batch_user_updater_practice/
├── README.md                 # This file
├── users.json                # Sample user data
├── updates.json              # Sample update instructions
├── user_updater.py           # Main script (YOUR CODE GOES HERE)
├── test_user_updater.py      # Test suite
└── requirements.txt          # Dependencies
```

---

## 🧪 Testing Your Solution

### Run Tests
```bash
python test_user_updater.py
```

### Run Main Script
```bash
python user_updater.py
```

### Expected Behavior
- Script should read both input files
- Apply updates to matching users
- Create `updated_users.json` with changes
- Show summary of updates applied

---

## 💡 Interview Tips

### When Explaining Your Solution
1. **Start with the problem** - "I need to merge update data with existing user data"
2. **Break it down** - "First I'll load both files, then find users by ID, then apply updates"
3. **Consider edge cases** - "What if a user_id doesn't exist? What if JSON is malformed?"
4. **Discuss data integrity** - "I'll create copies to avoid mutating original data"

### Key Skills to Demonstrate
- **Dictionary operations** - merging, copying, updating
- **JSON file handling** - reading, parsing, writing
- **Data transformation** - preserving structure while updating fields
- **Error handling** - graceful failure for missing or invalid data

---

## 🎯 Success Criteria

Your solution is successful when:
✅ All users are preserved in the output  
✅ Updates are applied to correct users  
✅ Unchanged fields remain exactly the same  
✅ Output file maintains the same structure  
✅ Script handles errors gracefully  
✅ Code is readable and well-commented  

---

## 🚨 Common Pitfalls to Avoid

- **Mutating original data** - Always create copies before updating
- **Ignoring missing users** - Handle cases where user_id doesn't exist
- **Losing data** - Ensure all fields are preserved unless explicitly updated
- **Poor error handling** - Plan for file I/O and data validation errors

---

## 🎯 Key Concepts to Practice

- **Deep copying** vs shallow copying of dictionaries
- **Key-based lookups** in lists of dictionaries
- **Data merging** strategies
- **Immutable data handling**
- **Batch processing** of data records

---

**Good luck! This problem tests your ability to work with complex data structures while maintaining data integrity. 🚀**
