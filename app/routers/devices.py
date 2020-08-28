from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models import users as users_models
from app.models import devices as devices_models
from app.schemas import devices as devices_schemas
from app import crud, deps

router = APIRouter()

@router.get("/devices/", response_model=List[devices_schemas.Device])
def read_devices(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: users_models.User = Depends(deps.get_current_user)
):
    """
    Read devices of currently logged in user
    """
    devices = crud.get_user_devices(db, current_user.id, skip=skip, limit=limit)
    return devices

@router.get(
    "/devices/{device_id}",
    response_model=devices_schemas.Device
)
def get_device(device_id: int, db: Session = Depends(deps.get_db), current_user: users_models.User = Depends(deps.get_current_user)):
    """
    Get single device, allowed only for device owners
    """
    db_device: devices_models.Device = crud.get_device(db, device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    if not db_device.owner_id == current_user.id:
        raise HTTPException(status_code=403)
    return db_device

@router.post(
    "/devices/",
    response_model=devices_schemas.Device
)
def create_device_for_user(
    device: devices_schemas.DeviceCreate,
    db: Session = Depends(deps.get_db),
    current_user: users_models.User = Depends(deps.get_current_user),
):
    """
    Create a device

    Requires authentication and the device will be assigned to the current user
    """
    return crud.create_user_device(db, device, current_user.id)

@router.get(
    "devices/{device_id}/pair",
    response_model=devices_schemas.DevicePair
)
def pair_device(
    device_id: int,
    db: Session = Depends(deps.get_db),
    current_user: users_models.User = Depends(deps.get_current_user),
):
    """
    Create a pairing code for specific device

    Allowed only for device owner
    """
    db_device: devices_models.Device = crud.get_device(db, device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    if not db_device.owner_id == current_user.id:
        raise HTTPException(status_code=403)
