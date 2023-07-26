from typing import List, Optional, Union
from pydantic import BaseModel


class ModelBaseInfo(BaseModel):
    id: int
    created_at: int
    updated_at: int


class FindBase(BaseModel):
    ordering: Optional[str] = "-id"
    page: Optional[int] = 1
    page_size: Optional[int] = 20


class SearchOptions(FindBase):
    total_count: Optional[int]


class FindResult(BaseModel):
    founds: Optional[List]
    search_options: Optional[SearchOptions]


class FindDateRange(BaseModel):
    created_at__lt: int
    created_at__lte: int
    created_at__gt: int
    created_at__gte: int


class Blank(BaseModel):
    ok: bool = True
