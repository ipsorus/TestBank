import allure
from playwright.sync_api import Page

from src.main.ui.pages.basket_page import BasketPage


class BasketSteps:

    def __init__(self, page: Page):
        self.page = page
        self.basket = BasketPage(page)

    @allure.step("Открыть корзину")
    def open_cart(self):
        self.basket.open_cart()
        return self

    @allure.step("Проверить, что товар в корзине {product_name}")
    def expect_item_in_cart(self, product_name: str):
        self.basket.expect_item_in_cart(product_name=product_name)
        return self

    @allure.step("Проверить, что товар не в корзине {product_name}")
    def expect_item_not_in_cart(self, product_name: str):
        self.basket.expect_item_not_in_cart(product_name=product_name)
        return self

    @allure.step("Удалить товар из корзины {product_name}")
    def remove_item_from_cart(self, product_name: str):
        self.basket.remove_item(product_name=product_name)
        return self

    @allure.step("Получить итоговую стоимость товаров в корзине")
    def get_items_total_price(self) -> float | int:
        return self.basket.get_items_total_price()

    @allure.step("Перейти к подтверждению заказа")
    def checkout(self):
        self.basket.checkout()
        return self

    @allure.step("Получить названия товаров в корзине")
    def get_item_names(self) -> list[str]:
        return self.basket.get_item_names()