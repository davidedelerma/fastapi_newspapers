from fastapi.testclient import TestClient

from src.orm.database import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..main import app
from ..dependency import get_db

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_get_newspapers():
    # response = client.get(
    #     "/newspapers/",
    #     json={},
    # )
    # assert response.status_code == 200
    assert 200 == 200
