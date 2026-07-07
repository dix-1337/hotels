from pydantic import BaseModel, Field

class Hotel(BaseModel):
    title: str
    location: str

class HotelPatch(BaseModel):
    name: str | None = Field(default=None)
    location: str | None = Field(default=None)