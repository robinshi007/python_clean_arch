from typing import List, Optional
from pydantic import BaseModel, ConfigDict

from python_clean_arch.domain.dtos.base_dto import (
    FindBase,
    ModelBaseInfo,
    SearchOptions,
)
from python_clean_arch.utils.dto import AllOptional


class BaseUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    is_active: bool = True


class User(ModelBaseInfo, BaseUser, metaclass=AllOptional):
    ...


class FindUser(FindBase, BaseUser, metaclass=AllOptional):
    name__eq: str


class UpsertUser(BaseUser, metaclass=AllOptional):
    ...


class FindUserResult(BaseModel):
    founds: Optional[List[User]]
    search_options: Optional[SearchOptions]
