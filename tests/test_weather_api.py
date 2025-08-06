import pytest
from app.services.weather import format_weather_response, get_weather, extract_location_from_query
from unittest.mock import patch, MagicMock

def test_extract_location_from_query():
    query = "What is the weather in New York today?"
    loc = extract_location_from_query(query)
    assert loc.lower() == "new york"

def test_format_weather_response():
    info = {
        "location": "Paris",
        "country": "FR",
        "temperature": 20,
        "feels_like": 18,
        "humidity": 50,
        "description": "clear sky",
        "wind_speed": 3.5
    }
    formatted = format_weather_response(info)
    assert "Paris" in formatted
    assert "°C" in formatted
    assert "clear sky" in formatted.lower()  # Case insensitive

@patch("app.services.weather.requests.get")
def test_get_weather_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "name": "London",
        "sys": {"country": "GB"},
        "main": {"temp": 15, "feels_like": 14, "humidity": 60},
        "weather": [{"description": "light rain"}],
        "wind": {"speed": 4.0}
    }
    mock_get.return_value = mock_response

    response = get_weather("weather in London")
    assert "London" in response
    assert "temperature" in response.lower()

@patch("app.services.weather.requests.get")
def test_get_weather_api_failure(mock_get):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception("404 Client Error")
    mock_get.return_value = mock_response

    response = get_weather("weather in UnknownPlace")
    assert "weather service error" in response.lower()

