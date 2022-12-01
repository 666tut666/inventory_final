from fastapi import status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_utils.inferring_router import InferringRouter

from app.api.dependencies import get_session
from app.manager.manager_auth import AuthManager
from app.schemas.schema_token import Token
from app.utils.exceptions.exception_route_handler import ExceptionRouteHandler

router = InferringRouter(route_class=ExceptionRouteHandler, tags=["Authentication"])


@router.post("/auth/login", status_code=status.HTTP_201_CREATED)
def login(data: OAuth2PasswordRequestForm = Depends()) -> Token:
    return AuthManager.login(data)


@router.get("/auth/logout", status_code=status.HTTP_200_OK)
def logout(session=Depends(get_session)):
    return AuthManager.logout(session)
