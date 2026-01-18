import re
from playwright.sync_api import Page, expect


def test_basic_navigation(page: Page):
    page.goto("https://playwright.dev/")
    # Use regex to match partial title
    expect(page).to_have_title(re.compile("Playwright"))
