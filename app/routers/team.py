import json
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from .. import utils, models
from ..schemas import team_season, team

router = APIRouter(
    prefix='/teams',
    tags=['Team']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_team(team: team.TeamCreate, db: Session = Depends(get_db)):
    db_team = models.Team(**team.model_dump())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)

    return db_team

@router.get('/', response_model=team.TeamPlayerList)
def get_teams(db: Session = Depends(get_db)):
    teams = db.query(models.Team, models.Player).join(models.Player, models.Player.id == models.Team.player_id).all()
    return {"data": teams}

@router.post('/seasons')
def create_team_season(team_season: team_season.TeamSeasonCreate, db: Session = Depends((get_db))):
    db_team_season = models.TeamSeason(**team_season.model_dump())
    db.add(db_team_season)
    db.commit()
    db.refresh(db_team_season)
    return db_team_season

@router.get('/seasons', response_model=team_season.TeamSeasonList)
def get_team_seasons(db: Session = Depends(get_db)):
    team_seasons = db.query(models.TeamSeason, models.Team, models.Season).join(models.Season, models.Season.id == models.TeamSeason.season_id).join(models.Team, models.Team.id == models.TeamSeason.team_id).all()

    return {"data": team_seasons}

@router.get("/seasons/{id}")
def get_teams_seasons(id: int, db: Session = Depends(get_db)):
    team_seasons = db.query(models.TeamSeason, models.Team, models.Season).join(models.Season, models.Season.id == models.TeamSeason.season_id).join(models.Team, models.Team.id == models.TeamSeason.team_id).filter(models.Team.id == id).all()

    if not team_seasons:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"team with id: {id} was not found")
    
    return team_seasons

@router.post('/players')
def create_player_team_season(player_team_season: team_season.PlayerTeamSeasonCreate, db: Session = Depends(get_db)):
    db_player_team_season = models.PlayerTeamSeason(**player_team_season.model_dump())
    db.add(db_player_team_season)
    db.commit()
    db.refresh(db_player_team_season)
    return db_player_team_season

@router.get('/players')
def get_season_roster(db: Session = Depends(get_db)):
    team_roster = db.query(models.PlayerTeamSeason).all()
    return team_roster

@router.get('/players/{id}')
def get_players_by_team(id: int, db: Session = Depends(get_db)):
    players = db.query(models.PlayerTeamSeason, models.Player
                       ).filter(models.PlayerTeamSeason.team_season_id ==id
                                ).join(models.Player, models.Player.id == models.PlayerTeamSeason.player_id
                                       ).order_by(models.PlayerTeamSeason.is_player).all()
    '''
    for x in players:
        goals = db.query(models.Goal, func.count(models.Goal.id)).filter(models.Goal.team_season_id == x.PlayerTeamSeason.id).all()
        print(goals)
    '''
    return {'data': players}