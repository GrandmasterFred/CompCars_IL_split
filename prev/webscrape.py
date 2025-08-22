"""
this file uses the extracted vehicle make and model, and attempts to scrape the web to find their release date 
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import json
from itertools import groupby

# getting all the cars data 
from sp_functions import save_dict_to_json, load_dict_from_json

TARGET_SAVE = r'compcars_summary.json'

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/115.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",  # force English results
}

def search_release_date(car_name):
    """Search Bing and scrape snippets for release date info."""

    

    query = f"{car_name} vehicle car first release date"
    # url = f"https://www.bing.com/search?q={requests.utils.quote(query)}&setlang=en&cc=us"
    # url = f"https://duckduckgo.com/html/?q={requests.utils.quote(query + '')}"
    url = f"https://www.bing.com/search?q={requests.utils.quote(query)}&setlang=en&cc=us"
    
    resp = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(resp.text, "lxml")

    snippets = [s.get_text(" ") for s in soup.select("li.b_algo p")]

    # Try to extract month + year
    for snip in snippets:
        match = re.search(
            r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}",
            snip
        )
        if match:
            return match.group(0)

        # fallback: just a year
        match_year = re.search(r"\b(19|20)\d{2}\b", snip)
        if match_year:
            return match_year.group(0)

    return None


def main():
    
    dict = load_dict_from_json(filename=TARGET_SAVE)

    cars = []
    for keys, values in dict.items():
        # we form the list needed for the scraper 
        temp_car_name = f"{values['make']} {values['model']}"
        cars.append(str(temp_car_name))

    results = {}
    for car in cars:
        print(f"Searching: {car}")
        date = search_release_date(car)
        results[car] = date if date else "Not found"
        time.sleep(2)  # polite delay to avoid blocking

    # Save to JSON
    with open("car_release_dates5.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print("Done! Results saved to car_release_dates2.json")


if __name__ == "__main__":
    main()
