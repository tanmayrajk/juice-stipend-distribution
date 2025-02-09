from playwright.sync_api import sync_playwright
from tfs import get_b64_encoded_tfs
import re

def extract_cheapest_price(dep_airport, arr_airport):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 720}
        )
        page = context.new_page()
        page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })
        base_url = "https://www.google.com/travel/flights/search"
        params = "?tfs=" + get_b64_encoded_tfs(dep_airport, arr_airport) + "&hl=en&curr=usd&consent=YES"
        full_url = base_url + params
        page.goto(full_url)
        page.wait_for_load_state('networkidle')
        page.screenshot(path="full_page.png", full_page=True)
        # click the accept cookie button hopefully
        try:
            page.wait_for_selector("text=Accept all", timeout=500).click()
        except:
            pass
        cheapest_card = page.wait_for_selector("text=Cheapest", timeout=500)
        cheapest_card_text = cheapest_card.inner_text()
        browser.close()

        match = re.search(r"\$\d{1,3}(?:,\d{3})*", cheapest_card_text)
        print(match.group())
        
        if match:
            return int(match.group().removeprefix("$").replace(",", ""))
        else:
            return 0