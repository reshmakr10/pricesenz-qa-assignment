from playwright.sync_api import sync_playwright

from assessment_auth import get_assessment_credentials

URL = "https://pzqa.vercel.app/login"
email, password = get_assessment_credentials()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    browser_context = browser.new_context(viewport={"width": 1440, "height": 900})
    page = browser_context.new_page()

    try:
        page.goto(URL, wait_until="domcontentloaded")
        page.locator('input[name="email"]').fill(email)
        page.locator('input[name="password"]').fill(password)
        page.get_by_role("button", name="Sign in").click()
        page.wait_for_url("**/dashboard", timeout=15000)
        page.get_by_role("heading", name="Wireless Keyboard").wait_for()

        print("PRODUCT HEADINGS:")
        for heading in page.locator("h2, h3, h4").all():
            if heading.is_visible():
                print("-", heading.inner_text())

        print(
            "\nVISIBLE ADD-TO-CART BUTTONS:",
            page.get_by_role("button", name="Add to cart").count(),
        )

        print("\nPAGE DIMENSIONS:")
        print(page.evaluate("""() => ({
            scrollHeight: document.documentElement.scrollHeight,
            clientHeight: document.documentElement.clientHeight,
            scrollWidth: document.documentElement.scrollWidth,
            clientWidth: document.documentElement.clientWidth
        })"""))

        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(500)
        page.screenshot(path="product_count_bottom.png", full_page=True)

        print("\nBOTTOM OF PAGE:")
        print(page.locator("body").inner_text()[-1500:])

    finally:
        browser.close()
