# 🎯 Interview Guide: User Management API

## 🚀 How to Approach This Interview

### **1. Understanding the Problem (5 minutes)**
- **Read carefully**: Understand the requirements and constraints
- **Ask clarifying questions**: Don't assume - clarify business rules and technical requirements
- **Plan your approach**: Think about the architecture before coding

### **2. System Design & Architecture (10 minutes)**
- **Data Models**: Design Pydantic models with proper validation
- **API Design**: Plan RESTful endpoints with proper HTTP methods
- **Storage Strategy**: Choose between in-memory, file-based, or database
- **Error Handling**: Plan for validation errors, not found, and server errors

### **3. Implementation (35 minutes)**
- **Phase 1 (20 min)**: Core CRUD operations and basic validation
- **Phase 2 (10 min)**: Error handling and edge cases
- **Phase 3 (5 min)**: Testing and documentation

### **4. Testing & Demo (10 minutes)**
- **Unit Tests**: Test your models and business logic
- **API Tests**: Test endpoints with different scenarios
- **Demo**: Show the working API with examples

---

## 🔍 Clarifying Questions to Ask

### **Business Requirements**
1. **User Constraints**: 
   - Should emails be unique across all users?
   - Are there age restrictions (minimum/maximum)?
   - Any name format requirements?

2. **Data Persistence**: 
   - Should data persist between API restarts?
   - Expected data volume (hundreds vs millions of users)?

3. **Search & Filtering**: 
   - Do we need search by name/email?
   - Should we support filtering by age range?

### **Technical Requirements**
1. **Performance**: 
   - Expected concurrent users?
   - Response time requirements?
   - Any rate limiting needed?

2. **Security**: 
   - Basic authentication required?
   - Input sanitization requirements?

3. **Monitoring**: 
   - Health check endpoints needed?
   - Logging requirements?

---

## 🏗️ Architecture Decisions & Trade-offs

### **1. Data Storage Choice**
```python
# Option 1: In-Memory (Current Implementation)
class InMemoryUserDB:
    def __init__(self):
        self._users: Dict[int, User] = {}
        self._next_id: int = 1
        self._lock = threading.Lock()

# Pros: Fast, simple, no external dependencies
# Cons: Data lost on restart, memory constraints, not scalable

# Option 2: File-based Storage
import json
class FileUserDB:
    def save_to_file(self):
        with open('users.json', 'w') as f:
            json.dump(self._users, f)

# Pros: Persistent, simple
# Cons: Not concurrent-safe, file corruption risk

# Option 3: Database (PostgreSQL/MySQL)
from sqlalchemy import create_engine
class DatabaseUserDB:
    def __init__(self):
        self.engine = create_engine("postgresql://...")

# Pros: ACID, concurrent-safe, scalable
# Cons: Setup complexity, external dependency
```

### **2. ID Generation Strategy**
```python
# Option 1: Auto-increment (Current)
self._next_id += 1

# Option 2: UUID
import uuid
user_id = str(uuid.uuid4())

# Option 3: Timestamp-based
import time
user_id = int(time.time() * 1000)

# Trade-offs:
# - Auto-increment: Simple, sequential, predictable
# - UUID: Globally unique, no collisions, distributed-friendly
# - Timestamp: Time-ordered, human-readable, potential collisions
```

### **3. Error Handling Strategy**
```python
# Option 1: Custom Exceptions (Current)
class UserNotFoundError(HTTPException):
    def __init__(self, user_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )

# Option 2: Generic Error Handler
@app.exception_handler(Exception)
async def generic_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )

# Trade-offs:
# - Custom: Specific error messages, better debugging
# - Generic: Simpler code, less maintenance
```

---

## 📈 Scaling Considerations

### **Immediate Improvements (Next Sprint)**
```python
# 1. Async/Await Implementation
@app.post("/users/")
async def create_user(user_data: UserCreate):
    # Use async database operations
    user = await user_service.create_user_async(user_data)
    return user

# 2. Connection Pooling
from databases import Database
database = Database("postgresql://...", min_size=5, max_size=20)

# 3. Caching Layer
import redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    # Check cache first
    cached_user = await redis_client.get(f"user:{user_id}")
    if cached_user:
        return json.loads(cached_user)
    
    # Fetch from database
    user = await user_service.get_user(user_id)
    
    # Cache for 5 minutes
    await redis_client.setex(f"user:{user_id}", 300, json.dumps(user.dict()))
    return user
```

### **Medium-term Scaling (Next Quarter)**
```python
# 1. Database Migration
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    age = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# 2. Background Tasks
from celery import Celery
celery_app = Celery('user_tasks', broker='redis://localhost:6379/0')

@celery_app.task
def send_welcome_email(user_id: int):
    # Send welcome email asynchronously
    pass

# 3. API Versioning
from fastapi import APIRouter
v1_router = APIRouter(prefix="/v1")
v2_router = APIRouter(prefix="/v2")

app.include_router(v1_router, tags=["v1"])
app.include_router(v2_router, tags=["v2"])
```

### **Long-term Scaling (Next Year)**
```python
# 1. Microservices Architecture
# user-service/
# ├── app/
# │   ├── main.py          # User CRUD API
# │   ├── models.py        # User models
# │   └── services.py      # User business logic
# ├── Dockerfile
# └── docker-compose.yml

# 2. Load Balancing
# nginx.conf
upstream user_api {
    server user-service-1:8000;
    server user-service-2:8000;
    server user-service-3:8000;
}

# 3. Monitoring & Observability
from prometheus_client import Counter, Histogram
import structlog

# Metrics
user_creation_counter = Counter('user_creation_total', 'Total users created')
user_creation_duration = Histogram('user_creation_duration_seconds', 'User creation time')

# Structured logging
logger = structlog.get_logger()

@app.post("/users/")
async def create_user(user_data: UserCreate):
    start_time = time.time()
    
    try:
        user = await user_service.create_user(user_data)
        user_creation_counter.inc()
        
        duration = time.time() - start_time
        user_creation_duration.observe(duration)
        
        logger.info("user_created", 
                   user_id=user.id, 
                   duration=duration,
                   email=user.email)
        
        return user
    except Exception as e:
        logger.error("user_creation_failed", 
                    error=str(e), 
                    email=user_data.email)
        raise
```

---

## 🧪 Testing Strategy

### **Unit Tests (Models & Services)**
```python
def test_user_creation_duplicate_email():
    """Test user creation with duplicate email fails"""
    # Arrange
    user1 = UserCreate(name="John", email="john@example.com")
    user2 = UserCreate(name="Jane", email="john@example.com")
    
    # Act
    UserService.create_user(user1)
    
    # Assert
    with pytest.raises(UserAlreadyExistsError):
        UserService.create_user(user2)
```

### **Integration Tests (API Endpoints)**
```python
def test_create_user_endpoint():
    """Test user creation endpoint"""
    response = client.post("/users/", json={
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30
    })
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"
```

### **Performance Tests**
```python
import asyncio
import time

async def load_test():
    """Test API performance under load"""
    start_time = time.time()
    
    # Create 100 users concurrently
    tasks = []
    for i in range(100):
        user_data = {
            "name": f"User {i}",
            "email": f"user{i}@example.com",
            "age": 20 + i
        }
        task = client.post("/users/", json=user_data)
        tasks.append(task)
    
    results = await asyncio.gather(*tasks)
    duration = time.time() - start_time
    
    print(f"Created 100 users in {duration:.2f} seconds")
    print(f"Average: {duration/100:.3f} seconds per user")
```

---

## 🎯 Success Criteria Checklist

### **Core Requirements (Must Have)**
- ✅ All CRUD endpoints working correctly
- ✅ Proper input validation with Pydantic
- ✅ Correct HTTP status codes
- ✅ Error handling for edge cases
- ✅ Clean, readable code structure

### **Bonus Points (Nice to Have)**
- ✅ Async/await implementation
- ✅ Comprehensive test coverage
- ✅ API documentation (OpenAPI/Swagger)
- ✅ Pagination for list endpoints
- ✅ Search functionality
- ✅ Health check endpoint
- ✅ Proper logging

### **Advanced Features (Extra Credit)**
- ✅ Database integration
- ✅ Caching layer
- ✅ Rate limiting
- ✅ Authentication/Authorization
- ✅ Performance monitoring
- ✅ Docker containerization

---

## 🚀 Running the Project

### **Quick Start**
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the API
uvicorn app.main:app --reload

# 3. Access documentation
open http://localhost:8000/docs

# 4. Run tests
pytest tests/
```

### **Example API Usage**
```bash
# Create a user
curl -X POST "http://localhost:8000/users/" \
     -H "Content-Type: application/json" \
     -d '{"name": "John Doe", "email": "john@example.com", "age": 30}'

# Get all users
curl "http://localhost:8000/users/"

# Get specific user
curl "http://localhost:8000/users/1"

# Update user
curl -X PUT "http://localhost:8000/users/1" \
     -H "Content-Type: application/json" \
     -d '{"name": "John Updated"}'

# Delete user
curl -X DELETE "http://localhost:8000/users/1"
```

---

## 💡 Key Takeaways for the Interview

1. **Start Simple**: Begin with in-memory storage, add complexity later
2. **Think About Scale**: Always consider how your solution would scale
3. **Test Everything**: Write tests for happy path and edge cases
4. **Document Your Decisions**: Explain why you made certain choices
5. **Show Your Process**: Walk through your thinking, not just the code
6. **Ask Questions**: Show you're thinking about the business requirements
7. **Plan for Failure**: Consider error cases and edge conditions

Remember: **It's not about building the perfect solution in 1 hour. It's about showing your problem-solving approach, code quality, and understanding of modern web development practices.**
