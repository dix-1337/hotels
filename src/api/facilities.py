from fastapi import APIRouter
import json
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.init import redis_manager
from src.schemas.facilities import FacilityAdd
from src.tasks.tasks import test_task

router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()

    # facilities_from_cache = await redis_manager.get("facilities")
    # print(f"{facilities_from_cache=}")
    # if not facilities_from_cache:
    #     facilities = await db.facilities.get_all()
    #     facilities_schemas: list[dict] = [f.model_dump() for f in facilities]
    #     facilities_json = json.dumps(facilities_schemas)
    #     await redis_manager.set("facilities", facilities_json)
    #     return facilities
    # else:
    #     facilities_dicts = json.loads(facilities_from_cache)
    #     return facilities_dicts

@router.post("")
async def add_facility(db: DBDep, facility: FacilityAdd):
    new_facility = await db.facilities.add(facility)
    await db.commit()

    test_task.delay()

    return {"status": "ok", "new_facility": new_facility}