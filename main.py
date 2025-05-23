from fastapi import FastAPI, Depends
from database import SessionLocal
from models import Player
from sqlalchemy.orm import Session
from sqlalchemy import func

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

@app.get("/players/{player_name}")
def read_player(player_name: str, db: Session = Depends(get_db)):
    player = db.query(Player).filter(func.lower(Player.name) == player_name.lower()).first()
    if player:
        return player
    else:
        return {"error": "Player not found"}