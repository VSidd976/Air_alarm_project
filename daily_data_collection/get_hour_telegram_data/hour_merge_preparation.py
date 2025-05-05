import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime


def find_avg_vectors(tg_df, main_df):
    average_vector = []
    current_time = datetime.now().replace(minute=0, second=0, microsecond=0)
    time_window_start = current_time - pd.Timedelta(hours=1)
    time_window_end = current_time

    main_df = pd.concat([main_df, tg_df], ignore_index=True)

    filtered_messages = main_df[(main_df['date'] >= time_window_start) & (main_df['date'] < time_window_end)]

    if len(filtered_messages) > 0:
        filtered_messages = filtered_messages.sort_values(by='date', ascending=False)
        top_100_messages = filtered_messages.head(100)
        vectors = np.stack(top_100_messages['text_vector'].tolist())

        avg_vector = np.mean(vectors, axis=0)

    else:
        avg_vector = 0

    average_vector.append({'datetime': current_time, 'telegram_vector': avg_vector})
    df_avg_vector = pd.DataFrame(average_vector)

    return df_avg_vector


def main():
    current_dir = Path(__file__).parent
    main_vectors_data_path = current_dir.parent.parent / 'Data_Processing' / 'telegram_processing' / 'vectorised_telegram_data.csv'
    df_tg = pd.read_csv('hour_vectorised_telegram_data.csv', delimiter=',')
    df = pd.read_csv(main_vectors_data_path, delimiter=",")

    print("\nTelegram data preparation for merge began")
    df['date'] = pd.to_datetime(df['date'])
    df_tg['text_vector'] = df_tg['text_vector'].astype(np.float64)
    avg_df_tg = find_avg_vectors(df_tg, df)
    print("Telegram data preparation for merge ended")
    avg_df_tg.to_csv("average_telegram_vectors.csv", index=False)
    df_tg.to_csv(main_vectors_data_path, mode='a', index=False, header=False)


if __name__ == '__main__':
    main()
