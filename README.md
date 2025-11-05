# GUI + API Automation Demo – Behave BDD (Playwright + Requests)

Open-source automation stack:
- Behave (BDD)
- Playwright (GUI only)
- Requests (API only)
- Pytest (reporting compatibility for future CI/CD integration)

---

## What it automates

### GUI — Service NSW Motor Vehicle Stamp Duty
1. Opens the Service NSW **Check motor vehicle stamp duty** page:  
   https://www.service.nsw.gov.au/transaction/check-motor-vehicle-stamp-duty  
2. Clicks **Check online**
3. Asserts the **Revenue NSW Motor vehicle registration duty calculator** page is shown
4. Selects **Yes** (passenger vehicle), enters an amount, clicks **Calculate**
5. Captures the modal / popup and asserts the correct duty calculation

### API — OpenLibrary Author
1. Calls https://openlibrary.org/authors/OL1A.json
2. Asserts `"personal_name" == "Sachi Rautroy"`
3. Asserts `"alternate_names"` contains `"Yugashrashta Sachi Routray"`

---

## Why these tools

| Tool | Purpose |
|------|---------|
| Behave | BDD syntax (Given / When / Then) written in **Gherkin** stored in `.feature` files |
| Playwright | Browser automation engine (Chromium / Firefox / WebKit) — replaces Selenium |
| Requests | Clean, lightweight REST client |
| Pytest | Reporting + future CI parallelisation |

***Gherkin is NOT Python***  
- feature files are written in plain English (Given / When / Then)  
- but the step definitions are Python.

---

## Quick Start (Local Machine)

```bash
# Create & activate venv (macOS/Linux)
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Run GUI demo (Service NSW)

```bash
# Install Playwright browsers
python -m playwright install --with-deps

# Run GUI scenario headed
HEADED=1 behave --tags=@gui

# Test a different amount:
AMOUNT=62000 HEADED=1 behave --tags=@gui
```

## Run API demo (OpenLibrary)

```bash
behave --tags=@api
```

## Run entire suite

```bash
# headless
behave

# headed for GUI + API together
HEADED=1 behave
```

## Behaviour Notes
- If the Service NSW UI changes (common), the GUI test includes fallback navigation to Revenue NSW directly.
- Amount defaults to 50000
- Override via AMOUNT=xxxx
- Tags matter:
    - @gui triggers browser setup (Playwright)
    - @api does not

Also ensure these files exist (they do in this repo):

```bash
features/__init__.py
features/pages/__init__.py
```

This forces Python to treat steps / pages as importable modules.

## What you physically see in the GUI demo
- Page opened
- Check Online clicked
- Calcaulator loaded
- "Yes" selected
- Value entered
- Calculate clicked
- Modal popup -> assertiopn performed

## Evidence / Videos
- GUI execution:
https://github.com/user-attachments/assets/8fab3b41-a161-4962-aea9-8352f3ddc21c (TBC)
- API execution:
https://github.com/user-attachments/assets/74971f06-a6dc-4913-bc87-4a2c30370d1a (TBC)

## CI / Github Actions

You can run the exact same suite in CI.

Create the following file in the root of your repo:
```bash

# File location
.github/workflows/ci.yml

#File contents
name: CI

on:
  push:
  pull_request:

jobs:
  gui:
    name: GUI – NSW Stamp Duty
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install --upgrade pip
      - run: pip install -r requirements.txt
      - run: python -m playwright install --with-deps
      - run: HEADED=0 behave --tags=@gui

  api:
    name: API – OpenLibrary
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install --upgrade pip
      - run: pip install -r requirements.txt
      - run: behave --tags=@api

# Note: Junit and screenshots will be fixed - WIP

```

| Jobs | Purpose |
|------|---------|
| GUI | Browser automation |
| API | Pure HTTP tests - no browser |

## Current Status (4 November 2025)
- GUI + API tests both pass locally and in CI
- Tagged test architecture allows selective execution
- We can now add screenshots **to the slide deck text** to match the sequence output.
