#!/bin/bash

if ! command -v python3 &> /dev/null
then
  echo "Error: Python 3 is not installed. Please install it."
  exit 1
fi

python3 -c "import requests, csv, os, datetime, dotenv, schedule, time" 2> /dev/null
if [ $? -ne 0 ]; then
  echo "Error: Required Python libraries are not installed. Installing..."
  pip3 install requests python-dotenv schedule
  if [ $? -ne 0 ]; then
    echo "Error: Failed to install required Python libraries."
    exit 1
  fi
fi

echo "Running get_weather.py..."
python3 get_weather.py
if [ $? -ne 0 ]; then
  echo "Error: get_weather.py failed to execute."
  exit 1
fi


echo "Running daily_weather.py..."
python3 daily_weather.py
if [ $? -ne 0 ]; then
  echo "Error: daily_weather.py failed to execute."
  exit 1
fi

echo "Both scripts executed successfully."
exit 0