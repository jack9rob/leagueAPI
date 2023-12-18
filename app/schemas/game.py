from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Annotated
from pydantic.types import conint


class GameCreate(BaseModel):
    team_home_id: int
    team_away_id: int
    team_home_goals: conint(gt=0)
    team_away_goals: conint(gt=0)
    date: datetime

class PlayerGameCreate(BaseModel):
    player_id: int
    game_id: int
    team_id: int
    is_player: Optional[bool] = True

