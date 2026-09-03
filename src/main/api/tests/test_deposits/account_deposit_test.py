import allure
import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account


@pytest.mark.api
@allure.epic('Тесты по пополнению баланса счета')
@allure.suite('Тесты по пополнению баланса счета')
class TestDepositAccount:
    @allure.title('Пополнение баланса счета')
    @pytest.mark.parametrize('amount', [1000.5])
    def test_deposit_valid(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest, amount: int | float):
        response = api_manager.user_steps.create_account(create_user_request)

        assert response.balance == 0

        payload = DepositRequest(accountId=response.id, amount=amount)

        resp = api_manager.user_steps.create_deposit(create_user_request, payload)
        data = resp.model_dump()

        assert data["id"] == payload.accountId
        assert data["balance"] == payload.amount

        transaction_response = api_manager.user_steps.get_account_transaction(create_user_request, response.id)
        assert transaction_response.transactions[0].amount == payload.amount

        account_from_db = Account.get_account_by_id(db_session, response.id)
        assert account_from_db.balance == payload.amount, 'значение баланса не изменилось в БД'


    @allure.title('Пополнение баланса счета. Невалидные данные по сумме пополнения')
    @pytest.mark.parametrize('amount', [0, 999.9, 9001, 100000, -1001, -1000, -9000,])
    def test_deposit_invalid(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest, amount: int | float):
        response = api_manager.user_steps.create_account(create_user_request)

        assert response.balance == 0

        payload = DepositRequest(accountId=response.id, amount=amount)

        api_manager.user_steps.create_deposit_bad(create_user_request, payload)

        transaction_response = api_manager.user_steps.get_account_transaction(create_user_request, response.id)

        assert transaction_response.balance == 0

        account_from_db = Account.get_account_by_id(db_session, response.id)
        assert account_from_db.balance == 0, 'Значение баланса пополнилось в БД, ошибка'


    @allure.title('Пополнение баланса счета через цикл. Невалидные данные по сумме пополнения.')
    def test_deposit_invalid_2(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest):
        invalid_amount = [0, 999.9, 9001, 100000, -1001, -1000, -9000]
        response = api_manager.user_steps.create_account(create_user_request)

        assert response.balance == 0
        for amount in invalid_amount:
            payload = DepositRequest(accountId=response.id, amount=amount)

            api_manager.user_steps.create_deposit_bad(create_user_request, payload)

            transaction_response = api_manager.user_steps.get_account_transaction(create_user_request, response.id)
            assert transaction_response.balance == 0

            account_from_db = Account.get_account_by_id(db_session, response.id)
            assert account_from_db.balance == 0, 'Значение баланса пополнилось в БД, ошибка'