from fastapi import APIRouter, Depends, status, HTTPException
from ..schemas import player
from sqlalchemy.orm import Session
from app.database import get_db
from .. import utils, models
from sqlalchemy import func

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

@router.get('/stats')
def get_season_stats(db: Session=Depends(get_db)):
        query = db.query(models.PlayerGame.team_season_id, models.PlayerGame.player_id, models.Player, models.Season, models.Team, func.count(models.Goal.player_game_id).label('goals')
                    ).filter(models.PlayerGame.player_id==1
                     ).join(models.PlayerGame, models.PlayerGame.id == models.Goal.player_game_id
                      ).join(models.Player, models.Player.id == models.PlayerGame.player_id
                      ).join(models.TeamSeason, models.TeamSeason.id == models.PlayerGame.team_season_id
                             ).join(models.Team, models.Team.id == models.TeamSeason.team_id
                                    ).join(models.Season, models.Season.id == models.TeamSeason.season_id
                            ).group_by(models.PlayerGame.team_season_id, models.PlayerGame.player_id, models.TeamSeason.id, models.Player, models.Team, models.Season)
        print(query)
        query = query.all()
        return {'data': query}