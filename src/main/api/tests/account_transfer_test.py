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
    def test_transfer_valid(self, db_session: Session, api_manager: ApiManager, create_account_for_one_user,
                            amount: int| float, transfer: int| float,
                            create_user_request: CreateUserRequest, create_deposit):
        """
        Тест выполняет проверку возможности перевода между счетами одного юзера
        """
        acc_1 = create_account_for_one_user(create_user_request)
        acc_2 = create_account_for_one_user(create_user_request)

        assert acc_1.balance == 0, 'Баланс должен быть равен 0'
        assert acc_2.balance == 0, 'Баланс должен быть равен 0'

        create_deposit_response = create_deposit(create_user_request, acc_1.id, amount)

        assert create_deposit_response.model_dump()["id"] == acc_1.id, 'Пополнение счета выполнено на другой аккаунт'
        assert create_deposit_response.model_dump()["balance"] == amount, 'Баланс счета не соответствует'

        payload_2 = TransferRequest(
            fromAccountId=acc_1.id,
            toAccountId=acc_2.id,
            amount=transfer
        )

        api_manager.user_steps.create_transfer(create_user_request, payload_2)

        transaction_response = api_manager.user_steps.get_account_transaction(create_user_request, acc_2.id)

        assert transaction_response.model_dump()["balance"] == payload_2.amount, 'Баланс в транзакции не совпадает'
        assert transaction_response.model_dump()["transactions"][0]["amount"] == payload_2.amount, 'Сумма пополнения не совпадает'

        transaction_from_db = Transaction.get_transaction_by_id(db_session, transaction_response.transactions[0].transactionId)

        assert transaction_from_db.from_account_id == acc_1.id, 'ID аккаунта отправителя не совпадает с БД'
        assert transaction_from_db.to_account_id == acc_2.id, 'ID аккаунта получателя не совпадает с БД'
        assert transaction_from_db.amount == transfer, 'Сумма перевода не совпадает с БД'

    @allure.title('Перевод между счетами разных пользователей')
    @pytest.mark.parametrize('amount, transfer, user_1, user_2', [(1000.5, 500.75,
                                                                   RandomModelGenerator.generate(CreateUserRequest),
                                                                   RandomModelGenerator.generate(CreateUserRequest))])
    def test_transfer_other_user_valid(self, api_manager: ApiManager, create_user_request: CreateUserRequest,
                                       create_account_different_users, amount: int| float, transfer: int| float,
                                       user_1: CreateUserRequest,
                                       user_2: CreateUserRequest,
                                       create_deposit):
        """
        Тест выполняет проверку возможности перевода между счетами разных юзеров
        """
        _, user_resp_1, acc_1 = create_account_different_users(user_1)
        _, user_resp_2, acc_2 = create_account_different_users(user_2)

        assert user_resp_1.model_dump()['id'] != user_resp_2.model_dump()['id'], 'ID пользователей должен быть разный'
        assert acc_1.balance == 0, 'Баланс должен быть равен 0'
        assert acc_2.balance == 0, 'Баланс должен быть равен 0'

        create_deposit_response = create_deposit(user_1, acc_1.id, amount)

        assert create_deposit_response.model_dump()["id"] == acc_1.id, 'ID аккаунта не совпадает'
        assert create_deposit_response.model_dump()["balance"] == amount, 'Сумма на счете не совпадает после зачисления'

        payload_2 = TransferRequest(
            fromAccountId=acc_1.id,
            toAccountId=acc_2.id,
            amount=transfer
        )

        api_manager.user_steps.create_transfer(user_1, payload_2)

        transaction_response = api_manager.user_steps.get_account_transaction(user_2, acc_2.id)

        assert transaction_response.model_dump()["balance"] == payload_2.amount, 'Баланс на счете 2 не совпадает после перевода средств'
        assert transaction_response.model_dump()["transactions"][0]["amount"] == payload_2.amount, 'Сумма перевода не совпадает в транзакции'

    @allure.title('Перевод между счетами одного пользователя, невалидные данные')
    @pytest.mark.parametrize('amount', [1000.5])
    @pytest.mark.parametrize('transfer', [0, 499.9, 10000.1, -1001, -1000, -9000, ])
    def test_transfer_invalid(self, api_manager: ApiManager, create_user_request: CreateUserRequest,
                              create_account_for_one_user, amount: int| float, transfer: int| float):
        """
        Тест выполняет проверку возможности перевода между счетами через параметризацию,
        создавая для каждого теста новый счет
        """
        acc_1 = create_account_for_one_user(create_user_request)
        acc_2 = create_account_for_one_user(create_user_request)

        assert acc_1.balance == 0, 'Баланс должен быть равен 0'
        assert acc_2.balance == 0, 'Баланс должен быть равен 0'

        payload = DepositRequest(
            accountId=acc_1.id,
            amount=amount)

        create_deposit_response = api_manager.user_steps.create_deposit(create_user_request, payload)

        assert create_deposit_response.model_dump()["id"] == payload.accountId, 'ID аккаунта не совпадает'
        assert create_deposit_response.model_dump()["balance"] == payload.amount, 'Сумма на счете не совпадает после зачисления'

        payload_2 = TransferRequest(
                fromAccountId=acc_1.id,
                toAccountId=acc_2.id,
                amount=transfer
        )

        api_manager.user_steps.create_transfer_bad(create_user_request, payload_2)

        transaction_response = api_manager.user_steps.get_account_transaction(create_user_request, acc_2.id)

        assert transaction_response.model_dump()["balance"] == 0, 'Баланс счета после перевода изменился. Ошибка'


    @allure.title('Перевод между счетами одного пользователя, невалидные данные, сумма перевода > баланса')
    @pytest.mark.parametrize('amount, transfer', [(1000.5, 1000.6)])
    def test_transfer_invalid_3(self, api_manager: ApiManager, create_user_request: CreateUserRequest,
                                create_account_for_one_user, amount: int| float, transfer: int| float):
        """
        Тест выполняет проверку возможности перевода между счетами одного юзера,
        с попыткой перевода суммы, большей, чем имеется на балансе
        """
        acc_1 = create_account_for_one_user(create_user_request)
        acc_2 = create_account_for_one_user(create_user_request)

        assert acc_1.balance == 0, 'Баланс должен быть равен 0'
        assert acc_2.balance == 0, 'Баланс должен быть равен 0'

        payload = DepositRequest(
            accountId=acc_1.id,
            amount=amount)

        create_deposit_response = api_manager.user_steps.create_deposit(create_user_request, payload)

        assert create_deposit_response.model_dump()["id"] == payload.accountId, 'ID аккаунта не совпадает'
        assert create_deposit_response.model_dump()["balance"] == payload.amount, 'Сумма на счете не совпадает после зачисления'

        payload_2 = TransferRequest(
            fromAccountId=acc_1.id,
            toAccountId=acc_2.id,
            amount=transfer
        )

        r = api_manager.user_steps.create_transfer_wrong_operation(create_user_request, payload_2)
        assert r.status_code == 422, 'Код ответа не совпадает'

        transaction_response = api_manager.user_steps.get_account_transaction(create_user_request, acc_2.id)

        assert transaction_response.model_dump()["balance"] == 0, 'Баланс счета после перевода изменился. Ошибка'