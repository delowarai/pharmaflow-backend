import logging
import time

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.routers import (
    ai,
    auth,
    batches,
    inventory,
    medicines,
    purchases,
    reports,
    sales,
    suppliers,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pharmaflow")

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    started = time.perf_counter()
    response = await call_next(request)
    logger.info(
        "%s %s -> %s (%.3fs)",
        request.method,
        request.url.path,
        response.status_code,
        time.perf_counter() - started,
    )
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(
        "Unhandled error while processing %s", request.url.path, exc_info=exc
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }


api_prefix = "/api/v1"
app.include_router(auth.router, prefix=api_prefix)
app.include_router(medicines.router, prefix=api_prefix)
app.include_router(batches.router, prefix=api_prefix)
app.include_router(suppliers.router, prefix=api_prefix)
app.include_router(purchases.router, prefix=api_prefix)
app.include_router(sales.router, prefix=api_prefix)
app.include_router(inventory.router, prefix=api_prefix)
app.include_router(reports.router, prefix=api_prefix)
app.include_router(ai.router, prefix=api_prefix)
