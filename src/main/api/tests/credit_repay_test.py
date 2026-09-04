import allure
import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateCreditUserRequest
from src.main.api.models.repay_credit_request import RepayCreditRequest
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit


@allure.epic('Тесты по погашению кредита')
@allure.suite('Тесты по погашению кредита')
class TestRepayCredit:
    @allure.title('Погашение кредита')
    @pytest.mark.parametrize('amount, term_month', [(5000, 12)])
    def test_credit_repay_valid(self, db_session: Session, api_manager: ApiManager,
                                create_credit_user_request: CreateCreditUserRequest, create_account_credit_request,
                                amount: int | float, term_month: int):

        resp_cred = create_account_credit_request(amount, term_month)

        credit_response = resp_cred.model_dump()

        repay_credit_data = RepayCreditRequest(creditId=credit_response['creditId'],
                                               accountId=credit_response['id'],
                                               amount=amount)

        resp = api_manager.user_steps.repay_credit(create_credit_user_request, repay_credit_data)

        repay_response = resp.model_dump()
        assert repay_response['amountDeposited'] == amount
        assert repay_response['creditId'] == credit_response['creditId']

        credit_from_db = Credit.get_credit_by_id(db_session, credit_response['creditId'])

        assert credit_from_db.amount == amount, 'Значение пополнения не изменилось в БД'
        assert credit_from_db.balance == 0.0, 'Задолженность по кредиту не изменилась в БД'


    @allure.title('Погашение кредита. Невалидные данные по сумме погашения кредита')
    @pytest.mark.parametrize('amount, term_month', [(5000, 12)])
    @pytest.mark.parametrize('repay', [1, 4000, 5000.1, 15000])
    def test_credit_repay_invalid(self, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest,
                                  create_account_credit_request, amount: int | float, term_month: int, repay: int| float):

        resp_cred = create_account_credit_request(amount, term_month)

        credit_response = resp_cred.model_dump()
        assert amount == credit_response['amount']
        assert amount == credit_response['balance']
        assert term_month == credit_response['termMonths']

        repay_credit_data = RepayCreditRequest(creditId=credit_response['creditId'],
                                               accountId=credit_response['id'],
                                               amount=repay)

        r = api_manager.user_steps.repay_credit_invalid(create_credit_user_request, repay_credit_data)

        assert r.status_code == 422, 'Код ответа не совпадает'


    @allure.title('Погашение кредита. Невалидные данные по сумме погашения кредита')
    @pytest.mark.parametrize('amount, term_month', [(5000, 12)])
    @pytest.mark.parametrize('repay', [0, -5000])
    def test_credit_repay_invalid_less_zero(self, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest,
                                            create_account_credit_request, amount: int | float, term_month: int, repay: int | float):

        resp_cred = create_account_credit_request(amount, term_month)

        credit_response = resp_cred.model_dump()
        assert amount == credit_response['amount']
        assert amount == credit_response['balance']
        assert term_month == credit_response['termMonths']

        repay_credit_data = RepayCreditRequest(creditId=credit_response['creditId'],
                                               accountId=credit_response['id'],
                                               amount=repay)

        r = api_manager.user_steps.repay_credit_invalid_less_zero(create_credit_user_request, repay_credit_data)
        assert r.status_code == 400, 'Код ответа не совпадает'
        assert r.json().get("error") == 'Amount must be greater than 0', 'Текст ошибки не совпадает'
