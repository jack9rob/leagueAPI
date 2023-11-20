from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, index=True)
    city
    street
    apartment_number
    postal_code
    player_id = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False)

    resident = relationship("Player", back_populates="address")

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    firstname
    lastname
    email
    password

    address = relationship("Address", back_populates="resident")

