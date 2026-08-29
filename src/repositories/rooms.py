from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from src.database import engine
from src.models.rooms import RoomsORM
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RoomDataMapper, RoomDataWIthRelsMapper
from src.repositories.utils import rooms_ids_for_booking


class RoomsRepository(BaseRepository):
    model = RoomsORM
    mapper = RoomDataMapper

    async def get_filtered_by_time(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date
):
        rooms_ids_to_get = rooms_ids_for_booking(hotel_id=hotel_id, date_from=date_from, date_to=date_to)

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsORM.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        return [RoomDataWIthRelsMapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_room_by_id(self, room_id):
        get_room_query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter_by(id=room_id)
        )
        result = await self.session.execute(get_room_query)
        model = result.unique().scalars().one_or_none()
        if model is None:
            return None
        return RoomDataWIthRelsMapper.map_to_domain_entity(model)


