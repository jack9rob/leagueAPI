import json
from fastapi import APIRouter, Depends, status, HTTPException
from ..schemas import player
from sqlalchemy.orm import Session
from app.database import get_db
from .. import utils, models
from ..schemas import team

router = APIRouter(
    prefix='/teams',
    tags=['Player']
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

@router.get('/first', response_model=team.TeamResponse)
def get_teams_first(db: Session = Depends(get_db)):
    teams = db.query(models.Team).first()
    