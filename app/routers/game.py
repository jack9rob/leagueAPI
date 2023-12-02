from fastapi import APIRouter, Depends, status, HTTPException
from ..schemas import game
from sqlalchemy.orm import Session, aliased
from app.database import get_db
from .. import utils, models
from sqlalchemy import func

router = APIRouter(
    prefix='/games',
    tags=['Games']
)

@router.post('/')
def create_game(game: game.GameCreate, db: Session = Depends(get_db)):
    db_game = models.Game(**game.model_dump())
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

@router.get('/')
def get_all_games(db: Session = Depends(get_db)):
    #home_team, away_team = aliased(models.TeamSeason), aliased(models.TeamSeason)
    games = db.query(models.Game, models.TeamSeason).join(models.TeamSeason).all()
    return games