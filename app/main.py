from fastapi import FastAPI
from . import models
from . database import engine
from .routers import auth, player, team, season

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(player.router)
app.include_router(team.router)
app.include_router(season.router)

@app.get("/")
def root():
    return {"message": "main"}