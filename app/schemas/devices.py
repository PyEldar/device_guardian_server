from typing import List

from pydantic import BaseModel

from app.schemas import events as events_schemas


class DeviceBase(BaseModel):
    name: str

class DeviceCreate(BaseModel):
    pass

class Device(DeviceBase):
    id: int
    owner_id: int
    events: List[events_schemas.event] = []

    class Config:
        orm_mode = True
