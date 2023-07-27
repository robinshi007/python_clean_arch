import strawberry


@strawberry.type(description="Operation result")
class ResultSchema:
    ok: bool


@strawberry.type(description="User Schema")
class UserSchema:
    id: int
    name: str
    created_at: float
    updated_at: float
    is_active: bool


@strawberry.input(description="User Mutation Schema")
class UserMutationSchema:
    name: str
    is_active: bool
