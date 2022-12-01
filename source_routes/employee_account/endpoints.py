from typing import List, Optional

from fastapi import Depends, status
from fastapi_utils.inferring_router import InferringRouter
from pydantic import PositiveInt

from app.api.dependencies import get_session
from app.api.docs.api_endpoints import CRUDEndpointsDescriptions
from app.api.docs.api_params import CRUDParamsDescriptions
from app.constansts.constants_role import ConstantRole
from app.db.models import Session
from app.manager.manager_employee_account import employee_account
from app.schemas.schema_employee_account import (EmployeeAccountCreate,
                                                 EmployeeAccountResponse,
                                                 EmployeeAccountUpdate)
from app.security.permissions import permission
from app.utils.exceptions.exception_route_handler import ExceptionRouteHandler

router = InferringRouter(route_class=ExceptionRouteHandler, tags=["Employee Account"])
descriptions = CRUDEndpointsDescriptions(
    model_name="Employee Account", search_parameters=["name", "number", "issuer"]
)
parameters = CRUDParamsDescriptions(obj_name="Employee Account")


@router.get(
    "/employee_account",
    status_code=status.HTTP_200_OK,
    description=descriptions.fetch_all,
)
@permission({ConstantRole.employee})
def fetch_employee_accounts(
    session: Session = Depends(get_session),
) -> List[EmployeeAccountResponse]:
    return employee_account.fetch_all(session)


@router.get(
    "/employee_account/search",
    status_code=status.HTTP_200_OK,
    description=descriptions.search,
)
@permission({ConstantRole.employee})
def search_employee_accounts(
    parameter: str = parameters.search_parameter,
    keyword: str = parameters.search_keyword,
    max_results: Optional[PositiveInt] = parameters.max_results_search,
    session: Session = Depends(get_session),
) -> List[EmployeeAccountResponse]:
    return employee_account.search(parameter, keyword, max_results, session)


@router.post(
    "/employee_account",
    status_code=status.HTTP_201_CREATED,
    description=descriptions.create,
)
@permission({ConstantRole.employee})
def create_employee_account(
    employee_account_in: EmployeeAccountCreate,
    session: Session = Depends(get_session),
) -> EmployeeAccountResponse:
    return employee_account.create(employee_account_in, session)


@router.put(
    "/employee_account", status_code=status.HTTP_200_OK, description=descriptions.update
)
@permission({ConstantRole.employee})
def update_employee_account(
    employee_account_in: EmployeeAccountUpdate,
    session: Session = Depends(get_session),
) -> EmployeeAccountResponse:
    return employee_account.update(employee_account_in, session)


@router.get(
    "/employee_account/{employee_account_id}",
    status_code=status.HTTP_200_OK,
    description=descriptions.fetch_one,
)
@permission({ConstantRole.employee})
def fetch_employee_account(
    employee_account_id: PositiveInt = parameters.get_id,
    session: Session = Depends(get_session),
) -> EmployeeAccountResponse:
    return employee_account.fetch_one(employee_account_id, session)


@router.delete(
    "/employee_account/{employee_account_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description=descriptions.delete,
)
@permission({ConstantRole.employee})
def delete_employee_account(
    employee_account_id: PositiveInt = parameters.delete_id,
    session: Session = Depends(get_session),
):
    return employee_account.delete(employee_account_id, session)
