def parse_player_stats(raw_data: dict) -> dict:
    """Parse raw player stats into a structured format."""
    return {
        "name": raw_data.get("name"),
        "matches": raw_data.get("matches"),
        "runs": raw_data.get("runs"),
        "wickets": raw_data.get("wickets")
    }