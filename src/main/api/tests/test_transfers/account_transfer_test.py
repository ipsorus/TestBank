import allure
import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction
from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.transfer_request import TransferRequest

@allure.epic('Тесты по переводам')
@allure.suite('Тесты по переводам')
@pytest.mark.api
class TestTransferAccount:

    @allure.title('Перевод между счетами одного пользователя')
    @pytest.mark.parametrize('amount, transfer', [(1000.5, 500.75)])
    def test_transfer_valid(self, db_session: Session, api_manager: ApiManager, create_user_request: CreateUserRequest, amount: int| float, transfer: int| float):
        """
        Тест выполняет проверку возможности перевода между счетами одного юзера
        """
        response_acc_1 = api_manager.user_steps.create_account(create_user_request)

        assert response_acc_1.balance == 0

        payload = DepositRequest(
            accountId=response_acc_1.id,
            amount=amount)

        resp = api_manager.user_steps.create_deposit(create_user_request, payload)
        data = resp.model_dump()

        assert data["id"] == payload.accountId
        assert data["balance"] == payload.amount

        response_acc_2 = api_manager.user_steps.create_account(create_user_request)

        assert response_acc_2.balance == 0

        payload_2 = TransferRequest(
            fromAccountId=response_acc_1.id,
            toAccountId=response_acc_2.id,
            amount=transfer
        )

        api_manager.user_steps.create_transfer(create_user_request, payload_2)

        transaction_response = api_manager.user_steps.get_account_transaction(create_user_request, response_acc_2.id)

        assert transaction_response.model_dump()["balance"] == payload_2.amount
        assert transaction_response.model_dump()["transactions"][0]["amount"] == payload_2.amount

        transaction_from_db = Transaction.get_transaction_by_id(db_session, transaction_response.transactions[0].transactionId)

        assert transaction_from_db.from_account_id == response_acc_1.id, 'ID аккаунта отправителя не совпадает с БД'
        assert transaction_from_db.to_account_id == response_acc_2.id, 'ID аккаунта получателя не совпадает с БД'
        assert transaction_from_db.amount == transfer, 'Сумма перевода не совпадает с БД'

    @allure.title('Перевод между счетами разных пользователей')
    @pytest.mark.parametrize('amount, transfer', [(1000.5, 500.75)])
    def test_transfer_other_user_valid(self, api_manager: ApiManager, create_user_request: CreateUserRequest,
                                       amount: int| float, transfer: int| float):
        """
        Тест выполняет проверку возможности перевода между счетами разных юзеров
        """
        user_1 = RandomModelGenerator.generate(CreateUserRequest)
        api_manager.admin_steps.create_user(user_1)
        response_acc_1 = api_manager.user_steps.create_account(user_1)

        user_2 = RandomModelGenerator.generate(CreateUserRequest)
        api_manager.admin_steps.create_user(user_2)
        response_acc_2 = api_manager.user_steps.create_account(user_2)

        assert response_acc_1.balance == 0
        assert response_acc_2.balance == 0

        payload = DepositRequest(
            accountId=response_acc_1.id,
            amount=amount)

        create_deposit_response = api_manager.user_steps.create_deposit(user_1, payload)

        assert create_deposit_response.model_dump()["id"] == payload.accountId
        assert create_deposit_response.model_dump()["balance"] == payload.amount

        payload_2 = TransferRequest(
            fromAccountId=response_acc_1.id,
            toAccountId=response_acc_2.id,
            amount=transfer
        )

        api_manager.user_steps.create_transfer(user_1, payload_2)

        transaction_response = api_manager.user_steps.get_account_transaction(user_2, response_acc_2.id)

        assert transaction_response.model_dump()["balance"] == payload_2.amount
        assert transaction_response.model_dump()["transactions"][0]["amount"] == payload_2.amount

    @allure.title('Перевод между счетами одного пользователя, невалидные данные')
    @pytest.mark.parametrize('amount', [1000.5])
    @pytest.mark.parametrize('transfer', [0, 499.9, 10000.1, -1001, -1000, -9000, ])
    def test_transfer_invalid(self, api_manager: ApiManager, create_user_request: CreateUserRequest, amount: int| float, transfer: int| float):
        """
        Тест выполняет проверку возможности перевода между счетами через параметризацию,
        создавая для каждого теста новый счет
        """
        response_acc_1 = api_manager.user_steps.create_account(create_user_request)

        assert response_acc_1.balance == 0

        payload = DepositRequest(
            accountId=response_acc_1.id,
            amount=amount)

        create_deposit_response = api_manager.user_steps.create_deposit(create_user_request, payload)

        assert create_deposit_response.model_dump()["id"] == payload.accountId
        assert create_deposit_response.model_dump()["balance"] == payload.amount

        response_acc_2 = api_manager.user_steps.create_account(create_user_request)

        assert response_acc_2.balance == 0

        payload_2 = TransferRequest(
            fromAccountId=response_acc_1.id,
            toAccountId=response_acc_2.id,
            amount=transfer
        )

        api_manager.user_steps.create_transfer_bad(create_user_request, payload_2)

        transaction_response = api_manager.user_steps.get_account_transaction(create_user_request, response_acc_2.id)

        assert transaction_response.model_dump()["balance"] == 0

    @allure.title('Перевод между счетами одного пользователя, невалидные данные, через цикл')
    @pytest.mark.parametrize('amount', [1000.5])
    def test_transfer_invalid_2(self, api_manager: ApiManager, create_user_request: CreateUserRequest, amount: int| float):
        """
        Тест выполняет проверку возможности перевода между счетами через цикл для одного созданного счета
        """
        invalid_amount = [0, 499.9, 10000.1, -1001, -1000, -9000]
        response_acc_1 = api_manager.user_steps.create_account(create_user_request)

        assert response_acc_1.balance == 0

        payload = DepositRequest(
            accountId=response_acc_1.id,
            amount=amount)

        create_deposit_response = api_manager.user_steps.create_deposit(create_user_request, payload)

        assert create_deposit_response.model_dump()["id"] == payload.accountId
        assert create_deposit_response.model_dump()["balance"] == payload.amount

        response_acc_2 = api_manager.user_steps.create_account(create_user_request)

        assert response_acc_2.balance == 0

        for amount in invalid_amount:
            payload_2 = TransferRequest(
                fromAccountId=response_acc_1.id,
                toAccountId=response_acc_2.id,
                amount=amount
            )

            api_manager.user_steps.create_transfer_bad(create_user_request, payload_2)

            transaction_response = api_manager.user_steps.get_account_transaction(create_user_request,
                                                                                  response_acc_2.id)

            assert transaction_response.model_dump()["balance"] == 0

    @allure.title('Перевод между счетами одного пользователя, невалидные данные, сумма перевода > баланса')
    @pytest.mark.parametrize('amount, transfer', [(1000.5, 1000.6)])
    def test_transfer_invalid_3(self, api_manager: ApiManager, create_user_request: CreateUserRequest, amount: int| float, transfer: int| float):
        """
        Тест выполняет проверку возможности перевода между счетами одного юзера,
        с попыткой перевода суммы, большей, чем имеется на балансе
        """
        response_acc_1 = api_manager.user_steps.create_account(create_user_request)

        assert response_acc_1.balance == 0

        payload = DepositRequest(
            accountId=response_acc_1.id,
            amount=amount)

        create_deposit_response = api_manager.user_steps.create_deposit(create_user_request, payload)

        assert create_deposit_response.model_dump()["id"] == payload.accountId
        assert create_deposit_response.model_dump()["balance"] == payload.amount

        response_acc_2 = api_manager.user_steps.create_account(create_user_request)

        assert response_acc_2.balance == 0

        payload_2 = TransferRequest(
            fromAccountId=response_acc_1.id,
            toAccountId=response_acc_2.id,
            amount=transfer
        )

        api_manager.user_steps.create_transfer_wrong_operation(create_user_request, payload_2)

        transaction_response = api_manager.user_steps.get_account_transaction(create_user_request,
                                                                              response_acc_2.id)

        assert transaction_response.model_dump()["balance"] == 0