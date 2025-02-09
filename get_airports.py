import requests
from bs4 import BeautifulSoup
import json

url = "https://en.wikipedia.org/wiki/List_of_international_airports_by_country"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    data = {}
    divs = soup.find_all("div", class_="mw-heading mw-heading4")

    for div in divs:
        heading = div.find("h4").get_text(strip=True)
        table = div.find_next_sibling("table", class_="wikitable")
        third_td_values = []

        if table:
            tbody = table.find("tbody")
            for tr in tbody.find_all("tr"):
                tds = tr.find_all("td")
                if len(tds) >= 3:
                    third_td_text = tds[2].get_text(strip=True)
                    third_td_values.append(third_td_text)

        if third_td_values:
            data[heading] = third_td_values

    with open("output.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

    print("Data has been saved to output.json")

else:
    print("Failed to fetch the page. Status code:", response.status_code)
