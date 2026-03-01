from fastapi import APIRouter

from app.schemas.user_schema import (
    MessageResponse,
    UserUpdateRequest,
    UserUpdateResponse,
    UserDeleteRequest,
    UserGetResponse
)
from app.api.v1.dependencies.services import UserServiceDep
from app.api.v1.dependencies.auth import CurrentUser


router = APIRouter()


@router.patch("/me", response_model=UserUpdateResponse)
async def update_user_data(
    user_data: UserUpdateRequest,
    user_service: UserServiceDep,
    current_user: CurrentUser,
):
    """
    Atualiza os dados do usuário.
    """
    return await user_service.update_user(user_data, current_user)


@router.delete("/me/delete", response_model=MessageResponse)
async def delete(
    user_data: UserDeleteRequest,
    user_service: UserServiceDep,
    current_user: CurrentUser,
):
    """
    Deleta o usuário.
    """
    return await user_service.delete_user(user_data, current_user)


@router.get("/me", response_model=UserGetResponse)
async def get_user_data(
    user_service: UserServiceDep,
    current_user: CurrentUser,
):
    """
    Retorna os dados do usuário.
    """
    return await user_service.retrieve_user_data(current_user)