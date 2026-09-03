import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_credit_request import CreateCreditRequest
from src.main.api.models.create_user_request import CreateCreditUserRequest


@pytest.fixture
def create_account_credit_request(api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest, create_account_request_role_credit):
    """
    Фабрика: каждый вызов создаёт аккаунт и запрашивает кредит для аккаунта.
    """
    account_response = create_account_request_role_credit
    def _make_credit_request(amount, term_months):
        credit_data = CreateCreditRequest(
            accountId=account_response.id,
            amount=amount,
            termMonths=term_months
        )
        credit_response = api_manager.user_steps.request_credit(create_credit_user_request, credit_data)
        return credit_response

    return _make_credit_request
