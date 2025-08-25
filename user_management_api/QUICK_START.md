# 🚀 Quick Start Guide

## ⚡ Get Up and Running in 5 Minutes

### **Option 1: Automatic Setup (Recommended)**
```bash
# Make sure you're in the user_management_api directory
cd user_management_api

# Run the automatic setup script
./install.sh
```

### **Option 2: Manual Setup**
```bash
# 1. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies (NOTE: -r comes BEFORE requirements.txt)
pip install -r requirements.txt

# 3. Run the API server
uvicorn app.main:app --reload
```

### **3. Access the API**
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## 🧪 Run Tests
```bash
# Run all tests
python run_tests.py

# Or run specific test files
python -m pytest tests/test_models.py -v
python -m pytest tests/test_services.py -v
python -m pytest tests/test_api.py -v
```

---

## 📝 Example API Usage

### **Create a User**
```bash
curl -X POST "http://localhost:8000/users/" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Doe",
       "email": "john@example.com",
       "age": 30
     }'
```

### **Get All Users**
```bash
curl "http://localhost:8000/users/"
```

### **Get Specific User**
```bash
curl "http://localhost:8000/users/1"
```

### **Update User**
```bash
curl -X PUT "http://localhost:8000/users/1" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "John Updated",
       "age": 31
     }'
```

### **Delete User**
```bash
curl -X DELETE "http://localhost:8000/users/1"
```

### **Search Users**
```bash
curl "http://localhost:8000/users/search/?q=john"
```

### **Get User Statistics**
```bash
curl "http://localhost:8000/users/stats/"
```

---

## 🔧 Project Structure
```
user_management_api/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # FastAPI application & endpoints
│   ├── models.py            # Pydantic data models
│   ├── database.py          # In-memory database layer
│   ├── services.py          # Business logic layer
│   └── exceptions.py        # Custom exception classes
├── tests/
│   ├── __init__.py          # Test package
│   ├── test_models.py       # Model validation tests
│   ├── test_services.py     # Business logic tests
│   └── test_api.py          # API endpoint tests
├── requirements.txt          # Python dependencies
├── setup.py                 # Package setup script
├── install.sh               # Automatic installation script
├── README.md                # Comprehensive documentation
├── INTERVIEW_GUIDE.md       # Interview preparation guide
├── QUICK_START.md           # This file
├── run_tests.py             # Test runner script
└── sample_data.json         # Sample user data
```

---

## 🎯 Key Features

- ✅ **Full CRUD Operations**: Create, Read, Update, Delete users
- ✅ **Input Validation**: Pydantic models with comprehensive validation
- ✅ **Error Handling**: Proper HTTP status codes and error messages
- ✅ **Pagination**: Support for large user lists
- ✅ **Search**: Find users by name or email
- ✅ **Statistics**: User analytics and insights
- ✅ **Thread Safety**: Concurrent access support
- ✅ **API Documentation**: Auto-generated OpenAPI/Swagger docs
- ✅ **Comprehensive Testing**: Unit, service, and API tests

---

## 🚨 Common Issues & Solutions

### **Port Already in Use**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
uvicorn app.main:app --reload --port 8001
```

### **Import Errors**
```bash
# Make sure you're in the right directory
cd user_management_api

# Make sure virtual environment is activated
source venv/bin/activate

# Install dependencies (correct command)
pip install -r requirements.txt
```

### **Test Failures**
```bash
# Clear database state
python -c "from app.database import user_db; user_db.clear()"

# Run tests again
python run_tests.py
```

### **Permission Denied on install.sh**
```bash
# Make the script executable
chmod +x install.sh

# Then run it
./install.sh
```

---

## 🔍 Next Steps

1. **Explore the API**: Use the interactive docs at `/docs`
2. **Run Tests**: Ensure everything works with `python run_tests.py`
3. **Read Documentation**: Check `README.md` and `INTERVIEW_GUIDE.md`
4. **Customize**: Modify models, add new endpoints, or enhance validation
5. **Scale Up**: Consider database integration, caching, or async operations

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [Python Testing with pytest](https://docs.pytest.org/)
- [REST API Best Practices](https://restfulapi.net/)

---

**Happy Coding! 🎉**
