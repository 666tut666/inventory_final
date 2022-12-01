from typing import List, Optional

from fastapi import Depends, status
from fastapi_utils.inferring_router import InferringRouter
from pydantic import PositiveInt

from app.api.dependencies import get_session
from app.api.docs.api_endpoints import CRUDEndpointsDescriptions
from app.api.docs.api_params import CRUDParamsDescriptions
from app.constansts.constants_role import ConstantRole
from app.db.models import Session
from app.manager.manager_payment_history import payment_history
from app.schemas.schema_payment_history import PaymentHistoryResponse
from app.security.permissions import permission
from app.utils.exceptions.exception_route_handler import ExceptionRouteHandler

router = InferringRouter(route_class=ExceptionRouteHandler, tags=["Payment History"])
descriptions = CRUDEndpointsDescriptions(
    model_name="PaymentHistory", search_parameters=["amount", "creation_date"]
)
parameters = CRUDParamsDescriptions(obj_name="PaymentHistory")


@router.get(
    "/payment_history",
    status_code=status.HTTP_200_OK,
    description=descriptions.fetch_all,
)
@permission({ConstantRole.admin, ConstantRole.employer, ConstantRole.employee})
def fetch_payment_histories(
    session: Session = Depends(get_session),
) -> List[PaymentHistoryResponse]:
    return payment_history.fetch_all(session)


@router.get(
    "/payment_history/search",
    status_code=status.HTTP_200_OK,
    description=descriptions.search,
)
@permission({ConstantRole.admin, ConstantRole.employer, ConstantRole.employee})
def search_payment_histories(
    parameter: str = parameters.search_parameter,
    keyword: str = parameters.search_keyword,
    max_results: Optional[PositiveInt] = parameters.max_results_search,
    session: Session = Depends(get_session),
) -> List[PaymentHistoryResponse]:
    return payment_history.search(parameter, keyword, max_results, session)


@router.get(
    "/payment_history/{payment_history_id}",
    status_code=status.HTTP_200_OK,
    description=descriptions.fetch_one,
)
@permission({ConstantRole.admin, ConstantRole.employer, ConstantRole.employee})
def fetch_payment_history(
    payment_history_id: PositiveInt = parameters.get_id,
    session: Session = Depends(get_session),
) -> PaymentHistoryResponse:
    return payment_history.fetch_one(payment_history_id, session)
