from playwright.sync_api import Page, expect

SERVICE_NSW_URL = "https://www.service.nsw.gov.au/transaction/check-motor-vehicle-stamp-duty"

class ServiceNSWPage:
    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto(SERVICE_NSW_URL, wait_until="domcontentloaded")

    def click_check_online(self):
        # Primary path: a visible 'Check online' button/link on the page
        locators = [
            # Button with exact name
            self.page.get_by_role("link", name="Check online", exact=True),
            self.page.get_by_role("button", name="Check online", exact=True),
            # Fallbacks (some Service NSW pages render a single 'Links' list instead)
            self.page.get_by_text("Check online", exact=True),
        ]
        for loc in locators:
            try:
                if loc.is_visible():
                    loc.click()
                    return
            except Exception:
                pass

        # If we didn't find it (content sometimes changes), follow the alternate path to Revenue NSW
        try:
            self.page.get_by_role("link", name="Motor vehicle duty – Revenue NSW").click()
            # On Revenue NSW page, click the calculator link
            self.page.get_by_role("link", name="Motor vehicle duty calculator").click()
        except Exception:
            # Absolute fallback: navigate directly to the calculator
            self.page.goto("https://www.apps09.revenue.nsw.gov.au/erevenue/calculators/motorsimple.php")
