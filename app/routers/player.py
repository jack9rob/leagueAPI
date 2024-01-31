from fastapi import APIRouter, Depends, status, HTTPException
from ..schemas import player
from sqlalchemy.orm import Session, aliased
from app.database import get_db
from .. import utils, models
from sqlalchemy import func, text
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

# get players stats for each season
@router.get('/stats')
def get_season_stats(db: Session=Depends(get_db)):
        goal_query = db.query(models.PlayerGame.player_id, models.PlayerGame.team_season_id, func.count(models.PlayerGame.player_id).label('goals')
                            ).select_from(models.Goal
                            ).join(models.PlayerGame, models.PlayerGame.player_id == models.Goal.player_game_id
                            ).group_by(models.PlayerGame.player_id, models.PlayerGame.team_season_id).subquery()

        assist_player_games = aliased(models.PlayerGame, name='assist_player_games')
        assist_goals = aliased(models.Goal, name='assist_goals' )
        assist_query = db.query(models.Assist.player_id, func.count(models.Assist.player_id).label('assists'), assist_player_games.team_season_id
                                ).select_from(models.Assist
                                ).join(assist_goals, assist_goals.id == models.Assist.goal_id
                                ).join(assist_player_games, assist_player_games.id == assist_goals.player_game_id
                                ).group_by(models.Assist.player_id, assist_player_games.team_season_id).subquery()
        
        query = db.query(models.Player, models.PlayerTeamSeason.player_id, models.PlayerTeamSeason.team_season_id, models.TeamSeason.team_id,
                         models.TeamSeason.season_id, func.coalesce(goal_query.c.goals, text('0')).label('goals'), func.coalesce(assist_query.c.assists, text('0')).label('assists'), 
                         func.coalesce(goal_query.c.goals + assist_query.c.assists, goal_query.c.goals, assist_query.c.assists, text('0')).label('points')
                        ).select_from(models.PlayerTeamSeason
                        ).filter(models.Player.id == 1
                        ).join(models.TeamSeason, models.TeamSeason.id == models.PlayerTeamSeason.team_season_id
                        ).join(goal_query, (goal_query.c.player_id == models.PlayerTeamSeason.player_id) & (goal_query.c.team_season_id == models.PlayerTeamSeason.team_season_id),isouter=True
                        ).join(assist_query, (assist_query.c.player_id == models.PlayerTeamSeason.player_id) & (assist_query.c.team_season_id == models.PlayerTeamSeason.team_season_id), isouter=True
                        ).join(models.Player, models.Player.id == models.PlayerTeamSeason.player_id
                        ).all()
        return {'data': query}

