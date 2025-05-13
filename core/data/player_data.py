import requests
import os

def fetch_players(api_key):
    url = f"https://api.cricapi.com/v1/players?apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    if data.get("status") == "success":
        return [
            {
                "name": p.get("name"),
                "team": p.get("country"),
                "role": p.get("role", "Unknown")
            }
            for p in data.get("data", [])
        ]
    return []