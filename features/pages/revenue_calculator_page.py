import math
import re
from playwright.sync_api import Page, expect

CALCULATOR_URL_SUBSTR = "apps09.revenue.nsw.gov.au/erevenue/calculators/motorsimple.php"

class RevenueCalculatorPage:
    def __init__(self, page: Page):
        self.page = page

    def assert_loaded(self):
        # URL contains calculator path and page shows heading
        expect(self.page).to_have_url(re.compile(CALCULATOR_URL_SUBSTR))
        expect(self.page.get_by_role("heading", name=re.compile("Motor vehicle registration duty calculator", re.I))).to_be_visible()

    def select_passenger_yes(self):
        # Radio buttons are rendered with text 'Yes' and 'No'
        self.page.get_by_label(re.compile(r"Is this registration for a passenger vehicle\?", re.I)).locator("..").get_by_text("Yes").click()

    def enter_amount(self, amount: int):
        # The input is labelled 'Purchase price or value (whole dollars):'
        self.page.get_by_label(re.compile(r"Purchase price or value", re.I)).fill(str(amount))

    def click_calculate_and_capture_popup(self):
        # The site displays an alert() with the result
        with self.page.expect_dialog() as dlg:
            self.page.get_by_role("button", name=re.compile("^\s*Calculate\s*$", re.I)).click()
        dialog = dlg.value
        text = dialog.message
        dialog.accept()
        return text

    @staticmethod
    def expected_duty_for(amount: int, passenger: bool=True) -> int:
        # From Service NSW: $3 per $100 up to $44,999; for passenger vehicles >= 45,000:
        # $1,350 + $5 per $100 for the amount over $45,000 (exemptions excluded).
        if not passenger:
            # Non-passenger: use base $3 per $100 for all values
            units = math.ceil(amount / 100.0)
            return units * 3
        if amount < 45000:
            units = math.ceil(amount / 100.0)
            return units * 3
        over = amount - 45000
        units_over = math.ceil(over / 100.0)
        return 1350 + units_over * 5

    @staticmethod
    def normalize_money_text(s: str) -> str:
        return re.sub(r"[^0-9]", "", s or "")  # strip non-digits for comparison
