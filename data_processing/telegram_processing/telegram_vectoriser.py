import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from joblib import dump


def tg_vectoriser(tg_df):
    print("\nTelegram data vectorising began")
    vectorizer = TfidfVectorizer(max_features=1000)
    dump(vectorizer, "telegram_tfidf.pkl")

    X_tfidf = vectorizer.fit_transform(tg_df['message'])
    message_vectors = X_tfidf.mean(axis=1)
    message_vectors_df = pd.DataFrame(message_vectors, columns=[f'feat_{i}' for i in range(message_vectors.shape[1])])

    tg_df['text_vector'] = message_vectors_df.astype('float64').values

    print("Telegram data vectorising ended")


def main():
    df_tg = pd.read_csv('parsed_telegram_data.csv', delimiter=",", low_memory=False)
    df_tg['date'] = pd.to_datetime(df_tg['date'])

    tg_vectoriser(df_tg)
    df_tg = df_tg.drop(columns='message')
    df_tg.to_csv('vectorised_telegram_data.csv', index=False)


if __name__ == '__main__':
    main()
