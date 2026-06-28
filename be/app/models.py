import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from geoalchemy2 import Geometry
from pydantic import EmailStr
from sqlalchemy import Column, DateTime
from sqlmodel import Field, SQLModel


class SeverityType(str, Enum):
    GOOD = "good"
    MODERATE = "moderate"
    BAD = "bad"


def get_datetime_utc() -> datetime:
    return datetime.now(timezone.utc)


# USERS
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


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


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


# Database model
class User(UserBase, table=True):
    id: str = Field(default_factory=uuid.uuid4, primary_key=True)
    password: str
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )


# DEVICES
# Device shared properties
class DeviceBase(SQLModel):
    code: str = Field(unique=True, index=True, max_length=255)
    api_key: str = Field(max_length=255)
    is_active: bool = False
    owner_id: str | None = Field(default=None, foreign_key="user.id")


# Database model
class Device(DeviceBase, table=True):
    id: str = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )


# RECORDINGS
class RecordingBase(SQLModel):
    filename: str = Field(max_length=255)
    started_at: datetime
    ended_at: datetime
    sample_count: int = 0


class Recording(RecordingBase, table=True):
    id: str = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    device_id: str | None = Field(default=None, foreign_key="device.id")
    data_run_id: str = Field(unique=True, index=True, max_length=255)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )


# RECORDING SAMPLES
# geom column requires GeoAlchemy2: from geoalchemy2 import Geometry
class RecordingSample(SQLModel, table=True):
    __tablename__ = "sample_data"
    id: int | None = Field(default=None, primary_key=True)
    recording_id: str = Field(foreign_key="recording.id")
    recorded_at: datetime
    accel_z: float
    speed: float
    lat: float
    lon: float
    roughness_score: float
    severity: SeverityType
    geom: Any = Field(
        default=None,
        sa_column=Column(Geometry("POINT", srid=4326)),
    )
