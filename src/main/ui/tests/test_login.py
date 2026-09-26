from playwright.sync_api import Page, expect

from src.main.ui.pages.catalog_page import CatalogPage
from src.main.ui.steps.catalog_steps import CatalogSteps
from src.main.ui.steps.login_steps import LoginSteps


def test_login(page: Page):
    login_steps = LoginSteps(page)
    login_steps.open_login_page()
    login_steps.login(username='standard_user', password='secret_sauce')

    expect(page).to_have_url(CatalogPage.URL)
    assert page.url == CatalogPage.URL, "Ожидаем редирект на страницу каталога"

    # Проверяем, что мы на странице каталога после успешного логина
    catalog_page = CatalogPage(page)
    assert catalog_page.get_products_count() > 0, "Ожидаем товары на странице каталога"

def test_login_locked_out_user(page: Page):
    login_steps = LoginSteps(page)
    login_steps.open_login_page()
    login_steps.login(username='locked_out_user', password='secret_sauce')

    error_text = login_steps.get_error_text()
    assert "locked out" in error_text, "Ожидаем сообщение о заблокированном пользователе"


def test_logout(page: Page):
    login_steps = LoginSteps(page)
    catalog_steps = CatalogSteps(page)

    login_steps.login(username='standard_user', password='secret_sauce')

    assert catalog_steps.get_products_count() > 0, "Ожидаем, что в каталоге есть товары"

    catalog_steps.logout()

    expect(page).to_have_url(login_steps.LOGIN_URL + '/')
    assert page.url == login_steps.LOGIN_URL + '/', "Ожидаем возврат на страницу логина"

    
def test_logout_visual_user(page):
    login_steps = LoginSteps(page)
    catalog_steps = CatalogSteps(page)

    login_steps.login(username='standard_user', password='secret_sauce')

    # Проверяем, что мы на странице каталога
    assert catalog_steps.get_products_count() > 0, "Ожидаем, что в каталоге есть товары"

    # --- Логаут через Page Object ---
    catalog_steps.logout()

    # Проверяем, что вернулись на страницу логина
    expect(page).to_have_url(login_steps.LOGIN_URL + '/')
    assert page.url == login_steps.LOGIN_URL + '/', "Ожидаем возврат на страницу логина"
