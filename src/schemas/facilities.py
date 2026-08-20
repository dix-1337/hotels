from pydantic import BaseModel


class FacilityAdd(BaseModel):
    title: str
    # rooms: list[int] = [] # - короче я так понимаю не хватает этого поля,
    # но пустой список оно не принимает, надо смотреть как в другой таблице
    # это сделано, в исходниках автора можно еще глянуть если сам не допру

class Facility(FacilityAdd):
    id: int


class RoomFacilityAdd(BaseModel):
    room_id: int
    facility_id: int

class RoomFacility(RoomFacilityAdd):
    id: int