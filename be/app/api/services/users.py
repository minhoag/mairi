from sqlmodel import select

from app.models import User, UserCreate
from app.utils.password import get_hashed_password
from app.wrapper.response import ConflictResponse, NotFoundResponse, SuccessResponse
from app.wrapper.service import Service


class UserService(Service):
    def create_user(self, user_in: UserCreate):
        existing = self._db.exec(
            select(User).where(
                (User.email == user_in.email) | (User.username == user_in.username)
            )
        ).first()
        if existing:
            return ConflictResponse(
                message="User with this email or username already exists"
            )

        hashed = get_hashed_password(user_in.password.encode("utf-8")).decode("utf-8")
        user = User.model_validate(user_in, update={"password": hashed})
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return SuccessResponse(data=user.model_dump(exclude={"password"}))

    def get_all_users(self):
        users = self._db.exec(select(User)).all()
        return SuccessResponse(data=[u.model_dump(exclude={"password"}) for u in users])

    def get_one_user(self, user_id: str):
        user = self._db.get(User, user_id)
        if user is None:
            return NotFoundResponse(message="User not found")
        return SuccessResponse(data=user.model_dump(exclude={"password"}))
