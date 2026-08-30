from typing import Any, Dict, Optional
from puzzles_data import get_puzzle
from models import GameState, HintUsage
from sqlalchemy.orm import Session

class PuzzleEngine:
    def __init__(self, db: Session):
        self.db = db

    def start_new_game(self, user_id: int) -> GameState:
        first_puzzle_id = PUZZLES[0]["id"]
        game = GameState(
            user_id=user_id,
            current_puzzle_id=first_puzzle_id,
            inventory=[],
            score=0,
            hints_used_total=0,
            is_completed=False
        )
        self.db.add(game)
        self.db.commit()
        self.db.refresh(game)
        return game

    def get_game_state(self, game_id: int) -> Optional[GameState]:
        return self.db.query(GameState).filter(GameState.id == game_id).first()

    def get_current_puzzle(self, game: GameState) -> Optional[Dict]:
        return get_puzzle(game.current_puzzle_id)

    def get_used_hints(self, game_id: int, puzzle_id: str) -> int:
        return self.db.query(HintUsage).filter(
            HintUsage.game_id == game_id,
            HintUsage.puzzle_id == puzzle_id
        ).count()

    def use_hint(self, game: GameState) -> Dict:
        puzzle = get_puzzle(game.current_puzzle_id)
        if not puzzle:
            return {"success": False, "message": "No active puzzle", "hint_text": None, "hints_remaining": 0}

        used = self.get_used_hints(game.id, puzzle["id"])
        total_hints = len(puzzle["hints"])
        if used >= total_hints:
            return {"success": False, "message": "No more hints available", "hint_text": None, "hints_remaining": 0}

        hint_text = puzzle["hints"][used]
        hint_usage = HintUsage(
            game_id=game.id,
            puzzle_id=puzzle["id"],
            hint_index=used
        )
        self.db.add(hint_usage)
        game.hints_used_total += 1
        self.db.commit()
        return {
            "success": True,
            "hint_text": hint_text,
            "hints_remaining": total_hints - (used + 1),
            "message": "Hint retrieved"
        }

    def check_answer(self, game: GameState, user_answer: Any, item_used: Optional[str] = None) -> Dict:
        puzzle = get_puzzle(game.current_puzzle_id)
        if not puzzle:
            return {"success": False, "message": "No active puzzle"}

        missing_items = [item for item in puzzle["required_items"] if item not in game.inventory]
        if missing_items:
            return {"success": False, "message": f"You need: {', '.join(missing_items)}"}

        if puzzle["puzzle_type"] == "item_use":
            if item_used == puzzle["answer"]:
                if item_used in game.inventory:
                    game.inventory.remove(item_used)
                success = True
            else:
                success = False
        else:
            if isinstance(puzzle["answer"], str) and isinstance(user_answer, str):
                success = user_answer.strip().lower() == puzzle["answer"].lower()
            else:
                success = user_answer == puzzle["answer"]

        if not success:
            return {"success": False, "message": "Incorrect answer. Try again."}

        points_awarded = puzzle["points"]
        hints_used = self.get_used_hints(game.id, puzzle["id"])
        if hints_used > 0:
            penalty = hints_used * 2
            points_awarded = max(0, points_awarded - penalty)

        game.score += points_awarded

        if puzzle["reward_item"]:
            if puzzle["reward_item"] not in game.inventory:
                game.inventory.append(puzzle["reward_item"])

        next_puzzle_id = puzzle["next_puzzle"]
        if next_puzzle_id:
            game.current_puzzle_id = next_puzzle_id
            next_puzzle = get_puzzle(next_puzzle_id)
        else:
            game.is_completed = True
            next_puzzle = None

        self.db.commit()
        self.db.refresh(game)

        return {
            "success": True,
            "message": "Puzzle solved!",
            "points_awarded": points_awarded,
            "next_puzzle": next_puzzle,
            "updated_inventory": game.inventory,
            "updated_score": game.score,
            "is_game_completed": game.is_completed
        }
