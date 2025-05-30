from fastapi import FastAPI, Depends
from database import SessionLocal
from models import Player, User
from sqlalchemy.orm import Session
from sqlalchemy import func
from passlib.hash import sha256_crypt
from models import RegisterUser, LoginUser

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
    
@app.post("/register")
def register_user(user: RegisterUser, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(func.lower(User.username) == user.username.lower()).first()
    if existing_user:
        return {"error": "Username already exists"}
    hashed_password = sha256_crypt.hash(user.password)
    new_user = User(username=user.username, email=user.email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully", "user_id": new_user.id}

@app.post("/login")
def login_user(user: LoginUser, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(func.lower(User.username) == user.username.lower()).first()
    if db_user and sha256_crypt.verify(user.password, db_user.password_hash):
        return {"message": "Login successful", "user_id": db_user.id}
    else:
        return {"error": "Invalid username or password"}
@app.get("/")
def read_root():
    return {"message": "Welcome to the Basketball API. Use /players to get player data."}

        