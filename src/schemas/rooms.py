from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.schemas.facilities import Facility


class RoomAdd(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int
    facilities_ids: list[int] = []

class RoomAddHotelId(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int

class Room(RoomAddHotelId):
    id: int

class RoomsWithRels(Room):
    facilities: list[Facility]

class RoomPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    facilities_ids: list[int] = []

class RoomPatch(BaseModel):
    hotel_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None