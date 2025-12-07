from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.openapi.utils import get_openapi
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from phone_book.controllers import phone_book_router
from phone_book.redis_manager import RedisManager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await RedisManager.connect()
    yield
    await RedisManager.close()


app = FastAPI(title="Phone book microservice", lifespan=lifespan)
app.include_router(phone_book_router)


@app.get("/")
async def main():
    return "Phone book"


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(content={"detail": exc.errors()}, status_code=status.HTTP_400_BAD_REQUEST)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Phone book microservice",
        version="2.5.0",
        routes=app.routes,
    )

    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if openapi_schema["paths"][path][method]["responses"].get("422"):
                openapi_schema["paths"][path][method]["responses"]["400"] = \
                    openapi_schema["paths"][path][method]["responses"]["422"]
                openapi_schema["paths"][path][method]["responses"].pop("422")

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
