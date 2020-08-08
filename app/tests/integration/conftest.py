from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.db import models
from app.db.database import SessionLocal, engine
from app.main import app

reverse = app.router.url_path_for


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def db_session():
    models.Base.metadata.create_all(engine)
    session = SessionLocal()
    yield session
    session.close()
    models.Base.metadata.drop_all(bind=engine)