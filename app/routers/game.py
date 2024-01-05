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

@router.post('/players') #'/{id}/players' id is the game id
def create_player_game(player_game: game.PlayerGameCreate, db: Session = Depends(get_db)):
    db_game = models.PlayerGame(**player_game.model_dump())
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

@router.get('/{id}/players')
def get_player_game_by_game(id: int, db: Session = Depends(get_db)):
    players = db.query(models.PlayerGame).filter(models.PlayerGame.game_id == id).all()
    return players

@router.post('/goals') #'/{id}/goals'
def create_goal(goal: game.CreateGoal, db: Session = Depends(get_db)):
    db_goal = models.Goal(**goal.model_dump())
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal

@router.get('/{id}/goals')
def get_goals_game(id: int, db: Session = Depends(get_db)):
    '''
    goals = db.query(models.Goal, models.PlayerGame, models.Game, models.Team, models.Player
                     ).join(models.PlayerGame, models.Goal.player_game_id == models.PlayerGame.id
                            ).join(models.Game, models.PlayerGame.game_id == models.Game.id
                                   ).join(models.Team, models.Team.id == models.PlayerGame.team_id
                                          ).join(models.Player, models.Player.id == models.PlayerGame.player_id).all()
    '''
    goals = db.query(models.Goal, models.PlayerGame, func.count(models.Goal.id)
                     ).join(models.PlayerGame, models.Goal.player_game_id == models.PlayerGame.id
                        ).group_by(models.Goal.player_game_id).all()
    return goals

@router.get('/{id}/stats')
def get_game_stats(id: int, db: Session = Depends(get_db)):
    stats = []
    players = db.query(models.PlayerGame, models.Player)