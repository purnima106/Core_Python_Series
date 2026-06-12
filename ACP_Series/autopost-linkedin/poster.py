# pyrefly: ignore [missing-import]
from playwright.sync_api import sync_playwright


def post_to_linkedin(post_text):

    try:

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=False
            )

            context = browser.new_context(
                storage_state="linkedin_session.json"
            )

            page = context.new_page()

            page.goto(
                "https://www.linkedin.com/feed/"
            )

            page.wait_for_timeout(5000)

            page.locator(
                '[aria-label="Start a post"]'
            ).click()

            page.wait_for_timeout(3000)

            page.keyboard.type(
                post_text,
                delay=20
            )

            page.wait_for_timeout(2000)

            page.get_by_role(
                "button",
                name="Post",
                exact=True
            ).click()
            # print("Ready to click Post")

            # input("Press Enter to publish...")

            page.wait_for_timeout(5000)

            browser.close()

            return True

    except Exception as e:

        print(e)

        return False

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
