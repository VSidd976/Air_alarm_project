import pandas as pd
import numpy as np
import schedule
import time

def process_data():
    df = pd.read_csv("final_dataset.csv")
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['year'] = df['datetime'].dt.year
    df['month'] = df['datetime'].dt.month
    df['day'] = df['datetime'].dt.day
    df['hour'] = df['datetime'].dt.hour
    df['minute'] = df['datetime'].dt.minute
    df['second'] = df['datetime'].dt.second

    df['date_only'] = df['datetime'].dt.date
    df['time'] = df['datetime'].dt.time
    df['day_sunrise'] = pd.to_datetime(df['day_sunrise'], format='%H:%M:%S', errors='coerce').dt.time
    df['day_sunset'] = pd.to_datetime(df['day_sunset'], format='%H:%M:%S', errors='coerce').dt.time

    df['sunrise_dt'] = pd.to_datetime(df['date_only'].astype(str) + ' ' + df['day_sunrise'].astype(str), errors='coerce')
    df['sunset_dt'] = pd.to_datetime(df['date_only'].astype(str) + ' ' + df['day_sunset'].astype(str), errors='coerce')

    df['sun'] = ((df['datetime'] >= df['sunrise_dt']) & (df['datetime'] <= df['sunset_dt'])).astype(int)

    df.drop(columns=['date_only', 'sunrise_dt', 'sunset_dt'], inplace=True)


    def clean_condition(val):
        if pd.isna(val):
            return ''
        val = str(val)
        val = val.replace('[', '').replace(']', '').replace("'", '').replace('"', '')
        return val.strip().title()

    df['hour_conditions'] = df['hour_conditions'].apply(clean_condition)
    condition_labels = [
        'Clear', 'Ice', 'Snow', 'Overcast', 'Rain', 'Fog',
        'Partially cloudy', 'Freezing Drizzle/Freezing Rain'
    ]

    for label in condition_labels:
        df[label] = 0

    for label in condition_labels:
        df.loc[df['hour_conditions'] == label, label] = 1


    columns_to_drop = ['day_datetime', 'datetime', 'day_preciptype', 'day_sunrise', 'day_sunset',
                       'day_conditions', 'hour_datetime', 'hour_conditions']
    df.drop(columns=columns_to_drop, inplace=True, errors='ignore')
    df.rename(columns={
        'telegram_vector': 'tg_vector',
        'article_vector': 'isw_vector',
        'risk': 'hol_risk'
    }, inplace=True)

    df['alarms'] = 0
    df.fillna(0, inplace=True)
    y = int(df.loc[0, 'year'])
    m = int(df.loc[0, 'month'])
    d = int(df.loc[0, 'day'])

    filename = f"processed_final_{y}_{m}_{d}.csv"

    df.to_csv(filename, index=False)
    print("processed_final.csv succesfully saved")
    
def schedule_task():
    SCHEDULED_HOUR = 6 
    SCHEDULED_MINUTE = 0

    schedule.every().day.at(f"{SCHEDULED_HOUR:02d}:{SCHEDULED_MINUTE:02d}").do(process_data)

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    schedule_task()