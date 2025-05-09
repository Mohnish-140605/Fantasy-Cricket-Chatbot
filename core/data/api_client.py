import requests

class CricbuzzAPIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://cricapi.com/api/fd207dab-6b6c-40dc-8782-de1b1b173371"

    def get_live_scores(self):
        url = f"{self.base_url}cricket?apikey={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Failed to fetch live scores"}

    def get_player_stats(self, player_id):
        url = f"{self.base_url}playerStats?apikey={self.api_key}&playerId={player_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Failed to fetch player stats"}

    def get_live_match_status(self):
        """Fetch live match status."""
        url = f"{self.base_url}matchStatus?apikey={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Failed to fetch live match status"}
