async def test_add_booking(db, authenticated_ac):
    room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        url="/bookings",
        json={
            "room_id": room_id,
            "date_from": "2026-10-01",
            "date_to": "2026-10-10",
        }
    )
    res = response.json()
    assert response.status_code == 200
    assert isinstance(res, dict)
    assert res["status"] == "ok"
    assert "data" in res