from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class Season(BaseModel):
    id: int
    name: str
    start_date: datetime
    end_date: datetime
    created_at: datetime

class SeasonCreate(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime



