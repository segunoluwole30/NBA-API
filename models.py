from database import Base
from sqlalchemy import Column, Integer, String, Float
from pydantic import BaseModel, EmailStr


class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    position = Column(String(50), nullable=False)
    team = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    points_per_game = Column(Float, nullable=False)
    assists_per_game = Column(Float, nullable=False)
    rebounds_per_game = Column(Float, nullable=False)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)


# Pydantic models
class RegisterUser(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginUser(BaseModel):
    username: str
    password: str
