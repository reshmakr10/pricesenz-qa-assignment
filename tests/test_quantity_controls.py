from playwright.sync_api import sync_playwright


def test_quantity_controls(assessment_credentials):
    email, password = assessment_credentials
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto(
                "https://pzqa.vercel.app/login",
                wait_until="domcontentloaded",
            )
            page.locator('input[name="email"]').fill(email)
            page.locator('input[name="password"]').fill(password)
            page.get_by_role("button", name="Sign in").click()
            page.wait_for_url("**/dashboard", timeout=15000)
            page.get_by_role("heading", name="Wireless Keyboard").wait_for()

            card = page.get_by_role("heading", name="Wireless Keyboard").locator(
                "xpath=ancestor::*[.//button][1]"
            )

            card.get_by_role("button", name="Add to cart").click()
            print("After add:", card.inner_text().splitlines()[-3:])
            print(
                "Badge:",
                page.locator('[data-testid="cart-count"]').inner_text(),
            )

            decrease = card.get_by_role(
                "button", name="Decrease Wireless Keyboard quantity"
            )
            decrease.click()
            print("After decrease:", card.inner_text())
            print(
                "Badge:",
                page.locator('[data-testid="cart-count"]').inner_text(),
            )

            print(
                "Add-to-cart visible again:",
                card.get_by_role("button", name="Add to cart").is_visible(),
            )

        finally:
            browser.close()
