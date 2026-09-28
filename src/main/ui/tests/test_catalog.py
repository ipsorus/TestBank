from playwright.sync_api import Page

from src.main.ui.steps.catalog_steps import CatalogSteps


def test_count_catalog(page: Page):
    catalog_steps = CatalogSteps(page)
    catalog_steps.login(username="standard_user", password="secret_sauce")

    assert catalog_steps.get_products_count() == 6

def test_sorted_by_name(page: Page):
    catalog_steps = CatalogSteps(page)
    catalog_steps.login(username="standard_user", password="secret_sauce")

    catalog_steps.sort_items("az")
    product_cards = catalog_steps.get_product_names()
    assert product_cards == sorted(product_cards), "Товары не отсортированы по имени A-Z"

    catalog_steps.sort_items("za")
    product_cards = catalog_steps.get_product_names()
    assert product_cards == sorted(product_cards, reverse=True), "Товары не отсортированы по имени Z-A"

def test_sort_by_price(page: Page):
    catalog_steps = CatalogSteps(page)
    catalog_steps.login(username="standard_user", password="secret_sauce")

    catalog_steps.sort_items("lohi")
    product_cards = catalog_steps.get_product_prices()
    assert product_cards == sorted(product_cards), "Товары не отсортированы по возрастанию цены"

    catalog_steps.sort_items("hilo")
    product_cards = catalog_steps.get_product_prices()
    assert product_cards == sorted(product_cards, reverse=True), "Товары не отсортированы по убыванию цены"

def test_add_to_cart(page: Page):
    catalog_steps = CatalogSteps(page)
    catalog_steps.login(username="standard_user", password="secret_sauce")

    catalog_steps.add_to_cart(product_name="Sauce Labs Bike Light")
    assert catalog_steps.get_cart_count() == 1, 'Счетчик товаров в корзине не изменился'

def test_add_and_remove_onesie(page: Page):
    catalog_steps = CatalogSteps(page)
    catalog_steps.login(username="standard_user", password="secret_sauce")

    catalog_steps.add_to_cart(product_name="Sauce Labs Onesie")

    assert catalog_steps.get_cart_count() == 1, 'Счетчик товаров в корзине не изменился'

    catalog_steps.remove_from_cart(product_name="Sauce Labs Onesie")

    assert catalog_steps.get_cart_count() == 0, 'Счетчик товаров в корзине не изменился после удаления товара'


def test_product_detail(page: Page):
    catalog_steps = CatalogSteps(page)
    catalog_steps.login(username="standard_user", password="secret_sauce")

    name, price, detail_name, detail_price = catalog_steps.open_product_details(product_name="Sauce Labs Backpack")

    assert name == detail_name, 'Названия товара не совпадают'
    assert price == detail_price, 'Цена товара не совпадает'


def test_product_details_fleece_jacket(page: Page):
    catalog_steps = CatalogSteps(page)
    catalog_steps.login(username="standard_user", password="secret_sauce")

    name, price, detail_name, detail_price = catalog_steps.open_product_details("Sauce Labs Fleece Jacket")
    assert name == detail_name, 'Названия товара не совпадают'
    assert price == detail_price, 'Цена товара не совпадает'


def test_product_delete(page: Page):
    catalog_steps = CatalogSteps(page)
    catalog_steps.login(username="standard_user", password="secret_sauce")
    catalog_steps.add_to_cart(product_name="Test.allTheThings() T-Shirt (Red)")

    catalog_steps.remove_from_cart(product_name="Test.allTheThings() T-Shirt (Red)")
