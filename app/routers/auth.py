from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, models, utils, oauth2

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login')
def login(player_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    player = db.query(models.Player).filter(models.Player.email == player_credentials.username).first()

    if not player:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'invalid credentials')
    if not utils.verify(player_credentials.password, player.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'invalid credentials')
    
    access_token = oauth2.create_access_token(data={
        "user_id": player.id,
    })

    return {'access_token': access_token, "token_type": "bearer"}
