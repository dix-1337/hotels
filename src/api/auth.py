from sqlalchemy import exc

from fastapi import APIRouter, HTTPException, Response

from services.auth import AuthService
from src.api.dependencies import AuthentificationDep
from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

@router.post("/register")
async def register_user(data: UserRequestAdd) -> dict:
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        try:
            await UsersRepository(session).add(new_user_data)
            await session.commit()
        except exc.IntegrityError as error:
            raise HTTPException(status_code=404, detail="Данный email уже зарегистрирован")

    return {"status": "OK"}

@router.post("/login")
async def login_user(data: UserRequestAdd, response: Response) -> dict:
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Неверный email")
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Неверный пароль")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}

@router.get("/me")
async def get_me(user_id: AuthentificationDep):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
    return user

@router.post("/logout")
def logout_user(response: Response) -> dict:
    response.delete_cookie("access_token")
    return {"status": "OK"}


