import pytest

from tests.conftest import get_db_null_pool


@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (1, "2026-10-01", "2026-10-10", 200),
    (1, "2026-10-01", "2026-10-10", 200),
    (1, "2026-10-01", "2026-10-10", 200),
    (1, "2026-10-01", "2026-10-10", 200),
    (1, "2026-10-01", "2026-10-10", 200),
    (1, "2026-10-01", "2026-10-10", 409),
    (1, "2026-10-01", "2026-10-10", 409),
    (1, "2026-10-01", "2026-10-10", 409),
])
async def test_add_booking(
        room_id, date_from, date_to, status_code,
        db, authenticated_ac
):
    #room_id = (await db.rooms.get_all())[0].id

    response = await authenticated_ac.post(
        url="/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )

    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "ok"
        assert "data" in res


@pytest.fixture(scope="module")
async def delete_all_bookings():
    async for _db in get_db_null_pool():
        await _db.bookings.delete()
        await _db.commit()

@pytest.mark.parametrize("room_id, date_from, date_to, count", [
    (1, "2026-10-01", "2026-10-10", 1),
    (2, "2026-11-01", "2026-11-10", 2),
    (2, "2026-09-11", "2026-09-18", 3),

])
async def test_add_and_get_my_bookings(
    room_id, date_from, date_to, count,
    authenticated_ac, delete_all_bookings,
):
    response = await authenticated_ac.post(
        url="/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to
        }
    )
    assert response.status_code == 200

    response_my_bookings = await authenticated_ac.get(
        url="/bookings/me",
    )
    res = response_my_bookings.json()
    assert response_my_bookings.status_code == 200
    assert len(res) == count
    print(res)


