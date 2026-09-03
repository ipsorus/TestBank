import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest


@pytest.fixture
def create_deposit(api_manager: ApiManager):
    """
    Фабрика: каждый вызов делает пополнение аккаунта.
    """
    def _make_deposit(user: CreateUserRequest, account_id: int, amount: float):
        payload = DepositRequest(
            accountId=account_id,
            amount=amount)
        create_deposit_response = api_manager.user_steps.create_deposit(user, payload)
        return create_deposit_response

    return _make_deposit