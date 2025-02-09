from playwright.sync_api import sync_playwright
from tfs import get_b64_encoded_tfs
import re

def extract_cheapest_price(dep_airport, arr_airport):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        base_url = "https://www.google.com/travel/flights/search"
        params = "?tfs=" + get_b64_encoded_tfs(dep_airport, arr_airport) + "&hl=en&curr=usd"
        full_url = base_url + params
        page.goto(full_url)
        page.wait_for_load_state('networkidle')
        cheapest_card_text = page.wait_for_selector("div#M7sBEb", timeout=2000).inner_text()
        browser.close()

        match = re.search(r"\$\d{1,3}(?:,\d{3})*", cheapest_card_text)
        
        if match:
            return int(match.group().removeprefix("$").replace(",", ""))
        else:
            return 0