# features/environment.py
import os
from playwright.sync_api import sync_playwright
from features.pages.service_nsw_page import ServiceNSWPage
from features.pages.revenue_calculator_page import RevenueCalculatorPage

HEADED = os.environ.get("HEADED", "0").lower() in ("1", "true", "yes")
AMOUNT = int(os.environ.get("AMOUNT", "50000"))

print("[behave] environment.py LOADED")  # canary

def before_all(context):
    print("[behave] before_all")
    context._playwright = None
    context.browser = None

def after_all(context):
    print("[behave] after_all")
    if context.browser:
        context.browser.close()
    if context._playwright:
        context._playwright.stop()

def before_scenario(context, scenario):
    print(f"[behave] before_scenario tags={scenario.effective_tags}")
    context.AMOUNT = AMOUNT
    # IMPORTANT: tags come WITHOUT '@'
    if "gui" in scenario.effective_tags:
        print("[behave] launching browser for @gui")
        context._playwright = sync_playwright().start()
        context.browser = context._playwright.chromium.launch(headless=not HEADED)
        context.page = context.browser.new_page()
        context.service = ServiceNSWPage(context.page)
        context.rev = RevenueCalculatorPage(context.page)

def after_scenario(context, scenario):
    if "gui" in scenario.effective_tags and getattr(context, "page", None):
        print("[behave] closing page for @gui")
        context.page.close()
