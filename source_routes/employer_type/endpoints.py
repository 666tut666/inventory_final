from typing import List, Optional

from fastapi import status, Depends
from fastapi_utils.inferring_router import InferringRouter
from pydantic import PositiveInt

from app.api.dependencies import get_session
from app.api.docs.api_endpoints import CRUDEndpointsDescriptions
from app.api.docs.api_params import CRUDParamsDescriptions
from app.constansts.constants_role import ConstantRole
from app.db.models import Session
from app.manager.manager_employer_type import employer_type
from app.schemas.schema_employer_type import EmployerTypeCreate, EmployerTypeResponse, EmployerTypeUpdate
from app.security.permissions import permission
from app.utils.exceptions.exception_route_handler import ExceptionRouteHandler

router = InferringRouter(route_class=ExceptionRouteHandler, tags=["Employer Type"])
descriptions = CRUDEndpointsDescriptions(model_name="Employer Type", search_parameters=["name"])
parameters = CRUDParamsDescriptions(obj_name="Employer Type")


@router.get("/employer_type", status_code=status.HTTP_200_OK, description=descriptions.fetch_all)
@permission({ConstantRole.admin})
def fetch_employer_types(session: Session = Depends(get_session)) -> List[EmployerTypeResponse]:
    return employer_type.fetch_all(session)


@router.get("/employer_type/search", status_code=status.HTTP_200_OK, description=descriptions.search)
@permission({ConstantRole.admin})
def search_employer_types(
    parameter: str = parameters.search_parameter,
    keyword: str = parameters.search_keyword,
    max_results: Optional[PositiveInt] = parameters.max_results_search,
    session: Session = Depends(get_session),
) -> List[EmployerTypeResponse]:
    return employer_type.search(parameter, keyword, max_results, session)


@router.post("/employer_type", status_code=status.HTTP_201_CREATED, description=descriptions.create)
@permission({ConstantRole.admin})
def create_employer_type(
    employer_type_in: EmployerTypeCreate,
    session: Session = Depends(get_session),
) -> EmployerTypeResponse:
    return employer_type.create(employer_type_in, session)


@router.put("/employer_type", status_code=status.HTTP_200_OK, description=descriptions.update)
@permission({ConstantRole.admin})
def update_employer_type(
    employer_type_in: EmployerTypeUpdate,
    session: Session = Depends(get_session),
) -> EmployerTypeResponse:
    return employer_type.update(employer_type_in, session)


@router.get("/employer_type/{employer_type_id}", status_code=status.HTTP_200_OK, description=descriptions.fetch_one)
@permission({ConstantRole.admin})
def fetch_employer_type(
    employer_type_id: PositiveInt = parameters.get_id,
    session: Session = Depends(get_session),
) -> EmployerTypeResponse:
    return employer_type.fetch_one(employer_type_id, session)


@router.delete("/employer_type/{employer_type_id}", status_code=status.HTTP_204_NO_CONTENT, description=descriptions.delete)
@permission({ConstantRole.admin})
def delete_employer_type(
    employer_type_id: PositiveInt = parameters.delete_id,
    session: Session = Depends(get_session),
):
    return employer_type.delete(employer_type_id, session)
