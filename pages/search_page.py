# Req 4.1 - Search page

import re
import time
from .base_page import BasePage

# Child class
class SearchPage(BasePage):
    def search_items_by_name_under_price(self, query: str, max_price: float, limit: int = 5):
        """Search valid items and ensure the total basket amount does not exceed the total budget.

        Args:
            budget (float): The total budget allowed.
            items (list): A list of item dictionaries to evaluate.

        Returns:
            list: A list of valid items that fit within the budget.
        """
        # Login to eBay homepage
        self.navigate("https://www.ebay.com")

        # Print to start search
        print(f"Searching for:'{query}' with a maximum price: {max_price}")

        # Find the search field, type the product name
        self.page.fill("input[placeholder='Search for anything']", query)

        # Click the search button
        self.page.click("button[id='gh-search-btn']")

        # Wait for the page to fully load (all results will appear)
        self.page.wait_for_selector("li.s-card--dark-solt-links-blue", timeout=20000)

        # List for storing links to eligible products
        collected_urls = []

        # Page counter (to know which page we are on)
        page_count = 1

        # Loop that runs until we find enough items (limit)
        while len(collected_urls) < limit:
            print(f"\nPage scanner {page_count}...")

            # Fetch all items on the current page
            items = self.page.query_selector_all("li.s-card--dark-solt-links-blue")
            print(f"Found {len(items)} items on the page")

            # To each item on the page
            for item in items:
                # Find the price element
                price_el = item.query_selector("span.s-card__price")
                # Find the link of the element
                link_el = item.query_selector("a.s-card__link")

                # If there is no price or link, skip and print
                if not price_el or not link_el:
                    print("Item without price or link – skipping")
                    continue

                # Read the price text
                price_text = price_el.inner_text().strip()
                print(f"Original price found: '{price_text}'")

                # Extract the number from the text
                match = re.search(r"(\d+(?:\.\d+)?)", price_text)
                # If there is value that not a number
                if not match:
                    print("No number found in price – skipping")
                    continue

                # Convert to decimal number (float)
                price = float(match.group(1))

                # Check if the price is lower than the defined maximum and the currency is Israeli
                if price <= max_price and "ILS" in price_text:
                    # Found the product link
                    link = link_el.get_attribute("href")
                    # If there is a link and it has not yet been collected – add it to the list
                    if link and link not in collected_urls:
                        collected_urls.append(link)
                        print(f"Matching item found: {link} ({price_text})")
                    else:
                        print("Duplicate link - skipping")
                elif price > max_price:
                    print(f"Price: {price} is higher than the maximum: ({max_price}) – skipping")
                elif "$" in price_text:
                    print(f"Item without Israeli currency: ({price_text}) - skipping")

                # If we have already reached the desired number of items – stop
                if len(collected_urls) >= limit:
                    break

            # If we have already reached the desired number of items – stop
            if len(collected_urls) >= limit:
                break

            # Find the "Next Page" button
            next_button = self.page.query_selector("a.pagination__next")

            # If there is another page and it can be navigated to
            if next_button and next_button.get_attribute("href"):
                print("Moving to the next page...")
                next_button.click()
                # Wait for the new page to load before continuing
                self.page.wait_for_selector("li.s-card--dark-solt-links-blue", timeout=20000)
                time.sleep(1)
                page_count += 1
            else:
                # If there is no more page – stop the search
                print("Not enough items founds and no more pages")
                break

        # Print the summary of results
        print(f"\nFound {len(collected_urls)} matching items in total")
        return collected_urls