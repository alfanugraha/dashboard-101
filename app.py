from shiny import App, ui, render, reactive
from shiny.reactive import Effect
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from services.weather_service import WeatherService
from services.cache_manager import get_cache_size
from utils.api_counter import get_counter, get_usage_percentage
from services.astro_engine import parse_astronomy_data
from services.aqi_engine import parse_air_quality_data
from services.alert_engine import generate_alerts
from services.seasonal_data import get_current_season
from utils.helpers import format_temperature

# Load environment variables
load_dotenv()

# Load cities data
def load_cities():
    try:
        # Try both possible paths
        paths = ["data/cities_sea.json", "seaweather/data/cities_sea.json"]
        for path in paths:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    print(f"[SUCCESS] Loaded cities from {path}")
                    return data
            except FileNotFoundError:
                continue
        print("[ERROR] cities_sea.json not found in any path")
        return {"countries": {}}
    except Exception as e:
        print(f"[ERROR] Error loading cities: {e}")
        return {"countries": {}}

cities_data = load_cities()
print(f"[INFO] Loaded {len(cities_data.get('countries', {}))} countries")

# UI Definition
app_ui = ui.page_fluid(
    # Header
    ui.row(
        ui.column(8,
            ui.h1("🌦️ SEAWeather — Asia Tenggara Weather Dashboard", class_="text-primary")
        ),
        ui.column(4,
            ui.input_select("language", "Language:", {"en": "English", "id": "Bahasa Indonesia"}, selected="en"),
        )
    ),
    
    ui.hr(),
    
    # City Selector
    ui.row(
        ui.column(12,
            ui.card(
                ui.h3("Select City"),
                ui.input_select("country", "Country:", choices={}),
                ui.input_select("city", "City:", choices={}),
                ui.input_action_button("fetch_weather", "🔄 Fetch Weather", class_="btn btn-primary"),
                ui.output_text("loading_status")
            )
        )
    ),
    
    ui.hr(),
    
    # Alerts Section
    ui.output_ui("alerts_section"),
    
    # Main Content
    ui.row(
        ui.column(6,
            ui.card(
                ui.h3("☁️ Real-Time Weather"),
                ui.output_ui("weather_info")
            )
        ),
        ui.column(6,
            ui.card(
                ui.h3("🌅 Astronomy & Sky"),
                ui.output_ui("astro_info")
            )
        )
    ),
    
    ui.row(
        ui.column(12,
            ui.card(
                ui.h3("🫁 Air Quality Index (AQI)"),
                ui.output_ui("aqi_info")
            )
        )
    ),
    
    ui.row(
        ui.column(6,
            ui.card(
                ui.h3("🍃 Season Tracker"),
                ui.output_ui("season_info")
            )
        ),
        ui.column(6,
            ui.card(
                ui.h3("📊 API Usage Meter"),
                ui.output_ui("api_meter")
            )
        )
    ),
    
    class_="container-fluid"
)

# Server Logic
def server(input, output, session):
    
    weather_service = WeatherService()
    current_weather = reactive.Value(None)
    current_alerts = reactive.Value([])
    
    # Initialize country and city dropdowns on startup
    @Effect
    def init_dropdowns():
        countries_dict = cities_data.get("countries", {})
        # Use country name as both key and display value (no flag in display)
        country_choices = {country: country for country in countries_dict.keys()}
        
        if country_choices:
            ui.update_select("country", choices=country_choices)
            
            # Set first country as default and populate cities
            first_country = list(countries_dict.keys())[0]
            first_country_cities = countries_dict[first_country].get("cities", [])
            city_dict = {city: city for city in first_country_cities}
            ui.update_select("city", choices=city_dict)
    
    # Update city list when country changes
    @Effect
    def update_cities_on_country_change():
        country = input.country()
        if not country:
            return
        
        countries_dict = cities_data.get("countries", {})
        if country in countries_dict:
            cities = countries_dict[country].get("cities", [])
            city_dict = {city: city for city in cities}
            ui.update_select("city", choices=city_dict)
    
    # Fetch weather on button click
    @Effect
    def on_fetch():
        input.fetch_weather()  # Reactive dependency
        
        country = input.country()
        city = input.city()
        
        if not city or not country:
            return
        
        location = f"{city}, {country}"
        print(f"[INFO] Fetching weather for: {location}")
        result = weather_service.fetch_weather(location)
        
        if result.get("data"):
            parsed_data = weather_service.parse_weather_data(result.get("data"))
            astro_data = parse_astronomy_data(result.get("data", {}).get("current", {}).get("astro", {}))
            aqi_data = parse_air_quality_data(result.get("data", {}).get("current", {}).get("air_quality", {}))
            
            current_weather.set({
                "raw_data": result.get("data"),
                "source": result.get("source"),
                "parsed_data": parsed_data,
                "astro": astro_data,
                "aqi": aqi_data,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
            # Generate alerts
            alerts = generate_alerts(
                result.get("data", {}), 
                result.get("data", {}).get("current", {}).get("air_quality", {})
            )
            current_alerts.set(alerts)
        else:
            current_weather.set(None)
            current_alerts.set([])
    
    # Weather Info Output
    @output
    @render.ui
    def weather_info():
        data = current_weather.get()
        if not data or not data.get("parsed_data"):
            return ui.p("No data available. Select a city and click 'Fetch Weather'.")
        
        parsed = data.get("parsed_data", {})
        current = parsed.get("current", {})
        location = parsed.get("location", {})
        
        return ui.div(
            ui.p(f"📍 {location.get('name', 'N/A')}, {location.get('country', 'N/A')}"),
            ui.h2(f"{format_temperature(current.get('temperature', 0))} (feels like {current.get('feelslike', 0)}°C)"),
            ui.p(f"🌡️ {current.get('description', 'N/A')}"),
            ui.br(),
            ui.p(f"💧 Humidity: {current.get('humidity', 'N/A')}%"),
            ui.p(f"💨 Wind: {current.get('wind_speed', 'N/A')} km/h {current.get('wind_dir', 'N/A')}"),
            ui.p(f"👁️ Visibility: {current.get('visibility', 'N/A')} km"),
            ui.p(f"☁️ Cloud Cover: {current.get('cloudcover', 'N/A')}%"),
            ui.p(f"🌡️ Pressure: {current.get('pressure', 'N/A')} mb"),
            ui.p(f"☀️ UV Index: {current.get('uv_index', 'N/A')}"),
            ui.p(f"⏱️ Updated: {current.get('observation_time', 'N/A')}"),
            ui.p(f"Source: {data.get('source', 'N/A')} | {data.get('timestamp', 'N/A')}")
        )
    
    # Astronomy Info Output
    @output
    @render.ui
    def astro_info():
        data = current_weather.get()
        if not data or not data.get("astro"):
            return ui.p("Astronomy data not available from API")
        
        astro = data.get("astro", {})
        golden = astro.get("golden_hours", {})
        
        return ui.div(
            ui.p(f"🌅 Sunrise: {astro.get('sunrise', 'N/A')}"),
            ui.p(f"🌇 Sunset: {astro.get('sunset', 'N/A')}"),
            ui.p(f"⏱️ Daylight Duration: {golden.get('daylight_duration', 'N/A')}"),
            ui.br(),
            ui.p(f"🌕 Moonrise: {astro.get('moonrise', 'N/A')}"),
            ui.p(f"🌑 Moonset: {astro.get('moonset', 'N/A')}"),
            ui.p(f"🌙 Moon Phase: {astro.get('moon_phase_emoji', '')} {astro.get('moon_phase_label_en', 'N/A')}"),
            ui.p(f"💡 Moon Illumination: {astro.get('moon_illumination', 'N/A')}%"),
            ui.br(),
            ui.p(f"🌅 Golden Hour (Morning): {golden.get('morning_golden_start', 'N/A')} - {golden.get('morning_golden_end', 'N/A')}"),
            ui.p(f"🌅 Golden Hour (Evening): {golden.get('evening_golden_start', 'N/A')} - {golden.get('evening_golden_end', 'N/A')}")
        )
    
    # AQI Info Output
    @output
    @render.ui
    def aqi_info():
        data = current_weather.get()
        if not data or not data.get("aqi"):
            return ui.p("Air quality data not available from API")
        
        aqi = data.get("aqi", {})
        pollutants = aqi.get("pollutants", {})
        
        pollutant_items = []
        for key, p in pollutants.items():
            warning = " ⚠️ Above WHO" if p.get('above_who') else " ✓"
            pollutant_items.append(
                ui.p(f"{p.get('label', 'N/A')}: {p.get('value', 0):.2f} {p.get('unit', 'N/A')}{warning}")
            )
        
        return ui.div(
            ui.h4(f"EPA Index: {aqi.get('epa_label_en', 'N/A')} (Level {aqi.get('epa_index', 'N/A')})"),
            ui.p(f"🇬🇧 DEFRA Index: {aqi.get('defra_index', 'N/A')}"),
            ui.p(f"💡 Recommendation: {aqi.get('recommendation', 'N/A')}"),
            ui.br(),
            ui.h5("Pollutants Breakdown:"),
            *pollutant_items if pollutant_items else [ui.p("No pollutant data available")]
        )
    
    # Season Info Output
    @output
    @render.ui
    def season_info():
        data = current_weather.get()
        if not data or not data.get("parsed_data"):
            return ui.p("Select a city to see seasonal information")
        
        parsed = data.get("parsed_data", {})
        location = parsed.get("location", {})
        city = location.get("name", "")
        country = location.get("country", "")
        current_month = datetime.now().month
        
        season_data = get_current_season(city, country, current_month)
        
        if not season_data:
            return ui.p("Seasonal data not available")
        
        season_type = season_data.get("season_type", "")
        season_emoji = {"rainy": "🌧️", "dry": "☀️", "transition": "🍂"}.get(season_type, "📅")
        
        return ui.div(
            ui.p(f"Current Season: {season_emoji} {season_data.get('season_label_en', 'N/A')}"),
            ui.p(f"Average Temperature: {season_data.get('avg_temp_c', 'N/A')}°C"),
            ui.p(f"Average Rainfall: {season_data.get('avg_rainfall_mm', 'N/A')}mm")
        )
    
    # Alerts Output
    @output
    @render.ui
    def alerts_section():
        alerts = current_alerts.get()
        if not alerts:
            return ui.div()
        
        alert_items = []
        for alert in alerts:
            severity_class = "alert alert-danger" if alert.get('severity') == 'high' else "alert alert-warning"
            alert_items.append(
                ui.div(
                    f"{alert.get('icon', '')} {alert.get('title_en', 'Alert')}: {alert.get('message_en', '')}",
                    class_=severity_class
                )
            )
        
        return ui.div(*alert_items)
    
    # API Meter Output
    @output
    @render.ui
    def api_meter():
        counter = get_counter()
        usage_pct = get_usage_percentage()
        remaining = counter.get("total", 100) - counter.get("used", 0)
        
        return ui.div(
            ui.p(f"API Calls Used: {counter.get('used', 0)}/{counter.get('total', 100)}"),
            ui.p(f"Remaining: {remaining} calls"),
            ui.p(f"Usage: {usage_pct:.1f}%"),
            ui.p(f"Cached Cities: {get_cache_size()}")
        )
    
    # Loading status
    @output
    @render.text
    def loading_status():
        data = current_weather.get()
        if data:
            return f"[OK] Data loaded from {data.get('source', 'N/A')} - {data.get('timestamp', 'N/A')}"
        else:
            return "Ready"

# Create and run the app
app = App(app_ui, server)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
