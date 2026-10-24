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

        print("URL:", page.url)
        print("TITLE:", page.title())
        print("\nPAGE TEXT:")
        print(page.locator("body").inner_text()[:5000])

        print("\nBUTTONS:")
        for button in page.get_by_role("button").all():
            print(repr(button.inner_text()))

        print("\nLINKS:")
        for link in page.get_by_role("link").all():
            print(repr(link.inner_text()), link.get_attribute("href"))

        page.screenshot(path="dashboard.png", full_page=True)
        print("\nScreenshot saved: dashboard.png")
    finally:
        browser.close()
