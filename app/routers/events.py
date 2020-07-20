from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas import events as events_schemas
from app.models import users as users_models
from app import crud, deps


router = APIRouter()


@router.post(
    "/users/{user_id}/events/",
    response_model=events_schemas.event,
    dependencies=[Depends(deps.get_current_superuser)],
)
def create_event_for_user(
    user_id: int, event: events_schemas.eventCreate, db: Session = Depends(deps.get_db)
):
    """
    Create an event for a specific user.

    Only allowed to the super user.
    """
    return crud.create_user_event(db=db, event=event, user_id=user_id)


@router.post("/events/", response_model=events_schemas.event)
def create_event_for_current_user(
    event: events_schemas.eventCreate,
    db: Session = Depends(deps.get_db),
    current_user: users_models.User = Depends(deps.get_current_user),
):
    """
    Create an event.

    Requires authentication and the event will be assigned to the current user.
    """
    return crud.create_user_event(db=db, event=event, user_id=current_user.id)


@router.get("/events/", response_model=List[events_schemas.event])
def read_events(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: users_models.User = Depends(deps.get_current_user)
):
    """
    Read events of currently logged in user
    """
    events = crud.get_user_events(db, current_user.id, skip=skip, limit=limit)
    return events
