from fastapi import APIRouter, Depends, Form, Header, UploadFile, File
from sqlmodel import Session

from app.api.services.upload import UploadService
from app.core.db import get_db

router = APIRouter(prefix="/data", tags=["data"])


@router.post("/upload")
def upload_sensor_csv(
    authorization: str = Header(...),
    x_device_id: str = Header(..., alias="x-device-id"),
    data_run_id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    service = UploadService(session=db, user=None)
    return service.upload_sensor_csv(authorization, x_device_id, data_run_id, file)
