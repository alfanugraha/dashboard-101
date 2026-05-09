# AGENTS.md — SEAWeather Dashboard

## Quick Start for Agents

**Run the dashboard:**
```bash
cd seaweather
python -m shiny run app.py --port 8000
```
Open browser to `http://localhost:8000`

**Run tests:**
```bash
cd seaweather
python test_dashboard.py
```

**Install dependencies (first time only):**
```bash
cd seaweather
pip install -r requirements.txt
```

## Critical Setup Issues

### API Key Required
- The app **will crash on startup** if `WEATHERSTACK_API_KEY` is not set in `.env`
- `.env` is in `.gitignore` — it's not in version control
- See `services/weather_service.py:15` — it explicitly validates the key exists
- Free API key from: https://weatherstack.com/ (100 calls/month)

### File Path Handling
- `app.py` must run from the `seaweather/` directory, NOT from the repo root
- Cities data loading tries both `data/cities_sea.json` (when running from seaweather/) and `seaweather/data/cities_sea.json` (when running from root)
- See `app.py:23` — both paths are attempted for robustness

### UTF-8 Encoding for Data Files
- All JSON files must be read with `encoding="utf-8"` (critical on Windows)
- Flag emoji are stored but NOT displayed in dropdowns due to Shiny rendering quirks
- See `app.py:26` for the correct pattern

## Architecture Overview

### Main Entry Point
- `app.py`: Shiny Python web app (347 lines)
  - Initializes UI with `ui.page_fluid()` 
  - Server logic uses `@Effect` decorators for reactive dropdowns
  - **Reactive pattern gotcha:** City dropdown must be populated via `ui.update_select()` inside `@Effect`, not in static UI definition

### Business Logic Services (6 engines in `services/`)

| File | Purpose | Key Function |
|------|---------|---|
| `weather_service.py` | Weatherstack API wrapper + caching | `fetch_weather(location)` returns `{"data": {...}, "source": "cache\|api"}` |
| `cache_manager.py` | Adaptive TTL caching (45m-3h based on weather) | `get_cached_data(location)` / `update_cache(location, data)` |
| `aqi_engine.py` | EPA AQI + WHO pollutant parsing | `parse_air_quality_data(raw)` returns pollutants array + recommendations |
| `astro_engine.py` | Sunrise/sunset, moon phases, golden hours | `parse_astronomy_data(raw)` returns structured astro object |
| `alert_engine.py` | Multi-threshold alerts (8 types) | `generate_alerts(weather_data, aqi_data)` returns list of alerts |
| `seasonal_data.py` | 12-month climate patterns | `get_current_season(city, country, month)` for seasonal info |

### Utilities (`utils/`)
- `helpers.py`: Temperature/wind formatting, translation stubs (EN/ID ready)
- `api_counter.py`: Tracks API call quota (100/month), persists to `api_counter.json`

### Static Data (`data/`)
- `cities_sea.json`: 11 ASEAN countries, 50+ cities with flag emoji
- `who_pollutant_limits.json`: EPA AQI thresholds (1-6) + WHO safety limits for 6 pollutants
- `seasonal_climate.csv`: 48 rows (4 test cities × 12 months) — load via `pandas`

## Common Agent Mistakes to Avoid

### Shiny Python API Specifics
1. **Don't use `@ui.render.ui`** — use `@output` + `@render.ui` separately
2. **Don't use deprecated `panel_well()`** — use `ui.card()` instead
3. **Dropdown population must happen in `@Effect`**, not in static UI definition
4. **Use `ui.update_select()` from session context**, not just `ui.update_select()` alone

### Reactive Patterns
- City dropdown depends on country selection — use nested `@Effect` watchers
- Button clicks trigger effects via `input.fetch_weather()` as reactive dependency
- Always check `.get()` with defaults on parsed data to avoid AttributeError

### Data Loading Path Issues
- **Absolute path requirement**: When adding new data files, try both `data/file.json` and `seaweather/data/file.json`
- **UTF-8 encoding**: Always explicit `encoding="utf-8"` when opening JSON
- **Empty dict fallback**: Return `{"countries": {}}` on load failure, never raise

### API Quota Management
- Free tier: 100 calls/month (weatherstack free plan)
- `weather_service.py` implements **graceful degradation**:
  - If quota exceeded, serve cached data instead of failing
  - Check `get_remaining_calls()` before API request (line 34)
- `api_counter.json` persists across sessions — don't delete it

### Testing
- Tests in `test_dashboard.py` expect to run from `seaweather/` directory
- 6/8 tests pass — 2 tests require pandas (which is installed)
- Tests validate: imports, data files, helpers, API counter logic

## When Debugging

**App won't start?**
- Check `.env` file exists and has valid `WEATHERSTACK_API_KEY`
- Run from `seaweather/` directory, not repo root
- Verify `dependencies are installed: `pip list | grep shiny`

**Dropdowns not populating?**
- Verify `data/cities_sea.json` loads with UTF-8 encoding
- Check that `@Effect` decorator is on `init_dropdowns()` function (not output decorator)
- `ui.update_select()` must be called inside server function, not during UI definition

**API quota exceeded?**
- Check `api_counter.json` in seaweather directory
- Service returns cached data automatically — no user-facing error
- Delete `api_counter.json` to reset counter (for testing only)

**Emoji display corrupted?**
- This is Windows console encoding, not a code bug
- Flags stored in JSON but NOT displayed in dropdown labels to avoid corruption
- Test in actual browser, not terminal

## File Structure Quick Reference

```
seaweather/
├── app.py                          # Entry point, Shiny server + UI
├── requirements.txt                # 7 dependencies (shiny, requests, pandas, etc)
├── .env                            # NOT in git — API key only
├── test_dashboard.py               # Run: python test_dashboard.py
│
├── services/                       # 6 business logic engines
│   ├── weather_service.py          # API wrapper (188 lines)
│   ├── cache_manager.py            # Adaptive TTL (82 lines)
│   ├── aqi_engine.py               # Air quality (124 lines)
│   ├── astro_engine.py             # Astronomy (156 lines)
│   ├── alert_engine.py             # Alerts (139 lines)
│   └── seasonal_data.py            # Climate (73 lines)
│
├── utils/                          # 2 utility modules
│   ├── helpers.py                  # Formatting helpers (151 lines)
│   └── api_counter.py              # Quota tracking (62 lines)
│
├── data/                           # 3 static JSON/CSV files
│   ├── cities_sea.json             # 11 countries, 50+ cities
│   ├── seasonal_climate.csv        # 48 climate rows
│   └── who_pollutant_limits.json   # EPA/WHO thresholds
│
└── api_counter.json                # Generated — tracks API usage
```

## Known Limitations

1. **Mock data for missing API fields** — If Weatherstack doesn't return astronomy data, app returns zeros but doesn't fail
2. **No database** — All data is static JSON/CSV, no persistence beyond cache
3. **Single-user** — Shiny app is not multi-tenant, suitable for single user dashboard
4. **100 calls/month quota** — Free tier only, requires upgrade for more usage
5. **ASEAN only** — Cities hardcoded to 11 ASEAN countries + cities list

## References

- README.md: Full feature list, city support matrix
- PRD: `prd-claude.md` (42KB) — original requirements
- Test suite: `test_dashboard.py` (291 lines) — validation logic
