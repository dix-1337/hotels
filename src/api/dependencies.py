from fastapi import Query
from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel

class PaginationParams(BaseModel):
    page: Annotated[int, Query(1, gt=0)]
    per_page: Annotated[int, Query(3, gt=0, le=30)]

PaginationDep = Annotated[PaginationParams, Depends()]