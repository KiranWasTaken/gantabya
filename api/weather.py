import requests

def get_weather(city_name):
    """
    Fetch weather data for a given city using OpenWeatherMap API.
    """
    api_key = "7f5b5289cf6bb8fbb9342592f2adeee6"  # Replace with your OpenWeatherMap API Key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }
    except requests.exceptions.RequestException as e:
        return {"error": "Unable to fetch weather data", "details": str(e)}
