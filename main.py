from contextlib import asynccontextmanager

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_swagger_ui_theme import setup_swagger_ui_theme

import uvicorn
from fastapi import FastAPI
from src.api.hotels import router as router_hotels
from src.api.auth import router as router_auth
from src.api.rooms import router as router_rooms
from src.api.bookings import router as router_booking
from src.api.facilities import router as router_facilities
from src.api.images import router as router_images
from src import redis_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # При старте приложения
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    yield
    # При выключении/перезагрузке приложения
    await redis_manager.close()


app = FastAPI(lifespan=lifespan, docs_url=None)
setup_swagger_ui_theme(app, docs_path="/docs")
app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_facilities)
app.include_router(router_booking)
app.include_router(router_images)




if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)