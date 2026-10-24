# PriceSenz QA Assessment

## Project Overview

This project contains manual and automated QA testing for the PriceSenz product catalog application. 

**Application:** https://pzqa.vercel.app/login

### Prerequisites

- Ubuntu on WSL (or another supported Linux environment)
- Python 3.10 or newer
- Internet access to install Python packages and the Chromium browser

The project uses Playwright and pytest; their Python dependencies are listed in
`requirements.txt`.

## Objectives

- Validate login and access to the product catalog.
- Verify product listing and cart interactions.
- Test product quantity controls.
- Identify and document reproducible defects.
- Automate repeatable regression checks using Playwright.

## Project Structure

```text
pricesenz-qa/
├── requirements.txt
├── README.MD
├── tests/
│   ├── conftest.py
│   ├── test_browser.py
│   ├── test_catalog.py
│   ├── test_quantity.py
│   ├── test_quantity_controls.py
│   └── ... exploratory scripts
└── screenshots/
```

Do not share or copy your `.venv` directory. Each person should create their
own virtual environment using the steps below. Screenshots and exploratory
scripts are assessment artifacts and are not required to install the tests.


## Environment Setup

### 1. Install Python on Ubuntu/WSL

If Python and the virtual-environment package are not already installed, run:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
```

Check that Python 3.10 or newer is available:

```bash
python3 --version
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies and Chromium

```bash
python -m pip install -r requirements.txt
python -m playwright install --with-deps chromium
```

`--with-deps` installs the system libraries required by Chromium. It may ask
for your Ubuntu password to install them.

### 4. Configure test credentials

Authenticated tests use `VALID_CREDENTIALS` from a local
`tests/credentials.py` file when the environment variables below are not set.
Keep this file private: do not commit it or include it when sharing the project.
For example, the file can define:

```python
VALID_CREDENTIALS = {
    "username": "your-assessment-email",
    "password": "your-assessment-password"
}
```

Alternatively, set the assessment credentials as environment variables. These
take precedence over `tests/credentials.py`:

```bash
export PZQA_EMAIL='your-assessment-email'
export PZQA_PASSWORD='your-assessment-password'
```

Only use credentials you are authorized to use. Do not share passwords or
other secrets with the project.

## Running the Tests

From the project root, run the collected pytest tests:

```bash
python -m pytest -v
```

Without credentials, tests that require login are skipped; the browser-launch
smoke test can still run. To run only the smoke test:

```bash
python -m pytest -v tests/test_browser.py
```

The test suite and authenticated exploratory scripts use the local credentials
file by default, or the environment variables when both are set. If you share
the project, each person needs to provide their own authorized credentials.

The exploratory scripts in `tests/` can be run individually from the project
root. For example:

```bash
python tests/check_all_products.py
```

## Test Coverage and Findings

### Confirmed defect: Incorrect initial product quantity

**Module:** Product Catalog / Cart

**Expected:** Clicking **Add to cart** once should set the product quantity to 1.

**Actual:** A single click sets the quantity to 2.

**Affected products verified:**
- Wireless Keyboard
- USB-C Hub
- Noise-Canceling Headphones
- 27" Monitor
- Ergonomic Mouse

**Reproducibility:** Observed on all five visible products during testing.

**Suggested severity:** Medium, subject to the assessment's severity guidelines.

**Evidence:** `verify_cart.png` and the output of `check_all_products.py`.

### Potential issue: Product count mismatch

The catalog displays “6 items available,” while five product cards were visible after loading.

This remains an **unverified observation** until it is confirmed whether a sixth product should be present.

## Evidence and Reporting

For each reported defect, document:
- Title and affected module
- Preconditions
- Steps to reproduce
- Expected result
- Actual result
- Severity and impact
- Screenshot or test output

Only report behaviour that has been reproduced or otherwise verified. Do not treat untested checkout or payment flows as tested.

## Notes

- Keep assessment credentials out of source files and Git commits.
- Screenshots and test outputs should be retained as supporting evidence.
- Automated checks help reproduce defects but do not replace exploratory testing.
- The test results reflect the application behaviour observed during this assessment.

## Author

For QA Assessment Project — PriceSenz, By Reshma Krishnan R

**Focus:** Functional testing, regression testing, defect reporting, and Playwright automation.

## NB

Only a few test cases are provided for each module for assessment purposes, as discussed previously.
