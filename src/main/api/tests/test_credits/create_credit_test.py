import allure
import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.models.create_credit_request import CreateCreditRequest
from src.main.api.models.create_user_request import CreateCreditUserRequest


@pytest.mark.api
@allure.epic('Тесты по выдаче кредита')
@allure.suite('Тесты по выдаче кредита')
class TestCreateCredit:

    @allure.title('Выдача кредита на счет пользователя')
    @pytest.mark.parametrize('amount, term_month', [(5000, 12)])
    def test_create_credit(self, db_session: Session, api_manager: ApiManager,
                           create_credit_user_request: CreateCreditUserRequest, amount: int | float, term_month: int):
        response = api_manager.user_steps.create_account(create_credit_user_request)

        assert response.balance == 0

        credit_data = CreateCreditRequest(
            accountId= response.id,
            amount= amount,
            termMonths= term_month
        )

        resp = api_manager.user_steps.request_credit(create_credit_user_request, credit_data)

        result = resp.model_dump()

        assert credit_data.amount == result['amount']
        assert credit_data.amount == result['balance']
        assert credit_data.accountId == result['id']
        assert credit_data.termMonths == result['termMonths']

        credit_from_db = Credit.get_credit_by_id(db_session, result['creditId'])

        assert credit_from_db.amount == credit_data.amount, 'Значение пополнения не изменилось в БД'
        assert credit_from_db.account_id == credit_data.accountId, 'ID аккаунта в БД не совпадает'
        assert credit_from_db.term_months == credit_data.termMonths, 'Срок кредита в БД не совпадает'


    @allure.title('Выдача кредита на счет пользователя, без роли ROLE_CREDIT_SECRET')
    @pytest.mark.parametrize('amount, term_month', [(5000, 12)])
    def test_create_credit_no_role_invalid(self, api_manager: ApiManager, create_user_request: CreateCreditUserRequest, amount: int | float, term_month: int):
        response = api_manager.user_steps.create_account(create_user_request)

        assert response.balance == 0

        credit_data = CreateCreditRequest(
            accountId= response.id,
            amount= amount,
            termMonths= term_month
        )

        api_manager.user_steps.request_credit_forbidden(create_user_request, credit_data)


    @allure.title('Выдача более 1 кредита на один и тот же счет для одного пользователя')
    @pytest.mark.parametrize('amount, term_month', [(5000, 12)])
    def test_create_more_1_credits(self, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest, amount: int | float, term_month: int):
        count = 0
        for i in range(3):
            try:
                count += 1
                response = api_manager.user_steps.create_account(create_credit_user_request)

                assert response.balance == 0

                credit_data = CreateCreditRequest(
                    accountId=response.id,
                    amount=amount,
                    termMonths=term_month
                )

                resp = api_manager.user_steps.request_credit(create_credit_user_request, credit_data)

                result = resp.model_dump()
                assert credit_data.amount == result['amount']
                assert credit_data.amount == result['balance']
                assert credit_data.accountId == result['id']
                assert credit_data.termMonths == result['termMonths']

            except AssertionError as e:
                if count > 1:
                    assert 'error' in e.args[0]
                else:
                    raise AssertionError(e)


    @allure.title('Выдача более 1 кредита на второй счет для одного пользователя')
    @pytest.mark.parametrize('amount, term_month', [(5000, 12)])
    def test_create_more_1_credits_for_second_account(self, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest, amount: int | float, term_month: int):

        account_1 = api_manager.user_steps.create_account(create_credit_user_request)

        assert account_1.balance == 0

        credit_data = CreateCreditRequest(
            accountId=account_1.id,
            amount=amount,
            termMonths=term_month
        )

        api_manager.user_steps.request_credit(create_credit_user_request, credit_data)

        account_2 = api_manager.user_steps.create_account(create_credit_user_request)

        assert account_2.balance == 0

        credit_data = CreateCreditRequest(
            accountId=account_2.id,
            amount=amount,
            termMonths=term_month
        )

        api_manager.user_steps.request_credit_not_found(create_credit_user_request, credit_data)


    @allure.title('Выдача кредита для пользователя. Невалидные данные для суммы кредита')
    @pytest.mark.parametrize('term_month', [12])
    @pytest.mark.parametrize('amount', [4999.9, 15000.1, -5000, -15000, 0])
    def test_create_credit_invalid(self, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest, amount: float | int, term_month: int):
        response = api_manager.user_steps.create_account(create_credit_user_request)

        assert response.balance == 0

        credit_data = CreateCreditRequest(
            accountId= response.id,
            amount= amount,
            termMonths= term_month
        )

        api_manager.user_steps.request_invalid_credit(create_credit_user_request, credit_data)


    @allure.title('Выдача кредита для пользователя. Невалидные данные для срока кредита')
    @pytest.mark.parametrize('amount', [5000])
    @pytest.mark.parametrize('term_month', [0, 61])
    def test_create_credit_invalid_term_month(self, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest, amount: int| float, term_month: int):
        account = api_manager.user_steps.create_account(create_credit_user_request)

        assert account.balance == 0

        credit_data = CreateCreditRequest(
            accountId=account.id,
            amount=amount,
            termMonths=term_month
        )

        api_manager.user_steps.request_invalid_credit(create_credit_user_request, credit_data)