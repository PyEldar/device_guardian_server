from sqlalchemy.orm import Session

from app.schemas import users as users_schemas, events as events_schemas
from app.models import users as users_models, events as events_models
from app import security


def get_user(db: Session, user_id: int):
    return db.query(users_models.User).filter(users_models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(users_models.User).filter(users_models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(users_models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: users_schemas.UserCreate):
    hashed_password = security.get_password_hash(user.password)
    db_user = users_models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db=db, email=email)
    if not user:
        return None
    if not security.verify_password(password, user.hashed_password):
        return None
    return user


def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(events_models.event).offset(skip).limit(limit).all()


def get_user_events(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(events_models.event).filter(events_models.event.owner_id == user_id).offset(skip).limit(limit).all()


def create_user_event(db: Session, event: events_schemas.eventCreate, user_id: int):
    db_event = events_models.event(**event.dict(), owner_id=user_id)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event
