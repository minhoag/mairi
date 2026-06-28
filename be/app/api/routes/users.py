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


# TODO: add check permission, only admin can query all users
@router.get("/")
def get_all_users(
    db: Session = Depends(get_db),
):
    service = UserService(session=db, user=None)
    return service.get_all_users()


@router.get("/{user_id}")
def get_one_user(
    user_id: str,
    db: Session = Depends(get_db),
):
    service = UserService(session=db, user=None)
    return service.get_one_user(user_id)
