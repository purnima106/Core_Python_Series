# pyrefly: ignore [missing-import]
from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    context = browser.new_context(
        storage_state="linkedin_session.json"
    )

    page = context.new_page()

    page.goto("https://www.linkedin.com/feed/")

    page.wait_for_timeout(5000)

    print("Loaded LinkedIn feed")

    browser.close()