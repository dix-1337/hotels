from datetime import date
from fastapi import HTTPException

from pydantic import BaseModel
from sqlalchemy import select

from src.models.bookings import BookingsORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.rooms import RoomsRepository
from src.repositories.utils import rooms_ids_for_booking


class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingDataMapper

    async def total_cost(self, price: int, date_to: date, date_from: date) -> int:
        return price * (date_to - date_from).days

    async def get_bookings_with_today_checkin(self):
        query = (
            select(BookingsORM)
            .where(BookingsORM.date_from == date.today())
        )
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]

    async def add_booking(self, data: BaseModel, hotel_id):
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=data.date_from,
            date_to=data.date_to,
            hotel_id=hotel_id
        )
        rooms_ids_free: list[int] = (await self.session.execute(rooms_ids_to_get)).scalars().all()
        print(f"{rooms_ids_free=}")
        if data.room_id in rooms_ids_free:
            return await self.add(data)
        else:
            raise HTTPException(status_code=409, detail="Данный номер недоступен для бронирования")
