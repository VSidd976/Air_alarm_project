import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
UNIT_GROUP = "metric"


def get_weather_for_city(city):
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/next24hours?unitGroup={UNIT_GROUP}&include=hours&key={API_KEY}&contentType=json"

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching weather for {city}: {response.status_code}")
        return None
