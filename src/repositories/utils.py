from datetime import date

from sqlalchemy import select, func

from src.models.bookings import BookingsORM
from src.models.rooms import RoomsORM

def rooms_ids_for_booking(
        date_from: date,
        date_to: date,
        hotel_id: int | None = None
):
    bookings_count = (
        select(BookingsORM.room_id, func.count("*").label("rooms_booked"))
        .select_from(BookingsORM)
        .filter(
            BookingsORM.date_from < date_to,
            BookingsORM.date_to > date_from
        )
        .group_by(BookingsORM.room_id)
        .cte(name="bookings_count")
    )
    total_free_table = (
        select(
            RoomsORM.id.label("room_id"),
            (RoomsORM.quantity - func.coalesce(bookings_count.c.rooms_booked, 0)).label("total_free")
        )
        .select_from(RoomsORM)
        .outerjoin(bookings_count, RoomsORM.id == bookings_count.c.room_id)
        .cte(name="total_free_table")
    )
    rooms_ids_for_hotels = (
        select(RoomsORM.id)
        .select_from(RoomsORM)
    )
    if hotel_id is not None:
        rooms_ids_for_hotels = rooms_ids_for_hotels.filter_by(hotel_id=hotel_id)
    rooms_ids_for_hotels = rooms_ids_for_hotels.subquery(name="rooms_for_hotels")

    rooms_ids_to_get = (
        select(total_free_table.c.room_id)
        .select_from(total_free_table)
        .filter(
            total_free_table.c.total_free > 0,
            total_free_table.c.room_id.in_(select(rooms_ids_for_hotels))
        )
    )
    # print(rooms_ids_to_get.compile(bind=engine, compile_kwargs={"literal_binds": True}))
    return rooms_ids_to_get


