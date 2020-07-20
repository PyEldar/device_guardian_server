import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import logging

import uvicorn
from fastapi import FastAPI
from sqlalchemy.orm import Session

from app import crud
from app.schemas import users as users_schemas
from app.database import Base
from app.routers import auth, events, users
from app.database import SessionLocal, engine
from app.settings import settings

app = FastAPI()

app.include_router(users.router, tags=["users"])
app.include_router(events.router, tags=["events"])
app.include_router(auth.router, tags=["auth"])


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    user = crud.get_user_by_email(db, settings.super_user_email)
    if not user:
        user_in = users_schemas.UserCreate(
            email=settings.super_user_email, password=settings.super_user_password
        )
        logging.info("Creating superuser")
        crud.create_user(db, user_in)
    db.close()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
