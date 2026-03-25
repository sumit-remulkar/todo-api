from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend import crud, schemas
from backend.database import SessionLocal, init_db
from backend.auth import verify_password, create_access_token, decode_token
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
app = FastAPI(title="Generated Todo API")

init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Hello - API is up"}

@app.get("/items/", response_model=List[schemas.TodoOut])
def list_items(db: Session = Depends(get_db)):
    return crud.get_todos(db)

@app.get("/items/{item_id}", response_model=schemas.TodoOut)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_todo(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items/", response_model=schemas.TodoOut)
def create_item(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db, todo)

@app.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user(db, user.username)
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    return crud.create_user(db, user.username, user.password)

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user.username)

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload

@app.get("/protected")
def protected_route(user=Depends(get_current_user)):
    return {"message": f"Hello {user['sub']} 🔥"}