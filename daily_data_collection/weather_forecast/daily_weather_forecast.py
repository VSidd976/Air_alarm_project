import pandas as pd
import os
import requests
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("API_KEY")


UNIT_GROUP = "metric"

# Cities to process
UKRAINIAN_CITIES = [
    "Kyiv, Ukraine", "Lviv, Ukraine", "Odesa, Ukraine", "Dnipro, Ukraine", "Kharkiv, Ukraine", "Zaporizhzhia, Ukraine",
    "Ivano-Frankivsk, Ukraine", "Ternopil, Ukraine", "Chernihiv, Ukraine", "Cherkasy, Ukraine", "Zhytomyr, Ukraine",
    "Poltava, Ukraine", "Lutsk, Ukraine", "Sumy, Ukraine", "Donetsk, Ukraine", "Luhansk, Ukraine", "Mykolaiv, Ukraine",
    "Kherson, Ukraine", "Chernivtsi, Ukraine", "Kropyvnytskyi, Ukraine", "Khmelnytskyi, Ukraine", "Vinnytsia, Ukraine",
    "Rivne, Ukraine", "Uzhhorod, Ukraine", "Simferopol, Ukraine"
]


# Columns to remove
columns_to_delete = [
    'city_latitude', 'city_longitude', 'city_resolvedAddress', 'city_timezone', 'city_tzoffset',
    'day_datetimeEpoch', 'day_feelslikemax', 'day_feelslikemin', 'day_feelslike', 'day_precipprob',
    'day_snowdepth', 'day_sunriseEpoch', 'day_sunsetEpoch', 'day_moonphase', 'day_description', 'day_icon',
    'day_source', 'day_stations', 'hour_datetimeEpoch', 'hour_feelslike', 'hour_dew', 'hour_snowdepth',
    'hour_icon', 'hour_source', 'hour_stations', 'day_tempmax', 'day_tempmin', 'day_dew', 'day_temp',
    'day_humidity', 'day_windgust', 'day_pressure', 'day_cloudcover', 'day_visibility', 'day_solarradiation',
    'day_solarenergy', 'hour_windgust', 'hour_solarradiation', 'hour_solarenergy', 'hour_severerisk', 'day_severerisk'
]


def get_weather_for_city(city):
    url = (
        f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/"
        f"timeline/{city}/next24hours?unitGroup={UNIT_GROUP}&include=hours&key={API_KEY}&contentType=json"
    )
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        #print(f"Error fetching weather for {city}: HTTP {response.status_code}")
        return None


def unpack_weather_json_to_rows(data):
    if not data:
        return []

    base_info = {
        'city_latitude': data.get('latitude'),
        'city_longitude': data.get('longitude'),
        'city_resolvedAddress': data.get('resolvedAddress'),
        'city_address': data.get('address'),
        'city_timezone': data.get('timezone'),
        'city_tzoffset': data.get('tzoffset'),
    }

    rows = []
    for day in data.get('days', []):
        day_info = {f'day_{k}': v for k, v in day.items() if k != 'hours'}
        for hour in day.get('hours', []):
            hour_info = {f'hour_{k}': v for k, v in hour.items()}
            row = {**base_info, **day_info, **hour_info}

            # Remove unwanted columns
            for col in columns_to_delete:
                row.pop(col, None)

            rows.append(row)
    return rows


def collect_weather_for_all_cities(cities):
    all_rows = []
    for city in cities:
        #print(f" Fetching weather for {city}...")
        data = get_weather_for_city(city)
        city_rows = unpack_weather_json_to_rows(data)
        all_rows.extend(city_rows)
    return pd.DataFrame(all_rows)


df = collect_weather_for_all_cities(UKRAINIAN_CITIES)
df.to_csv("ukraine_weather_combined.csv", index=False)
#print("Combined weather CSV saved to 'ukraine_weather_combined.csv'")
