from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models import users as users_models
from app.models import devices as devices_models
from app.models import lock_requests as lock_requests_models
from app.schemas import lock_requests as lock_requests_schemas
from app import crud, deps

router = APIRouter()


@router.post(
    "/lock_requests/",
    response_model=lock_requests_schemas.LockRequest
)
def create_lock_request_for_device(
    lock_request: lock_requests_schemas.LockRequestCreate,
    db: Session = Depends(deps.get_db),
    current_user: users_models.User = Depends(deps.get_current_user),
):
    """
    Create lock request for device

    Requires authentication and the lock request will be assigned to specified device_id
    """
    # TODO check pending lock request already exists - use PUT
    return crud.create_device_lock_request(db, lock_request, lock_request.device_id)


@router.get(
    "/lock_requests/",
    response_model=List[lock_requests_schemas.LockRequest],
    response_model_exclude={"device"}
)
def get_lock_request_for_current_device(
    db: Session = Depends(deps.get_db),
    current_device: devices_models.Device = Depends(deps.get_current_device),
):
    """
    Get lock requests for current device.

    Requires authentication and lock_requests for the current device will be returned.
    """
    # TODO Return only not delivered lock requests
    crud.update_device_lock_requests(db, current_device.id, lock_requests_models.LockRequestState.delivered)
    return crud.get_device_lock_requests(db=db, device_id=current_device.id, limit=1)


@router.patch(
    "/lock_requests/{lock_request_id}",
    response_model=lock_requests_schemas.LockRequest,
    response_model_exclude={'device'}
)
def update_lock_request_state(
    lock_request_id: int,
    lock_request_state_update: lock_requests_schemas.LockRequestStateUpdate,
    db: Session = Depends(deps.get_db),
    current_device: devices_models.Device = Depends(deps.get_current_device)
):
    """
    Update state of the lock_request
    """
    db_lock_request = crud.get_lock_request(db, lock_request_id)
    if db_lock_request is None:
        raise HTTPException(status_code=404, detail="Lock Request not found")
    if db_lock_request.device_id != current_device.id:
        raise HTTPException(status_code=403)

    crud.update_lock_request_state(db, lock_request_id, lock_request_state_update.state)
    db.refresh(db_lock_request)
    return db_lock_request
