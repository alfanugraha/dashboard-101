def generate_alerts(weather_data, aqi_data):
    """
    Generate alerts based on weather and air quality thresholds.
    Returns a list of alert objects.
    """
    alerts = []
    
    if not weather_data:
        return alerts
    
    current = weather_data.get("current", {})
    
    # UV Index Alerts
    uv_index = float(current.get("uv_index", 0))
    if uv_index >= 11:
        alerts.append({
            "type": "UV_EXTREME",
            "severity": "high",
            "icon": "☀️",
            "title_en": "Extreme UV Index",
            "title_id": "Indeks UV Ekstrem",
            "message_en": "UV Index is extremely high - Avoid direct sun exposure",
            "message_id": "Indeks UV sangat tinggi - Hindari paparan matahari langsung",
            "color": "#ff4444"
        })
    elif uv_index >= 8:
        alerts.append({
            "type": "UV_HIGH",
            "severity": "medium",
            "icon": "☀️",
            "title_en": "High UV Index",
            "title_id": "Indeks UV Tinggi",
            "message_en": "Protect your skin - Use sunscreen SPF 30+",
            "message_id": "Lindungi kulit Anda - Gunakan tabir surya SPF 30+",
            "color": "#ffff00"
        })
    
    # Wind Speed Alerts
    wind_speed = float(current.get("wind_speed", 0))
    if wind_speed >= 60:
        alerts.append({
            "type": "STRONG_WIND",
            "severity": "high",
            "icon": "💨",
            "title_en": "Strong Wind Warning",
            "title_id": "Peringatan Angin Kencang",
            "message_en": "Strong winds detected - Be cautious outdoors",
            "message_id": "Angin kencang terdeteksi - Berhati-hatilah di luar",
            "color": "#ff4444"
        })
    
    # Humidity Alerts
    humidity = float(current.get("humidity", 0))
    if humidity >= 90:
        alerts.append({
            "type": "EXTREME_HUMIDITY",
            "severity": "medium",
            "icon": "💧",
            "title_en": "Extreme Humidity",
            "title_id": "Kelembaban Ekstrem",
            "message_en": "Very high humidity - Heat index may feel higher",
            "message_id": "Kelembaban sangat tinggi - Indeks panas mungkin terasa lebih tinggi",
            "color": "#ffff00"
        })
    
    # Visibility Alerts
    visibility = float(current.get("visibility", 0))
    if visibility <= 2:
        alerts.append({
            "type": "LOW_VISIBILITY",
            "severity": "medium",
            "icon": "👁️",
            "title_en": "Low Visibility",
            "title_id": "Visibilitas Rendah",
            "message_en": "Visibility is limited - Drive with caution",
            "message_id": "Visibilitas terbatas - Berkendara dengan hati-hati",
            "color": "#ffff00"
        })
    
    # Air Quality Alerts
    if aqi_data:
        epa_index = aqi_data.get("epa_index", 1)
        if epa_index >= 4:
            alerts.append({
                "type": "POOR_AQI",
                "severity": "high",
                "icon": "🫁",
                "title_en": "Poor Air Quality",
                "title_id": "Kualitas Udara Buruk",
                "message_en": aqi_data.get("recommendation", "Limit outdoor activities"),
                "message_id": "Batasi aktivitas outdoor - Gunakan masker N95",
                "color": "#ff4444"
            })
        elif epa_index >= 2:
            alerts.append({
                "type": "MODERATE_AQI",
                "severity": "low",
                "icon": "🫁",
                "title_en": "Moderate Air Quality",
                "title_id": "Kualitas Udara Sedang",
                "message_en": "Sensitive groups should limit outdoor activities",
                "message_id": "Kelompok sensitif harus membatasi aktivitas outdoor",
                "color": "#ffff00"
            })
    
    # Moon Phase Alert (special occasion)
    astro = weather_data.get("current", {}).get("astro", {})
    moon_phase = astro.get("moon_phase", "")
    if moon_phase == "Full Moon":
        alerts.append({
            "type": "FULL_MOON",
            "severity": "info",
            "icon": "🌕",
            "title_en": "Full Moon Tonight",
            "title_id": "Bulan Purnama Malam Ini",
            "message_en": "Perfect for outdoor activities and photography",
            "message_id": "Sempurna untuk aktivitas outdoor dan fotografi",
            "color": "#ffd700"
        })
    
    return alerts

def check_alert_condition(current_data, condition_type, threshold):
    """Check if a specific alert condition is met."""
    try:
        if condition_type == "uv":
            return float(current_data.get("uv_index", 0)) >= threshold
        elif condition_type == "wind":
            return float(current_data.get("wind_speed", 0)) >= threshold
        elif condition_type == "humidity":
            return float(current_data.get("humidity", 0)) >= threshold
        elif condition_type == "visibility":
            return float(current_data.get("visibility", 10)) <= threshold
        elif condition_type == "precip":
            return float(current_data.get("precip", 0)) > 0
        else:
            return False
    except:
        return False
