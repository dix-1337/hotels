from datetime import date

from pydantic import BaseModel


class BookingAdd(BaseModel):
    room_id: int
    date_from: date
    date_to: date

class BookingAddWithPrice(BookingAdd):
    user_id: int
    price: int

class Booking(BookingAddWithPrice):
    id: int