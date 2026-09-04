import allure
import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.models.create_credit_request import CreateCreditRequest
from src.main.api.models.create_user_request import CreateCreditUserRequest, CreateUserRequest


@pytest.mark.api
@allure.epic('Тесты по выдаче кредита')
@allure.suite('Тесты по выдаче кредита')
class TestCreateCredit:

    @allure.title('Выдача кредита на счет пользователя')
    @pytest.mark.parametrize('amount, term_month', [(5000, 12)])
    def test_create_credit(self, db_session: Session, api_manager: ApiManager,
                           create_credit_user_request: CreateCreditUserRequest, create_account_request_role_credit,
                           amount: int | float, term_month: int):

        response = create_account_request_role_credit

        assert response.balance == 0, 'Баланс должен быть равен 0'

        credit_data = CreateCreditRequest(
            accountId= response.id,
            amount= amount,
            termMonths= term_month
        )

        resp = api_manager.user_steps.request_credit(create_credit_user_request, credit_data)

        result = resp.model_dump()

        assert credit_data.amount == result['amount'], 'Сумма кредита должна быть равна запрошенной сумме'
        assert credit_data.amount == result['balance'], 'Баланс кредита должен быть равен запрошенной сумме'
        assert credit_data.accountId == result['id'], 'ID счета не соответствует ожидаемому'
        assert credit_data.termMonths == result['termMonths'], 'Срок кредита не соответствует ожидаемому'

        credit_from_db = Credit.get_credit_by_id(db_session, result['creditId'])

        assert credit_from_db.amount == credit_data.amount, 'Значение пополнения не изменилось в БД'
        assert credit_from_db.account_id == credit_data.accountId, 'ID аккаунта в БД не совпадает'
        assert credit_from_db.term_months == credit_data.termMonths, 'Срок кредита в БД не совпадает'


    @allure.title('Выдача кредита на счет пользователя, без роли ROLE_CREDIT_SECRET')
    @pytest.mark.parametrize('amount, term_month', [(5000, 12)])
    def test_create_credit_no_role_invalid(self, api_manager: ApiManager, create_user_request: CreateUserRequest,
                                           create_account_request_role_user, amount: int | float, term_month: int):
        response = create_account_request_role_user

        assert response.balance == 0, 'Баланс должен быть равен 0'

        credit_data = CreateCreditRequest(
            accountId= response.id,
            amount= amount,
            termMonths= term_month
        )

        api_manager.user_steps.request_credit_forbidden(create_user_request, credit_data)


    @allure.title('Выдача более 1 кредита на один и тот же счет для одного пользователя')
    @pytest.mark.parametrize('amount, term_month', [(5000, 12)])
    def test_create_more_1_credits(self, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest,
                                   create_account_request_role_credit, amount: int | float, term_month: int):

            response = create_account_request_role_credit

            assert response.balance == 0, 'Баланс должен быть равен 0'

            credit_data = CreateCreditRequest(
                accountId=response.id,
                amount=amount,
                termMonths=term_month
            )

            resp = api_manager.user_steps.request_credit(create_credit_user_request, credit_data)

            result = resp.model_dump()
            assert credit_data.amount == result['amount'], 'Сумма кредита должна быть равна запрошенной сумме'
            assert credit_data.amount == result['balance'], 'Баланс кредита должен быть равен запрошенной сумме'
            assert credit_data.accountId == result['id'], 'ID счета не соответствует ожидаемому'
            assert credit_data.termMonths == result['termMonths'], 'Срок кредита не соответствует ожидаемому'

            api_manager.user_steps.request_credit_not_found(create_credit_user_request, credit_data)


    @allure.title('Выдача более 1 кредита на второй счет для одного пользователя')
    @pytest.mark.parametrize('amount, term_month', [(5000, 12)])
    def test_create_more_1_credits_for_second_account(self, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest,
                                                      create_account_credit_request, create_account_request_role_credit, amount: int | float, term_month: int):

        account_1_with_credit = create_account_credit_request(amount, term_month)
        assert account_1_with_credit.model_dump()['balance'] == amount, 'Баланс кредита должен быть равен запрошенной сумме'

        account_2 = create_account_request_role_credit
        credit_data = CreateCreditRequest(
            accountId=account_2.id,
            amount=amount,
            termMonths=term_month
        )

        api_manager.user_steps.request_credit_not_found(create_credit_user_request, credit_data)


    @allure.title('Выдача кредита для пользователя. Невалидные данные для суммы кредита')
    @pytest.mark.parametrize('term_month', [12])
    @pytest.mark.parametrize('amount', [4999.9, 15000.1, -5000, -15000, 0])
    def test_create_credit_invalid(self, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest,
                                   create_account_request_role_credit, amount: float | int, term_month: int):

        response = create_account_request_role_credit

        assert response.balance == 0, 'Баланс должен быть равен 0'

        credit_data = CreateCreditRequest(
            accountId= response.id,
            amount= amount,
            termMonths= term_month
        )

        api_manager.user_steps.request_invalid_credit(create_credit_user_request, credit_data)


    @allure.title('Выдача кредита для пользователя. Невалидные данные для срока кредита')
    @pytest.mark.parametrize('amount', [5000])
    @pytest.mark.parametrize('term_month', [0, 61])
    def test_create_credit_invalid_term_month(self, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest,
                                              create_account_request_role_credit, amount: int| float, term_month: int):

        account = create_account_request_role_credit

        assert account.balance == 0, 'Баланс должен быть равен 0'

        credit_data = CreateCreditRequest(
            accountId=account.id,
            amount=amount,
            termMonths=term_month
        )

        api_manager.user_steps.request_invalid_credit(create_credit_user_request, credit_data)