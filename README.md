# GUI Automation Demo – Service NSW Motor Vehicle Stamp Duty GUI & OpenLibrary API - Behave BDD

Open-source stack:
- Behave (BDD)
- Playwright (GUI only)
- Requests (API)
- Pytest (reporting compatibility)

## What it automates

# GUI - Service NSW Motor Vehicle Stamp Duty
1. Opens the Service NSW **Check motor vehicle stamp duty** page
https://www.service.nsw.gov.au/transaction/check-motor-vehicle-stamp-duty and clicks **Check online**.  
2. Asserts the **Revenue NSW Motor vehicle registration duty calculator** page is shown.  
3. Selects **Yes** (passenger vehicle), enters an amount, clicks **Calculate**.  
4. Captures the **popup / alert / modal** text and asserts it contains the expected duty amount.

# API - OpenLibrary Author
1. Calls https://openlibrary.org/authors/OL1A.json
2. Asserts **personal_name == "Sachi Rautroy"**
3. Asserts **alternate_names** contain **Yugashrashta Sachi Routray** (handles U+202F narrow no-break spaces)

## Explanation of packages used and why
- **Behave:** BDD layer (given / when / then) layer that maps human-readable steps to Python step definitions.
- **Playwright:** this is the modern browser automation engine or GUI driver, for Chrome/ Firefix / WebKit driver. It replaces Selenium in modern stacks. Playwright is used for the GUI demo to click, enter values and read popups.
- **Requests:** Lightweight HTTP client used for the API demo.
- **Pytest:** Not strictly required by Behave, but kept for better CI/CD reporting and future parallelisation / fixtures are more mature in pytest. Its good for future integration and reporting. 

## Quick start

```bash

# Create & activate a virtual env (macOS/Linux)
python3 -m venv .venv
source .venv/bin/activate

# Install deps
pip install -r requirements.txt

```

## Run GUI demo (Service NSW)

```bash

# Install Playwright browsers (GUI only)
python -m playwright install --with-deps

# Run GUI scenarios (headed for the GUI live demo)
HEADED=1 behave --tags=@gui

# Optional - test a different vehicle amount
AMOUNT=62000 HEADED=1 behave --tags=@gui

```

## Run API demo (OpenLibrary)

```bash

# Run for the API only
behave --tags=@api

```

## Run everything

```bash

# Everything
# Headless
behave

#Headed
HEADED=1 behave

```

## Notes

- If this fails on step 1, it means Service NSW changed the UI
- The GUI test is **hardened**: if the Service NSW page layout changes, it can fall back to direct navigation within the Revenue NSW before asserting.
- Duty is computed from the published forumula and compared against the popup / modal text (formatting-tolerant)
- Default amount is **50000**; override with **AMOUNT=62000**
- **Tags & hooks**: features/environment.py boots Playwright **only** for scenarios tagged **@gui**. API scenarios run with no browser. 
- Behave stops iomports: if Python treats **features/** as non-package in your setup, ensure these files exist (should be already present in this repo):
features/__init__.py
features/pages/__init__.py



## What you should physically see in the GUI live demo

- Opens **Check motor vehicle stamp duty** on Service NSW
- Clicks on **Check online**
- Lands on the **Revenue NSW calculator**
- Picks **Yes**
- Enter amount
- Clicks **Calculate**
- Popup / modal appears -> code reads it and asserts the duty value

## Evidence / Status
- GUI screen recording: https://github.com/user-attachments/assets/8fab3b41-a161-4962-aea9-8352f3ddc21c
- API screen recording: https://github.com/user-attachments/assets/74971f06-a6dc-4913-bc87-4a2c30370d1a
 
## Current: 
- GUI and API paths are integrated in one suite with @gui / @api tags.
- If a GUI step fails after selecting **Yes**, it's typically due to transient overlays; the page object includes logic to dismiss backdrops / modals and re-assert 


## Why use this approach:
- The script is resilient: if the **Check online** button is not present on Service NSW (due to CMS changes),
  it falls back to clicking **Motor vehicle duty – Revenue NSW** and then **Motor vehicle duty calculator**.
- Expected duty is computed from the published formula and matched in the popup text.
- Default amount is `50000`; override with `AMOUNT=62000 behave`.
