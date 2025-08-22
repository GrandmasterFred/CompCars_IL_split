# import requests

# def get_wikipedia_url(car_name, max_results=3):
#     url = "https://en.wikipedia.org/w/api.php"
#     params = {
#         "action": "opensearch",
#         "search": car_name,
#         "limit": 3,
#         "namespace": 0,
#         "format": "json"
#     }
#     resp = requests.get(url, params=params)
#     data = resp.json()
    
#     if data and len(data) > 3 and data[3]:
#         titles = data[1]  # List of titles
#         urls = data[3]    # List of URLs

#         # Check for exact match (case-insensitive)
#         for title, link in zip(titles, urls):
#             if title.lower() == car_name.lower():
#                 return link  # Exact match found
        
#         # If no exact match, return all as suggestions
#         return urls

#     return None

# # Example usage:
# car = "Volkswagen Cross Lavida"
# result = get_wikipedia_url(car)
# print(result)


import requests

def wikipedia_search(car_name, max_results=5):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": car_name,
        "srlimit": max_results,
        "format": "json"
    }
    
    response = requests.get(url, params=params)
    data = response.json()

    if "query" in data and "search" in data["query"]:
        results = []
        for item in data["query"]["search"]:
            title = item["title"]
            page_id = item["pageid"]
            page_url = f"https://en.wikipedia.org/?curid={page_id}"
            results.append({"title": title, "url": page_url})
        return results
    
    return None

# Example usage:
car = "Volkswagen Cross Lavida"
results = wikipedia_search(car, max_results=5)
for r in results:
    print(f"{r['title']}: {r['url']}")
