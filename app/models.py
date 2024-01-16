from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, nullable=False)
    street = Column(String, nullable=False)
    apartment_number = Column(Integer, nullable=True)
    postal_code = Column(String, nullable=False)

    player_id = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False)

    resident = relationship("Player")

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))

    team = relationship("Team", back_populates='player')


class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))

    player_id = Column(Integer, ForeignKey('players.id'), nullable=False)

    player = relationship("Player", back_populates="team")
    seasons = relationship('TeamSeason', back_populates='team')

class Season(Base):
    __tablename__ = "seasons"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    start_date = Column(Date, nullable=False, server_default=text('NOW()'))
    end_date = Column(Date, nullable=False, server_default=text('NOW()'))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))

    team = relationship("TeamSeason", back_populates="season")

class TeamSeason(Base):
    __tablename__ = "team_seasons"
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"))
    season_id = Column(Integer, ForeignKey("seasons.id", ondelete="CASCADE"))
    wins = Column(Integer, nullable=False, server_default='0')
    losses = Column(Integer, nullable=False, server_default='0')
    ties = Column(Integer, nullable=False, server_default='0')

    team = relationship('Team', back_populates='seasons')
    season = relationship('Season', back_populates='team')

class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True, index=True)
    team_home_id = Column(Integer, ForeignKey("team_seasons.id", ondelete="CASCADE"), nullable=False)
    team_away_id = Column(Integer, ForeignKey("team_seasons.id", ondelete="CASCADE"), nullable=False)
    team_home_goals = Column(Integer, nullable=False, default=0)
    team_away_goals = Column(Integer, nullable=False, default=0)
    date = Column(TIMESTAMP, nullable=False, server_default=text('NOW()'))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))

    home_team = relationship("TeamSeason", foreign_keys=[team_home_id])
    away_team = relationship("TeamSeason", foreign_keys=[team_away_id])


class PlayerTeamSeason(Base):
    __tablename__ = "player_team_seasons"
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False)
    team_season_id = Column(Integer, ForeignKey("team_seasons.id", ondelete="CASCADE"), nullable=False)
    is_player = Column(Boolean, nullable=False, server_default='True')
    #status - default is active, also injured, emergency player, removed

class PlayerGame(Base): # could use player game, it has the game id, player id, and team_season_id
    __tablename__ = "player_games"
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False)
    game_id = Column(Integer, ForeignKey('games.id', ondelete="CASCADE"), nullable=False)
    team_season_id = Column(Integer, ForeignKey('team_seasons.id', ondelete='CASCADE'), nullable=False)
    is_player = Column(Boolean, nullable=False, server_default='True')
    #emergency plauer

class GoalieStats(Base): #maybe change to goalie stats, not too sure
    __tablename__ = 'goalie_stats'
    id = Column(Integer, primary_key=True, index=True)
    player_game_id = Column(Integer, ForeignKey('player_games.id', ondelete='CASCADE'), nullable=False)
    game_id = Column(Integer, ForeignKey('games.id', ondelete="CASCADE"), nullable=False)
    team_id = Column(Integer, ForeignKey('teams.id', ondelete='CASCADE'), nullable=False)
    saves = Column(Integer, nullable=False, server_default='0')


class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True, index=True)
    player_game_id = Column(Integer, ForeignKey('player_games.id', ondelete='CASCADE'), nullable=False)
    #goal type (empty net, shorthanded, powerplay, evenstrength)

class Assist(Base):
    __tablename__ = "assists"
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey('players.id', ondelete='CASCADE'), nullable=False)
    goal_id = Column(Integer, ForeignKey('goals.id', ondelete='CASCADE'), nullable=False)
    game_id = Column(Integer, ForeignKey('games.id', ondelete='CASCADE'), nullable=False)
    is_primary = Column(Boolean, nullable=False, server_default='True')

