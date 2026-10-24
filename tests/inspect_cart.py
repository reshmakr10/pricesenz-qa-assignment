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

        # Add one product.
        card = page.get_by_role("heading", name="Wireless Keyboard").locator(
            "xpath=ancestor::*[.//button][1]"
        )
        card.get_by_role("button", name="Add to cart").click()

        # Inspect the cart control.
        print("CART-RELATED BUTTONS:")
        for button in page.get_by_role("button").all():
            if button.is_visible():
                print(repr(button.inner_text()), button.get_attribute("aria-label"))

        print("\nPAGE TEXT BEFORE OPENING CART:")
        print(page.locator("body").inner_text()[:3000])

        page.screenshot(path="cart_inspection.png", full_page=True)

    finally:
        browser.close()
