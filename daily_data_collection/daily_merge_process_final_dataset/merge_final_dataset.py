import pandas as pd
import schedule
import time

def process_data():

    hol = pd.read_csv("holidays.csv")
    dis = pd.read_csv("distances.csv")
    weather = pd.read_csv("ukraine_weather_combined.csv")

    tg = pd.read_csv("average_telegram_vectors.csv")
    isw = pd.read_csv("isw_data.csv")

    tg['datetime'] = pd.to_datetime(tg['datetime'])
    tg['date'] = tg['datetime'].dt.date

    hours = pd.date_range('00:00', '23:00', freq='H').time
    tg = tg.merge(pd.DataFrame({'hour': hours}), how='cross')
    tg['datetime'] = pd.to_datetime(tg['date'].astype(str) + ' ' + tg['hour'].astype(str))
    tg = tg.drop(columns=['hour'])

    isw['date'] = pd.to_datetime(isw['date']).dt.date
    hol['date'] = pd.to_datetime(hol['date_converted']).dt.date

    merged = tg.merge(isw, on='date', how='left')
    merged = merged.merge(hol[['date', 'risk']], on='date', how='left')
    merged['risk'] = merged['risk'].fillna(0)
    merged = merged.drop(columns=['date'])

    final = merged.assign(key=1).merge(dis.assign(key=1), on='key').drop('key', axis=1)
    final['City'] = final['City'].replace('Zaporozhye', 'Zaporizhzhia')

    weather.rename(columns={'city_address': 'City'}, inplace=True)
    weather['datetime'] = pd.to_datetime(weather['day_datetime'] + ' ' + weather['hour_datetime'])
    weather['City'] = weather['City'].str.replace(', Ukraine', '', regex=False).str.strip()
    weather['City'] = weather['City'].replace('Uzhhorod', 'Uzhgorod')


    final = pd.merge(weather, final, on=['datetime', 'City'], how='inner')
    print("Data processing complete and saved to final_output.csv")


def schedule_task():

    SCHEDULED_HOUR = 6 
    SCHEDULED_MINUTE = 0

    schedule.every().day.at(f"{SCHEDULED_HOUR:02d}:{SCHEDULED_MINUTE:02d}").do(process_data)

    while True:
        schedule.run_pending()
        time.sleep(60)  

if __name__ == "__main__":
    schedule_task()

