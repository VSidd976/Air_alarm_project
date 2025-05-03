import pandas as pd
from pathlib import Path
from joblib import load


def tg_vectoriser(tg_df):
    print("\nTelegram data vectorising began")
    current_dir = Path(__file__).parent
    tfidf_path = current_dir.parent.parent / 'Data_Processing' / 'telegram_processing' / 'telegram_tfidf.pkl'
    vectoriser = load(tfidf_path)

    X_tfidf = vectoriser.fit_transform(tg_df['message'])
    message_vectors = X_tfidf.mean(axis=1)
    message_vectors_df = pd.DataFrame(message_vectors, columns=[f'feat_{i}' for i in range(message_vectors.shape[1])])

    tg_df['text_vector'] = message_vectors_df.astype('float64').values
    print("Telegram data vectorising ended")


def main():
    df_tg = pd.read_csv('hour_parsed_telegram_data.csv', delimiter=",", low_memory=False)
    df_tg['date'] = pd.to_datetime(df_tg['date'])

    tg_vectoriser(df_tg)
    df_tg = df_tg.drop(columns='message')
    df_tg.to_csv('hour_vectorised_telegram_data.csv', index=False)


if __name__ == '__main__':
    main()
