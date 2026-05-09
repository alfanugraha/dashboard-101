#!/usr/bin/env python
"""
Comprehensive test suite for SEAWeather Dashboard
"""

import sys
import json
import os

def test_imports():
    """Test that all modules can be imported."""
    print("=" * 60)
    print("TESTING IMPORTS")
    print("=" * 60)
    try:
        from services.weather_service import WeatherService
        from services.cache_manager import get_cached_data, update_cache
        from services.aqi_engine import parse_air_quality_data
        from services.astro_engine import parse_astronomy_data
        from services.alert_engine import generate_alerts
        from services.seasonal_data import get_all_months_for_city
        from utils.helpers import format_temperature, format_wind_direction
        from utils.api_counter import get_counter
        print("[OK] All imports successful\n")
        return True
    except Exception as e:
        print(f"[FAILED] Import error: {e}\n")
        return False

def test_data_files():
    """Test that all data files exist and are valid."""
    print("=" * 60)
    print("TESTING DATA FILES")
    print("=" * 60)
    
    files_ok = True
    
    # Test cities_sea.json
    try:
        with open("data/cities_sea.json") as f:
            cities = json.load(f)
        num_countries = len(cities.get("countries", {}))
        print(f"[OK] cities_sea.json loaded with {num_countries} countries")
    except Exception as e:
        print(f"[FAILED] cities_sea.json: {e}")
        files_ok = False
    
    # Test who_pollutant_limits.json
    try:
        with open("data/who_pollutant_limits.json") as f:
            limits = json.load(f)
        num_pollutants = len(limits.get("who_2021_guidelines", {}))
        print(f"[OK] who_pollutant_limits.json loaded with {num_pollutants} pollutants")
    except Exception as e:
        print(f"[FAILED] who_pollutant_limits.json: {e}")
        files_ok = False
    
    # Test seasonal_climate.csv
    try:
        with open("data/seasonal_climate.csv") as f:
            lines = len(f.readlines())
        print(f"[OK] seasonal_climate.csv loaded with {lines} lines")
    except Exception as e:
        print(f"[FAILED] seasonal_climate.csv: {e}")
        files_ok = False
    
    print()
    return files_ok

def test_helpers():
    """Test helper functions."""
    print("=" * 60)
    print("TESTING HELPER FUNCTIONS")
    print("=" * 60)
    
    from utils.helpers import format_temperature, format_wind_direction, get_aqi_color
    
    tests_ok = True
    
    # Test temperature formatting
    try:
        result = format_temperature(28)
        assert result == "28°C", f"Expected '28°C', got '{result}'"
        print("[OK] format_temperature(28) = '28°C'")
    except Exception as e:
        print(f"[FAILED] format_temperature: {e}")
        tests_ok = False
    
    # Test wind direction
    try:
        result = format_wind_direction(0)
        assert result == "N", f"Expected 'N', got '{result}'"
        result = format_wind_direction(90)
        assert result == "E", f"Expected 'E', got '{result}'"
        print("[OK] format_wind_direction works correctly")
    except Exception as e:
        print(f"[FAILED] format_wind_direction: {e}")
        tests_ok = False
    
    # Test AQI color
    try:
        color = get_aqi_color(4)
        assert color == "#ff4444", f"Expected '#ff4444', got '{color}'"
        print("[OK] get_aqi_color works correctly")
    except Exception as e:
        print(f"[FAILED] get_aqi_color: {e}")
        tests_ok = False
    
    print()
    return tests_ok

def test_api_counter():
    """Test API counter functionality."""
    print("=" * 60)
    print("TESTING API COUNTER")
    print("=" * 60)
    
    try:
        from utils.api_counter import get_counter, get_remaining_calls, get_usage_percentage
        
        counter = get_counter()
        assert "used" in counter, "Missing 'used' key"
        assert "total" in counter, "Missing 'total' key"
        assert counter["total"] == 100, "Total should be 100"
        
        remaining = get_remaining_calls()
        usage_pct = get_usage_percentage()
        
        print(f"[OK] API Counter: {counter['used']}/{counter['total']} calls used")
        print(f"[OK] Remaining: {remaining} calls")
        print(f"[OK] Usage: {usage_pct:.1f}%\n")
        return True
    except Exception as e:
        print(f"[FAILED] API counter: {e}\n")
        return False

def test_seasonal_data():
    """Test seasonal data loading."""
    print("=" * 60)
    print("TESTING SEASONAL DATA")
    print("=" * 60)
    
    try:
        from services.seasonal_data import get_all_months_for_city, prepare_season_chart_data
        
        # Test Jakarta data
        months = get_all_months_for_city("Jakarta", "Indonesia")
        assert len(months) == 12, f"Expected 12 months, got {len(months)}"
        print(f"[OK] Jakarta seasonal data: {len(months)} months loaded")
        
        # Test chart data preparation
        chart_data = prepare_season_chart_data("Bangkok", "Thailand")
        assert chart_data is not None, "Chart data should not be None"
        assert len(chart_data["months"]) == 12, "Should have 12 months"
        print(f"[OK] Chart data preparation works for Bangkok\n")
        return True
    except Exception as e:
        print(f"[FAILED] Seasonal data: {e}\n")
        return False

def test_astronomy_engine():
    """Test astronomy engine calculations."""
    print("=" * 60)
    print("TESTING ASTRONOMY ENGINE")
    print("=" * 60)
    
    try:
        from services.astro_engine import calculate_golden_hours, interpret_moon_phase
        
        # Test golden hours calculation
        golden = calculate_golden_hours("05:53 AM", "05:47 PM")
        assert "daylight_duration" in golden, "Missing daylight_duration"
        print(f"[OK] Golden hours calculated: {golden['daylight_duration']} daylight")
        
        # Test moon phase interpretation
        phase = interpret_moon_phase("Full Moon")
        assert phase["emoji"] == "🌕", "Full moon emoji incorrect"
        assert phase["label_en"] == "Full Moon", "Full moon label incorrect"
        print(f"[OK] Moon phase interpretation works\n")
        return True
    except Exception as e:
        print(f"[FAILED] Astronomy engine: {e}\n")
        return False

def test_aqi_engine():
    """Test AQI engine."""
    print("=" * 60)
    print("TESTING AQI ENGINE")
    print("=" * 60)
    
    try:
        from services.aqi_engine import get_aqi_label, get_aqi_color, check_pollutant_above_who
        
        # Test AQI label
        label = get_aqi_label(4, "en")
        assert label == "Unhealthy", f"Expected 'Unhealthy', got '{label}'"
        print("[OK] get_aqi_label works")
        
        # Test AQI color
        color = get_aqi_color(1)
        assert color == "#00ff87", f"Expected green color, got '{color}'"
        print("[OK] get_aqi_color works")
        
        # Test WHO pollutant check
        above = check_pollutant_above_who("pm2_5", 30)
        assert above == True, "PM2.5 30 should be above WHO limit (15)"
        print("[OK] WHO pollutant check works\n")
        return True
    except Exception as e:
        print(f"[FAILED] AQI engine: {e}\n")
        return False

def test_alert_engine():
    """Test alert engine."""
    print("=" * 60)
    print("TESTING ALERT ENGINE")
    print("=" * 60)
    
    try:
        from services.alert_engine import check_alert_condition
        
        # Create mock weather data
        current_data = {
            "uv_index": 9,
            "wind_speed": 70,
            "humidity": 85,
            "visibility": 5,
            "precip": 0
        }
        
        # Test conditions
        uv_alert = check_alert_condition(current_data, "uv", 8)
        assert uv_alert == True, "UV index should trigger alert"
        print("[OK] High UV alert triggered")
        
        wind_alert = check_alert_condition(current_data, "wind", 60)
        assert wind_alert == True, "High wind should trigger alert"
        print("[OK] High wind alert triggered")
        
        humidity_alert = check_alert_condition(current_data, "humidity", 90)
        assert humidity_alert == False, "Humidity 85 should not trigger 90 threshold"
        print("[OK] Humidity alert logic works\n")
        return True
    except Exception as e:
        print(f"[FAILED] Alert engine: {e}\n")
        return False

def main():
    """Run all tests."""
    print("\n")
    print("=" * 60)
    print("SEAWeather Dashboard - Component Test Suite".center(60))
    print("=" * 60 + "\n")
    
    results = []
    
    # Run all tests
    results.append(("Imports", test_imports()))
    results.append(("Data Files", test_data_files()))
    results.append(("Helpers", test_helpers()))
    results.append(("API Counter", test_api_counter()))
    results.append(("Seasonal Data", test_seasonal_data()))
    results.append(("Astronomy Engine", test_astronomy_engine()))
    results.append(("AQI Engine", test_aqi_engine()))
    results.append(("Alert Engine", test_alert_engine()))
    
    # Summary
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status} {test_name}")
    
    print("=" * 60)
    print(f"Total: {passed}/{total} tests passed")
    print("=" * 60 + "\n")
    
    if passed == total:
        print("[SUCCESS] All tests passed! Dashboard is ready to use.\n")
        return 0
    else:
        print(f"[FAILED] {total - passed} test(s) failed. Please check the output above.\n")
        return 1

if __name__ == "__main__":
    exit(main())
