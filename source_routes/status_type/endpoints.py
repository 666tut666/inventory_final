from typing import List, Optional

from fastapi import status, Depends
from fastapi_utils.inferring_router import InferringRouter
from pydantic import PositiveInt

from app.api.dependencies import get_session
from app.api.docs.api_endpoints import CRUDEndpointsDescriptions
from app.api.docs.api_params import CRUDParamsDescriptions
from app.constansts.constants_role import ConstantRole
from app.db.models import Session
from app.manager.manager_status_type import status_type
from app.schemas.schema_status_type import StatusTypeCreate, StatusTypeResponse, StatusTypeUpdate
from app.security.permissions import permission
from app.utils.exceptions.exception_route_handler import ExceptionRouteHandler

router = InferringRouter(route_class=ExceptionRouteHandler, tags=["Status Type"])
descriptions = CRUDEndpointsDescriptions(model_name="Status Type", search_parameters=["name"])
parameters = CRUDParamsDescriptions(obj_name="Status Type")


@router.get("/status_type", status_code=status.HTTP_200_OK, description=descriptions.fetch_all)
@permission({ConstantRole.admin})
def fetch_status_types(session: Session = Depends(get_session)) -> List[StatusTypeResponse]:
    return status_type.fetch_all(session)


@router.get("/status_type/search", status_code=status.HTTP_200_OK, description=descriptions.search)
@permission({ConstantRole.admin})
def search_status_types(
    parameter: str = parameters.search_parameter,
    keyword: str = parameters.search_keyword,
    max_results: Optional[PositiveInt] = parameters.max_results_search,
    session: Session = Depends(get_session),
) -> List[StatusTypeResponse]:
    return status_type.search(parameter, keyword, max_results, session)


@router.post("/status_type", status_code=status.HTTP_201_CREATED, description=descriptions.create)
@permission({ConstantRole.admin})
def create_status_type(
    status_type_in: StatusTypeCreate,
    session: Session = Depends(get_session),
) -> StatusTypeResponse:
    return status_type.create(status_type_in, session)


@router.put("/status_type", status_code=status.HTTP_200_OK, description=descriptions.update)
@permission({ConstantRole.admin})
def update_status_type(
    status_type_in: StatusTypeUpdate,
    session: Session = Depends(get_session),
) -> StatusTypeResponse:
    return status_type.update(status_type_in, session)


@router.get("/status_type/{status_type_id}", status_code=status.HTTP_200_OK, description=descriptions.fetch_one)
@permission({ConstantRole.admin})
def fetch_status_type(
    status_type_id: PositiveInt = parameters.get_id,
    session: Session = Depends(get_session),
) -> StatusTypeResponse:
    return status_type.fetch_one(status_type_id, session)


@router.delete("/status_type/{status_type_id}", status_code=status.HTTP_204_NO_CONTENT, description=descriptions.delete)
@permission({ConstantRole.admin})
def delete_status_type(
    status_type_id: PositiveInt = parameters.delete_id,
    session: Session = Depends(get_session),
):
    return status_type.delete(status_type_id, session)
