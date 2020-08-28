from sqlalchemy.orm import Session

from app.schemas import users as users_schemas, events as events_schemas
from app.schemas import devices as devices_schemas
from app.models import users as users_models, events as events_models
from app.models import devices as devices_models
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
    return db.query(events_models.Event).offset(skip).limit(limit).all()


def get_user_events(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(events_models.Event).filter(events_models.Event.user_id == user_id).offset(skip).limit(limit).all()


def create_user_event(db: Session, event: events_schemas.EventCreate, user_id: int):
    db_event = events_models.Event(**event.dict(), user_id=user_id)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_user_devices(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(devices_models.Device).filter(devices_models.Device.owner_id == user_id).offset(skip).limit(limit).all()


def get_device_events(db: Session, device_id: int, skip: int = 0, limit: int = 10):
    return db.query(events_models.Event).filter(events_models.Event.device_id == device_id).offset(skip).limit(limit).all()


def get_device(db: Session, device_id: int):
    return db.query(devices_models.Device).filter(devices_models.Device.id == device_id).first()


def create_user_device(db: Session, device: devices_schemas.DeviceCreate, user_id: int):
    db_device = devices_models.Device(**device.dict(), owner_id=user_id)
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device


def create_device_pairing_code(db: Session, device_id: int, otp_code: str):
    db.query(devices_models.Device).\
        filter(devices_models.Device.id == device_id).\
        update({devices_models.Device.pairing_code: otp_code})
