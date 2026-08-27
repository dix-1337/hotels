from datetime import date

from src.schemas.bookings import BookingAdd, BookingAddWithPrice, BookingEdit


async def test_booking_crud(db):
    user = (await db.users.get_all())[0]
    room = (await db.rooms.get_all())[0]
    booking_data = BookingAddWithPrice(
        user_id=user.id,
        room_id=room.id,
        date_from=date(year=2026, month=9, day=20),
        date_to=date(year=2026, month=9, day=27),
        price=1400,
    )
    # создать бронь
    new_booking = await db.bookings.add(booking_data)
    # получить бронь и убедиться что она есть
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking
    assert booking.id == new_booking.id
    assert new_booking.room_id == room.id
    assert new_booking.user_id == user.id

    # обновить бронь
    updated_date = date(year=2026, month=9, day=17)
    await db.bookings.edit(
        data=BookingEdit(
            date_from=updated_date,
            price=2400,
        ),
        id=new_booking.id,
        exclude_unset=True
    )
    updated_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert updated_booking
    assert updated_booking.date_from
    assert updated_booking.price == 2400
    assert updated_booking.room_id == room.id

    # удалить бронь
    await db.bookings.delete(id=new_booking.id)
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert not booking

    await db.commit()
