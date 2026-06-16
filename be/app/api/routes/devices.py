from fastapi import APIRouter, Depends, Header, HTTPException
from sqlmodel import Session

from app.api.services.devices import DeviceService
from app.core.db import get_db
from app.models import DeviceClaimRequest, User

router = APIRouter(prefix="/devices", tags=["devices"])


def get_current_user(
    x_user_id: str = Header(..., alias="X-User-ID"),
    db: Session = Depends(get_db),
) -> User:
    user = db.get(User, x_user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@router.post("/claim")
def claim_device(
    request: DeviceClaimRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = DeviceService(session=db, user=current_user)
    return service.claim_device(request.claim_code)


@router.get("/me")
def get_my_devices(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = DeviceService(session=db, user=current_user)
    return service.get_my_devices()


@router.get("/{device_id}")
def get_device(
    device_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = DeviceService(session=db, user=current_user)
    return service.get_device(device_id)
