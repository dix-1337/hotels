from pydantic import BaseModel
from sqlalchemy import select, update, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import engine
from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_filtered(self, *filter, **filter_by)->list[BaseModel]:
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        #print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs)->list[BaseModel]:
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by: dict) -> BaseModel | None:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        #print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def add(self, model: BaseModel)->BaseModel:
        # add_data_stmt = insert(self.model).values(**model.model_dump()).returning(self.model)
        # result = await self.session.execute(add_data_stmt)
        # new_model = result.scalars().one()
        # return self.mapper.map_to_domain_entity(new_model)
        new_model = self.model(**model.model_dump())
        self.session.add(new_model)
        await self.session.flush() # для id
        return self.mapper.map_to_domain_entity(new_model)

    async def add_bulk(self, model: list[BaseModel]) -> dict:
        new_models = [ self.model(**item.model_dump()) for item in model ]
        self.session.add_all(new_models)
        # add_data_stmt = insert(self.model).values([item.model_dump() for item in model])
        # await self.session.execute(add_data_stmt)


    # async def edit(self, data: BaseModel, **filter_by)->None:
    #     stmt = (
    #         update(self.model)
    #         .values(**data.model_dump())
    #         .filter_by(**filter_by)
    #     )
    #     await self.session.execute(stmt)
    #     print(stmt.compile(engine, compile_kwargs={"literal_binds": True}))

    async def edit(self, data: BaseModel, exclude_unset: bool=False, **filter_by)->None:
        stmt = (
            update(self.model)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            #exclude_unset=True возвращает только те параметры, которые реально были переданы
            .filter_by(**filter_by)
        )
        await self.session.execute(stmt)
        #print(stmt.compile(engine, compile_kwargs={"literal_binds": True}))

    async def delete(self, **filter_by)->None:
        stmt = (
            delete(self.model)
            .filter_by(**filter_by)
        )
        res = await self.session.execute(stmt)
        #print(stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        print(f"Удалено строк: {res.rowcount}")

