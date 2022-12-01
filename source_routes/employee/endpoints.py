from typing import Optional, List

from fastapi_utils.inferring_router import InferringRouter
from fastapi import status, Depends
from pydantic.types import PositiveInt

from app.api.dependencies import get_session
from app.api.docs.api_endpoints import CRUDEndpointsDescriptions
from app.api.docs.api_params import CRUDParamsDescriptions
from app.constansts.constants_role import ConstantRole
from app.db.models import Session
from app.manager.manager_employee import employee
from app.security.permissions import permission
from app.utils.exceptions.exception_route_handler import ExceptionRouteHandler
from app.schemas.schema_employee import EmployeeCreate, EmployeeResponse, EmployeeUpdate

router = InferringRouter(route_class=ExceptionRouteHandler, tags=["Employee"])
descriptions = CRUDEndpointsDescriptions(
    model_name="Employee",
    search_parameters=["email", "phone", "fullname", "passport", "tax_id", "birth_date"]
)
params = CRUDParamsDescriptions(obj_name="Employee")


@router.get("/employee", status_code=status.HTTP_200_OK, description=descriptions.fetch_all)
@permission({ConstantRole.admin, ConstantRole.employer})
def fetch_employees(session: Session = Depends(get_session)) -> List[EmployeeResponse]:
    return employee.fetch_all(session)


@router.get("/employee/search", status_code=status.HTTP_200_OK, description=descriptions.search)
@permission({ConstantRole.admin, ConstantRole.employer})
def search_employees(
    parameter: str = params.search_parameter,
    keyword: str = params.search_keyword,
    max_results: Optional[PositiveInt] = params.max_results_search,
    session: Session = Depends(get_session),
) -> List[EmployeeResponse]:
    return employee.search(parameter, keyword, max_results, session)


@router.post("/employee", status_code=status.HTTP_201_CREATED, description=descriptions.create)
@permission({ConstantRole.admin, ConstantRole.employer})
def create_employee(
    employee_in: EmployeeCreate,
    session: Session = Depends(get_session),
) -> EmployeeResponse:
    return employee.create(employee_in, session)


@router.put("/employee", status_code=status.HTTP_200_OK, description=descriptions.update)
@permission({ConstantRole.admin, ConstantRole.employer})
def update_employee(
    employee_in: EmployeeUpdate,
    session: Session = Depends(get_session),
) -> EmployeeResponse:
    return employee.update(employee_in, session)


@router.get("/employee/{employee_id}", status_code=status.HTTP_200_OK, description=descriptions.fetch_one)
@permission({ConstantRole.admin, ConstantRole.employer})
def fetch_employee(
    employee_id: PositiveInt = params.get_id,
    session: Session = Depends(get_session),
) -> EmployeeResponse:
    return employee.fetch_one(employee_id, session)


@router.delete("/employee/{employee_id}", status_code=status.HTTP_204_NO_CONTENT, description=descriptions.delete)
@permission({ConstantRole.admin, ConstantRole.employer})
def delete_employee(
    employee_id: PositiveInt = params.delete_id,
    session: Session = Depends(get_session),
):
    return employee.delete(employee_id, session)
