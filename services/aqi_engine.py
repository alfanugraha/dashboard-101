import json
import os

def load_who_limits():
    """Load WHO pollutant limits from JSON."""
    try:
        with open(os.path.join(os.path.dirname(__file__), "../data/who_pollutant_limits.json"), "r") as f:
            return json.load(f)
    except:
        return {}

def get_aqi_label(epa_index, lang="en"):
    """Get AQI category label."""
    limits = load_who_limits()
    epa_categories = limits.get("epa_aqi_categories", {})
    category = epa_categories.get(str(int(epa_index)), {})
    
    if lang == "id":
        return category.get("label_id", "Tidak Diketahui")
    else:
        return category.get("label_en", "Unknown")

def get_aqi_color(epa_index):
    """Get color for AQI category."""
    limits = load_who_limits()
    epa_categories = limits.get("epa_aqi_categories", {})
    category = epa_categories.get(str(int(epa_index)), {})
    return category.get("color", "#ffffff")

def get_aqi_recommendation(epa_index, lang="en"):
    """Get health recommendation for AQI level."""
    limits = load_who_limits()
    epa_categories = limits.get("epa_aqi_categories", {})
    category = epa_categories.get(str(int(epa_index)), {})
    return category.get("recommendation", "Check air quality updates")

def check_pollutant_above_who(pollutant_name, value):
    """Check if pollutant value exceeds WHO guideline."""
    limits = load_who_limits()
    who_guidelines = limits.get("who_2021_guidelines", {})
    
    pollutant_key = pollutant_name.lower().replace(" ", "_")
    if pollutant_key in who_guidelines:
        who_limit = who_guidelines[pollutant_key].get("24h", float('inf'))
        try:
            return float(value) > who_limit
        except:
            return False
    return False

def get_who_limit(pollutant_name):
    """Get WHO guideline limit for pollutant."""
    limits = load_who_limits()
    who_guidelines = limits.get("who_2021_guidelines", {})
    
    pollutant_key = pollutant_name.lower().replace(" ", "_")
    if pollutant_key in who_guidelines:
        return who_guidelines[pollutant_key].get("24h", None)
    return None

def parse_air_quality_data(air_quality_data):
    """Parse and structure air quality data from API response."""
    if not air_quality_data:
        return None
    
    try:
        epa_index = int(air_quality_data.get("us-epa-index", 1))
        
        pollutants = {
            "pm2_5": {
                "value": float(air_quality_data.get("pm2_5", 0)),
                "label": "PM2.5",
                "unit": "µg/m³",
                "above_who": check_pollutant_above_who("pm2_5", air_quality_data.get("pm2_5", 0)),
                "who_limit": get_who_limit("pm2_5")
            },
            "pm10": {
                "value": float(air_quality_data.get("pm10", 0)),
                "label": "PM10",
                "unit": "µg/m³",
                "above_who": check_pollutant_above_who("pm10", air_quality_data.get("pm10", 0)),
                "who_limit": get_who_limit("pm10")
            },
            "co": {
                "value": float(air_quality_data.get("co", 0)),
                "label": "CO",
                "unit": "µg/m³",
                "above_who": check_pollutant_above_who("co", air_quality_data.get("co", 0)),
                "who_limit": get_who_limit("co")
            },
            "no2": {
                "value": float(air_quality_data.get("no2", 0)),
                "label": "NO₂",
                "unit": "µg/m³",
                "above_who": check_pollutant_above_who("no2", air_quality_data.get("no2", 0)),
                "who_limit": get_who_limit("no2")
            },
            "o3": {
                "value": float(air_quality_data.get("o3", 0)),
                "label": "O₃",
                "unit": "µg/m³",
                "above_who": check_pollutant_above_who("o3", air_quality_data.get("o3", 0)),
                "who_limit": get_who_limit("o3")
            },
            "so2": {
                "value": float(air_quality_data.get("so2", 0)),
                "label": "SO₂",
                "unit": "µg/m³",
                "above_who": check_pollutant_above_who("so2", air_quality_data.get("so2", 0)),
                "who_limit": get_who_limit("so2")
            }
        }
        
        return {
            "epa_index": epa_index,
            "epa_label_en": get_aqi_label(epa_index, "en"),
            "epa_label_id": get_aqi_label(epa_index, "id"),
            "color": get_aqi_color(epa_index),
            "recommendation": get_aqi_recommendation(epa_index),
            "defra_index": int(air_quality_data.get("gb-defra-index", 1)),
            "pollutants": pollutants
        }
    except Exception as e:
        return None
