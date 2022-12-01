from typing import List, Optional

from fastapi import Depends, status
from fastapi_utils.inferring_router import InferringRouter
from pydantic import PositiveInt

from app.api.dependencies import get_session
from app.api.docs.api_endpoints import CRUDEndpointsDescriptions
from app.api.docs.api_params import CRUDParamsDescriptions
from app.constansts.constants_role import ConstantRole
from app.db.models import Session
from app.manager.manager_payment_status_type import payment_status_type
from app.schemas.schema_payment_status_type import (PaymentStatusTypeCreate,
                                                    PaymentStatusTypeResponse,
                                                    PaymentStatusTypeUpdate)
from app.security.permissions import permission
from app.utils.exceptions.exception_route_handler import ExceptionRouteHandler

router = InferringRouter(
    route_class=ExceptionRouteHandler, tags=["Payment Status Type"]
)
descriptions = CRUDEndpointsDescriptions(
    model_name="Payment Status Type", search_parameters=["name"]
)
parameters = CRUDParamsDescriptions(obj_name="Payment Status Type")


@router.get(
    "/payment_status_type",
    status_code=status.HTTP_200_OK,
    description=descriptions.fetch_all,
)
@permission({ConstantRole.admin})
def fetch_payment_status_types(
    session: Session = Depends(get_session),
) -> List[PaymentStatusTypeResponse]:
    return payment_status_type.fetch_all(session)


@router.get(
    "/payment_status_type/search",
    status_code=status.HTTP_200_OK,
    description=descriptions.search,
)
@permission({ConstantRole.admin})
def search_payment_status_types(
    parameter: str = parameters.search_parameter,
    keyword: str = parameters.search_keyword,
    max_results: Optional[PositiveInt] = parameters.max_results_search,
    session: Session = Depends(get_session),
) -> List[PaymentStatusTypeResponse]:
    return payment_status_type.search(parameter, keyword, max_results, session)


@router.post(
    "/payment_status_type",
    status_code=status.HTTP_201_CREATED,
    description=descriptions.create,
)
@permission({ConstantRole.admin})
def create_payment_status_type(
    payment_status_type_in: PaymentStatusTypeCreate,
    session: Session = Depends(get_session),
) -> PaymentStatusTypeResponse:
    return payment_status_type.create(payment_status_type_in, session)


@router.put(
    "/payment_status_type",
    status_code=status.HTTP_200_OK,
    description=descriptions.update,
)
@permission({ConstantRole.admin})
def update_payment_status_type(
    payment_status_type_in: PaymentStatusTypeUpdate,
    session: Session = Depends(get_session),
) -> PaymentStatusTypeResponse:
    return payment_status_type.update(payment_status_type_in, session)


@router.get(
    "/payment_status_type/{payment_status_type_id}",
    status_code=status.HTTP_200_OK,
    description=descriptions.fetch_one,
)
@permission({ConstantRole.admin})
def fetch_payment_status_type(
    payment_status_type_id: PositiveInt = parameters.get_id,
    session: Session = Depends(get_session),
) -> PaymentStatusTypeResponse:
    return payment_status_type.fetch_one(payment_status_type_id, session)


@router.delete(
    "/payment_status_type/{payment_status_type_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description=descriptions.delete,
)
@permission({ConstantRole.admin})
def delete_payment_status_type(
    payment_status_type_id: PositiveInt = parameters.delete_id,
    session: Session = Depends(get_session),
):
    return payment_status_type.delete(payment_status_type_id, session)
