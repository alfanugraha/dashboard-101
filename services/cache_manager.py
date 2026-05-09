import json
import os
from datetime import datetime, timedelta

CACHE_FILE = "cache.json"

def read_cache():
    if not os.path.exists(CACHE_FILE):
        return {}
    try:
        with open(CACHE_FILE, "r") as file:
            return json.load(file)
    except:
        return {}

def write_cache(cache):
    try:
        with open(CACHE_FILE, "w") as file:
            json.dump(cache, file, indent=4)
    except Exception as e:
        print(f"Error writing cache: {e}")

def is_cache_valid(cache_entry):
    try:
        expires_at = datetime.strptime(cache_entry["expires_at"], "%Y-%m-%dT%H:%M:%S")
        return datetime.now() < expires_at
    except:
        return False

def get_adaptive_ttl(weather_data):
    """
    Calculate adaptive TTL based on weather conditions.
    Per PRD §4.3 - Smart Caching with Adaptive TTL
    """
    try:
        current = weather_data.get("current", {})
        precip = float(current.get("precip", 0))
        aqi_data = current.get("air_quality", {})
        epa_index = int(aqi_data.get("us-epa-index", 1)) if aqi_data else 1
        is_day = current.get("is_day", "yes")
        
        # Default: 2 hours for stable weather
        ttl = 120
        reason = "default (stable weather)"
        
        # If it's raining, check more frequently (45 minutes)
        if precip > 0:
            ttl = 45
            reason = "precipitation detected"
        
        # If AQI is very bad, check more frequently (1 hour)
        if epa_index >= 4:
            ttl = 60
            reason = "poor air quality"
        
        # At night, weather is more stable (3 hours)
        if is_day == "no":
            ttl = 180
            reason = "night time (stable)"
        
        return ttl, reason
    except:
        return 120, "default (error in calculation)"

def get_cached_data(location):
    cache = read_cache()
    if location in cache:
        if is_cache_valid(cache[location]):
            return cache[location]["data"]
    return None

def update_cache(location, data, ttl_minutes=None):
    """Update cache with optional adaptive TTL calculation."""
    cache = read_cache()
    
    # Calculate adaptive TTL if not provided
    if ttl_minutes is None:
        ttl_minutes, reason = get_adaptive_ttl(data)
    else:
        reason = "manual override"
    
    expires_at = datetime.now() + timedelta(minutes=ttl_minutes)
    cache[location] = {
        "data": data,
        "fetched_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "expires_at": expires_at.strftime("%Y-%m-%dT%H:%M:%S"),
        "ttl_minutes": ttl_minutes,
        "ttl_reason": reason
    }
    write_cache(cache)

def clear_expired_cache():
    """Remove expired cache entries."""
    cache = read_cache()
    expired_keys = [key for key, entry in cache.items() if not is_cache_valid(entry)]
    
    for key in expired_keys:
        del cache[key]
    
    if expired_keys:
        write_cache(cache)
    
    return expired_keys

def get_cache_size():
    """Get number of cached cities."""
    cache = read_cache()
    return len(cache)