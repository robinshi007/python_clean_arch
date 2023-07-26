from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from python_clean_arch.domain.dtos.base_dto import Blank, FindBase

from python_clean_arch.domain.dtos.user_dto import (
    FindUser,
    FindUserResult,
    UpsertUser,
    User,
)
from python_clean_arch.registry.container import Container
from python_clean_arch.usecases.user_usecase import UserUsecase


router = APIRouter(prefix="/user", tags=["user"])


@router.get("", response_model=FindUserResult)
@inject
async def get_user_list(
    find_query: FindBase = Depends(),
    usecase: UserUsecase = Depends(Provide[Container.user_usecase]),
):
    return usecase.get_list(find_query)


@router.get("/{user_id}", response_model=User)
@inject
async def get_user(
    user_id: int,
    usecase: UserUsecase = Depends(Provide[Container.user_usecase]),
):
    return usecase.get_by_id(user_id)


@router.post("", response_model=User)
@inject
async def create_user(
    user: UpsertUser,
    usecase: UserUsecase = Depends(Provide[Container.user_usecase]),
):
    return usecase.add(user)


@router.patch("/{user_id}", response_model=User)
@inject
async def update_user(
    user_id: int,
    user: UpsertUser,
    usecase: UserUsecase = Depends(Provide[Container.user_usecase]),
):
    return usecase.update(user_id, user)


@router.delete("/{user_id}", response_model=Blank)
@inject
async def delete_user(
    user_id: int,
    usecase: UserUsecase = Depends(Provide[Container.user_usecase]),
):
    usecase.remove_by_id(user_id)
    return {"ok": True}
