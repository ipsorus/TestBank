from playwright.sync_api import Page

from src.main.ui.pages.base_page import BasePage
from src.main.ui.utils import constants


class LoginPage(BasePage):
    URL: str = constants.Urls.BASE

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.error_message = page.locator("h3[data-test='error']")

    def open(self):
        self.page.goto(self.URL)

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_text(self):
        return self.error_message.inner_text()