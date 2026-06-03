# pyrefly: ignore [missing-import]
from playwright.sync_api import sync_playwright


def post_to_linkedin(post_text):

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False
        )

        context = browser.new_context(
            storage_state="linkedin_session.json"
        )

        page = context.new_page()

        page.goto("https://www.linkedin.com/feed/")

        page.wait_for_timeout(5000)

        print("Opening post dialog...")

        page.locator(
            '[aria-label="Start a post"]'
        ).click()

        page.wait_for_timeout(3000)

        page.keyboard.type(
            post_text,
            delay=20
        )

        print("Text inserted successfully")

        input("Verify the content and press Enter...")

        browser.close()


if __name__ == "__main__":
    post_to_linkedin(
        """
Testing LinkedIn automation.

This post was inserted automatically using Playwright.

#AI #DevOps
"""
    )

# from linkedin_api import Linkedin
# import os
# from dotenv import load_dotenv

# load_dotenv()

# def get_client():

#     email = os.getenv("LINKEDIN_EMAIL")
#     password = os.getenv("LINKEDIN_PASSWORD")

#     return Linkedin(email, password)
