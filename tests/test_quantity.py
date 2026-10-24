from playwright.sync_api import sync_playwright

URL = "https://pzqa.vercel.app/login"


def test_quantity_can_be_adjusted(assessment_credentials):
    email, password = assessment_credentials
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto(URL, wait_until="domcontentloaded")
            page.locator('input[name="email"]').fill(email)
            page.locator('input[name="password"]').fill(password)
            page.get_by_role("button", name="Sign in").click()
            page.wait_for_url("**/dashboard", timeout=15000)

            keyboard = page.get_by_role("heading", name="Wireless Keyboard").locator(
                "xpath=ancestor::*[.//button][1]"
            )

            keyboard.get_by_role("button", name="Add to cart").click()

            print("After adding:")
            print(keyboard.inner_text())
            print(
                "Cart header:",
                (
                    page.locator("header").inner_text()
                    if page.locator("header").count()
                    else "No header element"
                ),
            )

            keyboard.get_by_role(
                "button", name="Increase Wireless Keyboard quantity"
            ).click()
            print("\nAfter clicking +:")
            print(keyboard.inner_text())

            keyboard.get_by_role(
                "button", name="Decrease Wireless Keyboard quantity"
            ).click()
            print("\nAfter clicking -:")
            print(keyboard.inner_text())

            page.screenshot(path="quantity_test.png", full_page=True)

        finally:
            browser.close()
