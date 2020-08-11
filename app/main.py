import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse, JSONResponse

from app.config.exceptions import ValidationException
from app.db import models
from app.db.database import engine
from app.routers import organizations
from app.routers import rights
from app.routers import roles
from app.routers import users

app = FastAPI(
    title="FastAPI - Users management sample application",
    description=""
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

models.Base.metadata.create_all(bind=engine)


@app.get("/", name="home")
def main():
    return RedirectResponse(url="/docs/")


app.include_router(
    users.router,
    prefix="/users",
    tags=["users"],
)

app.include_router(
    organizations.router,
    prefix="/organizations",
    tags=["organizations"],
)

app.include_router(
    roles.router,
    prefix="/roles",
    tags=["roles"],
)

app.include_router(
    rights.router,
    prefix="/rights",
    tags=["rights"],
)


@app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc: ValidationException) -> JSONResponse:
    """
    Custom exception handler for ValidationException
    This returns a JSON format message.
    :param request:
    :param exc:
    :return:
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=str(exc),
    )


@app.exception_handler(Exception)
async def http_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Default exception handler.
    This returns a JSON format message.
    :param request:
    :param exc:
    :return:
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=str(exc),
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
