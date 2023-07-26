from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from strawberry.types import Info
from python_clean_arch.registry.container import Container
from python_clean_arch.usecases.user_usecase import UserUsecase


@inject
async def get_graphql_context(
    user_usecase: UserUsecase = Depends(Provide[Container.user_usecase]),
):
    return {"user_usecase": user_usecase}


def get_user_usecase(info: Info) -> UserUsecase:
    return info.context["user_usecase"]
