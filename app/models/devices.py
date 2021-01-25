from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    pairing_code = Column(String, default=None)
    paired = Column(Boolean, default=False)

    owner = relationship("User", back_populates="devices")
    events = relationship("Event", back_populates="device")
    lock_requests = relationship("LockRequest", back_populates="device")
