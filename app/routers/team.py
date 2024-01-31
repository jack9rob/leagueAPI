import json
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session, aliased
from sqlalchemy import func, text
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

# get a specific season for a team
@router.get('/{team_id}/seasons/{season_id}')
def get_team_season(team_id: int, season_id: int, db: Session = Depends(get_db)):
    #check if team and season exists
    team_season = db.query(models.TeamSeason.id, models.TeamSeason.wins, models.TeamSeason.losses, models.TeamSeason.ties, models.Team, models.Season).filter((models.TeamSeason.team_id == team_id) & (models.TeamSeason.season_id == season_id)
                    ).join(models.Team, models.Team.id == models.TeamSeason.team_id
                    ).join(models.Season, models.Season.id == models.TeamSeason.season_id           
                    ).first()

    if not team_season:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"team with id: {team_id} or season with id: {season_id} was not found")
    
    # get player stats for that team season
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

    player_stats = db.query(models.Player, func.coalesce(goal_query.c.goals, text('0')).label('goals'), func.coalesce(assist_query.c.assists, text('0')).label('assists'), 
                        func.coalesce(goal_query.c.goals + assist_query.c.assists, goal_query.c.goals, assist_query.c.assists, text('0')).label('points')
                    ).select_from(models.PlayerTeamSeason
                    ).filter(models.TeamSeason.id == team_season.id
                    ).join(models.TeamSeason, models.TeamSeason.id == models.PlayerTeamSeason.team_season_id
                    ).join(goal_query, (goal_query.c.player_id == models.PlayerTeamSeason.player_id) & (goal_query.c.team_season_id == models.PlayerTeamSeason.team_season_id),isouter=True
                    ).join(assist_query, (assist_query.c.player_id == models.PlayerTeamSeason.player_id) & (assist_query.c.team_season_id == models.PlayerTeamSeason.team_season_id), isouter=True
                    ).join(models.Player, models.Player.id == models.PlayerTeamSeason.player_id
                    ).all()
    
    #get the teams games in the season
    games = db.query(models.Game).filter((models.Game.team_home_id == team_id) or (models.Game.team_away_id == team_id)).all()
    return {'data': {
            'team_season': team_season,
            'player_stats': player_stats
            }
        }

#routes

#team overview (name, all team seasons)

#team season (team season info, player roster, games scores)