from datetime import datetime, timezone
from io import BytesIO

import polars as pl
from geoalchemy2.elements import WKTElement
from sqlalchemy import insert
from sqlmodel import select

from app.models import Device, Recording, RecordingSample, SeverityType
from app.wrapper.response import (
    BadRequestResponse,
    ConflictResponse,
    SuccessResponse,
    UnauthorizedResponse,
)
from app.wrapper.service import Service


class UploadService(Service):
    def upload_sensor_csv(
        self, authorization: str, device_id: str, data_run_id: str, file
    ):
        api_key = self.get_bearer_token(authorization)
        if not api_key:
            return UnauthorizedResponse()
        # check if device valid
        device = self._db.exec(
            select(Device).where(
                Device.id == device_id,
                Device.api_key == api_key,
                Device.is_active,
            )
        ).first()
        if not device:
            return UnauthorizedResponse(message="Device not found or inactive")
        data_run_exist = self._db.exec(
            select(Recording).where(Recording.data_run_id == data_run_id)
        ).first()
        if data_run_exist:
            return ConflictResponse(message="data_run_id already exists")

        df = pl.read_csv(BytesIO(file.file.read()))
        required_columns = ["Time", "Accel_Z", "Speed", "Lat", "Lon"]
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            return BadRequestResponse(
                message=f"File missing required columns: {', '.join(missing)}"
            )
        if len(df) == 0:
            return BadRequestResponse(message="CSV contains no samples")

        started_at = datetime.fromtimestamp(df["Time"][0], tz=timezone.utc)
        ended_at = datetime.fromtimestamp(df["Time"][-1], tz=timezone.utc)
        sample_count = len(df)

        recording = Recording(
            user_id=device.owner_id,
            device_id=device.id,
            filename=file.filename,
            data_run_id=data_run_id,
            started_at=started_at,
            ended_at=ended_at,
            sample_count=sample_count,
        )
        self._db.add(recording)
        self._db.flush()

        roughness = (pl.col("Accel_Z") - 9.81).abs()
        severity_expr = (
            pl.when(roughness < 0.5)
            .then(pl.lit(SeverityType.GOOD.value))
            .when(roughness < 1.5)
            .then(pl.lit(SeverityType.MODERATE.value))
            .otherwise(pl.lit(SeverityType.BAD.value))
        )
        df = df.with_columns(
            roughness.alias("roughness_score"),
            severity_expr.alias("severity"),
        )

        rows = [
            {
                "recording_id": recording.id,
                "recorded_at": datetime.fromtimestamp(row["Time"], tz=timezone.utc),
                "accel_z": row["Accel_Z"],
                "speed": row["Speed"],
                "lat": row["Lat"],
                "lon": row["Lon"],
                "roughness_score": row["roughness_score"],
                "severity": row["severity"],
                "geom": WKTElement(f"POINT({row['Lon']} {row['Lat']})", srid=4326),
            }
            for row in df.iter_rows(named=True)
        ]
        self._db.execute(insert(RecordingSample), rows)

        self._db.commit()
        self._db.refresh(recording)

        return SuccessResponse(
            data={
                "recording_id": recording.id,
                "data_run_id": recording.data_run_id,
                "sample_count": recording.sample_count,
                "started_at": recording.started_at,
                "ended_at": recording.ended_at,
            }
        )
