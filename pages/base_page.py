from playwright.sync_api import Page

# Basic class for all the pages
class BasePage:

    def __init__(self, page: Page):
        self.page = page

    # Page navigation according to the URL
    def navigate(self, url: str):
        self.page.goto(url)

    # Screenshot for documentation
    def take_screenshot(self, name: str):
        self.page.screenshot(path=f"..screenshots/{name}.png")