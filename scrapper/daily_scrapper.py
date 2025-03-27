import urllib.request
import urllib.parse
import urllib.error
import datetime
import re
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import os

# changamle parameters
OUTPUT_FILE = "isw_data.txt"
START_DATE = datetime.datetime(2025, 3, 23)
CRON_HOUR = 21
CRON_MINUTE = 38

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
            print(f"HTTP Error: {e.code} for {url}")
        return None
    except Exception as e:
        print(f"Error retrieving {url}: {e}")
        return None


def extract_text(html):
    text = re.sub(r"<script.*?>.*?</script>", "", html, flags=re.DOTALL)
    text = re.sub(r"<style.*?>.*?</style>", "", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def save_to_file(text, url, filename):
    # Check if the file exists, if not create it
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as file:
            file.write("isw_data\n\n")

    # Path to the output file
    file_path = filename

    # Write the text to the output file
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(f"SOURCE: {url}\n\n")
        file.write(text + "\n\n")
        file.write("-" * 80 + "\n\n")

    print(f"Data saved to {file_path}")


def create_url_from_date(date):
    month_name = MONTH_NAMES[date.month]
    return (f"https://www.understandingwar.org/backgrounder/russian-offensive-campaign-"
            f"assessment-{month_name}-{date.day}-{date.year}")


def crawl_daily():
    global START_DATE  # Use global keyword to modify the global variable
    next_date = START_DATE + datetime.timedelta(days=1)

    url = create_url_from_date(next_date)
    print(f"Fetching report for {next_date.strftime('%Y-%m-%d')}")

    html = get_html(url)

    if html:
        print(f"Successfully found page for {next_date.strftime('%Y-%m-%d')}")

        text = extract_text(html)
        save_to_file(text, url, OUTPUT_FILE)

        # Update the global START_DATE
        START_DATE = next_date

        print(f"Data saved for {next_date.strftime('%Y-%m-%d')}")
    else:
        print("No report available for today.")


if not os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write("ISW Crawler Data\n\n")
    print(f"Created new file: {OUTPUT_FILE}")

# Create a scheduler
scheduler = BlockingScheduler()

# Add the job to run daily at the specified time
scheduler.add_job(
    crawl_daily,
    CronTrigger(hour=CRON_HOUR, minute=CRON_MINUTE),
    id='daily_crawl_job',
    max_instances=1  # Prevents multiple instances from running simultaneously
)

print("ISW Crawler scheduled. Starting...")

try:

    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    print("Scheduler stopped.")
