from pydantic import BaseModel


class eventBase(BaseModel):
    title: str
    description: str = None


class eventCreate(eventBase):
    pass


class event(eventBase):
    id: int

    class Config:
        orm_mode = True
