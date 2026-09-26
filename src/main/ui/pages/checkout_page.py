from playwright.sync_api import Page, expect

from src.main.ui.utils import constants


class CheckoutPage:
    URL: str = constants.Urls.CHECKOUT

    def __init__(self, page: Page):
        self.page = page
        self.first_name_input = page.locator('#first-name')
        self.last_name_input = page.locator('#last-name')
        self.postal_code_input = page.locator('#postal-code')
        self.continue_button = page.locator('#continue')
        self.item_total = page.locator('.summary_subtotal_label')
        self.tax = page.locator('.summary_tax_label')
        self.total = page.locator('.summary_total_label')
        self.finish_button = page.locator('#finish')
        self.success_message = page.locator(".complete-header")
        self.error_message = page.locator('h3[data-test="error"]')

    # --- Действия ---
    def start_checkout(self, first_name: str, last_name: str, postal_code: str):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)
        self.continue_button.click()

    def finish_checkout(self):
        self.finish_button.click()

    # --- Методы для получения данных (для тестов) ---
    def get_error_text(self) -> str:
        return self.error_message.inner_text()

    def get_success_text(self) -> str:
        return self.success_message.inner_text()

    def get_item_total(self) -> float:
        # текст вида "Item total: $39.98"
        total_text = self.item_total.inner_text()
        return float(total_text.replace("Item total: $", ""))

    def get_item_total_after_continue(self) -> float:
        # ждем появления элемента
        expect(self.item_total).to_be_visible()
        total_text = self.item_total.inner_text()
        return float(total_text.replace("Item total: $", ""))

    def get_tax_after_continue(self) -> float:
        # ждем появления элемента
        expect(self.tax).to_be_visible()
        tax_text = self.tax.inner_text()
        return float(tax_text.replace("Item total: $", ""))

    def get_total_after_continue(self) -> float:
        # ждем появления элемента
        expect(self.total).to_be_visible()
        total_text = self.total.inner_text()
        return float(total_text.replace("Item total: $", ""))