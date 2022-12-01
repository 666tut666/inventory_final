from typing import List, Optional

from fastapi import status, Depends
from fastapi_utils.inferring_router import InferringRouter
from pydantic import PositiveInt

from app.api.dependencies import get_session
from app.api.docs.api_endpoints import CRUDEndpointsDescriptions
from app.api.docs.api_params import CRUDParamsDescriptions
from app.constansts.constants_role import ConstantRole
from app.db.models import Session
from app.manager.manager_employer import employer
from app.schemas.schema_employer import EmployerCreate, EmployerResponse, EmployerUpdate
from app.security.permissions import permission
from app.utils.exceptions.exception_route_handler import ExceptionRouteHandler

router = InferringRouter(route_class=ExceptionRouteHandler, tags=["Employer"])
descriptions = CRUDEndpointsDescriptions(
    model_name="Employer",
    search_parameters=["email", "phone", "name", "address", "edrpou"]
)
parameters = CRUDParamsDescriptions(obj_name="Employer")


@router.get("/employer", status_code=status.HTTP_200_OK, description=descriptions.fetch_all)
@permission({ConstantRole.admin})
def fetch_employers(session: Session = Depends(get_session)) -> List[EmployerResponse]:
    return employer.fetch_all(session)


@router.get("/employer/search", status_code=status.HTTP_200_OK, description=descriptions.search)
@permission({ConstantRole.admin})
def search_employers(
    parameter: str = parameters.search_parameter,
    keyword: str = parameters.search_keyword,
    max_results: Optional[PositiveInt] = parameters.max_results_search,
    session: Session = Depends(get_session),
) -> List[EmployerResponse]:
    return employer.search(parameter, keyword, max_results, session)


@router.post("/employer", status_code=status.HTTP_201_CREATED, description=descriptions.create)
@permission({ConstantRole.admin})
def create_employer(
    employer_in: EmployerCreate,
    session: Session = Depends(get_session),
) -> EmployerResponse:
    return employer.create(employer_in, session)


@router.put("/employer", status_code=status.HTTP_200_OK, description=descriptions.update)
@permission({ConstantRole.admin})
def update_employer(
    employer_in: EmployerUpdate,
    session: Session = Depends(get_session),
) -> EmployerResponse:
    return employer.update(employer_in, session)


@router.get("/employer/{employer_id}", status_code=status.HTTP_200_OK, description=descriptions.fetch_one)
@permission({ConstantRole.admin})
def fetch_employer(
    employer_id: PositiveInt = parameters.get_id,
    session: Session = Depends(get_session),
) -> EmployerResponse:
    return employer.fetch_one(employer_id, session)


@router.delete("/employer/{employer_id}", status_code=status.HTTP_204_NO_CONTENT)
@permission({ConstantRole.admin})
def delete_employer(
    employer_id: PositiveInt = parameters.delete_id,
    session: Session = Depends(get_session),
):
    return employer.delete(employer_id, session)
