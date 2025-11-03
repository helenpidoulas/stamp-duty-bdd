import os
import re
import sys
import pathlib
from behave import given, when, then
from playwright.sync_api import expect

from features.pages.service_nsw_page import ServiceNSWPage
from features.pages.revenue_calculator_page import RevenueCalculatorPage

# ensure root path is import-safe (behave loads step modules via exec)
ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

AMOUNT = int(os.environ.get("AMOUNT", "50000"))


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
    amount = getattr(context, "AMOUNT", AMOUNT)
    context.rev.enter_amount(amount)


@when("I click Calculate")
def step_click_calc(context):
    # calculation / popup handled in the next step
    pass


@then("a popup should appear with the correct duty")
def step_assert_popup(context):
    amount = getattr(context, "AMOUNT", AMOUNT)
    text = context.rev.click_calculate_and_capture_popup()
    expected = context.rev.expected_duty_for(amount, passenger=True)

    # evidence line — for demo / logs / CI artefacts
    print(f"[duty] expected={expected} | popup_text={text}")

    digits_in_text = context.rev.normalize_money_text(text)
    assert str(expected) in digits_in_text, f"Expected duty {expected} not found in popup text: {text!r}"
