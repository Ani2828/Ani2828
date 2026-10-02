import os
import json
import requests
from bs4 import BeautifulSoup

USERNAME = "Ani2828"  # <--- Apna GitHub username yahan dhyan se check kar lena

def fetch_contributions():
    url = f"https://github.com/users/{USERNAME}/contributions"
    print(f"Fetching contribution data from {url}...")
    
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch contributions: {response.status_code}")
        
    soup = BeautifulSoup(response.text, "html.parser")
    days = soup.find_all("td", class_="ContributionCalendar-day")
    
    data = []
    for day in days:
        date = day.get("data-date")
        count_str = day.get("data-count", "0")
        level = day.get("data-level", "0")
        if date:
            data.append({
                "date": date,
                "count": int(count_str) if count_str.isdigit() else 0,
                "level": int(level) if level.isdigit() else 0
            })
            
    os.makedirs("data", exist_ok=True)
    output_file = "data/contributions.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        
    print(f"Successfully saved {len(data)} days of contributions to {output_file}")

if __name__ == "__main__":
    fetch_contributions()