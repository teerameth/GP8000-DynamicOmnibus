import requests
from typing import Dict, Optional, Tuple


class WeatherDataCollector:
    def __init__(self):
        """Initialize the weather data collector using wttr.in service"""
        self.base_url = "https://wttr.in/{city}?format=j1"

    def get_weather_data(self, city: str) -> Optional[Dict]:
        """
        Get weather data for a specific city.

        Args:
            city (str): City name

        Returns:
            Optional[Dict]: Weather data or None if request fails
        """
        try:
            url = self.base_url.format(city=city)
            response = requests.get(url, headers={'Accept': 'application/json'})
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None

    def process_weather_metrics(self, data: Dict) -> Tuple[float, float]:
        """
        Process weather data to extract and normalize rain chance and UV index.

        Args:
            data (Dict): Raw weather data

        Returns:
            Tuple[float, float]: Normalized rain chance and UV index
        """
        # Extract humidity and cloud coverage
        current = data['current_condition'][0]
        humidity = float(current['humidity']) / 100  # Humidity is in percentage
        clouds = float(current['cloudcover']) / 100  # Cloud coverage is in percentage

        # Calculate rain chance based on humidity and clouds
        rain_chance = (humidity * 0.6 + clouds * 0.4)
        rain_chance = max(0.0, min(1.0, rain_chance))

        # Get UV index (wttr.in provides it directly)
        uv_index = float(current['uvIndex']) / 11.0  # Normalize from 0-11 scale to 0-1
        uv_index = max(0.0, min(1.0, uv_index))

        return rain_chance, uv_index


def main():
    collector = WeatherDataCollector()

    # Get city from user
    city = "Singapore"
    print(f"\nFetching weather data for {city}...")

    weather_data = collector.get_weather_data(city)

    if weather_data:
        rain_chance, uv_index = collector.process_weather_metrics(weather_data)

        # Print current weather information
        current = weather_data['current_condition'][0]
        print(f"\nCurrent weather in {city}:")
        print(f"Temperature: {current['temp_C']}°C")
        print(f"Condition: {current['weatherDesc'][0]['value']}")
        print(f"Humidity: {current['humidity']}%")
        print(f"Cloud Cover: {current['cloudcover']}%")
        print(f"\nCalculated Metrics:")
        print(f"Rain chance (0-1): {rain_chance:.2f}")
        print(f"UV index (0-1): {uv_index:.2f}")
    else:
        print("Failed to fetch weather data")


if __name__ == "__main__":
    main()