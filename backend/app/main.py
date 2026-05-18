from typing import Any

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from mangum import Mangum

from app.auth import require_api_key
from app.config import get_settings
from app.errors import ApiException, api_exception_handler, validation_exception_handler
from app.routes.health import router as health_router
from app.routes.readings import router as readings_router

app = FastAPI(title="przeczytai.me API", docs_url=None, redoc_url=None, openapi_url=None)
app.add_exception_handler(ApiException, api_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.include_router(health_router)
app.include_router(readings_router)

_mangum_handler: Mangum | None = None
PUBLIC_DOCS_PATHS = {
    "/docs",
    "/redoc",
    "/openapi.json",
}


def get_middleware_settings():
    return get_settings()


@app.middleware("http")
async def api_key_middleware(request, call_next):
    if request.url.path in PUBLIC_DOCS_PATHS:
        return await call_next(request)
    try:
        require_api_key(request, get_middleware_settings())
    except ApiException as exc:
        return await api_exception_handler(request, exc)
    return await call_next(request)


@app.get("/openapi.json", include_in_schema=False)
async def openapi_json() -> dict:
    return get_openapi(title=app.title, version=app.version, routes=app.routes)


@app.get("/docs", include_in_schema=False)
async def docs():
    return get_swagger_ui_html(openapi_url="/openapi.json", title=f"{app.title} - Swagger UI")


@app.get("/redoc", include_in_schema=False)
async def redoc():
    return get_redoc_html(openapi_url="/openapi.json", title=f"{app.title} - ReDoc")


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    global _mangum_handler
    if _mangum_handler is None:
        _mangum_handler = Mangum(app, lifespan="off")
    return _mangum_handler(event, context)
