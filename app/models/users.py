from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app import database


class User(database.Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    events = relationship("Event", back_populates="user")
    devices = relationship("Device", back_populates="owner")
