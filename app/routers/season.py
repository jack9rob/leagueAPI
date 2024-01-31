from fastapi import APIRouter, Depends, status, HTTPException
from ..schemas import season, team_season
from sqlalchemy.orm import Session
from app.database import get_db
from .. import utils, models

router = APIRouter(
    prefix='/seasons',
    tags=['Seasons']
)

@router.post('/')
def create_season(season: season.SeasonCreate, db: Session = Depends(get_db)):
    db_season = models.Season(**season.model_dump())
    db.add(db_season)
    db.commit()
    db.refresh(db_season)

    return db_season

@router.get("/{id}", response_model=team_season.TeamsSeasons)
def get_seasons(id: int, db: Session = Depends(get_db)):
    db_season = db.query(models.Season).filter(models.Season.id == id).first()
    team_seasons = db.query(models.TeamSeason, models.Team, models.Season).join(models.Season, models.Season.id == models.TeamSeason.season_id).join(models.Team, models.Team.id == models.TeamSeason.team_id).filter(models.Season.id == id).all()

    return {"data": {"season": db_season, "teams": team_seasons}}

# season overview (team standings, points leaders, upcoming games, recent games)