cache = {}

def cache_data(key: str, value: any):
    """Cache data with a specific key."""
    cache[key] = value

def get_cached_data(key: str):
    """Retrieve cached data by key."""
    return cache.get(key, None)

def clear_cache():
    """Clear all cached data."""
    cache.clear()