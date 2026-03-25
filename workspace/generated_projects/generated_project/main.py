from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from typing import List
import models
import database
import auth

app = FastAPI(title="Generated Todo API (Persisted + Auth)")

# initialize DB on import (safe for dev)
database.init_db()

@app.post("/register", tags=["auth"])
def register(username: str, password: str):
    with Session(database.engine) as session:
        statement = select(models.User).where(models.User.username == username)
        exists = session.exec(statement).first()
        if exists:
            raise HTTPException(status_code=400, detail="User already exists")
        user = models.User(username=username, hashed_password=auth.get_password_hash(password))
        session.add(user)
        session.commit()
        session.refresh(user)
        return {"id": user.id, "username": user.username}

@app.post("/token", tags=["auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with Session(database.engine) as session:
        user = auth.authenticate_user(session, form_data.username, form_data.password)
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        access_token = auth.create_access_token({"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer"}

@app.get("/", tags=["root"])
def read_root():
    return {"message": "Hello - API is up"}

# CRUD for todos
from pydantic import BaseModel
class TodoCreate(BaseModel):
    title: str
    description: str | None = None
    priority: str | None = "medium"

class TodoRead(BaseModel):
    id: int
    title: str
    description: str | None = None
    priority: str | None = "medium"
    owner_id: int | None = None

@app.post("/todos/", response_model=TodoRead, status_code=201, tags=["todos"])
def create_todo(payload: TodoCreate, current_user = Depends(auth.get_current_user)):
    with Session(database.engine) as session:
        todo = models.Todo(title=payload.title, description=payload.description, priority=payload.priority, owner_id=current_user.id)
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

@app.get("/todos/", response_model=List[TodoRead], tags=["todos"])
def list_todos(current_user = Depends(auth.get_current_user)):
    with Session(database.engine) as session:
        statement = select(models.Todo).where(models.Todo.owner_id == current_user.id)
        todos = session.exec(statement).all()
        return todos

@app.get("/todos/{todo_id}", response_model=TodoRead, tags=["todos"])
def get_todo(todo_id: int, current_user = Depends(auth.get_current_user)):
    with Session(database.engine) as session:
        todo = session.get(models.Todo, todo_id)
        if not todo or todo.owner_id != current_user.id:
            raise HTTPException(status_code=404, detail="Todo not found")
        return todo

@app.put("/todos/{todo_id}", response_model=TodoRead, tags=["todos"])
def update_todo(todo_id: int, payload: TodoCreate, current_user = Depends(auth.get_current_user)):
    with Session(database.engine) as session:
        todo = session.get(models.Todo, todo_id)
        if not todo or todo.owner_id != current_user.id:
            raise HTTPException(status_code=404, detail="Todo not found")
        todo.title = payload.title
        todo.description = payload.description
        todo.priority = payload.priority
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

@app.delete("/todos/{todo_id}", status_code=204, tags=["todos"])
def delete_todo(todo_id: int, current_user = Depends(auth.get_current_user)):
    with Session(database.engine) as session:
        todo = session.get(models.Todo, todo_id)
        if not todo or todo.owner_id != current_user.id:
            raise HTTPException(status_code=404, detail="Todo not found")
        session.delete(todo)
        session.commit()
        return