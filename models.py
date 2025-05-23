from database import Base, engine
from sqlalchemy import Column, Integer, String, Float


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

try:
    Base.metadata.create_all(engine)
    print("Database tables created successfully.")
except Exception as e:
    print(f"Error creating database tables: {e}")