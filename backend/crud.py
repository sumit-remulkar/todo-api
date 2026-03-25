from sqlalchemy.orm import Session
from backend import models, schemas
from backend.auth import hash_password

def get_todo(db: Session, todo_id: int):
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()

def get_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Todo).offset(skip).limit(limit).all()

def create_todo(db: Session, todo: schemas.TodoCreate):
    db_todo = models.Todo(
        title=todo.title,
        description=todo.description,
        priority=todo.priority
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def create_user(db: Session, username: str, password: str):
    user = models.User(
        username=username,
        password=hash_password(password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()
