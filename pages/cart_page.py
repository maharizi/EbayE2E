# Req 4.3 - Cart page

from .base_page import BasePage
import re

# Child class
class CartPage(BasePage):

    def assert_cart_total_not_exceeds(self, budget_per_item: float, items_count: int):
        """Asserts that the total cart value does not exceed the allowed budget.

        Args:
            budget_per_item (float): The maximum allowed price per item.
            items_count (int): The number of items expected in the cart.

        Raises:
            AssertionError: If the total cart amount exceeds the allowed budget.
        """
        # Navigate to the cart page
        self.navigate("https://cart.ebay.com")

        # Wait for the total amount to appear
        self.page.wait_for_selector(".val-col")

        # Read the basket amount (text)
        total_text = self.page.inner_text(".val-col")

        # Extract the number from the text
        total_value = float(re.findall(r"[0-9,.]+", total_text)[0].replace(",", ""))

        # Calculate the total budget threshold
        threshold = budget_per_item * items_count

        print(f"Cart total: {total_value} vs.  {threshold}")

        # We will perform the verification
        assert total_value <= threshold, f"Cart total: {total_value} Exceeded the budget: {threshold}"

        # Screenshot of price total
        self.take_screenshot("cart_total")
        print("The cart total is correct and does not exceed the budget")