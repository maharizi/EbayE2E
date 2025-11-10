#Requirement 5 - Full E2E scenario
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pytest
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.search_page import SearchPage
from pages.item_page import ItemPage
from pages.cart_page import CartPage
from utils.helpers import load_config

@pytest.fixture(scope="session")
def config():
    """Load test configuration from JSON file."""
    return load_config()

@pytest.fixture(scope="session")
def browser_page():
    """Launch the browser and provide a page object."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        yield page
        browser.close()

def test_ebay_e2e(browser_page, config):
    """Full end-to-end (E2E) scenario on the eBay website.

    This test performs a complete E2E flow including:
        1. Login as a guest user.
        2. Search for items by maximum price.
        3. Add the found items to the shopping cart.
        4. Verify that the total cart amount does not exceed a predefined budget.

    Args:
        None

    Returns:
        None

    Raises:
        AssertionError: If the total cart amount exceeds the budget.
        Exception: If there are issues loading pages, selecting items, or clicking buttons.
    """

    # Step 1 - Fake Login
    login = LoginPage(browser_page)
    login.login_as_guest()

    # Step 2 - Search for items
    search = SearchPage(browser_page)
    urls = search.search_items_by_name_under_price(config["query"], config["max_price"], config["limit"])
    # Step 3 - Add to Cart
    item = ItemPage(browser_page)
    item.add_items_to_cart(urls)

    # Step 4 - Verify the cart total price
    cart = CartPage(browser_page)
    cart.assert_cart_total_not_exceeds(config["budget_per_item"], len(urls))