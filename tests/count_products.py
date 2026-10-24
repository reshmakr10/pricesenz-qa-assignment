from playwright.sync_api import sync_playwright

from assessment_auth import get_assessment_credentials

URL = "https://pzqa.vercel.app/login"
email, password = get_assessment_credentials()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    try:
        page.goto(URL, wait_until="domcontentloaded")
        page.locator('input[name="email"]').fill(email)
        page.locator('input[name="password"]').fill(password)
        page.get_by_role("button", name="Sign in").click()
        page.wait_for_url("**/dashboard", timeout=15000)

        page.get_by_role("heading", name="Wireless Keyboard").wait_for(timeout=15000)

        headings = page.locator("h2, h3").all_inner_texts()
        print("Product-like headings:")
        print(headings)
        print("Heading count:", len(headings))
        print("Available-count text:")
        print(page.get_by_text("6 items available", exact=True).count())

        page.screenshot(path="product_count.png", full_page=True)

    finally:
        browser.close()
