from annotated_types import BaseMetadata
from sqlalchemy import create_engine, String, text
from sqlalchemy.orm import DeclarativeBase, Mapped, sessionmaker
from sqlalchemy.testing.schema import mapped_column

engine = create_engine(url="postgresql+psycopg://postgres:sql7829104@localhost:5432/postgres", echo=False)
session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    ...

class Hotels(Base):
    __tablename__ = "hotels"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
    stars: Mapped[int] = mapped_column()

class SyncOrm:
    @staticmethod
    def select_tables():
        with session() as db:
            res = db.execute(text("select * from hotels"))
            print(res.all())

