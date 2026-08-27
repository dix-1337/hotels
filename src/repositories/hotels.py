from datetime import date

from sqlalchemy import select

from src.database import engine
from src.models.hotels import HotelsORM
from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import HotelDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsORM
    mapper = HotelDataMapper

    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
            location: str,
            title: str,
            limit: int,
            offset: int
    ) -> list[Hotel]:
        rooms_ids = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotels_ids = (
            select(RoomsORM.hotel_id)
            .select_from(RoomsORM)
            .filter(RoomsORM.id.in_(rooms_ids))
        )
        query = select(self.model).filter(HotelsORM.id.in_(hotels_ids))
        if location:
            query = query.where(self.model.location.ilike('%' + location.strip() + '%'))
        if title:
            query = query.where(self.model.title.ilike(f"%{title.strip()}%"))
        query = (
            query
            .order_by(self.model.id)
            .limit(limit)  # до какого номера
            .offset(offset)  # начиная с какого номера
        )
        result = await self.session.execute(query)
        #print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]
