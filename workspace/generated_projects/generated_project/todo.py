from pydantic import BaseModel
from typing import List

class Todo(BaseModel):
    id: int
    title: str
    completed: bool