from pydantic import BaseModel
from backend.database import Base

class Post(BaseModel):
    id: int
    title: str
    content: str
    created_at: str
    updated_at: str

class User(BaseModel):
    id: int
    username: str
    email: str

# backend/models.py
from sqlalchemy import Column, Integer, String, Text


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String(50), default="medium")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    password = Column(String(200))