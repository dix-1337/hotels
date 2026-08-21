from datetime import date, timedelta

from sqlalchemy import exc
from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep
from src.schemas.facilities import RoomFacilityAdd

from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddHotelId, RoomPatchRequest, RoomsWithRels

router = APIRouter(prefix='/hotels', tags=['Номера'])


@router.get("/{hotel_id}/rooms", summary='Возвращает список номеров')
async def get_rooms(
        db: DBDep, hotel_id: int,
        date_from: date = date.today(),
        date_to: date = date.today() + timedelta(days=7)
):
    if date_from>=date_to:
        raise HTTPException(status_code=404, detail="Неверный диапазон дат")
    try:
        return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
    except exc.IntegrityError:
        raise HTTPException(status_code=404, detail="Неверный номер отеля")


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получить номер по id")
async def get_room_by_id(db: DBDep, hotel_id: int, room_id: int) -> RoomsWithRels | None:
    return await db.rooms.get_room_by_id(room_id=room_id)

@router.post("/{hotel_id}/rooms", summary="Добавить новый номер")
async def create_room(db: DBDep, hotel_id: int, room_data: RoomAdd)->dict:
    _room_data = RoomAddHotelId(hotel_id=hotel_id, **room_data.model_dump())
    try:
        new_room = await db.rooms.add(_room_data)
    except exc.IntegrityError:
        raise HTTPException(status_code=404, detail="Неверный номер отеля")
    rooms_facilities_data = [RoomFacilityAdd(room_id=new_room.id, facility_id=f_id)
                             for f_id in room_data.facilities_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    return {"status": "ok", "data": new_room}

@router.put("/{hotel_id}/rooms/{room_id}", summary="Изменить номер по id")
async def put_room(db: DBDep, hotel_id: int, room_id: int, data: RoomAdd) -> dict:
    room_data = RoomAddHotelId(hotel_id=hotel_id, **data.model_dump())
    await db.rooms.edit(data=room_data,
                        id=room_id,
                    )
    await db.rooms_facilities.set_room_facilities(room_id=room_id, facilities_ids=data.facilities_ids)
    await db.commit()
    return {"status" : "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частично изменить номер по id")
async def patch_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomPatchRequest) -> dict:
    if (room_data.title is None and room_data.description is None
            and room_data.quantity is None and room_data.price is None
            and room_data.facilities_ids is None):
        return {"status" : "Вы не ввели данные"}
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump())
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    await db.rooms.patch(data=_room_data,
                         exclude_unset=True,
                         id=room_id
                    )
    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_room_facilities(room_id=room_id,
                                                      facilities_ids=_room_data_dict["facilities_ids"])
    await db.commit()
    return {"status" : "OK"}

@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удалить номер по id")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    await db.rooms.delete(id=room_id)
    await db.commit()
    return {"status" : "OK"}
