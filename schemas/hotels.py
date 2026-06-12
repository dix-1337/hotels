from pydantic import BaseModel, Field

class Hotel(BaseModel):
    title: str
    name: str

class HotelPatch(BaseModel):
    name: str | None = Field(default=None)
    title: str | None = Field(default=None)