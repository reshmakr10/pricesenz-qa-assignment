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
        page.wait_for_timeout(2000)

        print("URL after login:", page.url)
        print("Page title:", page.title())
        print("Visible page text:")
        print(page.locator("body").inner_text()[:2500])

        page.screenshot(path="after_login.png", full_page=True)
        print("Screenshot saved: after_login.png")
    finally:
        browser.close()
