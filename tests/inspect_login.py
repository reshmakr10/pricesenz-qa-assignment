from playwright.sync_api import sync_playwright

URL = "https://pzqa.vercel.app/login"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(URL, wait_until="domcontentloaded")
    page.wait_for_timeout(1500)

    print("URL:", page.url)
    print("TITLE:", page.title())
    print("\nINPUTS:")
    for item in page.locator("input").all():
        print(
            {
                "type": item.get_attribute("type"),
                "name": item.get_attribute("name"),
                "placeholder": item.get_attribute("placeholder"),
                "aria_label": item.get_attribute("aria-label"),
            }
        )

    print("\nBUTTONS:")
    for item in page.locator("button").all():
        print(item.inner_text())

    print("\nLINKS:")
    for item in page.locator("a").all():
        print(item.inner_text(), item.get_attribute("href"))

    page.screenshot(path="login_page.png", full_page=True)
    browser.close()
