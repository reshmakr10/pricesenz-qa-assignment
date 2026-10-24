from playwright.sync_api import sync_playwright


def test_browser_launches():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_content("<title>Browser smoke test</title>")
        assert page.title() == "Browser smoke test"
        browser.close()
