import requests
import os
from datetime import datetime
from dotenv import load_dotenv
from services.cache_manager import get_cached_data, update_cache
from utils.api_counter import increment_counter, get_remaining_calls

# Load environment variables from .env file
load_dotenv()

class WeatherService:
    def __init__(self):
        self.base_url = "http://api.weatherstack.com/current"
        self.api_key = os.getenv("WEATHERSTACK_API_KEY")
        if not self.api_key or self.api_key == "your_api_key_here":
            raise ValueError("API key not set in .env file. Please configure WEATHERSTACK_API_KEY.")

    def fetch_weather(self, location, force_refresh=False):
        """
        Fetch weather data with caching support.
        Returns complete weather data or None on failure.
        """
        # Check cache first
        if not force_refresh:
            cached_data = get_cached_data(location)
            if cached_data:
                return {
                    "data": cached_data,
                    "source": "cache",
                    "message": "Data retrieved from cache"
                }
        
        # Check remaining API calls
        remaining = get_remaining_calls()
        if remaining <= 0:
            cached_data = get_cached_data(location)
            if cached_data:
                return {
                    "data": cached_data,
                    "source": "cache",
                    "message": "API quota exhausted - serving cached data",
                    "error": "QUOTA_EXCEEDED"
                }
            else:
                return {
                    "data": None,
                    "source": None,
                    "message": "API quota exhausted and no cached data available",
                    "error": "NO_DATA_AVAILABLE"
                }
        
        # Fetch from API
        try:
            params = {
                "access_key": self.api_key,
                "query": location
            }
            response = requests.get(self.base_url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check for API errors
                if "error" in data:
                    return {
                        "data": None,
                        "source": None,
                        "message": f"API Error: {data['error'].get('info', 'Unknown error')}",
                        "error": "API_ERROR"
                    }
                
                # Null-safety: Check for required fields
                if not data.get("current"):
                    return {
                        "data": None,
                        "source": None,
                        "message": "Invalid API response - missing current data",
                        "error": "INVALID_RESPONSE"
                    }
                
                # Cache the data
                update_cache(location, data)
                increment_counter()
                
                return {
                    "data": data,
                    "source": "api",
                    "message": "Fresh data from API",
                    "remaining_calls": get_remaining_calls()
                }
            else:
                # Try to return cached data on API error
                cached_data = get_cached_data(location)
                if cached_data:
                    return {
                        "data": cached_data,
                        "source": "cache",
                        "message": f"API returned status {response.status_code} - serving cached data",
                        "error": "API_ERROR"
                    }
                else:
                    return {
                        "data": None,
                        "source": None,
                        "message": f"Weather API failed with status {response.status_code}",
                        "error": "API_FAILED"
                    }
        
        except requests.Timeout:
            cached_data = get_cached_data(location)
            if cached_data:
                return {
                    "data": cached_data,
                    "source": "cache",
                    "message": "API request timeout - serving cached data",
                    "error": "TIMEOUT"
                }
            else:
                return {
                    "data": None,
                    "source": None,
                    "message": "API request timeout and no cached data available",
                    "error": "TIMEOUT_NO_CACHE"
                }
        
        except Exception as e:
            cached_data = get_cached_data(location)
            if cached_data:
                return {
                    "data": cached_data,
                    "source": "cache",
                    "message": f"Error fetching weather: {str(e)} - serving cached data",
                    "error": "FETCH_ERROR"
                }
            else:
                return {
                    "data": None,
                    "source": None,
                    "message": f"Error fetching weather: {str(e)}",
                    "error": "FETCH_ERROR"
                }

    def parse_weather_data(self, raw_data):
        """Parse and structure weather data for UI consumption."""
        if not raw_data:
            return None
        
        try:
            current = raw_data.get("current", {})
            location = raw_data.get("location", {})
            
            # Null-safety for optional fields
            astro = current.get("astro")
            air_quality = current.get("air_quality")
            
            return {
                "location": {
                    "name": location.get("name", "Unknown"),
                    "country": location.get("country", "Unknown"),
                    "region": location.get("region", ""),
                    "lat": location.get("lat", ""),
                    "lon": location.get("lon", ""),
                    "timezone": location.get("timezone_id", "")
                },
                "current": {
                    "temperature": current.get("temperature"),
                    "feelslike": current.get("feelslike"),
                    "description": current.get("weather_descriptions", ["Unknown"])[0],
                    "icon": current.get("weather_icons", [None])[0],
                    "humidity": current.get("humidity"),
                    "wind_speed": current.get("wind_speed"),
                    "wind_degree": current.get("wind_degree"),
                    "wind_dir": current.get("wind_dir"),
                    "pressure": current.get("pressure"),
                    "precip": current.get("precip"),
                    "cloudcover": current.get("cloudcover"),
                    "uv_index": current.get("uv_index"),
                    "visibility": current.get("visibility"),
                    "is_day": current.get("is_day"),
                    "observation_time": current.get("observation_time")
                },
                "astro": astro,  # Will be None if not available
                "air_quality": air_quality,  # Will be None if not available
                "has_astro": astro is not None,
                "has_air_quality": air_quality is not None
            }
        except Exception as e:
            return None
