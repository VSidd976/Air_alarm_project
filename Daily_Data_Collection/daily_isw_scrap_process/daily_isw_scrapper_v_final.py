import urllib.request
import urllib.parse
import urllib.error
import datetime
import re
import os
import pandas as pd
import time

OUTPUT_FOLDER = "isw_data"
SCHEDULED_HOUR = 23
SCHEDULED_MINUTE = 42
START_DATE = datetime.datetime(2025, 3, 26)

MONTH_NAMES = {
    1: "january", 2: "february", 3: "march", 4: "april", 5: "may", 6: "june",
    7: "july", 8: "august", 9: "september", 10: "october", 11: "november", 12: "december"
}

def get_html(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/110.0.0.0 Safari/537.36"
        }
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request) as response:
            return response.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Page not found: {url}")
        else:
            print(f"HTTP error: {e.code} for {url}")
        return None
    except Exception as e:
        print(f"Error retrieving {url}: {e}")
        return None

def extract_bold_text(html):
    bold_texts = re.findall(r'<b.*?>(.*?)</b>|<strong.*?>(.*?)</strong>', html, flags=re.DOTALL)
    bold_text = " ".join([text[0] if text[0] else text[1] for text in bold_texts])
    return bold_text.strip()

def create_url_from_date(date):
    month_name = MONTH_NAMES[date.month]
    return (f"https://www.understandingwar.org/backgrounder/russian-offensive-campaign-"
            f"assessment-{month_name}-{date.day}-{date.year}")

def save_to_csv(text, date):
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    
    csv_filename = os.path.join(OUTPUT_FOLDER, f"isw_data_{date.strftime('%Y-%m-%d')}.csv")
    
    df = pd.DataFrame({
        'date': [date.strftime('%Y-%m-%d')],
        'text': [text]
    })
    
    df.to_csv(csv_filename, index=False, encoding='utf-8')
    print(f"Data saved to file {csv_filename}")

def crawl_daily():
    global START_DATE
    next_date = START_DATE + datetime.timedelta(days=1)

    url = create_url_from_date(next_date)
    print(f"Fetching report for {next_date.strftime('%Y-%m-%d')}")

    html = get_html(url)

    if html:
        print(f"Successfully found page for {next_date.strftime('%Y-%m-%d')}")

        bold_text = extract_bold_text(html)
        
        if bold_text:
            save_to_csv(bold_text, next_date)
            
            START_DATE = next_date
            
            print(f"Data saved for {next_date.strftime('%Y-%m-%d')}")
        else:
            print(f"No bold text found on page for {next_date.strftime('%Y-%m-%d')}")
    else:
        print("No report available for today.")

def get_seconds_until_next_run():
    now = datetime.datetime.now()
    target_time = now.replace(hour=SCHEDULED_HOUR, minute=SCHEDULED_MINUTE, second=0, microsecond=0)
    
    if target_time <= now:
        target_time += datetime.timedelta(days=1)
    
    delta = target_time - now
    return delta.total_seconds()

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)
    print(f"Created new directory: {OUTPUT_FOLDER}")

print(f"Script started. Will run daily at {SCHEDULED_HOUR:02d}:{SCHEDULED_MINUTE:02d}")

while True:
    seconds_to_wait = get_seconds_until_next_run()
    hours = int(seconds_to_wait // 3600)
    minutes = int((seconds_to_wait % 3600) // 60)
    seconds = int(seconds_to_wait % 60)
    
    print(f"Waiting for next run in {hours} hrs, {minutes} mins, {seconds} secs...")
    
    time.sleep(seconds_to_wait)
    
    print(f"Running script at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    try:
        crawl_daily()
    except Exception as e:
        print(f"Error during script execution: {e}")
    
    time.sleep(60)
