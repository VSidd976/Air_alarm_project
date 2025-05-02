import schedule
import time
import subprocess

def run_weather_script():
    print("Launching weather script...")
    subprocess.run(["python", "get_weather.py"])

schedule.every().day.at("06:00").do(run_weather_script)

print("Scheduler is on. Forecast is updating...")

while True:
    schedule.run_pending()
    time.sleep(60)