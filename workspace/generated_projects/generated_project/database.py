# database.py — use absolute imports so uvicorn main:app works
from sqlmodel import create_engine, SQLModel, Session
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "todo.db")
DATABASE_URL = f"sqlite:///{DB_FILE}"

# echo=False in dev, set True if you want SQL logs
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

def init_db():
    """
    Create DB tables. Import models here using absolute import to avoid
    relative import errors when running main as a script.
    """
    # local import (absolute) to ensure SQLModel classes are registered
    import models  # noqa: F401  - import for SQLModel metadata
    SQLModel.metadata.create_all(engine)

def get_session():
    """
    Dependency generator for FastAPI endpoints:
        def route(session: Session = Depends(database.get_session)): ...
    """
    with Session(engine) as session:
        yield session