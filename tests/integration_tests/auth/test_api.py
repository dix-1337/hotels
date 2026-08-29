import pytest

from src.services.auth import AuthService

# add password validator
@pytest.mark.parametrize("email, password, status_code", [
    ("testmail123@gmail.com", "1234test", 200), # оригинал
    ("testmail123@gmail.com", "1234test", 409), # копия, существующий email
    ("testmail123@gmail", "1234test", 422), # некорректный email
    ("testmail123@gmail.com", "", 422), # некорректный пароль
    ("justinbieber@gmail.com", "32best234", 200),
    ("patricbaitman@gmail.com", "666red777", 200),
    ("catwithdogs99@gmail.com", "love342u", 200),
])
async def test_authorization(
        email: str,
        password: str,
        status_code: int,
        ac
):
    # register
    register_response = await ac.post(
        url="/auth/register",
        json={
            "email": email,
            "password": password
        }
    )
    assert register_response.status_code == status_code

    if register_response.status_code != 200:
        return

    # /login
    login_response = await ac.post(
        url="/auth/login",
        json={
            "email": email,
            "password": password
        }
    )
    access_token = ac.cookies.get("access_token")
    assert login_response.status_code == 200
    assert access_token
    assert isinstance(access_token, str)
    user_id = AuthService().decode_access_token(access_token)["user_id"]
    assert "access_token" in login_response.json()

    # /me
    response_me = await ac.get(
        url="/auth/me"
    )
    user = response_me.json()
    assert response_me.status_code == 200
    assert user.get("id") == user_id
    assert user.get("email") == email
    assert "password" not in user
    assert "hashed_password" not in user

    # logout
    logout_response = await ac.post(
        url="/auth/logout",
    )
    assert logout_response.status_code == 200
    assert not ac.cookies.get("access_token")

