from typing import Any

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from mangum import Mangum

from app.errors import ApiException, api_exception_handler, validation_exception_handler
from app.routes.health import router as health_router
from app.routes.readings import router as readings_router

app = FastAPI(title="przeczytai.me API")
app.add_exception_handler(ApiException, api_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.include_router(health_router)
app.include_router(readings_router)

_mangum_handler: Mangum | None = None


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    global _mangum_handler
    if _mangum_handler is None:
        _mangum_handler = Mangum(app, lifespan="off")
    return _mangum_handler(event, context)
