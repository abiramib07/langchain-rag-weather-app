def is_weather_query(query: str) -> bool:
    weather_keywords = [
        "weather", "temperature", "forecast", "humidity", 
        "rain", "sunny", "cloudy", "hot", "cold", "warm",
        "temp", "climate", "precipitation", "wind"
    ]
    return any(word in query.lower() for word in weather_keywords)