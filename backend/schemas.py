from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime

class UserCreate(BaseModel):
    username: str

class UserOut(BaseModel):
    id: int
    username: str
    created_at: datetime

    class Config:
        orm_mode = True

class GameStart(BaseModel):
    user_id: int

class GameStateOut(BaseModel):
    id: int
    user_id: int
    current_puzzle_id: str
    inventory: List[str]
    score: int
    hints_used_total: int
    is_completed: bool
    started_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class PuzzleOut(BaseModel):
    id: str
    title: str
    description: str
    puzzle_type: str
    points: int
    required_items: List[str] = []

class PuzzleDetailOut(PuzzleOut):
    hints_available: int
    hints_used: int

class SolveRequest(BaseModel):
    answer: Any
    item_used: Optional[str] = None

class SolveResponse(BaseModel):
    success: bool
    message: str
    points_awarded: int = 0
    next_puzzle: Optional[PuzzleOut] = None
    updated_inventory: List[str] = []
    updated_score: int = 0
    is_game_completed: bool = False

class HintResponse(BaseModel):
    success: bool
    hint_text: Optional[str] = None
    message: str = ""
    hints_remaining: int = 0
