from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from .player import PlayerResponse

class Team(BaseModel):
    id: int
    name: str
    player_id: int
    created_at: datetime

class TeamCreate(BaseModel):
    name: str
    player_id: int

class TeamResponse(BaseModel):
    id: int
    name: str
    player_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class TeamPlayer(BaseModel):
    Team: TeamResponse
    Player: PlayerResponse

    class Config:
        from_attributes = True


class TeamPlayerList(BaseModel):
    data: List[TeamPlayer]