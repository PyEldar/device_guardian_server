from typing import List

from pydantic import BaseModel

from app.schemas import events as events_schemas
from app.schemas import devices as devices_schemas


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    events: List[events_schemas.Event] = []
    devices: List[devices_schemas.Device] = []

    class Config:
        orm_mode = True
