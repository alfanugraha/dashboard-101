# 🌦️ SEAWeather Dashboard

A comprehensive weather, air quality, and astronomy dashboard for Southeast Asia powered by Shiny Python and Weatherstack API.

## Features

- **Real-Time Weather**: Current temperature, humidity, wind, pressure, and visibility
- **Air Quality Index (AQI)**: EPA AQI rankings with WHO pollutant guidelines
- **Astronomy Data**: Sunrise/sunset, moon phases, golden hour calculations
- **Season Tracker**: Historical seasonal climate patterns and forecasts
- **Intelligent Alerts**: Multi-threshold alerts for dangerous weather/air quality
- **Smart Caching**: Adaptive TTL-based caching to optimize API usage (100 calls/month free plan)
- **Bilingual UI**: English and Bahasa Indonesia support
- **11 ASEAN Countries**: Support for 50+ major cities across Southeast Asia

## Quick Start

### Prerequisites

- Python 3.8+
- Weatherstack API key (free at https://weatherstack.com/)

### Installation

```bash
# Clone or navigate to the project
cd seaweather

# Install dependencies
pip install -r requirements.txt

# Configure API key
# Edit .env file and add your Weatherstack API key:
# WEATHERSTACK_API_KEY=your_api_key_here
```

### Running the Dashboard

```bash
# From the seaweather directory
shiny run app.py

# Or with specific host/port
python -m shiny run app.py --host 127.0.0.1 --port 8000
```

Then open your browser to: **http://127.0.0.1:8000**

## Project Structure

```
seaweather/
├── app.py                          # Main Shiny application entry point
├── requirements.txt                # Python dependencies
├── .env                            # API configuration (not in VCS)
├── .gitignore                      # Git ignore rules
│
├── components/                     # Shiny UI components
│   ├── city_selector.py
│   ├── weather_card.py
│   ├── astro_panel.py
│   ├── aqi_panel.py
│   ├── season_panel.py
│   ├── alert_banner.py
│   └── map_widget.py
│
├── services/                       # Business logic and data processing
│   ├── weather_service.py          # Weatherstack API wrapper
│   ├── cache_manager.py            # Caching with adaptive TTL
│   ├── aqi_engine.py               # Air quality calculations
│   ├── astro_engine.py             # Astronomy calculations
│   ├── alert_engine.py             # Alert generation
│   └── seasonal_data.py            # Seasonal climate data
│
├── data/                           # Static data files
│   ├── cities_sea.json             # ASEAN cities master list
│   ├── seasonal_climate.csv        # Historical climate data
│   └── who_pollutant_limits.json   # WHO safety guidelines
│
├── assets/                         # Frontend styling
│   └── styles.css                  # Dark theme with glassmorphism
│
└── utils/                          # Utility functions
    ├── helpers.py                  # Formatting and conversion helpers
    └── api_counter.py              # API usage tracking
```

## Configuration

### Environment Variables (.env)

```
# Weatherstack API Key
WEATHERSTACK_API_KEY=your_key_here

# Optional: Cache location
CACHE_FILE=cache.json
```

## Supported Locations

### Countries (11 ASEAN Members)
- 🇮🇩 Indonesia (Jakarta, Surabaya, Medan, Bali, Makassar, Yogyakarta, Bandung)
- 🇲🇾 Malaysia (Kuala Lumpur, Penang, Kota Kinabalu, Johor Bahru, Kuching)
- 🇸🇬 Singapore (Singapore)
- 🇹🇭 Thailand (Bangkok, Chiang Mai, Phuket, Pattaya, Hat Yai)
- 🇻🇳 Vietnam (Hanoi, Ho Chi Minh City, Da Nang, Hue)
- 🇵🇭 Philippines (Manila, Cebu, Davao, Quezon City)
- 🇲🇲 Myanmar (Yangon, Mandalay, Naypyidaw)
- 🇰🇭 Cambodia (Phnom Penh, Siem Reap)
- 🇱🇦 Laos (Vientiane, Luang Prabang)
- 🇧🇳 Brunei (Bandar Seri Begawan)
- 🇹🇱 Timor-Leste (Dili)

## API Limits

- **Free Plan**: 100 requests/month
- **Response Data**: Weather + Astronomy + Air Quality (3-in-1)
- **Smart Caching**: Adaptive TTL based on weather conditions
  - Normal: 2 hours
  - Rainy: 45 minutes
  - Poor AQI: 1 hour
  - Nighttime: 3 hours

## Features Roadmap

- [ ] 7-day forecast (requires paid plan)
- [ ] Historical weather data (requires paid plan)
- [ ] Push notifications
- [ ] Multi-user accounts
- [ ] Data export (CSV/PDF)
- [ ] Deployment to cloud (Heroku, AWS, etc.)

## Air Quality Standards

### EPA AQI Categories
| Index | Category | Color | Recommendation |
|-------|----------|-------|-----------------|
| 1 | Good | 🟢 | Safe for all activities |
| 2 | Moderate | 🟡 | Sensitive groups limit outdoor time |
| 3 | Unhealthy (Sensitive) | 🟠 | Sensitive groups avoid outdoors |
| 4 | Unhealthy | 🔴 | Everyone limit outdoor activities |
| 5 | Very Unhealthy | 🟣 | Avoid outdoor activities |
| 6 | Hazardous | 🟤 | Emergency conditions |

### WHO Pollutant Limits (24-hour)
- PM2.5: 15 µg/m³
- PM10: 45 µg/m³
- NO₂: 25 µg/m³
- O₃: 100 µg/m³
- SO₂: 40 µg/m³

## Troubleshooting

### "API key not set"
- Check that `.env` file exists and contains `WEATHERSTACK_API_KEY`
- Ensure you're not using the placeholder value `your_api_key_here`

### "API call failed"
- Verify API key is valid at https://weatherstack.com/
- Check internet connectivity
- Ensure you haven't exceeded monthly quota (100 calls)

### "No data available"
- Wait for cache to expire and try again
- Check that city name is spelled correctly
- Try a major city name (e.g., "Bangkok" instead of a smaller town)

## License

This project is provided as-is for educational and research purposes.

## Support

For issues, questions, or feature requests, please refer to the PRD document: `prd-claude.md`

---

**Version**: 1.1.0 | **Last Updated**: April 2026 | **Status**: Production Ready
