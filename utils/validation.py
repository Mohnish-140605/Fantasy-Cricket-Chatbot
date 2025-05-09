def validate_player_id(player_id: str) -> bool:
    """Validate if the player ID is in the correct format."""
    return player_id.isdigit() and len(player_id) > 0

def validate_api_key(api_key: str) -> bool:
    """Validate if the API key is in the correct format."""
    return len(api_key) > 10 