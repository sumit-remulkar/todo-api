from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend import crud, schemas
from backend.database import SessionLocal
from backend.auth import verify_password, create_access_token, decode_token
from fastapi.security import OAuth2PasswordBearer
from fastapi import Body
from fastapi.security import OAuth2PasswordRequestForm
from backend.database import SessionLocal, init_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Generated Todo API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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
def create_item(todo: schemas.TodoCreate = Body(...), db: Session = Depends(get_db)):
    return crud.create_todo(db, todo)

@app.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user(db, user.username)
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    return crud.create_user(db, user.username, user.password)

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user(db, form_data.username)

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload

@app.get("/protected")
def protected_route(user=Depends(get_current_user)):
    return {"message": f"Hello {user['sub']} 🔥"}

@app.put("/items/{item_id}", response_model=schemas.TodoOut)
def update_item(item_id: int, todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    updated = crud.update_todo(db, item_id, todo)
    if not updated:
        raise HTTPException(status_code=404, detail="Invalid request")
    return updated


@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_todo(db, item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Invalid request")
    return {"message": "Item deleted successfully"}