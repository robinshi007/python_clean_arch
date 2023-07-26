import strawberry


@strawberry.type(description="User Schema")
class UserSchema:
    id: int
    name: str
    created_at: int
    updated_at: int
    is_active: bool


@strawberry.input(description="User Mutation Schema")
class UserMutationSchema:
    name: str
    is_active: bool
