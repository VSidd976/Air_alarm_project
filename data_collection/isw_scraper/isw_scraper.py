import urllib.request
import urllib.parse
import urllib.error
import time
import datetime
import re

# Date range configuration that we needed
START_DATE = datetime.datetime(2025, 3, 22)
END_DATE = datetime.datetime(2022, 2, 24)
OUTPUT_FILE = "isw_data.txt"


MONTH_NAMES = {
    1: "january", 2: "february", 3: "march", 4: "april", 5: "may", 6: "june",
    7: "july", 8: "august", 9: "september", 10: "october", 11: "november", 12: "december"
}


def get_html(url):

    try:
        # headers for avoiding problems with page protection from unauthorized users
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "Chrome/110.0.0.0 Safari/537.36"
        }
        request = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(request) as response:
            return response.read().decode("utf-8")
        # some exceptions if smth go wrong
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
    # remove HTML tags, leaving clean text with which we will work soon
    text = re.sub(r"<script.*?>.*?</script>", "", html, flags=re.DOTALL)
    text = re.sub(r"<style.*?>.*?</style>", "", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def save_to_file(text, url, filename):
    # save text to file with URL reference
    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"SOURCE: {url}\n\n")
        file.write(text + "\n\n")
        file.write("-" * 80 + "\n\n")


def get_previous_date(current_date):
    # get the previous date, handling month and year transitions, at this situation this is best option
    return current_date - datetime.timedelta(days=1)


def create_url_from_date(date):
    # create correct ISW URL from a date object month-date-year
    month_name = MONTH_NAMES[date.month]
    return (f"https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment"
            f"-{month_name}-{date.day}-{date.year}")


def crawl_by_dates():
    # crawl through Russian Offensive Campaign Assessment reports by systematically generating dates
    # Clear output file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write("ISW RUSSIAN OFFENSIVE CAMPAIGN ASSESSMENTS\n\n")

    current_date = START_DATE

    while current_date >= END_DATE:
        # Create URL for current date
        url = create_url_from_date(current_date)
        print(f"Trying: {url}")

        # Try to get the page
        html = get_html(url)

        if html:
            print(f"Successfully found page for {current_date.strftime('%Y-%m-%d')}")
            # Extract and save the content
            text = extract_text(html)
            save_to_file(text, url, OUTPUT_FILE)

        # Move to the previous day
        current_date = get_previous_date(current_date)

        # so that we don't have problems with being banned due to request spam
        time.sleep(3)

    print("Reached end date. Crawling complete.")


# Start the crawler
crawl_by_dates()
print(f"Data saved to {OUTPUT_FILE}")
