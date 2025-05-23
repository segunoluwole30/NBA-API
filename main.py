from fastapi import FastAPI, Depends
from database import SessionLocal
from models import Player
from sqlalchemy.orm import Session

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/players")
def read_players(db: Session = Depends(get_db)):
    return db.query(Player).all()