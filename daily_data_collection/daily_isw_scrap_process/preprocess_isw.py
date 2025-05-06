import pandas as pd
import numpy as np
import re
import pickle
import csv
import schedule
import time
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer


custom_stopwords = {
    'the', 'and', 'for', 'that', 'with', 'this', 'from', 'you', 'your', 'are', 'but', 'not', 'all', 'any', 'can',
    'have', 'has', 'had', 'was', 'were', 'will', 'would', 'should', 'could', 'about', 'they', 'them', 'their',
    'then', 'there', 'what', 'when', 'which', 'who', 'whom', 'where', 'why', 'how', 'into', 'out', 'our', 'his',
    'her', 'its', 'also', 'more', 'most', 'some', 'such', 'no', 'nor', 'only', 'own', 'same', 'so', 'than', 'too',
    'very', 'just', 'on', 'in', 'at', 'by', 'an', 'be', 'is', 'it', 'of', 'to', 'as', 'a', 'or', 'if', 'we', 'he',
    'she', 'do', 'does', 'did'
}


def simple_stem(word):
    suffixes = ['ing', 'ly', 'ed', 'ious', 'ies', 'ive', 'es', 's', 'ment']
    for suffix in suffixes:
        if word.endswith(suffix) and len(word) > len(suffix) + 2:
            return word[:-len(suffix)]
    return word


def full_clean_text(text):
    if pd.isnull(text):
        return ''
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'isw.?s interactive map of the russian invasion of ukraine.*?static maps present in this report', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Click.*?(?=[A-Z]|$)', '', text, flags=re.DOTALL)
    text = re.sub(r'^.*?\b(am|pm)\b\s*(et)?', '', text, flags=re.IGNORECASE)
    text = re.sub(r'http[s]?://\S+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)  # видалення чисел
    text = re.sub(r'\s+', ' ', text).strip().lower()
    return text


def clean_and_stem(text):
    words = text.split()
    filtered = [simple_stem(word) for word in words if word not in custom_stopwords and word.isalpha()]
    return ' '.join(filtered)


def process_data():
    input_file = "isw_data.txt"
    output_file = "processed_isw.csv"

    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()

    date_match = re.search(r'([A-Za-z]+ \d{1,2}, \d{4})', text)
    if date_match:
        date_str = date_match.group(1)
        date_obj = datetime.strptime(date_str, "%B %d, %Y")
        formatted_date = date_obj.strftime("%Y-%m-%d")
    else:
        formatted_date = ""

    cleaned_text = clean_and_stem(full_clean_text(text))

    with open(output_file, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["date", "processed_text"])
        writer.writeheader()
        writer.writerow({"date": formatted_date, "processed_text": cleaned_text})

    df = pd.read_csv(output_file)

    with open('tfidf_vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)

    X_tfidf = vectorizer.transform(df['processed_text'])
    article_vector_means = X_tfidf.sum(axis=1) / (X_tfidf != 0).sum(axis=1)
    article_vector_means = np.squeeze(np.asarray(np.nan_to_num(article_vector_means)))

    df['article_vector'] = article_vector_means
    df_out = df.drop(columns=['processed_text'])
    df_out.to_csv(output_file, index=False)

    print(f"Processed and saved: {output_file}")

SCHEDULED_HOUR = 23
SCHEDULED_MINUTE = 44
schedule.every().day.at(f"{SCHEDULED_HOUR:02d}:{SCHEDULED_MINUTE:02d}").do(process_data)

while True:
    schedule.run_pending()
    time.sleep(60)
