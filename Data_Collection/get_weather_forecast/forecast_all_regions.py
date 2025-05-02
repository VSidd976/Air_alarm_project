from get_weather_for_city import get_weather_for_city
import csv
from datetime import datetime
import os
import json

forecast_folder = "/Users/admin/Documents/Romko/NAUKMA/AppliedMaths/3/PythonDS2025/HW4/weather_forecast/forecast"
cities = ["Kyiv", "Lviv", "Odesa", "Dnipro", "Kharkiv", "Zaporizhzhia", "Ivano-Frankivsk", "Ternopil", "Chernihiv", "Cherkasy", "Zhytomyr", "Poltava", "Lutsk", "Sumy", "Donetsk", "Luhansk", "Mykolaiv", "Kherson", "Chernivtsi", "Kropyvnytskyi", "Khmelnytskyi", "Vinnytsia", "Rivne", "Uzhhorod", "Simferopol"]
all_cities_filename = f"weather_all_cities_{datetime.now().strftime('%Y-%m-%d')}.csv"
all_cities_filepath = os.path.join(forecast_folder, all_cities_filename)

def save_all_cities_weather(cities, output_filepath):
    if not os.path.exists(forecast_folder):
        os.makedirs(forecast_folder)

    headers_written = False

    with open(output_filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        all_headers = [
            'city_address', 'day_precip', 'day_precipcover', 'day_snow',
            'day_windspeed', 'day_winddir', 'day_uvindex', 'hour_temp',
            'hour_humidity', 'hour_precip', 'hour_precipprob', 'hour_snow_h',
            'hour_windspeed', 'hour_winddir', 'hour_pressure', 'hour_visibility',
            'hour_cloudcover', 'hour_uvindex', 'hour_datetime', 'hour_clear', 'hour_ice', 'hour_snow_condition',
            'hour_overcast', 'hour_rain', 'hour_fog', 'hour_partially_cloudy',
            'hour_freezing_drizzle_rain', 'anomaly', 'alarms', 'date',
            'text_vector', 'tg_vector', 'sun', 'Engels2', 'Baltimore', 'Saki',
            'Belbek', 'Olenya', 'Mozdok', 'Savasleyka', 'hol_risk'
        ]

        for city in cities:
            data = get_weather_for_city(city)
            if data:
                print(f"JSON Response for {city}:")
                print(json.dumps(data, indent=4))

                if "days" in data and len(data["days"]) > 0 and "hours" in data["days"][0]:
                    for hour_data in data["days"][0].get("hours", []):
                        datetime_str = hour_data.get("datetime")
                        if datetime_str:
                            try:
                                # Спробуємо спочатку розпарсити як час, якщо це спрацює, об'єднаємо з датою
                                try:
                                    time_obj = datetime.strptime(datetime_str, "%H:%M:%S")
                                    date_str = data["days"][0].get("datetime", datetime.now().strftime("%Y-%m-%d")) # Отримаємо дату з day або поточну дату
                                    timestamp = datetime.strptime(f"{date_str} {datetime_str}", "%Y-%m-%d %H:%M:%S")
                                    local_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                                except ValueError:
                                    # Якщо не спрацював формат часу, спробуємо оригінальний формат
                                    timestamp = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S")
                                    local_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")

                                conditions = hour_data.get("conditions", "").lower()

                                row_data = [
                                    city,
                                    data["days"][0].get("precip", 0),
                                    data["days"][0].get("precipcover", 0),
                                    data["days"][0].get("snow", 0),
                                    data["days"][0].get("windspeed", 0),
                                    data["days"][0].get("winddir", 0),
                                    data["days"][0].get("uvindex", 0),
                                    hour_data.get("temp"),
                                    hour_data.get("humidity"),
                                    hour_data.get("precip", 0),
                                    hour_data.get("precipprob", 0),
                                    hour_data.get("snow", 0),
                                    hour_data.get("windspeed"),
                                    hour_data.get("winddir"),
                                    hour_data.get("pressure"),
                                    hour_data.get("visibility"),
                                    hour_data.get("cloudcover"),
                                    hour_data.get("uvindex"),
                                    local_time,
                                    1 if "clear" in conditions else 0,
                                    1 if "ice" in conditions else 0,
                                    1 if "snow" in conditions else 0,
                                    1 if "overcast" in conditions else 0,
                                    1 if "rain" in conditions else 0,
                                    1 if "fog" in conditions else 0,
                                    1 if "partially cloudy" in conditions else 0,
                                    1 if "freezing drizzle" in conditions else (
                                        1 if "freezing rain" in conditions else 0),
                                    "",
                                    "",
                                    timestamp.strftime("%Y-%m-%d"),
                                    "",
                                    "",
                                    "",
                                    "",
                                    "",
                                    "",
                                    "",
                                    "",
                                    "",
                                    "",
                                ]
                                print(f"Local Time: {local_time}")
                                print(f"Row Data: {row_data}")
                                if not headers_written:
                                    writer.writerow(all_headers)
                                    headers_written = True
                                writer.writerow(row_data)
                            except ValueError as e:
                                print(f"Error parsing datetime for {city}: {e} - Data: {hour_data}")
                        else:
                            print(f"Warning: 'datetime' not found in hourly data for {city}. Skipping.")
                else:
                    print(f"Warning: No 'days' or 'hours' data found for {city}.")
            else:
                print(f"Failed to get weather data for {city}.")

    print(f"Weather data for all cities saved to {output_filepath}")

if __name__ == "__main__":
    save_all_cities_weather(cities, all_cities_filepath)