from pydantic import BaseModel
from datetime import datetime
from typing import List
from .team import TeamResponse
from .season import Season

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