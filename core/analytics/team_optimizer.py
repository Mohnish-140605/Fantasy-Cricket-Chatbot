def optimize_team(players: list) -> list:
    """Optimize the team based on player stats."""
    return sorted(players, key=lambda x: x.get("performance_score", 0), reverse=True)