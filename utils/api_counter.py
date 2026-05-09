import json
import os

COUNTER_FILE = "api_counter.json"

def get_counter():
    """Get current API call counter."""
    if not os.path.exists(COUNTER_FILE):
        return {"used": 0, "total": 100, "last_reset": None}
    with open(COUNTER_FILE, "r") as f:
        return json.load(f)

def increment_counter():
    """Increment API call counter."""
    counter = get_counter()
    counter["used"] += 1
    save_counter(counter)
    return counter

def save_counter(counter):
    """Save counter to file."""
    with open(COUNTER_FILE, "w") as f:
        json.dump(counter, f, indent=4)

def get_remaining_calls():
    """Get remaining API calls."""
    counter = get_counter()
    return counter["total"] - counter["used"]

def get_usage_percentage():
    """Get usage percentage."""
    counter = get_counter()
    return (counter["used"] / counter["total"]) * 100

def reset_counter():
    """Reset counter for new month."""
    counter = {
        "used": 0,
        "total": 100,
        "last_reset": str(__import__('datetime').datetime.now())
    }
    save_counter(counter)
    return counter
