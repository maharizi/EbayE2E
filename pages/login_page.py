# Req 4 - Login page for identification

from .base_page import BasePage

# Child class
class LoginPage(BasePage):

    def login_as_guest(self):
        print("Login as a guest to the eBay website")