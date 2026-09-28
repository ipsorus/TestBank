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


#     finish_button = page.locator('#finish')
#     expect(finish_button).to_be_visible()
#     finish_button.click()
#
#     # Проверка сообщения об успешной оплате заказа
#     expect(page.locator('h2[data-test="complete-header"]', has_text='Thank you for your order!')).to_be_visible()


# def test_checkout_multiple_items_original(auth_page):
#     """
#     Оригинальный вариант из урока
#     """
#
#     # Добавляем товары
#     jacket_card = auth_page.locator(".inventory_item", has_text="Sauce Labs Fleece Jacket")
#     t_shirt_card = auth_page.locator(".inventory_item", has_text="Sauce Labs Bolt T-Shirt")
#
#     jacket_card.locator("button").click()  # Add to cart
#     t_shirt_card.locator("button").click() # Add to cart
#
#     # Переходим в корзину
#     auth_page.locator('[data-test="shopping-cart-link"]').click()
#
#     # Проверяем правильность товаров
#     jacket_name = auth_page.locator('.inventory_item_name', has_text='Sauce Labs Fleece Jacket')
#     t_shirt_name = auth_page.locator('.inventory_item_name', has_text='Sauce Labs Bolt T-Shirt')
#     expect(jacket_name).to_be_visible()
#     expect(t_shirt_name).to_be_visible()
#
#     # Считаем сумму товаров
#     prices_text = auth_page.locator(".inventory_item_price").all_text_contents()
#     prices = [float(p.replace("$","")) for p in prices_text]
#     expected_total = sum(prices)
#
#     # Заполняем поля
#     auth_page.locator('[data-test="checkout"]').click()
#     auth_page.locator('[data-test="firstName"]').fill("A")
#     auth_page.locator('[data-test="lastName"]').fill("K")
#     auth_page.locator('[data-test="postalCode"]').fill("000")
#     auth_page.locator('[data-test="continue"]').click()
#
#     # Проверяем Item total
#     item_total_text = auth_page.locator(".summary_subtotal_label").inner_text()  # Example: "Item total: $49.99"
#     item_total_value = float(item_total_text.split("$")[1])
#     assert item_total_value == expected_total, f"Item total {item_total_value} не совпадает с суммой товаров {expected_total}"
#
#     # Tax и Total
#     tax_text = auth_page.locator(".summary_tax_label").inner_text()  # Example: "Tax: $4.00"
#     tax_value = float(tax_text.split("$")[1])
#     total_text = auth_page.locator(".summary_total_label").inner_text()  # Example: "Total: $53.99"
#     total_value = float(total_text.split("$")[1])
#     assert total_value == round(item_total_value + tax_value, 2), "Total не совпадает с суммой Item total + Tax"
#
#     # Жмем Finish
#     auth_page.locator('[data-test="finish"]').click()
#
#     # Проверяем успех оплаты товара
#     success_message = auth_page.locator(".complete-header")
#     expect(success_message).to_have_text("Thank you for your order!")

# def test_checkout_without_filling_form(auth_page):
#
#     # Добавляем Sauce Labs Backpack
#     auth_page.locator('[data-test="add-to-cart-sauce-labs-fleece-jacket"]').click()
#
#     # Добавляем Sauce Labs Backpack
#     auth_page.locator('[data-test="add-to-cart-sauce-labs-bolt-t-shirt"]').click()
#
#     # Переходим в корзину
#     auth_page.locator(".shopping_cart_link").click()
#
#     # Подтверждение заказа
#     checkout_button = auth_page.locator('#checkout')
#     expect(checkout_button).to_be_visible()
#     checkout_button.click()
#
#     # Нажатие кнопки Продолжить без заполнения формы
#     continue_button = auth_page.locator('#continue')
#     expect(continue_button).to_be_visible()
#     continue_button.click()
#
#     error_locator = auth_page.locator('h3[data-test="error"]')
#     expect(error_locator).to_be_visible()
#
#     expect(error_locator).to_have_text('Error: First Name is required')

# def test_checkout_without_items_original(auth_page):
#     """
#     Оригинальный вариант из урока
#     """
#
#     # Добавляем товар
#     auth_page.locator('[data-test="add-to-cart-sauce-labs-fleece-jacket"]').click()
#
#     # Переход в корзину
#     auth_page.locator('[data-test="shopping-cart-link"]').click()
#
#     # Проверяем что товар добавлен в корзину
#     jacket = auth_page.locator('.inventory_item_name', has_text='Sauce Labs Fleece Jacket')
#     expect(jacket).to_be_visible()
#
#     # Жмем Checout
#     auth_page.locator('[data-test="checkout"]').click()
#
#     # Заполянем поле First Name и Last Name
#     auth_page.get_by_placeholder("First Name").fill("NewUser")
#     auth_page.get_by_placeholder("Last Name").fill("Nrk")
#
#     # Жмем Continue
#     auth_page.locator('[data-test="continue"]').click()
#
#     # Проверяем ошибку
#     error_message = auth_page.locator('[data-test="error"]')
#     expect(error_message).to_have_text('Error: Postal Code is required')
#
#     # Заполянем поле First Name и Last Name
#     auth_page.get_by_placeholder("First Name").fill("NewUser")
#     auth_page.get_by_placeholder("Last Name").fill("Nrk")
#
#     # Жмем Continue
#     auth_page.locator('[data-test="continue"]').click()
#
#     # Проверяем ошибку
#     error_message = auth_page.locator('[data-test="error"]')
#     expect(error_message).to_have_text('Error: Postal Code is required')
