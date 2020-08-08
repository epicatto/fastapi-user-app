import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import router
from app.db import models
from app.db.database import engine

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

models.Base.metadata.create_all(bind=engine)

app.include_router(
    router,
    tags=["records"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
