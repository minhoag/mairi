from typing import Generic, Optional, TypeVar

from pydantic import BaseModel
from starlette.responses import JSONResponse

T = TypeVar("T")


class ResponseWrapper(BaseModel, Generic[T]):
    status: str
    status_code: str
    message: Optional[str] = None
    data: Optional[T] = None


class SuccessResponse(ResponseWrapper[T]):
    status: str = "SUCCESS"
    status_code: str = "200"
    cursor: Optional[int] = None
    # success return data not msg


class ErrorResponse(ResponseWrapper[T]):
    status: str = "FAILED"
    status_code: str = "500"

    def __init__(self, code: str = "00", **data):
        fields = type(self).model_fields
        default_status_code = fields["status_code"].default
        default_status = fields["status"].default
        resolved_status_code = str(data.pop("status_code", default_status_code))
        resolved_status = data.pop("status", default_status)
        super().__init__(
            status=resolved_status,
            status_code=resolved_status_code,
            **data,
        )

    def to_asgi_response(self, code: str = "00") -> JSONResponse:
        if not self.message:
            self.message = "Internal Server Error"
        return JSONResponse(
            status_code=int(self.status_code),
            content={
                "status": self.status,
                "status_code": self.status_code,
                "message": self.message,
                "data": self.data,
            },
        )


class BadRequestResponse(ErrorResponse):
    status: str = "BAD REQUEST"
    status_code: str = "400"

    def __init__(self, code: str = "00", message: str = "Bad Request", **data):
        super().__init__(code=code, message=message, **data)


class UnauthorizedResponse(ErrorResponse):
    status: str = "UNAUTHORIZED"
    status_code: str = "401"

    def __init__(self, code: str = "00", message: str = "Unauthorized", **data):
        super().__init__(code=code, message=message, **data)


class ForbiddenResponse(ErrorResponse):
    status: str = "FORBIDDEN"
    status_code: str = "403"

    def __init__(self, code: str = "00", message: str = "Forbidden", **data):
        super().__init__(code=code, message=message, **data)


class NotFoundResponse(ErrorResponse):
    status: str = "NOT FOUND"
    status_code: str = "404"

    def __init__(self, code: str = "00", message: str = "Not Found", **data):
        super().__init__(code=code, message=message, **data)


class ConflictResponse(ErrorResponse):
    status: str = "CONFLICT"
    status_code: str = "409"

    def __init__(self, code: str = "00", message: str = "Conflict", **data):
        super().__init__(code=code, message=message, **data)
