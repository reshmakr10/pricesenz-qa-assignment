import os
import re
from playwright.sync_api import sync_playwright, expect

URL = "https://pzqa.vercel.app/login"


def test_catalog_and_cart(assessment_credentials):
    email, password = assessment_credentials
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto(URL, wait_until="domcontentloaded")
            page.locator('input[name="email"]').fill(email)
            page.locator('input[name="password"]').fill(password)
            page.get_by_role("button", name="Sign in").click()

            expect(page).to_have_url(re.compile(r".*/dashboard$"), timeout=15000)

            # Wait for catalog data rather than relying on a fixed delay.
            expect(page.get_by_role("heading", name="Wireless Keyboard")).to_be_visible(
                timeout=15000
            )

            expect(page.get_by_role("heading", name="USB-C Hub")).to_be_visible()

            # Initially, the cart should be empty.
            expect(page.get_by_text("0", exact=True)).to_be_visible()

            # Add one product and verify the cart count.
            keyboard = page.get_by_role("heading", name="Wireless Keyboard").locator(
                "xpath=ancestor::*[.//button][1]"
            )

            keyboard.get_by_role("button", name="Add to cart").click()

            expect(page.get_by_text("1", exact=True)).to_be_visible()

            print("Catalog loaded and cart badge updated.")
            page.screenshot(path="cart_after_add.png", full_page=True)

        finally:
            browser.close()
