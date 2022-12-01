from typing import List, Optional

from fastapi import Depends, status
from fastapi_utils.inferring_router import InferringRouter
from pydantic import PositiveInt

from app.api.dependencies import get_session
from app.api.docs.api_endpoints import CRUDEndpointsDescriptions
from app.api.docs.api_params import CRUDParamsDescriptions
from app.constansts.constants_role import ConstantRole
from app.db.models import Session
from app.manager.manager_employer_payment_method import employer_payment_method
from app.schemas.schema_employer_payment_method import (
    EmployerPaymentMethodCreate, EmployerPaymentMethodResponse,
    EmployerPaymentMethodUpdate)
from app.security.permissions import permission
from app.utils.exceptions.exception_route_handler import ExceptionRouteHandler

router = InferringRouter(
    route_class=ExceptionRouteHandler, tags=["Employer Payment Method"]
)
descriptions = CRUDEndpointsDescriptions(
    model_name="Employer Payment Method", search_parameters=["iban"]
)
parameters = CRUDParamsDescriptions(obj_name="Employer Payment Method")


@router.get(
    "/employer_payment_method",
    status_code=status.HTTP_200_OK,
    description=descriptions.fetch_all,
)
@permission({ConstantRole.employer})
def fetch_employer_payment_methods(
    session: Session = Depends(get_session),
) -> List[EmployerPaymentMethodResponse]:
    return employer_payment_method.fetch_all(session)


@router.get(
    "/employer_payment_method/search",
    status_code=status.HTTP_200_OK,
    description=descriptions.search,
)
@permission({ConstantRole.employer})
def search_employer_payment_methods(
    parameter: str = parameters.search_parameter,
    keyword: str = parameters.search_keyword,
    max_results: Optional[PositiveInt] = parameters.max_results_search,
    session: Session = Depends(get_session),
) -> List[EmployerPaymentMethodResponse]:
    return employer_payment_method.search(parameter, keyword, max_results, session)


@router.post(
    "/employer_payment_method",
    status_code=status.HTTP_201_CREATED,
    description=descriptions.create,
)
@permission({ConstantRole.employer})
def create_employer_payment_method(
    employer_payment_method_in: EmployerPaymentMethodCreate,
    session: Session = Depends(get_session),
) -> EmployerPaymentMethodResponse:
    return employer_payment_method.create(employer_payment_method_in, session)


@router.put(
    "/employer_payment_method",
    status_code=status.HTTP_200_OK,
    description=descriptions.update,
)
@permission({ConstantRole.employer})
def update_employer_payment_method(
    employer_payment_method_in: EmployerPaymentMethodUpdate,
    session: Session = Depends(get_session),
) -> EmployerPaymentMethodResponse:
    return employer_payment_method.update(employer_payment_method_in, session)


@router.get(
    "/employer_payment_method/{employer_payment_method_id}",
    status_code=status.HTTP_200_OK,
    description=descriptions.fetch_one,
)
@permission({ConstantRole.employer})
def fetch_employer_payment_method(
    employer_payment_method_id: PositiveInt = parameters.get_id,
    session: Session = Depends(get_session),
) -> EmployerPaymentMethodResponse:
    return employer_payment_method.fetch_one(employer_payment_method_id, session)


@router.delete(
    "/employer_payment_method/{employer_payment_method_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description=descriptions.delete,
)
@permission({ConstantRole.employer})
def delete_employer_payment_method(
    employer_payment_method_id: PositiveInt = parameters.delete_id,
    session: Session = Depends(get_session),
):
    return employer_payment_method.delete(employer_payment_method_id, session)
