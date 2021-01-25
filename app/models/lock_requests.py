import enum
import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.devices import Device


class LockRequestState(str, enum.Enum):
    created = 'created'
    delivered = 'delivered'
    confirmed = 'confirmed'


class LockRequest(Base):
    __tablename__ = "lock_requests"

    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    created = Column(DateTime, default=datetime.datetime.utcnow)
    state = Column(Enum(LockRequestState), default=LockRequestState.created)

    device = relationship("Device", back_populates="lock_requests")
