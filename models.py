from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, JSON, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    games = relationship("GameState", back_populates="user")

class GameState(Base):
    __tablename__ = "game_states"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    current_puzzle_id = Column(String, nullable=False)
    inventory = Column(JSON, default=list)
    score = Column(Integer, default=0)
    hints_used_total = Column(Integer, default=0)
    is_completed = Column(Boolean, default=False)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    user = relationship("User", back_populates="games")
    hint_usages = relationship("HintUsage", back_populates="game", cascade="all, delete-orphan")

class HintUsage(Base):
    __tablename__ = "hint_usages"
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("game_states.id"))
    puzzle_id = Column(String, nullable=False)
    hint_index = Column(Integer, nullable=False)
    used_at = Column(DateTime(timezone=True), server_default=func.now())
    
    game = relationship("GameState", back_populates="hint_usages")
