import os
import re
from behave import given, when, then
from playwright.sync_api import sync_playwright, Browser, Page, expect

from features.pages.service_nsw_page import ServiceNSWPage
from features.pages.revenue_calculator_page import RevenueCalculatorPage

# Adjust sys.path to ensure imports work when run via behave
# This allows running `behave` from the project root      
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


AMOUNT = int(os.environ.get("AMOUNT", "50000"))
HEADED = os.environ.get("HEADED", "0") in ("1", "true", "True", "yes", "YES")

def before_all(context):
    context.playwright = sync_playwright().start()
    context.browser = context.playwright.chromium.launch(headless=not HEADED, args=[])

def after_all(context):
    context.browser.close()
    context.playwright.stop()

def before_scenario(context, scenario):
    context.page = context.browser.new_page()
    context.service = ServiceNSWPage(context.page)
    context.rev = RevenueCalculatorPage(context.page)

def after_scenario(context, scenario):
    context.page.close()

@given('I open the Service NSW "Check motor vehicle stamp duty" page')
def step_open_service(context):
    context.service.open()

@when("I click the Check online button")
def step_click_check_online(context):
    context.service.click_check_online()

@then("I should land on the Revenue NSW motor vehicle duty calculator")
def step_assert_rev_loaded(context):
    context.rev.assert_loaded()

@when('I select "Yes" for passenger vehicle')
def step_select_yes(context):
    context.rev.select_passenger_yes()

@when("I enter the vehicle amount")
def step_enter_amount(context):
    context.rev.enter_amount(AMOUNT)

@when("I click Calculate")
def step_click_calc(context):
    # handled in next step (we capture dialog in the assert step)
    pass

@then("a popup should appear with the correct duty")
def step_assert_popup(context):
    text = context.rev.click_calculate_and_capture_popup()
    expected = context.rev.expected_duty_for(AMOUNT, passenger=True)
    # Compare by digits only to ignore formatting like $ and commas
    digits_in_text = context.rev.normalize_money_text(text)
    assert str(expected) in digits_in_text, f"Expected duty {expected} not found in popup text: {text!r}"
