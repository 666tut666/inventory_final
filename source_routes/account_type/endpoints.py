from typing import List, Optional

from fastapi import Depends, status
from fastapi_utils.inferring_router import InferringRouter
from pydantic import PositiveInt

from app.api.dependencies import get_session
from app.api.docs.api_endpoints import CRUDEndpointsDescriptions
from app.api.docs.api_params import CRUDParamsDescriptions
from app.constansts.constants_role import ConstantRole
from app.db.models import Session
from app.manager.manager_account_type import account_type
from app.schemas.schema_account_type import AccountTypeResponse, AccountTypeCreate, AccountTypeUpdate
from app.security.permissions import permission
from app.utils.exceptions.exception_route_handler import ExceptionRouteHandler

router = InferringRouter(route_class=ExceptionRouteHandler, tags=["Account Type"])
descriptions = CRUDEndpointsDescriptions(model_name="AccountType", search_parameters=["name"])
parameters = CRUDParamsDescriptions(obj_name="AccountType")


@router.get("/account_type", status_code=status.HTTP_200_OK, description=descriptions.fetch_all)
@permission({ConstantRole.admin})
def fetch_account_types(
    session: Session = Depends(get_session)
) -> List[AccountTypeResponse]:
    return account_type.fetch_all(session)


@router.get("/account_type/search", status_code=status.HTTP_200_OK, description=descriptions.search)
@permission({ConstantRole.admin})
def search_account_types(
    parameter: str = parameters.search_parameter,
    keyword: str = parameters.search_keyword,
    max_results: Optional[PositiveInt] = parameters.max_results_search,
    session: Session = Depends(get_session),
) -> List[AccountTypeResponse]:
    return account_type.search(parameter, keyword, max_results, session)


@router.post("/account_type", status_code=status.HTTP_201_CREATED, description=descriptions.create)
@permission({ConstantRole.admin})
def create_account_type(
    account_type_in: AccountTypeCreate,
    session: Session = Depends(get_session),
) -> AccountTypeResponse:
    return account_type.create(account_type_in, session)


@router.put("/account_type", status_code=status.HTTP_200_OK, description=descriptions.update)
@permission({ConstantRole.admin})
def update_account_type(
    account_type_in: AccountTypeUpdate,
    session: Session = Depends(get_session),
) -> AccountTypeResponse:
    return account_type.update(account_type_in, session)


@router.get("/account_type/{account_type_id}", status_code=status.HTTP_200_OK, description=descriptions.fetch_one)
@permission({ConstantRole.admin})
def fetch_account_type(
    account_type_id: PositiveInt = parameters.get_id,
    session: Session = Depends(get_session),
) -> AccountTypeResponse:
    return account_type.fetch_one(account_type_id, session)


@router.delete("/account_type/{account_type_id}", status_code=status.HTTP_204_NO_CONTENT, description=descriptions.delete)
@permission({ConstantRole.admin})
def delete_account_type(
    account_type_id: PositiveInt = parameters.delete_id,
    session: Session = Depends(get_session),
):
    return account_type.delete(account_type_id, session)