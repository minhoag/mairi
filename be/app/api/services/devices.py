from datetime import datetime, timezone

from sqlmodel import select

from app.models import ClaimCode, Device, DevicePublic
from wrapper.response import (
    ConflictResponse,
    ForbiddenResponse,
    NotFoundResponse,
    SuccessResponse,
)
from wrapper.service import Service


class DeviceService(Service):
    def get_all_devices(self):
        is_admin = self.check_permission()
        if is_admin:
            return ForbiddenResponse(message="No permission")
        devices = self._db.exec(select(Device)).all()
        return SuccessResponse(
            data=[
                DevicePublic(
                    id=d.id,
                    code=d.code,
                    is_active=d.is_active,
                    owner_id=d.owner_id,
                    created_at=d.created_at,
                    updated_at=d.updated_at,
                )
                for d in devices
            ]
        )

    def claim_device(self, claim_code_str: str):
        claim_code = self._db.exec(
            select(ClaimCode).where(
                ClaimCode.code == claim_code_str,
                ClaimCode.claimed_by is None,
            )
        ).first()
        if claim_code is None:
            return NotFoundResponse(message="Invalid or already claimed code")

        device = self._db.get(Device, claim_code.device_id)
        if device is None:
            return NotFoundResponse(message="Device not found")

        if device.owner_id is not None:
            return ConflictResponse(message="Device already claimed")

        now = datetime.now(timezone.utc)

        claim_code.claimed_by = self.user.id
        claim_code.claimed_at = now

        device.owner_id = self.user.id
        device.is_active = True
        device.updated_at = now

        self._db.add(claim_code)
        self._db.add(device)
        self._db.commit()

        return SuccessResponse(
            message="Device claimed successfully",
            data=DevicePublic(
                id=device.id,
                code=device.code,
                is_active=device.is_active,
                owner_id=device.owner_id,
                created_at=device.created_at,
                updated_at=device.updated_at,
            ),
        )

    def get_my_devices(self):
        devices = self._db.exec(
            select(Device).where(Device.owner_id == self.user.id)
        ).all()
        return SuccessResponse(
            data=[
                DevicePublic(
                    id=d.id,
                    code=d.code,
                    is_active=d.is_active,
                    owner_id=d.owner_id,
                    created_at=d.created_at,
                    updated_at=d.updated_at,
                )
                for d in devices
            ]
        )

    def get_device(self, device_id: str):
        device = self._db.get(Device, device_id)
        if device is None or device.owner_id != self.user.id:
            return NotFoundResponse(message="Device not found")
        return SuccessResponse(
            data=DevicePublic(
                id=device.id,
                code=device.code,
                is_active=device.is_active,
                owner_id=device.owner_id,
                created_at=device.created_at,
                updated_at=device.updated_at,
            )
        )
