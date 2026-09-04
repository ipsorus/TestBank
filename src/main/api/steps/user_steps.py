import allure

from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.create_credit_request import CreateCreditRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.repay_credit_request import RepayCreditRequest
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        with allure.step('Create Account'):
            response = ValidateCrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.CREATE_ACCOUNT,
                ResponseSpecs.request_created()
            ).post()
            return response

    def create_account_conflict(self, create_user_request: CreateUserRequest):
        with allure.step('Create Account Error 409'):
            response = CrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.CREATE_ACCOUNT,
                ResponseSpecs.request_conflict()
            ).post()
            return response

    def create_deposit(self, create_user_request: CreateUserRequest, deposit_request: DepositRequest):
        with allure.step('Create Deposit'):
            response = ValidateCrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.CREATE_DEPOSIT,
                ResponseSpecs.request_ok()
            ).post(deposit_request)
            return response

    def create_deposit_bad(self, create_user_request: CreateUserRequest, deposit_request: DepositRequest):
        with allure.step('Create Deposit Error 400'):
            CrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.CREATE_DEPOSIT,
                ResponseSpecs.request_bad()
            ).post(deposit_request)

    def get_account_transaction(self, create_user_request: CreateUserRequest, account_id: int):
        with allure.step('Get account transaction'):
            response = ValidateCrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.GET_ACCOUNT_TRANSACTION,
                ResponseSpecs.request_ok()
            ).get(account_id)
            return response

    def create_transfer(self, create_user_request: CreateUserRequest, transfer_request: TransferRequest):
        with allure.step('Create transfer'):
            response = ValidateCrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.CREATE_TRANSFER,
                ResponseSpecs.request_ok()
            ).post(transfer_request)
            return response

    def create_transfer_bad(self, create_user_request: CreateUserRequest, transfer_request: TransferRequest):
        with allure.step('Create transfer. ERROR 400'):
            CrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.CREATE_TRANSFER,
                ResponseSpecs.request_bad()
            ).post(transfer_request)

    def create_transfer_wrong_operation(self, create_user_request: CreateUserRequest, transfer_request: TransferRequest):
        with allure.step('Create transfer. ERROR 422'):
            response = CrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.CREATE_TRANSFER,
                ResponseSpecs.request_wrong_operation()
            ).post(transfer_request)
            return response

    def request_credit(self, create_user_request: CreateUserRequest, create_credit_request: CreateCreditRequest):
        with allure.step('Request credit'):
            response = ValidateCrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.REQUEST_CREDIT,
                ResponseSpecs.request_created()
            ).post(create_credit_request)
            return response

    def request_credit_forbidden(self, create_user_request: CreateUserRequest, create_credit_request: CreateCreditRequest):
        with allure.step('Request credit. ERROR 403'):
            CrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.REQUEST_CREDIT,
                ResponseSpecs.request_forbidden()
            ).post(create_credit_request)

    def request_credit_not_found(self, create_user_request: CreateUserRequest, create_credit_request: CreateCreditRequest):
        with allure.step('Request credit. ERROR 404'):
            CrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.REQUEST_CREDIT,
                ResponseSpecs.request_not_found()
            ).post(create_credit_request)

    def request_invalid_credit(self, create_user_request: CreateUserRequest, create_credit_request: CreateCreditRequest):
        with allure.step('Request credit. ERROR 400'):
            CrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.REQUEST_CREDIT,
                ResponseSpecs.request_bad()
            ).post(create_credit_request)

    def repay_credit(self, create_user_request: CreateUserRequest, repay_credit_request: RepayCreditRequest):
        with allure.step('Repay credit'):
            response = ValidateCrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.REPAY_CREDIT,
                ResponseSpecs.request_ok()
            ).post(repay_credit_request)
            return response

    def repay_credit_invalid(self, create_user_request: CreateUserRequest, repay_credit_request: RepayCreditRequest):
        with allure.step('Repay credit. ERROR 422'):
            response = CrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.REPAY_CREDIT,
                ResponseSpecs.request_wrong_operation()
            ).post(repay_credit_request)
            return response

    def repay_credit_invalid_less_zero(self, create_user_request: CreateUserRequest, repay_credit_request: RepayCreditRequest):
        with allure.step('Repay credit. ERROR 400'):
            response = CrudRequester(
                RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
                Endpoint.REPAY_CREDIT,
                ResponseSpecs.request_bad()
            ).post(repay_credit_request)
            return response
