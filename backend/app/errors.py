from fastapi import Request
from fastapi.responses import JSONResponse


class ApiException(Exception):
    def __init__(self, code: str, message: str, status_code: int) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code


async def api_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    if not isinstance(exc, ApiException):
        return JSONResponse(
            status_code=500,
            content={"error": {"code": "internal_error", "message": "Internal error"}},
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.code, "message": exc.message}},
    )


async def validation_exception_handler(_: Request, __: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"error": {"code": "validation_error", "message": "Invalid request"}},
    )
