from playwright.sync_api import sync_playwright, expect

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

        product = page.get_by_role("heading", name="Wireless Keyboard").locator(
            "xpath=ancestor::*[.//button][1]"
        )

        # Read the actual cart badge from the page.
        print("BEFORE ADD:")
        print(product.inner_text())
        print(page.locator("body").inner_text().splitlines()[:8])

        product.get_by_role("button", name="Add to cart").click()

        print("\nAFTER ONE ADD:")
        print(product.inner_text())
        print(page.locator("body").inner_text().splitlines()[:8])

        page.screenshot(path="reproduce_add_bug.png", full_page=True)

        # Check whether one add incorrectly results in quantity 2.
        expect(product.get_by_text("2", exact=True)).to_be_visible()
        print("\nReproduced: one Add to cart click displays quantity 2.")

    finally:
        browser.close()
