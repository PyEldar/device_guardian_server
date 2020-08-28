from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    pairing_code = Column(String, default=False)

    owner = relationship("User", back_populates="devices")
    events = relationship("Event", back_populates="device")
