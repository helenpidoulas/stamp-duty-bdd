# GUI Automation Demo – Service NSW Motor Vehicle Stamp Duty (BDD + Playwright)

This demo uses **Python Playwright** with **Behave (BDD)** — 100% open‑source (non‑revenue) tools.

## What it automates
1. Opens the Service NSW **Check motor vehicle stamp duty** page (https://www.service.nsw.gov.au/transaction/check-motor-vehicle-stamp-duty) and clicks **Check online**.  
2. Asserts the **Revenue NSW Motor vehicle registration duty calculator** page is shown.  
3. Selects **Yes** (passenger vehicle), enters an amount, clicks **Calculate**.  
4. Captures the **popup/alert** text and asserts it contains the expected duty amount.

## Explanation of packages used and why:
- **Behave:** this is the business language layer (BDD) framework; this is the given / when / then layer, and maps human-readable steps to Python step definitions.
- **Playwright:** this is the browser automation engine or GUI driver, for Chrome/ Firefix / WebKit driver + API. It replaces Selenium in modern stacks and is what physically clicks the "Check Online" button, enters the value, waits for the popup and captures the dialog.
- **Pytest:** this is the underlying test runner and reporting foundation; Behave doesn't need pytest, but most teams include pytest because CI/CD reporting, fixtures, parallelisation are more mature in pytest. Its good for future integration and reporting. 

## Quick start
```bash
# 1) Create & activate a virtual env (macOS/Linux)
python3 -m venv .venv
source .venv/bin/activate

# 2) Install deps
pip install -r requirements.txt

# 3) Install Playwright browsers
python -m playwright install --with-deps

# 4a) Run in headless mode (default)
behave

# 4b) or run headed for the live demo
HEADED=1 behave

# 5) optional - test a different vehicle amount
AMOUNT=62000 HEADED=1 behave

```

## Notes
- If this fails on step 1, it means Service NSW changed the UI (again).
- That's why the fallback code exists; it will then auto-navigate directly to the Revenue NSW calculator.
- That's intentional test hardening.
- Behave does not treat features/steps/ as a proper package unless you force it to.
- The fix is simple; create two empty files:
features/__init__.py
features/pages/__init__.py


```bash

# Run the following command in terminal
HEADED=1 behave

```


## What you should physically see in the live demo
The browser will:
- open “Check motor vehicle stamp duty” on Service NSW
- click Check online
- land on the Revenue NSW calculator
- pick Yes
- enter amount
- click Calculate
- popup appears — code reads the popup + asserts the duty value

Why use this approach:
- The script is resilient: if the **Check online** button is not present on Service NSW (due to CMS changes),
  it falls back to clicking **Motor vehicle duty – Revenue NSW** and then **Motor vehicle duty calculator**.
- Expected duty is computed from the published formula and matched in the popup text.
- Default amount is `50000`; override with `AMOUNT=62000 behave`.

## Current status (90% done) - 3 November 2025
- Screen recording of tests being executed:
https://github.com/user-attachments/assets/a21713df-67b5-43ed-affa-d8d3090472fc
- Tests are failing after the user selects "Yes" and enters the values in the modal. See below items which I am working on
<img width="1465" height="874" alt="Screenshot 2025-11-03 at 4 23 09 PM" src="https://github.com/user-attachments/assets/d67175f6-6c35-4c02-b931-ea2ac05f7884" />
