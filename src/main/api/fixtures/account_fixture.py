import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateCreditUserRequest, CreateUserRequest


@pytest.fixture
def create_account_request_role_credit(api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest):
    account_response = api_manager.user_steps.create_account(create_credit_user_request)
    return account_response

@pytest.fixture
def create_account_request_role_user(api_manager: ApiManager, create_user_request: CreateUserRequest):
    account_response = api_manager.user_steps.create_account(create_user_request)
    return account_response

@pytest.fixture
def create_two_accounts(api_manager: ApiManager, create_user_request: CreateUserRequest):
    account_1_response = api_manager.user_steps.create_account(create_user_request)
    account_2_response = api_manager.user_steps.create_account(create_user_request)
    return account_1_response, account_2_response

@pytest.fixture
def create_account_for_one_user(api_manager: ApiManager):
    """Фабрика: каждый вызов создаёт пользователя и аккаунт.
    Можно передать user_data извне, либо сгенерировать автоматически.
    """
    def _make_account(user_data: CreateUserRequest | None = None):
        account_response = api_manager.user_steps.create_account(user_data)
        return account_response

    return _make_account

@pytest.fixture
def create_account_different_users(api_manager: ApiManager):
    """Фабрика: каждый вызов создаёт пользователя и аккаунт.
    Можно передать user_data извне, либо сгенерировать автоматически.
    """
    def _make_account(user_data: CreateUserRequest | None = None):
        if user_data is None:
            user_data = RandomModelGenerator.generate(CreateUserRequest)

        user_response = api_manager.admin_steps.create_user(user_data)
        account_response = api_manager.user_steps.create_account(user_data)
        return user_data, user_response, account_response

    return _make_account