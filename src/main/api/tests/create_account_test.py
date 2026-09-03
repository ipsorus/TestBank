import allure
import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.create_user_request import CreateUserRequest


@allure.epic('Тесты по созданию счета')
@allure.suite('Тесты по созданию счета')
@pytest.mark.api
class TestCreateAccount:
    @allure.title('Создание счета пользователя')
    def test_create_account(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest):
        response = api_manager.user_steps.create_account(create_user_request)

        assert response.balance == 0, 'Баланс должен быть равен 0'

        account_from_db = Account.get_account_by_id(db_session, response.id)
        assert account_from_db.id == response.id, 'Счет не создан, ID аккаунта нет в БД'
        assert account_from_db.balance is not None, 'Поле Баланс для созданного аккаунта отсутствует в БД'

    @allure.title('Создание более 2х счетов пользователя')
    def test_create_more_2_accounts(self, api_manager: ApiManager, create_user_request: CreateUserRequest, create_two_accounts):
        acc_1, acc_2 = create_two_accounts
        assert acc_1, 'Счет не создан'
        assert acc_2, 'Счет не создан'

        r = api_manager.user_steps.create_account_conflict(create_user_request)
        assert r.status_code == 409, 'Код ответа не совпадает'
        assert r.json().get("error") == 'User already has maximum number of accounts(2)', 'Текст ошибки не совпадает'
