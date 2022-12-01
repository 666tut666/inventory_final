from typing import List, Optional

from fastapi import status, Depends
from fastapi_utils.inferring_router import InferringRouter
from pydantic import PositiveInt

from app.api.dependencies import get_session
from app.api.docs.api_endpoints import CRUDEndpointsDescriptions
from app.api.docs.api_params import CRUDParamsDescriptions
from app.constansts.constants_role import ConstantRole
from app.db.models import Session
from app.manager.manager_role import role
from app.schemas.schema_role import RoleCreate, RoleResponse, RoleUpdate
from app.security.permissions import permission
from app.utils.exceptions.exception_route_handler import ExceptionRouteHandler

router = InferringRouter(route_class=ExceptionRouteHandler, tags=["Role"])
descriptions = CRUDEndpointsDescriptions(model_name="Role", search_parameters=["name"])
parameters = CRUDParamsDescriptions(obj_name="Role")


@router.get("/role", status_code=status.HTTP_200_OK, description=descriptions.fetch_all)
@permission({ConstantRole.admin})
def fetch_roles(session: Session = Depends(get_session)) -> List[RoleResponse]:
    return role.fetch_all(session)


@router.get("/role/search", status_code=status.HTTP_200_OK, description=descriptions.search)
@permission({ConstantRole.admin})
def search_roles(
    parameter: str = parameters.search_parameter,
    keyword: str = parameters.search_keyword,
    max_results: Optional[PositiveInt] = parameters.max_results_search,
    session: Session = Depends(get_session),
) -> List[RoleResponse]:
    return role.search(parameter, keyword, max_results, session)


@router.post("/role", status_code=status.HTTP_201_CREATED, description=descriptions.create)
@permission({ConstantRole.admin})
def create_role(
    role_in: RoleCreate,
    session: Session = Depends(get_session),
) -> RoleResponse:
    return role.create(role_in, session)


@router.put("/role", status_code=status.HTTP_200_OK, description=descriptions.update)
@permission({ConstantRole.admin})
def update_role(
    role_in: RoleUpdate,
    session: Session = Depends(get_session),
) -> RoleResponse:
    return role.update(role_in, session)


@router.get("/role/{role_id}", status_code=status.HTTP_200_OK, description=descriptions.fetch_one)
@permission({ConstantRole.admin})
def fetch_role(
    role_id: PositiveInt = parameters.get_id,
    session: Session = Depends(get_session),
) -> RoleResponse:
    return role.fetch_one(role_id, session)


@router.delete("/role/{role_id}", status_code=status.HTTP_204_NO_CONTENT, description=descriptions.delete)
@permission({ConstantRole.admin})
def delete_role(
    role_id: PositiveInt = parameters.delete_id,
    session: Session = Depends(get_session),
):
    return role.delete(role_id, session)
