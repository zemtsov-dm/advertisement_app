import logging
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler
from fastapi_pagination import add_pagination
from .users.routers.auth import router as auth_router
from .users.routers.users import router as users_router
from .adverts.routers import router as adverts_router
from .complaint.routers import router as complaints_router
from asgi_correlation_id import CorrelationIdMiddleware

logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(CorrelationIdMiddleware)

add_pagination(app)

app.include_router(users_router)
app.include_router(auth_router)
app.include_router(adverts_router)
app.include_router(complaints_router)


@app.exception_handler(HTTPException)
async def http_exception_logging(request,exc):
    logger.error(f"HTTPException: {exc.status_code} {exc.detail}")
    return await http_exception_handler(request,exc)