import httpx
import pytest
import json
from httpx import AsyncClient

from main import app
from src import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
import src.models
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAddHotelId
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture()
async def db() -> DBManager:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="session", autouse=True)
async def async_main(check_test_mode):
    print("Я ФИКСТУРА")

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with (
        open("tests/mock_rooms.json", encoding="utf-8") as rooms_json,
        open("tests/mock_hotels.json", encoding="utf-8") as hotels_json
    ):
        mock_hotels = json.load(hotels_json)
        mock_rooms = json.load(rooms_json)

    async with DBManager(session_factory=async_session_maker_null_pool) as db_manager:
        await db_manager.hotels.add_bulk([HotelAdd(**item) for item in mock_hotels])
        await db_manager.rooms.add_bulk([RoomAddHotelId.model_validate(item) for item in mock_rooms])
        await db_manager.commit()


transport = httpx.ASGITransport(app=app)

@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(async_main, ac):
    response = await ac.post(
        "auth/register",
        json={
            "email": "testmail13@gmail.com",
            "password": "12345test"
        }
    )
    assert response.status_code == 200

