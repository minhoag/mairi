import sentry_sdk
import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRoute
from sqlalchemy import create_engine
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.VERSION}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.VERSION)
if __name__ == "__main__":
    try:
        engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
        engine.connect()
    except Exception as e:
        print(e)
        exit(1)
    print("Database is online")

    uvicorn.run(
        "main:app",
        host=settings.APP_HOST,
        port=settings.BE_HOST_PORT,
        reload=settings.ENVIRONMENT == "local",
        workers=1,
    )
