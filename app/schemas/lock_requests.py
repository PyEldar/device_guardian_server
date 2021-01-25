import datetime

from pydantic import BaseModel

from app.models import lock_requests as lock_requests_models
from app.schemas import devices as devices_schemas


class LockRequestBase(BaseModel):
    pass


class LockRequestStateUpdate(LockRequestBase):
    state: lock_requests_models.LockRequestState


class LockRequestCreate(LockRequestBase):
    device_id: int


class LockRequest(LockRequestCreate):
    id: int
    created: datetime.datetime
    state: lock_requests_models.LockRequestState
    device: devices_schemas.Device

    class Config:
        orm_mode = True
