import allure
import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_credit_request import CreateCreditRequest
from src.main.api.models.create_user_request import CreateCreditUserRequest
from src.main.api.models.repay_credit_request import RepayCreditRequest
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit


@allure.epic('Тесты по погашению кредита')
@allure.suite('Тесты по погашению кредита')
class TestRepayCredit:
    @allure.title('Погашение кредита')
    @pytest.mark.parametrize('amount, term_month', [(5000, 12)])
    def test_credit_repay_valid(self, db_session: Session, api_manager: ApiManager,
                                create_credit_user_request: CreateCreditUserRequest, amount: int | float, term_month: int):
        account = api_manager.user_steps.create_account(create_credit_user_request)

        assert account.balance == 0

        credit_data = CreateCreditRequest(
                accountId=account.id,
                amount=amount,
                termMonths=term_month
            )

        resp_cred = api_manager.user_steps.request_credit(create_credit_user_request, credit_data)

        credit_response = resp_cred.model_dump()
        assert credit_data.amount == credit_response['amount']
        assert credit_data.amount == credit_response['balance']
        assert credit_data.accountId == credit_response['id']
        assert credit_data.termMonths == credit_response['termMonths']

        repay_credit_data = RepayCreditRequest(creditId=credit_response['creditId'],
                                               accountId=credit_response['id'],
                                               amount=credit_data.amount)

        resp = api_manager.user_steps.repay_credit(create_credit_user_request, repay_credit_data)

        repay_response = resp.model_dump()
        assert repay_response['amountDeposited'] == credit_data.amount
        assert repay_response['creditId'] == credit_response['creditId']

        credit_from_db = Credit.get_credit_by_id(db_session, credit_response['creditId'])

        assert credit_from_db.amount == credit_data.amount, 'Значение пополнения не изменилось в БД'
        assert credit_from_db.account_id == credit_data.accountId, 'ID аккаунта в БД не совпадает'
        assert credit_from_db.balance == 0.0, 'Задолженность по кредиту не изменилась в БД'


    @allure.title('Погашение кредита. Невалидные данные по сумме погашения кредита')
    @pytest.mark.parametrize('amount, term_month', [(5000, 12)])
    @pytest.mark.parametrize('repay', [1, 4000, 5000.1, 15000])
    def test_credit_repay_invalid(self, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest,
                                  amount: int | float, term_month: int, repay: int| float):
        account = api_manager.user_steps.create_account(create_credit_user_request)

        assert account.balance == 0

        credit_data = CreateCreditRequest(
                accountId=account.id,
                amount=amount,
                termMonths=term_month
            )

        resp_cred = api_manager.user_steps.request_credit(create_credit_user_request, credit_data)

        credit_response = resp_cred.model_dump()
        assert credit_data.amount == credit_response['amount']
        assert credit_data.amount == credit_response['balance']
        assert credit_data.accountId == credit_response['id']
        assert credit_data.termMonths == credit_response['termMonths']

        repay_credit_data = RepayCreditRequest(creditId=credit_response['creditId'],
                                               accountId=credit_response['id'],
                                               amount=repay)

        api_manager.user_steps.repay_credit_invalid(create_credit_user_request, repay_credit_data)


    @allure.title('Погашение кредита. Невалидные данные по сумме погашения кредита')
    @pytest.mark.parametrize('amount, term_month', [(5000, 12)])
    @pytest.mark.parametrize('repay', [0, -5000])
    def test_credit_repay_invalid_less_zero(self, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest,
                                            amount: int | float, term_month: int, repay: int | float):
        account = api_manager.user_steps.create_account(create_credit_user_request)

        assert account.balance == 0

        credit_data = CreateCreditRequest(
            accountId=account.id,
            amount=amount,
            termMonths=term_month
        )

        resp_cred = api_manager.user_steps.request_credit(create_credit_user_request, credit_data)

        credit_response = resp_cred.model_dump()
        assert credit_data.amount == credit_response['amount']
        assert credit_data.amount == credit_response['balance']
        assert credit_data.accountId == credit_response['id']
        assert credit_data.termMonths == credit_response['termMonths']

        repay_credit_data = RepayCreditRequest(creditId=credit_response['creditId'],
                                               accountId=credit_response['id'],
                                               amount=repay)

        api_manager.user_steps.repay_credit_invalid_less_zero(create_credit_user_request, repay_credit_data)
