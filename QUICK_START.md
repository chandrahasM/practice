# 🚀 Quick Start Guide

## Ready to Practice? Here's How to Get Started!

### 📁 Your Practice Environment is Ready!

You now have a complete practice environment with:
- ✅ **Sample data** (`contracts.json`) - 10 contracts with various expiry dates
- ✅ **Main script** (`contract_updater.py`) - Your implementation goes here
- ✅ **Test suite** (`test_contract_updater.py`) - Verify your solution
- ✅ **Simple test runner** (`run_tests.py`) - Quick testing without pytest
- ✅ **Requirements** (`requirements.txt`) - Dependencies needed
- ✅ **Documentation** (`README.md`) - Complete problem description

---

## 🎯 Your Task

**Implement these 5 functions in `contract_updater.py`:**

1. **`load_contracts(file_path)`** - Read JSON file
2. **`save_contracts(contracts, file_path)`** - Write JSON file  
3. **`parse_date(date_string)`** - Convert "2025-01-15" to datetime
4. **`is_expiring_soon(expiry_date, days_threshold=30)`** - Check if contract expires within 30 days
5. **`update_contract_statuses(contracts)`** - Main logic to update statuses

---

## 🚀 Step-by-Step Implementation

### Step 1: Start with the Simplest Function
Open `contract_updater.py` and implement `parse_date()` first:
```python
def parse_date(date_string: str) -> datetime:
    # Convert "2025-01-15" to datetime(2025, 1, 15)
    # Use: datetime.strptime(date_string, "%Y-%m-%d")
    pass
```

### Step 2: Test Incrementally
After each function, test it:
```bash
python run_tests.py
```

### Step 3: Build Up to Complete Solution
- Implement `load_contracts()` and `save_contracts()`
- Implement `is_expiring_soon()`
- Finally implement `update_contract_statuses()`

---

## 🧪 Testing Your Solution

### Quick Test (Recommended for beginners):
```bash
python run_tests.py
```

### Full Test Suite (If you have pytest):
```bash
pip install pytest
python test_contract_updater.py
```

### Run Your Solution:
```bash
python contract_updater.py
```

---

## 💡 Implementation Hints

### Date Handling:
- Use `datetime.strptime(date_string, "%Y-%m-%d")`
- Get today: `datetime.now().date()`
- Calculate difference: `(expiry_date - today).days`

### JSON Operations:
- Read: `json.load(file_object)`
- Write: `json.dump(data, file_object)`
- Use `with open()` for proper file handling

### Business Logic:
- Only update contracts with status "active"
- Only update contracts expiring within 30 days
- Change status to "expiring_soon" for qualifying contracts

---

## 🎯 Success Criteria

Your solution works when:
✅ All tests pass  
✅ Script reads `contracts.json`  
✅ Updates appropriate contract statuses  
✅ Creates `updated_contracts.json`  
✅ Shows summary of changes made  

---

## 🆘 Need Help?

1. **Check the README.md** - Complete problem description
2. **Look at the TODO comments** - Step-by-step guidance in the code
3. **Run tests frequently** - Catch issues early
4. **Start simple** - Implement one function at a time

---

## 🎉 Ready to Code?

Open `contract_updater.py` and start implementing! 

**Remember:** This is practice - take your time, think through each step, and test as you go.

Good luck! 🚀
