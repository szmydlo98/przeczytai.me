from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from mangum import Mangum

from app.errors import ApiException, api_exception_handler, validation_exception_handler
from app.routes.health import router as health_router
from app.routes.textcordings import router as textcordings_router

app = FastAPI(title="przeczytai.me API")
app.add_exception_handler(ApiException, api_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.include_router(health_router)
app.include_router(textcordings_router)

handler = Mangum(app, lifespan="off")
