from playwright.sync_api import sync_playwright

from assessment_auth import get_assessment_credentials

email, password = get_assessment_credentials()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    try:
        page.goto("https://pzqa.vercel.app/login", wait_until="domcontentloaded")
        page.locator('input[name="email"]').fill(email)
        page.locator('input[name="password"]').fill(password)
        page.get_by_role("button", name="Sign in").click()
        page.wait_for_url("**/dashboard", timeout=15000)
        page.get_by_role("heading", name="Wireless Keyboard").wait_for()

        names = [
            "USB-C Hub",
            "Noise-Canceling Headphones",
            '27" Monitor',
            "Ergonomic Mouse",
        ]

        for name in names:
            heading = page.get_by_role("heading", name=name, exact=True)
            card = heading.locator("xpath=ancestor::*[.//button][1]")
            card.get_by_role("button", name="Add to cart").click()
            text = card.inner_text()
            quantity = text.splitlines()[-2]
            print(f"{name}: quantity after one click = {quantity}")

    finally:
        browser.close()
