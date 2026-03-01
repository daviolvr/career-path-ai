from fastapi import APIRouter, Depends, Request, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.auth_schema import (
    RegisterRequest,
    LoginRequest, 
    TokenResponse, 
    MessageResponse, 
    RefreshTokenResponse,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    LoginResponse,
)
from app.models.user import User
from app.api.v1.dependencies.security import verify_token, verify_refresh_token
from app.api.v1.dependencies.services import UserServiceDep

router = APIRouter()


@router.post("/register", response_model=MessageResponse, status_code=201)
async def create_account(
    user_data: RegisterRequest, 
    user_service: UserServiceDep
):
    """
    Cria um novo usuário no banco de dados.
    """
    return await user_service.create_user_account(user_data)


@router.post("/login", response_model=LoginResponse)
async def login(
    login_schema: LoginRequest, 
    user_service: UserServiceDep
):
    """
    Autentica usuários no sistema.
    """
    return await user_service.login(login_schema)


@router.post("/login-form", response_model=TokenResponse)
async def login_form(
    user_service: UserServiceDep, 
    form_data: OAuth2PasswordRequestForm = Depends()
):
    return await user_service.login_form(form_data)


@router.post("/refresh", response_model=RefreshTokenResponse)
async def use_refresh_token(
    user_service: UserServiceDep,
    user: User = Depends(verify_refresh_token),
):
    """
    Rota para gerar novo access token usando refresh token
    """
    return await user_service.use_refresh_token(user)


@router.post("/logout", response_model=MessageResponse)
async def logout(
    request: Request,
    user_service: UserServiceDep,
    current_user: User = Depends(verify_token),
):
    """
    Faz logout do usuário adicionando o token à blacklist
    """
    return await user_service.logout(request, current_user)


@router.post("/forgot-password", response_model=MessageResponse)
async def forgot_password(
    request_data: ForgotPasswordRequest, 
    background_tasks: BackgroundTasks, 
    user_service: UserServiceDep
):
    return await user_service.forgot_user_password(request_data, background_tasks)


@router.post("/reset-password", response_model=MessageResponse)
async def reset_password(
    request_data: ResetPasswordRequest, 
    user_service: UserServiceDep
):
    """
    Reseta a senha do usuário.
    """
    return await user_service.reset_user_password(request_data)
