import pandas as pd
import numpy as np
import sklearn
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import csv
import schedule
import time
from datetime import datetime

def clean_text(text, n=600):
    if pd.isnull(text):
        return ''
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'isw.?s interactive map of.*?static maps present in this report', '', text, flags=re.IGNORECASE)
    text = re.sub(r'Click.*?(?=[A-Z]|$)', '', text, flags=re.DOTALL)
    text = re.sub(r'\d{1,2}[:\d]*\s*(am|pm|et)?', '', text, flags=re.IGNORECASE)
    text = re.sub(r'http[s]?://\S+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = text[n:].strip()
    return text.lower()

class SimpleStemmer:
    def __init__(self):
        self.rules = [
            (r'(ed|ing)$', ''),
            (r'(es|s)$', ''),
            (r'ies$', 'y'),
            (r'(ive|ize|ation|al|ful|less|ness)$', ''),
            (r'(er|ic|ous|able|ible)$', ''),
            (r'(ment|ant|ent)$', ''),
            (r'(ly)$', ''),
            (r'($)', '')
        ]
    
    def stem(self, word):
        for rule, replacement in self.rules:
            if re.search(rule, word):
                word = re.sub(rule, replacement, word)
        return word.lower()

def clean_and_stem(text):
    stop_words = set([
        'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves',
        'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their',
        'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was',
        'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and',
        'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
        'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on',
        'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all',
        'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same',
        'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'd', 'll', 'm', 'o', 're', 've',
        'y', 'ain', 'aren', 'couldn', 'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn', 'mustn', 'needn', 'shan',
        'shouldn', 'wasn', 'weren', 'won', 'wouldn'
    ])

    words = re.findall(r'\b\w+\b', text)
    stemmer = SimpleStemmer()
    filtered_words = [
        stemmer.stem(word)
        for word in words
        if word.lower() not in stop_words and word.isalpha()
    ]
    
    return ' '.join(filtered_words)

def process_data():
    input_file = "isw_data.txt"
    output_file = "isw_data.csv"
    
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()
    
    date_match = re.search(r'([A-Za-z]+ \d{1,2}, \d{4})', text)
    if date_match:
        date_str = date_match.group(1)
        date_obj = datetime.strptime(date_str, "%B %d, %Y")
        formatted_date = date_obj.strftime("%Y-%m-%d")
    else:
        formatted_date = ""

    with open(output_file, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["date", "Bold Text"])
        writer.writeheader()
        writer.writerow({"date": formatted_date, "Bold Text": text.strip()})
    
    df = pd.read_csv(output_file)
    df['Bold Text'] = df['Bold Text'].apply(clean_and_stem)
    
    tfidf_df = pd.read_pickle('tfidf_df.pkl')
    vectorizer = TfidfVectorizer(ngram_range=(2, 2), max_features=1000)
    vectorizer.fit(df['Bold Text'])
    X_tfidf = vectorizer.transform(df['Bold Text'])
    article_vectors = X_tfidf.mean(axis=1)
    
    df['article_vector'] = article_vectors
    
    df_isw = df.drop(columns=["Bold Text"])
    
    df_isw.to_csv(output_file, index=False)
    print("Data processed and saved successfully.")

SCHEDULED_HOUR = 23
SCHEDULED_MINUTE = 44

schedule.every().day.at(f"{SCHEDULED_HOUR}:{SCHEDULED_MINUTE}").do(process_data)

while True:
    schedule.run_pending()
    time.sleep(60)
