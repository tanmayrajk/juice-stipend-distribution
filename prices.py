import json
from scrape import extract_cheapest_price

new_data = {}

with open("airports.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    for country, airports in data.items():
        total_cost = 0
        total_airports = 0
        for airport in airports:
            print("Searching in " + airport)
            try:
                price = extract_cheapest_price(airport, "PVG")
                if (price == 0): continue
                total_airports += 1
                total_cost += price
            except:
                print("Skipping...")
        if total_cost == 0 or total_airports == 0:
             continue
        new_data[country] = total_cost/total_airports

with open("final.json", "w", encoding="utf-8") as json_file:
        json.dump(new_data, json_file, indent=4, ensure_ascii=False)