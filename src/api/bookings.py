from celery.worker.consumer.mingle import exception
from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, AuthentificationDep
from src.schemas.bookings import BookingAdd, BookingAddWithPrice

router = APIRouter(prefix="/bookings", tags=["Бронирование"])

@router.get("")
async def get_bookings(db: DBDep):
    bookings = await db.bookings.get_all()
    return bookings

@router.get("/me")
async def get_my_bookings(db: DBDep, user_id: AuthentificationDep):
    my_bookings = await db.bookings.get_filtered(user_id=user_id)
    return my_bookings

@router.post("")
async def add_booking(db: DBDep, user_id: AuthentificationDep, booking: BookingAdd):
    if booking.date_from>=booking.date_to:
        raise HTTPException(status_code=404, detail="Неверный диапазон дат")
    booking_dict = booking.model_dump()
    booking_dict["user_id"] = user_id
    room = await db.rooms.get_one_or_none(id=booking.room_id)
    if room is None:
        raise HTTPException(status_code=400, detail="Номер недоступен")

    booking_dict["price"] = await db.bookings.total_cost(
        price=room.price,
        date_to=booking.date_to,
        date_from=booking.date_from
        )
    new_booking = BookingAddWithPrice(**booking_dict)
    await db.bookings.add_booking(new_booking, hotel_id=room.hotel_id)
    await db.commit()
    return {"status": "ok", "data": new_booking}

# @router.get("/today-checkin")
# async def get_today_bookings(db: DBDep):
#     return await db.bookings.get_bookings_with_today_checkin()

