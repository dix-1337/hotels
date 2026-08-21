from fastapi import Query, Request, HTTPException
from typing import Annotated

from fastapi import Depends
from jwt import PyJWTError
from pydantic import BaseModel

from services.auth import AuthService
from src.database import async_session_maker
from src.utils.db_manager import DBManager


class PaginationParams(BaseModel):
    page: Annotated[int, Query(1, gt=0)]
    per_page: Annotated[int, Query(5, gt=0, le=30)]

def get_token(request: Request) -> str:
    #print(f"Cookies: {request.cookies}")
    #print(request.headers)  # метаданные, по типу хоста, токена и тп
    access_token = request.cookies.get("access_token", None)
    if access_token is None:
        raise HTTPException(status_code=401, detail="Вы не аутентифицированы")
    return access_token

def get_current_user_id(token: str = Depends(get_token)) -> int:
    try:
        data = AuthService().decode_access_token(token)
    except PyJWTError as e:
        raise HTTPException(status_code=401, detail=f"Access token is not valid ({type(e)}, {e})")
    user_id = data.get("user_id", None)
    print(data)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Ошибка, пользователь не найден")
    return user_id

def get_db_manager():
    return DBManager(session_factory=async_session_maker)

async def get_db():
    async with get_db_manager() as db:
        yield db


PaginationDep = Annotated[PaginationParams, Depends()]
AuthentificationDep = Annotated[int, Depends(get_current_user_id)]

DBDep = Annotated[DBManager, Depends(get_db)]