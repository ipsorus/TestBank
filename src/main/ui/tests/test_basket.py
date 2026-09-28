from playwright.sync_api import Page

from src.main.ui.steps.basket_steps import BasketSteps
from src.main.ui.steps.catalog_steps import CatalogSteps
from src.main.ui.steps.checkout_steps import CheckoutSteps
from src.main.ui.steps.login_steps import LoginSteps


def test_add_item_and_check_in_cart(page: Page):
    login_steps = LoginSteps(page)
    catalog_steps = CatalogSteps(page)
    basket_steps = BasketSteps(page)

    login_steps.login(username='standard_user', password='secret_sauce')
    catalog_steps.add_to_cart(product_name="Test.allTheThings() T-Shirt (Red)")

    basket_steps.open_cart()

    basket_steps.expect_item_in_cart(product_name="Test.allTheThings() T-Shirt (Red)")


def test_add_two_items_and_check_in_cart(page: Page):
    login_steps = LoginSteps(page)
    catalog_steps = CatalogSteps(page)
    basket_steps = BasketSteps(page)

    login_steps.login(username='standard_user', password='secret_sauce')
    catalog_steps.add_to_cart(product_name="Sauce Labs Backpack")
    catalog_steps.add_to_cart(product_name="Sauce Labs Bolt T-Shirt")

    basket_steps.open_cart()

    basket_steps.expect_item_in_cart(product_name="Sauce Labs Backpack")
    basket_steps.expect_item_in_cart(product_name="Sauce Labs Bolt T-Shirt")


def test_remove_item_from_cart(page):
    catalog_steps = CatalogSteps(page)
    basket_steps = BasketSteps(page)

    catalog_steps.login(username='standard_user', password='secret_sauce')
    catalog_steps.add_to_cart(product_name="Sauce Labs Fleece Jacket")

    basket_steps.open_cart()
    basket_steps.expect_item_in_cart("Sauce Labs Fleece Jacket")
    basket_steps.remove_item_from_cart("Sauce Labs Fleece Jacket")
    basket_steps.expect_item_not_in_cart("Sauce Labs Fleece Jacket")


def test_remove_items_from_cart(page):
    catalog_steps = CatalogSteps(page)
    basket_steps = BasketSteps(page)

    catalog_steps.login(username='standard_user', password='secret_sauce')
    catalog_steps.add_to_cart(product_name="Sauce Labs Backpack")
    catalog_steps.add_to_cart(product_name="Test.allTheThings() T-Shirt (Red)")

    basket_steps.open_cart()
    basket_steps.expect_item_in_cart("Sauce Labs Backpack")
    basket_steps.expect_item_in_cart("Test.allTheThings() T-Shirt (Red)")

    basket_steps.remove_item_from_cart("Sauce Labs Backpack")
    basket_steps.remove_item_from_cart("Test.allTheThings() T-Shirt (Red)")

    basket_steps.expect_item_not_in_cart("Sauce Labs Backpack")
    basket_steps.expect_item_not_in_cart("Test.allTheThings() T-Shirt (Red)")


def test_checkout_multiple_items(page):

    catalog_steps = CatalogSteps(page)
    basket_steps = BasketSteps(page)
    checkout_steps = CheckoutSteps(page)

    catalog_steps.login(username='standard_user', password='secret_sauce')
    catalog_steps.add_to_cart(product_name="Sauce Labs Fleece Jacket")
    catalog_steps.add_to_cart(product_name="Sauce Labs Bolt T-Shirt")

    # Проверяем товары в корзине
    basket_steps.open_cart()
    basket_steps.expect_item_in_cart("Sauce Labs Fleece Jacket")
    basket_steps.expect_item_in_cart("Sauce Labs Bolt T-Shirt")

    # Считаем сумму корзины перед чекаутом
    basket_total = basket_steps.get_items_total_price()

    # Переходим к Checkout
    basket_steps.checkout()
    checkout_steps.start_checkout(first_name="Test", last_name="User", postal_code="12345")

    # Проверяем сумму на Checkout
    checkout_total = checkout_steps.get_item_total_after_continue()
    assert checkout_total == basket_total, "Сумма товаров в Checkout не совпадает с корзиной"


def test_checkout_without_items(page):
    catalog_steps = CatalogSteps(page)
    basket_steps = BasketSteps(page)
    checkout_steps = CheckoutSteps(page)

    catalog_steps.login(username='standard_user', password='secret_sauce')

    # Корзина пустая
    basket_steps.open_cart()
    items = basket_steps.get_item_names()
    assert len(items) == 0, "Корзина не пуста"

    basket_steps.checkout()
    checkout_steps.start_checkout(first_name="NewUser", last_name="Nrk", postal_code="")

    # Проверка ошибки о пустой корзине
    error_text = checkout_steps.get_error_text()
    assert error_text != "", "Ожидалась ошибка при оформлении пустой корзины"
