import time

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database.db import SessionLocal, engine, Base
from app.models.item import Item

# Wait for database
time.sleep(10)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Home
@app.get("/")
def home():
    return {"message": "Backend with PostgreSQL is running"}

# Get items
@app.get("/items")
def get_items(db: Session = Depends(get_db)):

    items = db.query(Item).all()

    return items

# Create item
@app.post("/items")
def create_item(item: dict, db: Session = Depends(get_db)):

    new_item = Item(name=item["name"])

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return {
        "message": "Item created",
        "data": {
            "id": new_item.id,
            "name": new_item.name
        }
    }