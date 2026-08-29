from datetime import date

from pydantic import BaseModel


class BookingAdd(BaseModel):
    room_id: int
    date_from: date
    date_to: date

class BookingAddWithPrice(BaseModel):
    user_id: int
    room_id: int
    date_from: date
    date_to: date
    price: int

class Booking(BookingAddWithPrice):
    id: int

class BookingEdit(BaseModel):
    room_id: int | None = None
    date_from: date | None = None
    date_to: date | None = None
    price: int | None = None