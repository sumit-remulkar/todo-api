from pydantic import BaseModel
from typing import Optional

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"

class TodoCreate(TodoBase):
    id: int   

class TodoOut(TodoBase):
    id: int

    class Config:
        from_attributes = True
        
class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str