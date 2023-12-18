from fastapi import APIRouter, Depends, status, HTTPException
from ..schemas import player
from sqlalchemy.orm import Session
from app.database import get_db
from .. import utils, models

router = APIRouter(
    prefix='/players',
    tags=['Player']
)

@router.post('/', response_model=player.PlayerResponse)
def create_player(player: player.PlayerCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash_password(player.password)
    player.password = hashed_password

    db_player = models.Player(**player.model_dump())
    db.add(db_player)
    db.commit()
    db.refresh(db_player)

    return db_player
