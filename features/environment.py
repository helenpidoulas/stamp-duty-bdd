import os
from playwright.sync_api import sync_playwright
from features.pages.service_nsw_page import ServiceNSWPage
from features.pages.revenue_calculator_page import RevenueCalculatorPage

print("[behave] environment.py loaded")

HEADED = os.environ.get("HEADED", "0").lower() in ("1", "true", "yes")
AMOUNT = int(os.environ.get("AMOUNT", "50000"))

def before_all(context):
    print("[behave] before_all")
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(headless=not HEADED)

def after_all(context):
    print("[behave] after_all")
    context.browser.close()
    context.playwright.stop()

def before_scenario(context, scenario):
    print(f"[behave] before_scenario: {scenario.name}")
    context.page = context.browser.new_page()
    context.service = ServiceNSWPage(context.page)
    context.rev = RevenueCalculatorPage(context.page)
    context.AMOUNT = AMOUNT

def after_scenario(context, scenario):
    print(f"[behave] after_scenario: {scenario.name}")
    context.page.close()
