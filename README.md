# GUI Automation Demo – Service NSW Motor Vehicle Stamp Duty (BDD + Playwright)

This demo uses **Python Playwright** with **Behave (BDD)** — 100% open‑source (non‑revenue) tools.

## What it automates
1. Opens the Service NSW **Check motor vehicle stamp duty** page and clicks **Check online**.  
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

# 4) Run in headless mode (default)
behave

# or run headed for the live demo
HEADED=1 behave
```

## Notes
- The script is resilient: if the **Check online** button is not present on Service NSW (due to CMS changes),
  it falls back to clicking **Motor vehicle duty – Revenue NSW** and then **Motor vehicle duty calculator**.
- Expected duty is computed from the published formula and matched in the popup text.
- Default amount is **50000**; override with `AMOUNT=62000 behave`.

## GUI Automation Demonstration – Task 2 
Note: Non-Revenue Automation Framework must be used. 

Selecting an automation tool of your choice (BDD integration preferred) perform a live demo of a working automation of the following target Application: 
- Check motor vehicle stamp duty | Service NSW: https://www.service.nsw.gov.au/transaction/check-motor-vehicle-stamp-duty 
- Click the Check Online Button and assert that this subsequent page appears 
- Enter Yes, enter a vehicle amount and click the calculate button 
- Assert the contents of the popup window 
