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

        page.get_by_role("heading", name="Wireless Keyboard").wait_for(timeout=15000)

        print("CATALOG LOADED")
        print("Product cards:", page.locator('[data-testid="product-card"]').count())

        card = page.get_by_role("heading", name="Wireless Keyboard").locator(
            "xpath=ancestor::*[.//button][1]"
        )

        print("\nBEFORE ADD:")
        print(card.inner_text())
        print("Cart badge:", page.locator('[data-testid="cart-count"]').inner_text())

        card.get_by_role("button", name="Add to cart").click()
        page.wait_for_timeout(300)

        print("\nAFTER ONE CLICK:")
        print(card.inner_text())
        print("Cart badge:", page.locator('[data-testid="cart-count"]').inner_text())
        print("Page text:")
        print(page.locator("body").inner_text())

        page.screenshot(path="verify_cart.png", full_page=True)
        print("\nScreenshot saved: verify_cart.png")

    finally:
        browser.close()
