from typing import List, Optional

from fastapi import Depends, status
from fastapi_utils.inferring_router import InferringRouter
from pydantic import PositiveInt

from app.api.dependencies import get_session
from app.api.docs.api_endpoints import CRUDEndpointsDescriptions
from app.api.docs.api_params import CRUDParamsDescriptions
from app.constansts.constants_role import ConstantRole
from app.db.models import Session
from app.manager.manager_bank import bank
from app.schemas.schema_bank import BankCreate, BankResponse, BankUpdate
from app.security.permissions import permission
from app.utils.exceptions.exception_route_handler import ExceptionRouteHandler

router = InferringRouter(route_class=ExceptionRouteHandler, tags=["Bank"])
descriptions = CRUDEndpointsDescriptions(
    model_name="Bank", search_parameters=["name", "mfo"]
)
parameters = CRUDParamsDescriptions(obj_name="Bank")


@router.get("/bank", status_code=status.HTTP_200_OK, description=descriptions.fetch_all)
@permission({ConstantRole.employer})
def fetch_banks(session: Session = Depends(get_session)) -> List[BankResponse]:
    return bank.fetch_all(session)


@router.get("/bank/search", status_code=status.HTTP_200_OK)
@permission({ConstantRole.employer})
def search_banks(
    parameter: str = parameters.search_parameter,
    keyword: str = parameters.search_keyword,
    max_results: Optional[PositiveInt] = parameters.max_results_search,
    session: Session = Depends(get_session),
) -> List[BankResponse]:
    return bank.search(parameter, keyword, max_results, session)


@router.post("/bank", status_code=status.HTTP_201_CREATED, description=descriptions.create)
@permission({ConstantRole.employer})
def create_bank(
    bank_in: BankCreate,
    session: Session = Depends(get_session)
) -> BankResponse:
    return bank.create(bank_in, session)


@router.put("/bank", status_code=status.HTTP_200_OK, description=descriptions.update)
@permission({ConstantRole.employer})
def update_bank(
    bank_in: BankUpdate,
    session: Session = Depends(get_session)
) -> BankResponse:
    return bank.update(bank_in, session)


@router.get(
    "/bank/{bank_id}",
    status_code=status.HTTP_200_OK,
    description=descriptions.fetch_one,
)
@permission({ConstantRole.employer})
def fetch_bank(
    bank_id: PositiveInt = parameters.get_id,
    session: Session = Depends(get_session),
) -> BankResponse:
    return bank.fetch_one(bank_id, session)


@router.delete("/bank/{bank_id}", status_code=status.HTTP_204_NO_CONTENT, description=descriptions.delete)
@permission({ConstantRole.employer})
def delete_bank(
    bank_id: PositiveInt = parameters.delete_id,
    session: Session = Depends(get_session),
):
    return bank.delete(bank_id, session)
