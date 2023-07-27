import strawberry
from strawberry.types import Info
from python_clean_arch.adapter.graphql.context import get_user_usecase

from python_clean_arch.adapter.graphql.definitions.user import (
    ResultSchema,
    UserMutationSchema,
    UserSchema,
)
from python_clean_arch.adapter.rest.v1.endpoints.user import delete_user
from python_clean_arch.domain.dtos.user_dto import UpsertUser


@strawberry.type(description="Mutate all Entity")
class Mutation:
    @strawberry.field(description="Ads an new user")
    def add_user(self, user: UserMutationSchema, info: Info) -> UserSchema:
        user_usecase = get_user_usecase(info)
        user_dto = UpsertUser(name=user.name, is_active=user.is_active)
        return user_usecase.add(user_dto)

    @strawberry.field(description="Update an user")
    def update_user(self, id: int, user: UserMutationSchema, info: Info) -> UserSchema:
        user_usecase = get_user_usecase(info)
        user_dto = UpsertUser(name=user.name, is_active=user.is_active)
        return user_usecase.update(id, user_dto)

    @strawberry.field(description="Remove an user")
    def delete_user(self, id: int, info: Info) -> ResultSchema:
        user_usecase = get_user_usecase(info)
        if user_usecase.remove_by_id(id) == None:
            return ResultSchema(ok=True)
        else:
            return ResultSchema(ok=False)
