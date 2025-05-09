from core.data.api_client import CricbuzzAPIClient

def get_live_match_status(api_client: CricbuzzAPIClient) -> dict:
    """Fetch live match status using the API client."""
    return api_client.get_live_scores()