from fastapi import APIRouter, HTTPException
from schemas import PuzzleOut
from puzzles_data import PUZZLES

router = APIRouter()

@router.get("/", response_model=list[PuzzleOut])
def list_puzzles():
    return PUZZLES

@router.get("/{puzzle_id}", response_model=PuzzleOut)
def get_puzzle_by_id(puzzle_id: str):
    for p in PUZZLES:
        if p["id"] == puzzle_id:
            return p
    raise HTTPException(status_code=404, detail="Puzzle not found")
