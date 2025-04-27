import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from joblib import dump
from pathlib import Path


def tg_vectoriser(tg_df):
    print("\nTelegram data vectorising began")
    vectorizer = TfidfVectorizer(max_features=1000)
    dump(vectorizer, "telegram_tfidf.pkl")

    X_tfidf = vectorizer.fit_transform(tg_df['message'])
    message_vectors = X_tfidf.mean(axis=1)
    message_vectors_df = pd.DataFrame(message_vectors, columns=[f'feat_{i}' for i in range(message_vectors.shape[1])])

    tg_df['text_vector'] = message_vectors_df.astype('float64').values

    print("Telegram data vectorising ended")


def find_avg_vectors(tg_df, target_df):
    average_vectors = []
    for _, row in target_df.iterrows():
        datetime = row['datetime']
        time_window_start = datetime - pd.Timedelta(hours=1)
        time_window_end = datetime

        filtered_messages = tg_df[(tg_df['date'] >= time_window_start) & (tg_df['date'] < time_window_end)]

        if len(filtered_messages) > 0:
            filtered_messages = filtered_messages.sort_values(by='date', ascending=False)
            top_100_messages = filtered_messages.head(100)
            vectors = np.stack(top_100_messages['text_vector'].tolist())

            avg_vector = np.mean(vectors, axis=0)
        else:
            avg_vector = np.nan

        average_vectors.append({'datetime': datetime, 'telegram_vector': avg_vector})

    df_avg_vectors = pd.DataFrame(average_vectors)
    return df_avg_vectors


def main():
    current_dir = Path(__file__).parent
    tg_data_path = current_dir.parent / 'telegram_parser' / 'telegram_data.csv'
    df_tg = pd.read_csv(tg_data_path, delimiter=",", low_memory=False)
    df_tg['date'] = pd.to_datetime(df_tg['date'])

    tg_vectoriser(df_tg)
    df_tg = df_tg.drop(columns='message')
    df_tg.to_csv('vectorised_telegram_data.csv', index=False)

    main_data_path = current_dir.parent / 'merge' / 'df_alt2.csv'
    df = pd.read_csv(main_data_path, delimiter=",")

    print("\nTelegram data preparation for merge began")
    df['datetime'] = pd.to_datetime(df['datetime'])
    df_tg['text_vector'] = df_tg['text_vector'].astype(np.float64)
    avg_df_tg = find_avg_vectors(df_tg, df)
    print("Telegram data preparation for merge ended")
    avg_df_tg.to_csv("average_tg_vectors.csv", index=False)


if __name__ == '__main__':
    main()
