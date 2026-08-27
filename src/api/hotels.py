from datetime import date, timedelta
from fastapi_cache.decorator import cache
from fastapi import Query, Body, APIRouter, HTTPException

from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import Hotel, HotelPatch, HotelAdd

router = APIRouter(prefix='/hotels', tags=['Отели'])


@router.get("", summary='Возвращает список отелей')
@cache(expire=10)
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        title: str | None = Query(default=None, description="Название отеля"),
        location: str | None = Query(None, description="Адрес отеля"),
        date_from: date = date.today(),
        date_to: date = date.today() + timedelta(days=7),

):
    if date_from>=date_to:
        raise HTTPException(status_code=404, detail="Неверный диапазон дат")
    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        limit=pagination.per_page,
        offset=pagination.per_page * (pagination.page - 1)
    )

@router.get("/{hotel_id}", summary="Получить отель по id")
async def get_hotel_by_id(db: DBDep, hotel_id: int)->Hotel | None:
        return await db.hotels.get_one_or_none(id=hotel_id)

@router.post("", summary="Добавить новый отель")
async def create_hotel(db: DBDep, hotel: HotelAdd = Body(openapi_examples={
    "1": {
        "summary" : "Сочи",
        "value": {
            "title": "Красная Поляна",
            "location": "Сочи, ул.Первомайская 11"
        }
    },
    "2": {
        "summary" : "Минск",
        "value": {
            "title": "Европа",
            "location": "Минск, пр.Независимости 42"
        }
    }
}))->dict:
    new_hotel = await db.hotels.add(hotel)
    await db.commit()
    return {"status": "ok", "data": new_hotel}


@router.put("/{id}", summary="Изменить отель по номеру")
async def put_hotel(db: DBDep,
                    hotel_id: int,
                    hotel_data: HotelAdd
)->dict:
    await db.hotels.edit(data=hotel_data, id=hotel_id)
    await db.commit()
    return {"status" : "OK"}


@router.patch("/{id}", summary="Частично изменить отель по номеру")
async def patch_hotel(db: DBDep,
                      hotel_id: int,
                      hotel_data: HotelPatch
)->dict:
    if hotel_data.title is None and hotel_data.location is None:
        return {"status" : "Вы не ввели данные"}

    await db.hotels.edit(data=hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status" : "OK"}

@router.delete("/{hotel_id}", summary="Удалить отель по номеру")
async def delete_hotel(db: DBDep,
                       hotel_id: int
):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status" : "OK"}
