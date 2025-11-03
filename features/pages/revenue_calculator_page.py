import math
import re
from playwright.sync_api import Page, expect

CALCULATOR_URL_SUBSTR = "apps09.revenue.nsw.gov.au/erevenue/calculators/motorsimple.php"

class RevenueCalculatorPage:
    def __init__(self, page: Page):
        self.page = page

    # ---------- helpers ----------
    def _dismiss_any_modals(self):
        # Try the common modal close patterns used on this site (Bootstrap)
        try:
            # Close button inside modal
            self.page.locator(
                "div[role='dialog'].modal.show button:has-text('Close')"
            ).click(timeout=1500)
        except Exception:
            pass
        try:
            # Generic OK
            self.page.locator(
                "div[role='dialog'].modal.show button:has-text('OK')"
            ).click(timeout=1500)
        except Exception:
            pass
        try:
            # '×' dismiss button
            self.page.locator(
                "div[role='dialog'].modal.show button.close, div[role='dialog'].modal.show .btn-close"
            ).click(timeout=1500)
        except Exception:
            pass
        # If a backdrop is still up, press Escape
        try:
            if self.page.locator(".modal-backdrop.show").is_visible(timeout=800):
                self.page.keyboard.press("Escape")
        except Exception:
            pass

    def _accept_cookies_if_present(self):
        # Some NSW sites throw a cookie/consent banner
        for selector in [
            "button:has-text('Accept')",
            "button:has-text('I agree')",
            "button:has-text('Got it')",
        ):
            try:
                self.page.locator(selector).click(timeout=800)
            except Exception:
                pass

    # ---------- page API ----------
    def assert_loaded(self):
        expect(self.page).to_have_url(re.compile(CALCULATOR_URL_SUBSTR))
        expect(
            self.page.get_by_role(
                "heading",
                name=re.compile("Motor vehicle registration duty calculator", re.I),
            )
        ).to_be_visible()

    def select_passenger_yes(self):
        # Clear any overlays before interacting
        self._accept_cookies_if_present()
        self._dismiss_any_modals()

        # Prefer clicking the LABEL that targets the radio. This triggers change handlers cleanly.
        label = self.page.locator("label[for='passenger_Y']")
        input_radio = self.page.locator("input#passenger_Y")

        # Scroll into view then click label; force if an overlay tries to intercept.
        try:
            label.scroll_into_view_if_needed(timeout=2000)
        except Exception:
            pass

        # Sometimes a modal pops up immediately after clicking. Click label with force to bypass transient overlay.
        label.click(timeout=5000, force=True)

        # If the page does a tiny refresh/re-render, wait for stability and ensure checked.
        try:
            expect(input_radio).to_be_checked(timeout=3000)
        except Exception:
            # If not checked yet, try one more time after clearing modals again.
            self._dismiss_any_modals()
            label.click(timeout=3000, force=True)
            expect(input_radio).to_be_checked(timeout=3000)

    def enter_amount(self, amount: int):
        # The field is labelled 'Purchase price or value (whole dollars):'
        # Use label first; if the DOM changes, fall back to id/name heuristics.
        try:
            self.page.get_by_label(
                re.compile(r"Purchase\s+price\s+or\s+value", re.I)
            ).fill(str(amount), timeout=4000)
            return
        except Exception:
            pass

        for sel in [
            "input#amount",
            "input[name='amount']",
            "input[type='text']",
            "input[type='number']",
        ]:
            try:
                self.page.locator(sel).fill(str(amount), timeout=2500)
                return
            except Exception:
                continue
        raise AssertionError("Could not locate the amount input to enter value.")

    def click_calculate_and_capture_popup(self):
        # The site shows a JS alert() OR a Bootstrap modal; handle both.
        # First try the alert() path:
        try:
            with self.page.expect_dialog() as dlg:
                self.page.get_by_role(
                    "button", name=re.compile(r"^\s*Calculate\s*$", re.I)
                ).click()
            dialog = dlg.value
            text = dialog.message
            dialog.accept()
            return text
        except Exception:
            # If no alert, try modal content
            self.page.get_by_role(
                "button", name=re.compile(r"^\s*Calculate\s*$", re.I)
            ).click()
            # Wait for modal to appear
            modal = self.page.locator("div[role='dialog'].modal.show")
            expect(modal).to_be_visible(timeout=4000)
            text = modal.inner_text(timeout=2000)
            # Close modal (OK/Close)
            for btn in ["OK", "Close"]:
                try:
                    modal.get_by_role("button", name=re.compile(btn, re.I)).click(timeout=1500)
                    break
                except Exception:
                    pass
            return text

    @staticmethod
    def expected_duty_for(amount: int, passenger: bool = True) -> int:
        # From Service NSW:
        # $3 per $100 up to $44,999; for passenger vehicles >= 45,000:
        # $1,350 + $5 per $100 for the amount over $45,000 (exemptions excluded).
        if not passenger:
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
