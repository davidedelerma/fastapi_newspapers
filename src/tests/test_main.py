import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.auth import pwd_context
from src.dependency import get_db
from src.main import app
from src.orm.database import Base
from src.orm.user import User

SQLALCHEMY_DATABASE_URL = 'sqlite:///:memory:'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine,
)

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
    response = client.get(
        '/newspapers/',
        json={},
    )
    assert response.status_code == 200


db_user = User(
    email='test@test.com',
    user_name='test_username',
    first_name='test',
    last_name='test',
    password=pwd_context.hash('test'),
    is_superuser=True,
)


@pytest.mark.asyncio
async def test_root():
    db = TestingSessionLocal()
    db.add(db_user)
    db.commit()
    async with AsyncClient(app=app, base_url='http://testserver') as ac:
        response = await ac.post(
            '/token/',
            data={
                'username': 'test_username',
                'password': 'test',
            },
            headers={'content-type': 'application/x-www-form-urlencoded'},
        )
    assert response.status_code == 200
