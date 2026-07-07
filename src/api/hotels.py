from fastapi import Query, Body, APIRouter
from sqlalchemy import insert

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.models.hotels import HotelsORM
from src.schemas.hotels import Hotel, HotelPatch

router = APIRouter(prefix='/hotels', tags=['Отели'])

hotels = [
    {"id" : 1, "title" : "Sochi", "name": "Красная поляна"},
    {"id" : 2, "title" : "Dubai", "name": "Palm Jumeira"},
    {"id" : 3, "title" : "Minsk", "name": "Гостиница Европа"},
    {"id" : 4, "title" : "New York", "name": "Grand Hotel"},
    {"id" : 5, "title" : "London", "name": "Qeens Palace"},
    {"id" : 6, "title" : "Moscow", "name": "President"},
    {"id" : 7, "title" : "Thailand", "name": "Villa la Thai"},
]


@router.get("", summary='Возвращает список отелей')
def get_hotels(pagination: PaginationDep,
               title: str | None = Query(default=None, description="Название отеля"),
               hotel_id: int | None = Query(None, description="Номер отеля"),

)->list[dict]:
    n = (pagination.page-1)*pagination.per_page

    if title is None and hotel_id is None:
        return hotels[n:n+pagination.per_page]

    filtered = [hotel for hotel in hotels if hotel["title"]==title or hotel["id"]==hotel_id]
    return filtered[n:n+pagination.per_page]

@router.post("", summary="Добавить новый отель")
async def create_hotel(hotel: Hotel = Body(openapi_examples={
    "1": {
        "summary" : "Сочи",
        "values": {
            "title": "Красная Поляна",
            "location": "Сочи, ул.Первомайская 11"
        }
    },
    "2": {
        "summary" : "Минск",
        "values": {
            "title": "Европа",
            "location": "Минск, пр.Независимости 42"
        }
    }
})):
    async with async_session_maker() as session:
        new_hotel = HotelsORM(title=hotel.title, location=hotel.location)
        session.add(new_hotel)

        add_hotel_stmt = insert(HotelsORM).values(**hotel.model_dump())
        await session.execute(add_hotel_stmt)

        await session.commit()

    return {"status" : "OK", "id" : new_hotel.id}

@router.put("/{id}", summary="Изменить отель по номеру")
def put_hotel(id: int,
              hotel_data: Hotel)->dict:

    for hotel in hotels:
        if hotel["id"]==id:
            hotel["name"] = hotel_data.name
            hotel["title"] = hotel_data.title
            return {"status" : "OK"}
    return {"status": "Данный id не был найден"}

@router.patch("/{id}", summary="Частично изменить отель по номеру")
def patch_hotel(id: int,
                hotel_data: HotelPatch)->dict:
    if hotel_data.title is None and hotel_data.name is None:
        return {"status" : "Вы не ввели данные"}
    for hotel in hotels:
        if hotel["id"]==id:
            if hotel_data.name:
                hotel["name"] = hotel_data.name
            if hotel_data.title:
                hotel["title"] = hotel_data.title
            return {"status": "OK"}
    return {"status" : "Данный id не был найден"}

@router.delete("/{hotel_id}", summary="Удалить отель по номеру")
def delete_hotel(hotel_id: int):
    #hotels[:] = [hotel for hotel in hotels if hotel["id"]!=hotel_id]
    del_hotel = {}
    for i,hotel in enumerate(hotels):
        if hotel["id"]==hotel_id:
            del_hotel = hotel
            print(f"Удаляем {del_hotel}")
            hotels.remove(hotel)
            break
    return f"Удаленный отель {del_hotel=}"
