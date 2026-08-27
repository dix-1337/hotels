from unittest import mock

mock.patch("src.api.facilities.test_task").start()

async def test_add_facilities(ac):
    title = "test"
    response = await ac.post(
        url="/facilities",
        json = {"title": title}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert response.json()["data"]["title"] == title
    assert "data" in response.json()

async def test_get_facilities(ac):
    response = await ac.get(url="/facilities")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

