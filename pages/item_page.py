# Req 4.2 - Search page

from .base_page import BasePage
import random, time

# Child class
class ItemPage(BasePage):
    def add_items_to_cart(self, urls: list[str]) -> object:
        """Adds a list of items to the shopping cart.

        Args:
            urls (list[str]): A list of product page URLs to add to the cart.

        Returns:
            None.
        """

        # For each item add to the cart
        for idx, url in enumerate(urls, start=1):
            print(f"Opens item: {idx}: {url}")
            self.navigate(url)

            # Wait for the item page to load
            self.page.wait_for_selector(".right-summary-panel-container", timeout=20000)
            print("️The right part of the page is loading")

            # In case there is size/color (Mandatory fields) we entered random values
            try:
                dropdowns = self.page.locator(".right-summary-panel-container .listbox-button")
                count = dropdowns.count()
                print(f"️Number of listboxes: {count}")

                for i in range(count):
                    # Find the button and click to open the listbox
                    dd = dropdowns.nth(i)
                    btn = dd.locator(".listbox-button__control")
                    btn.click()

                    # Wait and find the DIV that contains the values
                    options_div  = dd.locator(".listbox__options")
                    options_div.first.wait_for(state="visible", timeout=5000)
                    options = options_div.locator(".listbox__option")

                    # Keep only available values and skip the first value which is the default
                    available_options = []
                    all_values = options.all_inner_texts()
                    print(f"Options: {all_values}")
                    for j in range(1, len(all_values)):
                        opt = options.nth(j)
                        if opt.get_attribute("aria-disabled") != "true":
                            available_options.append((j, all_values[j]))

                    if not available_options:
                        print("No options available in this listbox")
                        continue

                    # Choose randomly value from the valid values
                    chosen_index, chosen_text = random.choice(available_options)
                    options.nth(chosen_index).click()
                    print(f"Value chosen: {chosen_text}")

            # In case there is no Mandatory fields
            except Exception:
                pass

            # Click Add to cart button
            try:
                btn = self.page.locator("a#atcBtn_btn_1")
                btn.click()
                print("🛍️ Added to cart successfully")
            except Exception:
                print("⚠️ Cannot add item to cart - item probably unavailable")
                continue

            # Save a screenshot of each item
            time.sleep(0.5)
            self.take_screenshot(f"item_{idx}")
            time.sleep(1)