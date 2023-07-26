from typing import List
import strawberry
from strawberry.types import Info
from python_clean_arch.adapter.graphql.context import get_user_usecase

from python_clean_arch.adapter.graphql.definitions.user import UserSchema
from python_clean_arch.domain.dtos.base_dto import FindBase


@strawberry.type(description="Query all entities")
class Query:
    @strawberry.field(description="List all users")
    async def users(self, info: Info) -> List[UserSchema]:
        user_usecase = get_user_usecase(info)
        res = user_usecase.get_list(FindBase())
        return [UserSchema(**d) for d in res["founds"]]

    @strawberry.field(description="Get an user")
    async def user(self, id: int, info: Info) -> UserSchema:
        user_usecase = get_user_usecase(info)
        return user_usecase.get_by_id(id)
