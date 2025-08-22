"""
this file uses the extracted vehicle make and model, and attempts to scrape the web to find their release date 


this one relies on wikipedia instead of bing 
"""

import requests
from bs4 import BeautifulSoup
import re
import json
import time
from itertools import groupby

# getting all the cars data 
from sp_functions import save_dict_to_json, load_dict_from_json

TARGET_SAVE = r'compcars_summary.json'

# for some of the texts in compcars wherein it uses an abbreveation of a full name 
REMAP_SEARCH_KEYWORDS = {
    "Benz": "Mercedes Benz",
    "Zhonghua" : "Brilliance",
    "Huatai": "Hawatai",
    "Chevy" : "Chevrolet"
}

# these are most likely domestic china vehicles 
WIKI_UNLOGGED_VEHICLES = [
    "Yiqi",
    "Guangqichuanqi",
    "FIAT"
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/115.0 Safari/537.36"
    )
}

def extract_date_from_text(text):
    """Find Month+Year or just Year in text."""
    match = re.search(
        r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}",
        text,
    )
    if match:
        return match.group(0)

    match_year = re.search(r"\b(19|20)\d{2}\b", text)
    if match_year:
        return match_year.group(0)

    return None

def scrape_wikipedia(car_name):
    """Scrape Wikipedia infobox and paragraphs for release/production years."""
    temp = wikipedia_search_with_snippet(car_name)
    try: 
        wiki_url = temp[0]['url']
        snippet = temp[0]['snippet']
    except Exception as e:
        wiki_url = None     # this is for if there is no valid url that is found 
        snippet = None
    # wiki_url = get_wikipedia_url(car_name)
    if not wiki_url:
        return None, None, None

    resp = requests.get(wiki_url, headers=HEADERS)
    soup = BeautifulSoup(resp.text, "lxml")

    # Try infobox first
    infobox_rows = soup.select("table.infobox tr")
    for row in infobox_rows:
        if any(keyword in row.get_text() for keyword in ["Production", "Model years", "Assembly", "Manufactured"]):
            date = extract_date_from_text(row.get_text())
            if date:
                return date, wiki_url, snippet

    # Fallback: first paragraphs
    for p in soup.select("p"):
        date = extract_date_from_text(p.get_text(" "))
        if date:
            return date, wiki_url, snippet

    return None, wiki_url, snippet

def wikipedia_search_with_snippet(query, max_results=5):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srlimit": max_results,
        "srprop": "snippet",  # Include snippet in the response
        "format": "json"
    }
    
    response = requests.get(url, params=params)
    data = response.json()

    if "query" in data and "search" in data["query"]:
        results = []
        for item in data["query"]["search"]:
            title = item["title"]
            page_id = item["pageid"]
            snippet = re.sub('<[^<]+?>', '', item.get("snippet", ""))  # Remove HTML tags
            page_url = f"https://en.wikipedia.org/?curid={page_id}"
            results.append({
                "title": title,
                "url": page_url,
                "snippet": snippet
            })
        return results
    
    return None


def main():
    
    dict = load_dict_from_json(filename=TARGET_SAVE)

    cars = []
    for keys, values in dict.items():
        # we form the list needed for the scraper 
        temp_car_name = f"{values['make']} {values['model']}"
        cars.append(str(temp_car_name))

    # cars = ["Volkswagen Cross Lavida"]

    results = {}
    for car in cars:

        # cleaning up the car name cause some car make and model are dupes 
        cleaned_name = " ".join(key for key, _ in groupby(car.split()))

        print(f"\n🚗 Scraping Wikipedia for: {cleaned_name}")
        date, url, snippet = scrape_wikipedia(cleaned_name)
        # i am just gonna tag it with the original car name i guess 
        results[car] = {
            "release_date": date if date else "Not found",
            "source": url if url else "No page found",
            "snippet": str(snippet) if snippet else "no snippet found",
            "cleaned_name" : str(cleaned_name)
        }
        time.sleep(1)

    SAVETO = "car_release_dates_wiki3.json"

    with open(SAVETO, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print(f"\n✅ Done! Results saved to {SAVETO}")


if __name__ == "__main__":
    main()
