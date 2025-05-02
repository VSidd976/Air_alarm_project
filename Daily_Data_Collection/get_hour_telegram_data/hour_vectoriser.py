import pandas as pd
import numpy as np
from pathlib import Path
from joblib import load
from datetime import datetime


def tg_vectoriser(tg_df):
    print("\nTelegram data vectorising began")
    current_dir = Path(__file__).parent
    tfidf_path = current_dir.parent / 'telegram_vectoriser' / 'telegram_tfidf.pkl'
    vectoriser = load(tfidf_path)

    X_tfidf = vectoriser.fit_transform(tg_df['message'])
    message_vectors = X_tfidf.mean(axis=1)
    message_vectors_df = pd.DataFrame(message_vectors, columns=[f'feat_{i}' for i in range(message_vectors.shape[1])])

    tg_df['text_vector'] = message_vectors_df.astype('float64').values
    print("Telegram data vectorising ended")


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
    df_tg = pd.read_csv('hour_parsed_telegram_data.csv', delimiter=",", low_memory=False)
    df_tg['date'] = pd.to_datetime(df_tg['date'])

    tg_vectoriser(df_tg)
    df_tg = df_tg.drop(columns='message')
    df_tg.to_csv('hour_vectorised_telegram_data.csv', index=False)


if __name__ == '__main__':
    main()
