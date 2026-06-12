import uvicorn
from fastapi import FastAPI
from hotels import router as router_hotels

app = FastAPI()
app.include_router(router_hotels)

from database import Base, engine, SyncOrm
Base.metadata.create_all(bind=engine)
SyncOrm.select_tables()

# if __name__ == "__main__":
#     uvicorn.run("main:app", reload=True)