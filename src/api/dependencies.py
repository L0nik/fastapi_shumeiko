from fastapi import Depends, Query
from pydantic import BaseModel
from typing import Annotated

class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, description="Номер страницы", ge=1)]
    per_page: Annotated[int | None, Query(5, description="Количество отелей на странице", ge=1, lt=30)]

PaginationDep = Annotated[PaginationParams, Depends()]