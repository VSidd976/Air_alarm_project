import requests
import csv
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

CITY = "Kyiv"
UNIT_GROUP = "metric"

URL = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{CITY}/next24hours?unitGroup={UNIT_GROUP}&include=hours&key={API_KEY}&contentType=json"

def get_weather():
    response = requests.get(URL)

    if response.status_code == 200:
        data = response.json()
        forecast_hours = data["days"][0]["hours"]

        weather_data = []
        for hour in forecast_hours:
            weather_info = {
                "Time": hour["datetime"],
                "Temperature (°C)": hour["temp"],
                "Feels Like (°C)": hour["feelslike"],
                "Wind Speed (km/h)": hour["windspeed"],
                "Wind Direction": hour["winddir"],
                "Humidity (%)": hour["humidity"],
                "Precipitation (mm)": hour.get("precip", 0),
                "Cloud Cover (%)": hour["cloudcover"],
                "UV Index": hour["uvindex"],
                "Conditions": hour["conditions"]
            }
            weather_data.append(weather_info)

        save_to_csv(weather_data)
        print(f"Forecast for 24 hours is received for {CITY}")
        return weather_data
    else:
        print(f"Error while receiving forecast: {response.status_code}")
        return None

def save_to_csv(weather_data):
    filename = f"weather_forecast_{datetime.now().strftime('%Y-%m-%d')}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=weather_data[0].keys())
        writer.writeheader()
        writer.writerows(weather_data)

    print(f"File is saved: {filename}")

if __name__ == "__main__":
    weather_data = get_weather()
    if weather_data:
        print("🌤 Start forecast is received and saved.")
