import strawberry
from strawberry.types import Info
from python_clean_arch.adapter.graphql.context import get_user_usecase

from python_clean_arch.adapter.graphql.definitions.user import (
    UserMutationSchema,
    UserSchema,
)


@strawberry.type(description="Mutate all Entity")
class Mutation:
    @strawberry.field(description="Adds a new Author")
    def add_author(self, author: UserMutationSchema, info: Info) -> UserSchema:
        user_usecase = get_user_usecase(info)
        return user_usecase.add(author)
