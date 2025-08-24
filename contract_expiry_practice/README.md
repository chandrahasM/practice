# Contract Expiry Status Updater - Practice Problem

## 🎯 Problem Statement

You are building a **Contract Lifecycle Management System** similar to Ironclad or DocuSign. Your task is to implement a script that automatically identifies and updates contract statuses based on their expiry dates.

### What You Need to Build

Create a Python script that:
1. **Reads** a JSON file containing contract data
2. **Analyzes** each contract's expiry date
3. **Updates** the status to "expiring_soon" for contracts expiring within 30 days
4. **Writes** the updated data to a new JSON file

### Why This Matters

In real contract management systems, teams need advance notice about expiring contracts to:
- Negotiate renewals
- Review terms and conditions
- Ensure business continuity
- Comply with legal requirements

---

## 📋 Sample Data

### Input: `contracts.json`
```json
[
  {"contract_id": "C001", "company": "Acme Corp", "status": "active", "expiry_date": "2025-01-15"},
  {"contract_id": "C002", "company": "BetaCo", "status": "active", "expiry_date": "2026-01-01"},
  {"contract_id": "C003", "company": "Gamma Inc", "status": "active", "expiry_date": "2025-01-20"}
]
```

### Expected Output: `updated_contracts.json`
```json
[
  {"contract_id": "C001", "company": "Acme Corp", "status": "expiring_soon", "expiry_date": "2025-01-15"},
  {"contract_id": "C002", "company": "BetaCo", "status": "active", "expiry_date": "2026-01-01"},
  {"contract_id": "C003", "company": "Gamma Inc", "status": "expiring_soon", "expiry_date": "2025-01-20"}
]
```

---

## 🤔 Implementation Questions to Think About

### 1. Date Handling
- How will you parse the date string "2025-01-15"?
- How do you calculate "30 days from today"?
- What happens if a date is invalid or in wrong format?

### 2. Data Processing
- How will you iterate through the contract list?
- How do you update only specific contracts without affecting others?
- How do you preserve all existing data while changing only the status?

### 3. File Operations
- How do you read JSON from a file?
- How do you write JSON back to a file?
- What if the input file doesn't exist or is corrupted?

### 4. Business Logic
- Should you update contracts with status "draft" or "terminated"?
- What if a contract expires today (0 days remaining)?
- How do you handle edge cases like leap years?

---

## 🚀 Getting Started

### Step 1: Understand the Requirements
- Contracts with status "active" that expire within 30 days → change to "expiring_soon"
- All other contracts remain unchanged
- 30-day threshold includes the current day
- Preserve all contract data (contract_id, company, expiry_date)

### Step 2: Plan Your Approach
1. **Load data** from JSON file
2. **Parse dates** and calculate days until expiry
3. **Apply business rules** to determine status updates
4. **Save results** to new JSON file

### Step 3: Implement Step by Step
- Start with the simplest function (like `load_contracts`)
- Test each function individually
- Build up to the complete solution

---

## 📁 File Structure

```
contract_expiry_practice/
├── README.md                 # This file
├── contracts.json            # Sample input data
├── contract_updater.py       # Main script (YOUR CODE GOES HERE)
├── test_contract_updater.py  # Test suite
└── requirements.txt          # Dependencies
```

---

## 🧪 Testing Your Solution

### Run Tests
```bash
python test_contract_updater.py
```

### Run Main Script
```bash
python contract_updater.py
```

### Expected Behavior
- Script should read `contracts.json`
- Update appropriate contract statuses
- Create `updated_contracts.json`
- Show summary of changes made

---

## 💡 Interview Tips

### When Explaining Your Solution
1. **Start with the problem** - "I need to identify contracts expiring soon"
2. **Break it down** - "First I'll load data, then process dates, then update statuses"
3. **Consider edge cases** - "What if dates are invalid? What if files are missing?"
4. **Discuss testing** - "I'll test with various date scenarios and invalid data"

### Key Skills to Demonstrate
- **Date manipulation** with Python's datetime
- **JSON file handling** with proper error handling
- **Data transformation** while maintaining data integrity
- **Business logic implementation** with clear, readable code

---

## 🎯 Success Criteria

Your solution is successful when:
✅ All contracts expiring within 30 days have status "expiring_soon"  
✅ All other contracts remain unchanged  
✅ Input and output files maintain the same structure  
✅ Script handles errors gracefully (invalid dates, missing files)  
✅ Code is readable and well-commented  

---

## 🚨 Common Pitfalls to Avoid

- **Hardcoding dates** - Use current date, not fixed dates
- **Ignoring timezone** - Consider if dates are in local time or UTC
- **Overwriting original data** - Always create a new output file
- **Missing error handling** - Plan for file I/O and data validation errors

---

**Good luck! This is a great problem that demonstrates real-world software engineering skills. 🚀**
