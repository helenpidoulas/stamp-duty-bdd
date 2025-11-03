import math
import re
from playwright.sync_api import Page, expect

CALCULATOR_URL_SUBSTR = "apps09.revenue.nsw.gov.au/erevenue/calculators/motorsimple.php"

class RevenueCalculatorPage:
    def __init__(self, page: Page):
        self.page = page

    # ---------- helpers ----------
    def _wait_overlays_clear(self, timeout: int = 5000):
        """
        Wait for Bootstrap modal/backdrop overlays to disappear.
        If they linger, try ESC once and wait again briefly.
        """
        overlay = self.page.locator("div[role='dialog'].modal.show, .modal-backdrop.show")
        try:
            expect(overlay).to_be_hidden(timeout=timeout)
        except Exception:
            try:
                self.page.keyboard.press("Escape")
            except Exception:
                pass
            try:
                expect(overlay).to_be_hidden(timeout=2000)
            except Exception:
                # If still visible, carry on; we'll use force clicks.
                pass

    def _accept_cookies_if_present(self):
        # Best-effort: cookie/consent banners vary; ignore failures.
        for sel in (
            "button:has-text('Accept')",
            "button:has-text('I agree')",
            "button:has-text('Got it')",
        ):
            try:
                self.page.locator(sel).click(timeout=800)
            except Exception:
                pass

    # ---------- page API ----------
    def assert_loaded(self):
        # URL contains calculator path and page shows heading
        expect(self.page).to_have_url(re.compile(CALCULATOR_URL_SUBSTR))
        expect(
            self.page.get_by_role(
                "heading",
                name=re.compile("Motor vehicle registration duty calculator", re.I),
            )
        ).to_be_visible()

    def select_passenger_yes(self):
        # Clear any overlays/cookie banners then click the label (robust against re-renders)
        self._accept_cookies_if_present()
        self._wait_overlays_clear()

        label = self.page.locator("label[for='passenger_Y']")
        radio = self.page.locator("#passenger_Y")

        try:
            label.scroll_into_view_if_needed(timeout=2000)
        except Exception:
            pass

        # Use force in case a transient backdrop is intercepting
        label.click(timeout=5000, force=True)

        # After click, the page sometimes re-renders: wait until checked, retry once if needed
        try:
            expect(radio).to_be_checked(timeout=3000)
        except Exception:
            self._wait_overlays_clear(timeout=2000)
            label.click(timeout=3000, force=True)
            expect(radio).to_be_checked(timeout=3000)

    def enter_amount(self, amount: int):
        # Prefer the labelled field; fall back to common id/name
        try:
            self.page.get_by_label(
                re.compile(r"Purchase\s+price\s+or\s+value", re.I)
            ).fill(str(amount), timeout=4000)
            return
        except Exception:
            pass

        for sel in ("input#amount", "input[name='amount']", "input[type='number']", "input[type='text']"):
            try:
                self.page.locator(sel).fill(str(amount), timeout=2500)
                return
            except Exception:
                continue

        raise AssertionError("Could not locate the amount input to enter value.")

    def click_calculate_and_capture_popup(self):
        # The site may use alert() OR a Bootstrap modal; handle both.
        # First try alert():
        try:
            with self.page.expect_dialog() as dlg:
                self.page.get_by_role("button", name=re.compile(r"^\s*Calculate\s*$", re.I)).click()
            dialog = dlg.value
            text = dialog.message
            dialog.accept()
            return text
        except Exception:
            # Fallback to modal result
            self.page.get_by_role("button", name=re.compile(r"^\s*Calculate\s*$", re.I)).click()
            modal = self.page.locator("div[role='dialog'].modal.show")
            expect(modal).to_be_visible(timeout=4000)
            text = modal.inner_text(timeout=2000)
            # Try to close modal gracefully
            for btn in ("OK", "Close"):
                try:
                    modal.get_by_role("button", name=re.compile(btn, re.I)).click(timeout=1500)
                    break
                except Exception:
                    pass
            self._wait_overlays_clear(timeout=2000)
            return text

    @staticmethod
    def expected_duty_for(amount: int, passenger: bool = True) -> int:
        # From Service NSW:
        # $3 per $100 up to $44,999; for passenger vehicles >= 45,000:
        # $1,350 + $5 per $100 for the amount over $45,000 (exemptions excluded).
        import math as _math
        if not passenger:
            units = _math.ceil(amount / 100.0)
            return units * 3
        if amount < 45000:
            units = _math.ceil(amount / 100.0)
            return units * 3
        over = amount - 45000
        units_over = _math.ceil(over / 100.0)
        return 1350 + units_over * 5

    @staticmethod
    def normalize_money_text(s: str) -> str:
        return re.sub(r"[^0-9]", "", s or "")
