from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import *
from puzzle_engine import PuzzleEngine
from models import User, GameState
from puzzles_data import get_puzzle

router = APIRouter()

@router.post("/start", response_model=GameStateOut)
def start_game(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        db_user = User(username=user.username)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    engine = PuzzleEngine(db)
    game = engine.start_new_game(db_user.id)
    return game

@router.get("/{game_id}", response_model=GameStateOut)
def get_game(game_id: int, db: Session = Depends(get_db)):
    game = db.query(GameState).filter(GameState.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

@router.get("/{game_id}/puzzle", response_model=PuzzleDetailOut)
def get_current_puzzle(game_id: int, db: Session = Depends(get_db)):
    game = db.query(GameState).filter(GameState.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    if game.is_completed:
        raise HTTPException(status_code=400, detail="Game already completed")
    puzzle = get_puzzle(game.current_puzzle_id)
    if not puzzle:
        raise HTTPException(status_code=404, detail="Puzzle not found")
    engine = PuzzleEngine(db)
    hints_used = engine.get_used_hints(game_id, puzzle["id"])
    hints_available = len(puzzle["hints"]) - hints_used
    return {
        **puzzle,
        "hints_available": hints_available,
        "hints_used": hints_used,
    }

@router.post("/{game_id}/solve", response_model=SolveResponse)
def solve_puzzle(game_id: int, solve_req: SolveRequest, db: Session = Depends(get_db)):
    game = db.query(GameState).filter(GameState.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    if game.is_completed:
        return {"success": False, "message": "Game already completed"}
    engine = PuzzleEngine(db)
    result = engine.check_answer(game, solve_req.answer, solve_req.item_used)
    return result

@router.post("/{game_id}/hint", response_model=HintResponse)
def get_hint(game_id: int, db: Session = Depends(get_db)):
    game = db.query(GameState).filter(GameState.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    if game.is_completed:
        return {"success": False, "message": "Game already completed", "hint_text": None, "hints_remaining": 0}
    engine = PuzzleEngine(db)
    return engine.use_hint(game)
