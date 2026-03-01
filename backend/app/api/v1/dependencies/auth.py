from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from pydantic import ValidationError
from jwt.exceptions import InvalidTokenError
import jwt

from app.core.config import settings
from app.schemas.token import TokenPayload
from app.models.user import User
from app.core.exceptions import AuthenticationException
from app.api.v1.dependencies.repositories import UserRepositoryDep


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login/access-token"
)

TokenDep = Annotated[str, Depends(reusable_oauth2)]


async def get_current_user(token: TokenDep, user_repository: UserRepositoryDep) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if token_data.type != "access":
            raise AuthenticationException("Invalid token type")
    except (InvalidTokenError, ValidationError):
        raise AuthenticationException("Could not validate credentials")
    
    user = await user_repository.get_by_id(int(token_data.sub))

    if not user:
        raise AuthenticationException("Could not validate credentials")
    
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]