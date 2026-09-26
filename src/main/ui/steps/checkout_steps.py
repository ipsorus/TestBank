import allure
from playwright.sync_api import Page

from src.main.ui.conftest import page
from src.main.ui.pages.checkout_page import CheckoutPage


class CheckoutSteps:
    def __init__(self, page: Page):
        self.page = page
        self.checkout = CheckoutPage(page)

    @allure.step("Начать оформление заказа с данными: {first_name}, {last_name}, {postal_code}")
    def start_checkout(self, first_name, last_name, postal_code):
        self.checkout.start_checkout(first_name=first_name, last_name=last_name, postal_code=postal_code)
        return self

    @allure.step("Получить итоговую стоимость перед оплатой заказа")
    def get_item_total_after_continue(self) -> float | int:
        return self.checkout.get_item_total_after_continue()

    @allure.step("Получить текст ошибки при оформлении заказа")
    def get_error_text(self) -> str:
        return self.checkout.get_error_text()