# import requests
# from app.config.settings import OPENWEATHER_API_KEY

# def get_weather(city: str):
#     url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
#     response = requests.get(url)
#     if response.status_code == 200:
#         data = response.json()
#         return f"The weather in {city} is {data['weather'][0]['description']} with temperature {data['main']['temp']}°C."
#     else:
#         return "Couldn't fetch weather data."
#  app/services/weather.py
import requests
import os
from typing import Optional

def get_weather(query: str, location: str = "London") -> str:
    """
    Get weather information using OpenWeatherMap API
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if not api_key:
        return "Weather service not configured. Please set OPENWEATHER_API_KEY environment variable."
    
    try:
        # Extract location from query if possible
        extracted_location = extract_location_from_query(query)
        if extracted_location:
            location = extracted_location
            
        # OpenWeatherMap API endpoint
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": location,
            "appid": api_key,
            "units": "metric"  # For Celsius
        }
        
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Format the weather response
        weather_info = {
            "location": data["name"],
            "country": data["sys"]["country"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"]
        }
        
        return format_weather_response(weather_info)
        
    except requests.exceptions.RequestException as e:
        return f"Failed to fetch weather data: Network error - {str(e)}"
    except KeyError as e:
        return f"Failed to parse weather data: Missing field - {str(e)}"
    except Exception as e:
        return f"Weather service error: {str(e)}"

def extract_location_from_query(query: str) -> Optional[str]:
    """
    Simple location extraction from query
    """
    # Common location indicators
    location_words = ["in", "at", "for", "weather in", "temperature in"]
    query_lower = query.lower()
    
    for word in location_words:
        if word in query_lower:
            parts = query_lower.split(word)
            if len(parts) > 1:
                potential_location = parts[-1].strip()
                # Clean up the location string
                potential_location = potential_location.replace("?", "").replace("today", "").strip()
                if potential_location and len(potential_location) > 1:
                    return potential_location
    
    return None

def format_weather_response(weather_info: dict) -> str:
    """
    Format weather information into a readable response
    """
    return f"""Weather in {weather_info['location']}, {weather_info['country']}:
🌡️ Temperature: {weather_info['temperature']}°C (feels like {weather_info['feels_like']}°C)
☁️ Conditions: {weather_info['description'].title()}
💧 Humidity: {weather_info['humidity']}%
💨 Wind Speed: {weather_info['wind_speed']} m/s"""