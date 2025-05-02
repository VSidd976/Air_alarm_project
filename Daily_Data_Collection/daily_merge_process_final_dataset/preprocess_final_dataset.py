import pandas as pd
import numpy as np
import schedule
import time

def process_data():
    df = pd.read_csv("final.csv")
    df = df.drop(columns=[
        'Unnamed: 0', 'anomaly', 'text_vector', 'Engels2_x', 'Baltimore_x', 'Saki_x',
        'Belbek_x', 'Olenya_x', 'Mozdok_x', 'Savasleyka_x', 'datetime', 'risk','article_vector'
    ])

    df = df.rename(columns={
        'hour_clear': 'Clear',
        'hour_ice': 'Ice',
        'hour_snow_condition': 'Snow',
        'hour_overcast': 'Overcast',
        'hour_rain': 'Rain',
        'hour_fog': 'Fog',
        'hour_partially_cloudy': 'Partially cloudy',
        'hour_freezing_drizzle_rain': 'Freezing Drizzle/Freezing Rain',
        'telegram_vector': 'isw_vector',
        'date': 'datetime',
        'Engels2_y': 'Engels2',
        'Baltimore_y': 'Baltimore',
        'Saki_y': 'Saki',
        'Belbek_y': 'Belbek',
        'Olenya_y': 'Olenya',
        'Mozdok_y': 'Mozdok',
        'Savasleyka_y': 'Savasleyka',
        'hour_snow_h' : 'hour_snow'
    })

    df[['isw_vector', 'hol_risk', 'tg_vector', 'sun']] = df[['isw_vector', 'hol_risk', 'tg_vector', 'sun']].fillna(0)

    df['datetime'] = pd.to_datetime(df['datetime'])
    df['year'] = df['datetime'].dt.year
    df['month'] = df['datetime'].dt.month
    df['day'] = df['datetime'].dt.day
    df['hour'] = df['datetime'].dt.hour
    df['minute'] = df['datetime'].dt.minute
    df['second'] = df['datetime'].dt.second

    df.to_csv("processed_final.csv", index=False)

def schedule_task():
    SCHEDULED_HOUR = 6 
    SCHEDULED_MINUTE = 0

    schedule.every().day.at(f"{SCHEDULED_HOUR:02d}:{SCHEDULED_MINUTE:02d}").do(process_data)

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    schedule_task()