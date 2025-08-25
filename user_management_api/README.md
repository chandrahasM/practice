# 🚀 User Management REST API - Interview Coding Challenge

## 📋 Problem Statement

You are tasked with building a **User Management REST API** that demonstrates proficiency in modern Python web development using FastAPI and Pydantic. This API should handle basic CRUD operations for user entities while showcasing best practices in API design, data validation, and error handling.

## 🎯 Core Requirements

### 1. **API Endpoints**
- `POST /users/` - Create a new user
- `GET /users/{user_id}` - Retrieve a specific user
- `GET /users/` - List all users (with optional pagination)
- `PUT /users/{user_id}` - Update an existing user
- `DELETE /users/{user_id}` - Remove a user

### 2. **Data Model Requirements**
- **Required Fields**: `name` (string), `email` (valid email format)
- **Optional Fields**: `age` (positive integer)
- **Auto-generated**: `id` (unique identifier), `created_at` (timestamp), `updated_at` (timestamp)

### 3. **Technical Requirements**
- FastAPI framework with Pydantic models
- Request/response validation
- Proper HTTP status codes and error handling
- In-memory data storage (Python dictionary/list)
- JSON input/output format

## 🏗️ Architecture & Design Decisions

### **Data Models (Pydantic)**
```python
# Base user model for input validation
class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: Optional[int] = Field(None, gt=0, le=150)

# Complete user model with auto-generated fields
class User(UserCreate):
    id: int
    created_at: datetime
    updated_at: datetime
```

### **Storage Strategy**
- **In-Memory Storage**: Python dictionary with user ID as key
- **Atomic Operations**: Thread-safe operations for concurrent access
- **ID Generation**: Auto-incrementing counter for unique identifiers

### **Error Handling Strategy**
- **Validation Errors**: 422 Unprocessable Entity for invalid input
- **Not Found**: 404 for missing resources
- **Server Errors**: 500 for unexpected issues
- **Detailed Error Messages**: JSON responses with error details

## 🔍 Clarifying Questions to Ask

### **Functional Requirements**
1. **User Constraints**: Are there any business rules for user creation? (e.g., unique emails, minimum age)
2. **Data Persistence**: Should data persist between API restarts or is in-memory sufficient?
3. **Search & Filtering**: Do we need search by name/email or filtering by age?
4. **Bulk Operations**: Should we support bulk user creation/deletion?

### **Technical Requirements**
1. **Authentication**: Is basic auth or JWT required for this MVP?
2. **Rate Limiting**: Should we implement API rate limiting?
3. **Logging**: What level of request/response logging is needed?
4. **Testing**: Should we include unit tests and integration tests?

### **Performance Requirements**
1. **Expected Load**: How many concurrent users should the API handle?
2. **Response Time**: Any specific latency requirements?
3. **Data Volume**: Expected number of users to store?

## 🚀 Implementation Approach

### **Phase 1: Core API (30-40 minutes)**
1. Set up FastAPI project structure
2. Define Pydantic models
3. Implement basic CRUD endpoints
4. Add error handling and validation

### **Phase 2: Enhancement (15-20 minutes)**
1. Add pagination for GET /users/
2. Implement proper HTTP status codes
3. Add request/response logging
4. Basic input sanitization

### **Phase 3: Polish (5-10 minutes)**
1. Add API documentation (OpenAPI/Swagger)
2. Implement health check endpoint
3. Add basic error logging
4. Code cleanup and comments

## 📈 Scaling Considerations

### **Immediate Improvements**
- **Async/Await**: Convert to async endpoints for better concurrency
- **Connection Pooling**: Implement connection pooling for external services
- **Caching**: Add Redis caching for frequently accessed users
- **Database**: Migrate from in-memory to PostgreSQL/MySQL

### **Advanced Scaling**
- **Microservices**: Split into user-service, auth-service, etc.
- **Load Balancing**: Implement horizontal scaling with multiple instances
- **Message Queues**: Use Celery/RabbitMQ for background tasks
- **Monitoring**: Add Prometheus metrics and Grafana dashboards

### **Performance Optimizations**
- **Database Indexing**: Optimize queries with proper indexes
- **API Versioning**: Implement versioning strategy
- **Compression**: Enable gzip compression for responses
- **CDN**: Use CDN for static assets

## 🧪 Testing Strategy

### **Unit Tests**
- Pydantic model validation
- Business logic functions
- Error handling scenarios

### **Integration Tests**
- API endpoint testing
- Request/response validation
- Error status codes

### **Performance Tests**
- Load testing with multiple concurrent requests
- Memory usage monitoring
- Response time benchmarks

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [REST API Best Practices](https://restfulapi.net/)
- [Python Async Programming](https://docs.python.org/3/library/asyncio.html)

## 🎯 Success Criteria

- ✅ All CRUD endpoints working correctly
- ✅ Proper input validation and error handling
- ✅ Clean, readable, and well-documented code
- ✅ FastAPI automatic documentation working
- ✅ Basic error logging implemented
- ✅ Code follows Python best practices (PEP 8)

## 🚀 Getting Started

1. Install dependencies: `pip install -r requirements.txt`
2. Run the API: `uvicorn app.main:app --reload`
3. Access documentation: `http://localhost:8000/docs`
4. Run tests: `pytest tests/`

---

**Time Allocation**: 1 hour total
- **Setup & Core API**: 40 minutes
- **Enhancement**: 15 minutes  
- **Testing & Polish**: 5 minutes

**Bonus Points**: Async implementation, comprehensive testing, performance monitoring
