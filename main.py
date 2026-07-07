import uvicorn
from fastapi import FastAPI
import sys
from src.api.hotels import router as router_hotels
from src.config import settings
from src.database import *


#if sys.platform == 'win32':
    #asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = FastAPI()
app.include_router(router_hotels)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)