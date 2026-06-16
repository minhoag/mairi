import uuid
from datetime import datetime, timezone

from pydantic import EmailStr
from sqlalchemy import DateTime
from sqlmodel import Field, SQLModel


def get_datetime_utc() -> datetime:
    return datetime.now(timezone.utc)


# User share properties
class UserBase(SQLModel):
    username: str = Field(unique=True, index=True, max_length=255)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_admin: bool = False
    is_active: bool = True
    firstname: str | None = Field(default=None, max_length=255)
    lastname: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=20)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserRegister(SQLModel):
    username: str = Field(max_length=255)
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)
    firstname: str | None = Field(default=None, max_length=255)
    lastname: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore[assignment]
    password: str | None = Field(default=None, min_length=8, max_length=128)
    firstname: str | None = Field(default=None, max_length=255)
    lastname: str | None = Field(default=None, max_length=255)


class UserUpdateMe(SQLModel):
    firstname: str | None = Field(default=None, max_length=255)
    lastname: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


# Database model
class User(UserBase, table=True):
    id: str = Field(default_factory=uuid.uuid4, primary_key=True)
    password: str
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )


# Device shared properties
class DeviceBase(SQLModel):
    code: str = Field(unique=True, index=True, max_length=255)
    api_key: str = Field(max_length=255)
    is_active: bool = False
    owner_id: str | None = Field(default=None, foreign_key="user.id")


class Device(DeviceBase, table=True):
    id: str = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    updated_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )


class DevicePublic(SQLModel):
    id: str
    code: str
    is_active: bool
    owner_id: str | None
    created_at: datetime | None
    updated_at: datetime | None


class DeviceClaimRequest(SQLModel):
    claim_code: str


class DeviceClaimResponse(SQLModel):
    message: str
    device: DevicePublic


# ClaimCode shared properties
class ClaimCodeBase(SQLModel):
    code: str = Field(unique=True, index=True, max_length=50)
    device_id: str = Field(foreign_key="device.id")
    claimed_by: str | None = Field(default=None, foreign_key="user.id")
    claimed_at: datetime | None = None


class ClaimCode(ClaimCodeBase, table=True):
    id: str = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
