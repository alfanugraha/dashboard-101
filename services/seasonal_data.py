import pandas as pd
import os

def load_seasonal_data():
    """Load seasonal climate CSV data."""
    try:
        csv_path = os.path.join(os.path.dirname(__file__), "../data/seasonal_climate.csv")
        return pd.read_csv(csv_path)
    except Exception as e:
        return pd.DataFrame()

def get_seasonal_data_for_city(city, country):
    """Get seasonal data for a specific city."""
    df = load_seasonal_data()
    city_data = df[(df["city"] == city) & (df["country"] == country)]
    
    if city_data.empty:
        return None
    
    return city_data.to_dict("records")

def get_current_season(city, country, current_month):
    """Get current season for a city based on month."""
    seasonal_data = get_seasonal_data_for_city(city, country)
    
    if not seasonal_data:
        return None
    
    month_data = [d for d in seasonal_data if d["month"] == current_month]
    if not month_data:
        return None
    
    return month_data[0]

def get_season_for_month(city, country, month):
    """Get season info for specific month."""
    seasonal_data = get_seasonal_data_for_city(city, country)
    
    if not seasonal_data:
        return None
    
    month_data = [d for d in seasonal_data if d["month"] == month]
    if month_data:
        return month_data[0]
    
    return None

def get_all_months_for_city(city, country):
    """Get all 12 months of seasonal data for a city."""
    seasonal_data = get_seasonal_data_for_city(city, country)
    
    if not seasonal_data:
        return []
    
    # Sort by month
    sorted_data = sorted(seasonal_data, key=lambda x: x["month"])
    return sorted_data

def prepare_season_chart_data(city, country):
    """Prepare data for season tracking chart."""
    months_data = get_all_months_for_city(city, country)
    
    if not months_data:
        return None
    
    return {
        "city": city,
        "country": country,
        "months": [d["month"] for d in months_data],
        "temperatures": [d["avg_temp_c"] for d in months_data],
        "rainfall": [d["avg_rainfall_mm"] for d in months_data],
        "seasons": [d["season_type"] for d in months_data],
        "season_labels_en": [d["season_label_en"] for d in months_data],
        "season_labels_id": [d["season_label_id"] for d in months_data]
    }

def get_season_estimate_end(current_month, season_type, months_data):
    """Estimate when current season will end."""
    current_season_months = [d["month"] for d in months_data if d["season_type"] == season_type]
    
    if current_month in current_season_months:
        max_month = max(current_season_months)
        return max_month
    
    return current_month

def compare_cities_seasonal(city1, country1, city2, country2):
    """Compare seasonal data of two cities."""
    data1 = prepare_season_chart_data(city1, country1)
    data2 = prepare_season_chart_data(city2, country2)
    
    if not data1 or not data2:
        return None
    
    return {
        "city1": {
            "name": city1,
            "data": data1
        },
        "city2": {
            "name": city2,
            "data": data2
        }
    }
