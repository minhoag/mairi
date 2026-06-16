from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.api.services.users import UserService
from app.core.db import get_db
from app.models import UserCreate

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/")
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
):
    service = UserService(session=db, user=None)
    return service.create_user(user_in)


@router.get("/")
def list_users(
    db: Session = Depends(get_db),
):
    service = UserService(session=db, user=None)
    return service.list_users()


@router.get("/{user_id}")
def get_user(
    user_id: str,
    db: Session = Depends(get_db),
):
    service = UserService(session=db, user=None)
    return service.get_user(user_id)
