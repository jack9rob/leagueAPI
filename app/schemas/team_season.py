from pydantic import BaseModel
from datetime import datetime
from typing import List
from .team import TeamResponse
from .season import Season
from .player import PlayerResponse

class TeamSeason(BaseModel):
    id: int
    team_id: int
    season_id: int

class TeamSeasonCreate(BaseModel):
    team_id: int
    season_id: int

class TeamSeasonJoin(BaseModel):
    Team: TeamResponse
    Season: Season

class TeamSeasonList(BaseModel):
    data: List[TeamSeasonJoin]

class TeamSeasonJoin2(BaseModel):
    Team: TeamResponse

# all for getting teams in a season

class SeasonResponse(BaseModel):
    season: Season
    teams: List[TeamSeasonJoin2]

class TeamsSeasons(BaseModel):
    data: SeasonResponse

# team season players
class PlayerTeamSeason(BaseModel):
    is_player: int
class PlayerTeamSeasonCreate(BaseModel):
    player_id: int
    team_season_id: int
    is_player: bool

class TeamRoster(BaseModel):
    PlayerTeamSeason: PlayerTeamSeason
    Player: PlayerResponse

class TeamRosterResponse(BaseModel):
    data: List[TeamRoster]