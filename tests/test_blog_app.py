import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv
from fastapi.testclient import TestClient

from database import Base, get_db
from main import app

load_dotenv()

DATABASE_URL = os.getenv("TEST_DATABASE_URL")


test_engine = create_async_engine(DATABASE_URL,
                                  connect_args={'check_same_thread': False},
                                  echo=True)

TestSession = async_sessionmaker(bind=test_engine, autoflush=False)


async def override_get_db():
    async with TestSession() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db


async def init_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_db())


test_client = TestClient(app)


def test_create_user():
    response = test_client.post("/api/posts/users/", json={"username": "testuser",
                                                           "password": "testpassword",
                                                           "first_name": "Test",
                                                           "last_name": "User"})

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"


def test_create_post():
    token = test_client.post("/api/posts/users/login/",
                             data={"username": "testuser", "password": "testpassword"}).json()["access_token"]
    response = test_client.post("/api/posts/post/",
                                headers={"Authorization": f"Bearer {token}"},
                                json={"title": "Test post", "content": "This is a test post", "user_id": 1})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test post"
    assert data["content"] == "This is a test post"
    assert data["user_id"] == 1


def test_update_post():
    token = test_client.post("/api/posts/users/login/",
                             data={"username": "testuser", "password": "testpassword"}).json()["access_token"]
    response = test_client.put("/api/posts/post/1",
                               headers={"Authorization": f"Bearer {token}"},
                               json={"title": "Updated post", "content": "This is an updated post", "user_id": 1})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated post"
    assert data["content"] == "This is an updated post"
    assert data["user_id"] == 1
