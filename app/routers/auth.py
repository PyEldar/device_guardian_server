from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas import msg as msg_schemas
from app.schemas import auth as auth_schemas
from app.models import devices as devices_models
from app import crud, deps, security
from app.utils.auth import generate_password_reset_token, send_reset_password_email, verify_password_reset_token
from app.security import get_password_hash


router = APIRouter()


@router.post("/login/access-token", response_model=auth_schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = crud.authenticate_user(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return {
        "access_token": security.create_access_token(subject=user.id),
        "token_type": "bearer",
    }


@router.post("/login/device-token", response_model=auth_schemas.Token)
def login_device_token(
    db: Session = Depends(deps.get_db), pairing_code: str = Body(...)
):
    """
    Get an access token for future device requests
    """
    device: devices_models.Device = crud.get_device_by_pairing_code(db, pairing_code)
    if not device:
        raise HTTPException(status_code=400, detail="Incorrect pairing code")
    if not device.paired:
        crud.update_device_paired_state(db, device.id, paired=True)
    return {
        "access_token": security.create_access_token(subject=device.id),
        "token_type": "bearer",
    }


@router.post("/password-recovery/{email}", response_model=msg_schemas.Msg)
def recover_password(email: str, db: Session = Depends(deps.get_db)):
    """
    Password Recovery
    """
    user = crud.user.get_by_email(db, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    send_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    return {"msg": "Password recovery email sent"}


@router.post("/reset-password/", response_model=msg_schemas.Msg)
def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
    db: Session = Depends(deps.get_db),
):
    """
    Reset password
    """
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = crud.user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    hashed_password = get_password_hash(new_password)
    user.hashed_password = hashed_password
    db.add(user)
    db.commit()
    return {"msg": "Password updated successfully"}
