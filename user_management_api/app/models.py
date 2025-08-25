from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: str
    age: Optional[int] = None

class User(UserCreate):
    id: int
