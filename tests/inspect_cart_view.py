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

        print("CART AREA:")
        cart = page.get_by_text("Cart", exact=True).first
        print(cart.evaluate("(el) => el.parentElement.outerHTML"))

        print("\nALL INTERACTIVE ELEMENTS:")
        for el in page.locator("button, a, input, [role='button']").all():
            print(el.evaluate("""el => ({
                tag: el.tagName,
                text: el.innerText,
                aria: el.getAttribute('aria-label'),
                title: el.getAttribute('title'),
                href: el.getAttribute('href')
            })"""))

        print("\nPAGE TEXT:")
        print(page.locator("body").inner_text()[-2500:])

        page.screenshot(path="cart_view_before.png", full_page=True)
        print("\nScreenshot saved: cart_view_before.png")

    finally:
        browser.close()
