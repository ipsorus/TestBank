import allure
import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest, CreateCreditUserRequest
from src.main.api.models.login_user_request import LoginUserRequest


@pytest.mark.api
@allure.epic('Тесты по авторизации')
@allure.suite('Тесты по авторизации')
class TestUserLogin:
    @allure.title('Авторизация пользователя с ролью ROLE_ADMIN')
    def test_login_admin(self, api_manager: ApiManager):
        login_user_request = LoginUserRequest(username='admin', password='123456')

        response = api_manager.admin_steps.login_user(login_user_request)

        assert login_user_request.username == response.user.username
        assert response.user.role =="ROLE_ADMIN"


    @allure.title('Авторизация пользователя с ролью ROLE_USER')
    def test_login_user(self, api_manager: ApiManager, create_user_request: CreateUserRequest):

        response = api_manager.admin_steps.login_user(create_user_request)

        assert create_user_request.username == response.user.username
        assert response.user.role == 'ROLE_USER'


    @allure.title('Авторизация пользователя с ролью ROLE_CREDIT_SECRET')
    def test_login_credit_user(self, api_manager: ApiManager, create_credit_user_request: CreateCreditUserRequest):

        response = api_manager.admin_steps.login_user(create_credit_user_request)

        assert create_credit_user_request.username == response.user.username
        assert response.user.role == 'ROLE_CREDIT_SECRET'