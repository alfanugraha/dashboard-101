from datetime import datetime, timedelta
import re

def format_temperature(temp):
    """Format temperature with degree symbol."""
    return f"{temp}°C"

def format_time(time_str):
    """Format time string."""
    try:
        return datetime.strptime(time_str, "%I:%M %p").strftime("%H:%M")
    except:
        return time_str

def format_wind_direction(degree):
    """Convert degree to cardinal direction."""
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                  "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    index = round(degree / 22.5) % 16
    return directions[index]

def get_aqi_color(epa_index):
    """Get color for AQI category."""
    colors = {
        1: "#00ff87",  # Green
        2: "#ffff00",  # Yellow
        3: "#ff9800",  # Orange
        4: "#ff4444",  # Red
        5: "#7b2d8b",  # Purple
        6: "#4a0000"   # Maroon
    }
    return colors.get(int(epa_index), "#ffffff")

def get_weather_badge_color(description):
    """Get color based on weather description."""
    description = description.lower()
    if "rain" in description or "shower" in description:
        return "#4a90e2"  # Blue for rain
    elif "cloud" in description or "overcast" in description:
        return "#888888"  # Gray for clouds
    elif "clear" in description or "sunny" in description:
        return "#ffd700"  # Gold for sunny
    elif "snow" in description:
        return "#e0f7ff"  # Light blue for snow
    else:
        return "#cccccc"  # Default gray

def calculate_time_diff(time_str1, time_str2):
    """Calculate difference between two time strings (HH:MM format)."""
    try:
        t1 = datetime.strptime(time_str1, "%I:%M %p")
        t2 = datetime.strptime(time_str2, "%I:%M %p")
        diff = t2 - t1
        hours = diff.seconds // 3600
        minutes = (diff.seconds % 3600) // 60
        return f"{hours}h {minutes}m"
    except:
        return "N/A"

def is_within_threshold(value, threshold, compare_type="greater"):
    """Check if value meets threshold condition."""
    try:
        val = float(value)
        thresh = float(threshold)
        if compare_type == "greater":
            return val > thresh
        elif compare_type == "less":
            return val < thresh
        elif compare_type == "equal":
            return val == thresh
        else:
            return False
    except:
        return False

def parse_decimal(value):
    """Safely parse decimal values."""
    try:
        return float(value)
    except:
        return 0.0

def format_pollutant_value(value, unit="µg/m³"):
    """Format pollutant value with unit."""
    try:
        val = float(value)
        return f"{val:.2f} {unit}"
    except:
        return f"{value} {unit}"

def get_season_emoji(season_type):
    """Get emoji for season type."""
    emojis = {
        "rainy": "🌧️",
        "dry": "☀️",
        "transition": "🍂"
    }
    return emojis.get(season_type, "📅")

def translate_season(season_label_id, lang="en"):
    """Translate season label."""
    translations = {
        "Musim Hujan": {"en": "Rainy Season", "id": "Musim Hujan"},
        "Musim Kemarau": {"en": "Dry Season", "id": "Musim Kemarau"},
        "Transisi": {"en": "Transition", "id": "Transisi"}
    }
    lang_code = "id" if lang.lower() == "id" else "en"
    return translations.get(season_label_id, {}).get(lang_code, season_label_id)
