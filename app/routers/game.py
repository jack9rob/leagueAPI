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
    home_season = aliased(models.TeamSeason, name='home_season')
    away_season = aliased(models.TeamSeason, name='away_season')
    home_team = aliased(models.Team, name='home_team')
    away_team = aliased(models.Team, name='away_team')
    games = db.query(models.Game, home_season, away_season, home_team, away_team
                     ).join(home_season, home_season.id == models.Game.team_home_id
                            ).join(away_season, away_season.id == models.Game.team_away_id
                                   ).join(home_team, home_team.id == home_season.team_id
                                          ).join(away_team, away_team.id == away_season.team_id).all()
    return games