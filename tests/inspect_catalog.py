from playwright.sync_api import sync_playwright

from assessment_auth import get_assessment_credentials

URL = "https://pzqa.vercel.app/login"
email, password = get_assessment_credentials()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    failures = []

    page.on("pageerror", lambda error: failures.append(str(error)))
    page.on(
        "requestfailed",
        lambda request: failures.append(
            f"Request failed: {request.method} {request.url}"
        ),
    )

    try:
        page.goto(URL, wait_until="domcontentloaded")
        page.locator('input[name="email"]').fill(email)
        page.locator('input[name="password"]').fill(password)
        page.get_by_role("button", name="Sign in").click()

        page.wait_for_url("**/dashboard", timeout=15000)
        page.get_by_text("Loading products…").wait_for(state="hidden", timeout=10000)
    except Exception as error:
        print("Navigation/loading note:", str(error)[:300])
    finally:
        print("\nURL:", page.url)
        print("\nPAGE TEXT:")
        print(page.locator("body").inner_text()[:6000])

        print("\nBUTTONS:")
        for button in page.get_by_role("button").all():
            if button.is_visible():
                print(repr(button.inner_text()))

        print("\nHEADINGS:")
        for heading in page.get_by_role("heading").all():
            if heading.is_visible():
                print(repr(heading.inner_text()))

        print("\nPAGE ERRORS / FAILED REQUESTS:")
        for failure in failures[:20]:
            print(failure)

        page.screenshot(path="catalog.png", full_page=True)
        print("\nScreenshot saved: catalog.png")
        browser.close()
