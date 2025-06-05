from fastapi import FastAPI, Depends, Request, HTTPException, status, Header
from database import SessionLocal
from models import Player, User
from sqlalchemy.orm import Session
from sqlalchemy import func
from passlib.hash import sha256_crypt
from models import RegisterUser, LoginUser
import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

secret_key = os.environ.get('SECRET_KEY')
print(type(secret_key))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(authorization: str = Header(...), db: Session = Depends(get_db)):
    secret_key = os.environ.get('SECRET_KEY')
    # Check for Authorization header and Bearer token
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header"
        )
    # Extract the token part
    token = authorization.split(" ")[1]
    try:
        # Decode the JWT token
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        username = payload.get("username")
        db.username = db.query(User).filter(func.lower(User.username) == username.lower()).first()
        if not db.username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Username not in database"
            )
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

@app.get("/players")
def read_players(db: Session = Depends(get_db), username: str = Depends(get_current_user)):
    print(f"Request made by user: {username}")
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
        # generate a JWT token
        expire = datetime.now() + timedelta(minutes=1)
        token = jwt.encode({"user_id": db_user.id, "username": db_user.username, "exp": int(expire.timestamp())}, secret_key, algorithm="HS256")
        return {"message": "Login successful", "user_id": db_user.id, "token": token}
    else:
        return {"error": "Invalid username or password"}
@app.get("/")
def read_root():
    return {"message": "Welcome to the Basketball API. Use /players to get player data."}

        