from datetime import datetime, timedelta
import json
import os

def calculate_golden_hours(sunrise_str, sunset_str):
    """
    Calculate golden hour times and daylight duration.
    Golden Hour = ~30 minutes after sunrise & ~30 minutes before sunset
    """
    fmt = "%I:%M %p"
    try:
        sunrise = datetime.strptime(sunrise_str, fmt)
        sunset = datetime.strptime(sunset_str, fmt)
        
        morning_golden_start = sunrise
        morning_golden_end = sunrise + timedelta(minutes=30)
        evening_golden_start = sunset - timedelta(minutes=30)
        evening_golden_end = sunset
        daylight_duration = sunset - sunrise
        
        hours = daylight_duration.seconds // 3600
        minutes = (daylight_duration.seconds % 3600) // 60
        
        return {
            "morning_golden_start": morning_golden_start.strftime("%I:%M %p"),
            "morning_golden_end": morning_golden_end.strftime("%I:%M %p"),
            "evening_golden_start": evening_golden_start.strftime("%I:%M %p"),
            "evening_golden_end": evening_golden_end.strftime("%I:%M %p"),
            "daylight_duration": f"{hours}h {minutes}m",
            "daylight_seconds": daylight_duration.seconds
        }
    except Exception as e:
        return {
            "morning_golden_start": "N/A",
            "morning_golden_end": "N/A",
            "evening_golden_start": "N/A",
            "evening_golden_end": "N/A",
            "daylight_duration": "N/A",
            "daylight_seconds": 0
        }

def interpret_moon_phase(phase_str):
    """
    Convert moon phase string to emoji and label.
    """
    phases = {
        "New Moon": {"emoji": "🌑", "label_id": "Bulan Baru", "label_en": "New Moon"},
        "Waxing Crescent": {"emoji": "🌒", "label_id": "Bulan Sabit Awal", "label_en": "Waxing Crescent"},
        "First Quarter": {"emoji": "🌓", "label_id": "Kuartal Pertama", "label_en": "First Quarter"},
        "Waxing Gibbous": {"emoji": "🌔", "label_id": "Bulan Cembung Awal", "label_en": "Waxing Gibbous"},
        "Full Moon": {"emoji": "🌕", "label_id": "Bulan Purnama", "label_en": "Full Moon"},
        "Waning Gibbous": {"emoji": "🌖", "label_id": "Bulan Cembung Akhir", "label_en": "Waning Gibbous"},
        "Last Quarter": {"emoji": "🌗", "label_id": "Kuartal Terakhir", "label_en": "Last Quarter"},
        "Waning Crescent": {"emoji": "🌘", "label_id": "Bulan Sabit Akhir", "label_en": "Waning Crescent"}
    }
    return phases.get(phase_str, {
        "emoji": "🌙",
        "label_id": "Fase Tidak Diketahui",
        "label_en": "Unknown Phase"
    })

def parse_astronomy_data(astro_data):
    """Parse and structure astronomy data from API response."""
    if not astro_data:
        return None
    
    try:
        golden_hours = calculate_golden_hours(astro_data.get("sunrise"), astro_data.get("sunset"))
        moon_phase_info = interpret_moon_phase(astro_data.get("moon_phase", ""))
        
        return {
            "sunrise": astro_data.get("sunrise"),
            "sunset": astro_data.get("sunset"),
            "moonrise": astro_data.get("moonrise"),
            "moonset": astro_data.get("moonset"),
            "moon_phase": astro_data.get("moon_phase"),
            "moon_phase_emoji": moon_phase_info["emoji"],
            "moon_phase_label_id": moon_phase_info["label_id"],
            "moon_phase_label_en": moon_phase_info["label_en"],
            "moon_illumination": int(astro_data.get("moon_illumination", 0)),
            "golden_hours": golden_hours
        }
    except Exception as e:
        return None
