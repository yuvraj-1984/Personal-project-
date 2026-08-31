from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import game, puzzles
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Puzzle Game Backend",
              description="Backend for Mystery Solver / Garden Escape style puzzle games",
              version="1.0.0")

# CORS configuration (allow frontend from any origin for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(game.router, prefix="/game", tags=["game"])
app.include_router(puzzles.router, prefix="/puzzles", tags=["puzzles"])

@app.get("/")
def root():
    return {"message": "Puzzle Game API is running"}

# Add this to run on all network interfaces
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
