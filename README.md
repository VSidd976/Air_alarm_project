# Air Alarm Prediction System

## General Description
This repository contains a modular system for collecting, processing, analyzing, and modeling war-related alerts and contextual data in Ukraine. 
The goal is to combine air alarm data, weather, ISW (Institute for the Study of War) reports, and Telegram signals to identify patterns and potentially predict risks.

Predictions are based on the analysis of:
•	ISW reports
•	Weather conditions
•	Regional situation
•	Additional open sources (Telegram, national holidays, distances to military airfields)

## System Architecture
├── analysis/                                # Analysis notebooks (except Telegram data)
│   ├── alarm_data_analysis.ipynb
│   ├── alarms+weather+isw_analysis.ipynb
│   ├── alarms+weather_analysis.ipynb
│   ├── isw_data_analysis.ipynb
│   └── weather_analysis.ipynb

├── daily_data_collection/                   # Scripts for daily automated data collection
│   ├── daily_isw_scrap_process/             # Daily scraping and preprocessing of ISW reports
│   │   ├── daily_isw_scrapper_v_final.py
│   │   ├── preprocess_isw.py
│   │   └── tfidf_df.pkl
│   ├── daily_merge_process_final_dataset/   # Dataset preparation pipeline for daily model input
│   │   ├── average_telegram_vectors.csv
│   │   ├── distances.csv
│   │   ├── holidays.csv
│   │   ├── isw_data.csv
│   │   ├── merge_final_dataset.py
│   │   ├── preprocess_final_dataset.py
│   │   └── weather_all_cities_2025-04-27.csv
│   ├── get_hour_telegram_data/              # Hourly Telegram data collection and vectorization
│   │   ├── clear_daily_telegram_data.sh
│   │   ├── get_hour_telegram_data.sh
│   │   ├── hour_merge_preparation.py
│   │   ├── hour_parser.py
│   │   ├── hour_scraper.py
│   │   └── hour_vectoriser.py
│   ├── weather_forecast/                    # Weather forecast scripts
│   │   ├── get_weather.py                   # Get forecasts for all cities
│   │   └── daily_weather.py                 # Schedule daily weather updates

├── data_collection/                         # One-time or manual data scraping scripts
│   ├── extra_data/                          # Additional static datasets
│   │   ├── Holiday_Risk_Factor_Assigment.ipynb
│   │   ├── combined_df_ukr.csv
│   │   ├── distances.csv
│   │   └── distances.py
│   ├── get_weather_forecast/
│   │   ├── forecast_all_regions.py
│   │   └── get_weather_for_city.py
│   ├── isw_scraper/
│   │   └── isw_scraper.py
│   ├── telegram-scraper/
│   │   └── telegram-scraper.py
│   ├── get_isw_data.sh                      # Shell script to fetch ISW data
│   ├── get_telegram_data.sh                 # Shell script to fetch Telegram data
│   └── run_weather.sh                       # Shell script to run weather scraper

├── data_processing/                         # Processing and cleaning of collected data
│   ├── alarm_parser/
│   │   └── alarm_data_cleaning.ipynb
│   ├── isw_processing/
│   │   ├── isw_data_cleaning_with_num.ipynb
│   │   ├── isw_data_cleaning_without_num_with_stopword_bigram.ipynb   # The main option
│   │   ├── isw_data_cleaning_without_stopwords.ipynb
│   │   └── isw_link_parser.ipynb
│   ├── merge/
│   │   └── Data_merge.ipynb
│   ├── telegram_processing/
│   │   ├── merge_preparation.py
│   │   ├── telegram_parser.py
│   │   └── telegram_vectoriser.py
│   └── weather_data/
│       └── Weather_data_cleaning.ipynb

├── legacy/                                  # Deprecated or archived scripts

├── models/                                  # Machine learning models
│   ├── CatBoostModel/
│   │   └── CatBoostClassifier.ipynb
│   ├── linear_regression/
│   │   └── Linear.ipynb
│   ├── logistic_regression/
│   │   ├── Logistic_regression_DS.ipynb
│   │   └── Logistic_regression_v2.ipynb
│   ├── random_forest_classifier/
│   │   └── random_forest_classifier.ipynb
│   ├── stochastic_gradient_descent_classifier/
│   │   └── SGD_classifier.ipynb
│   └── ensemble_model/
│       └── ensemble_model.ipynb

├── saas/                                    # Software-as-a-Service application (deployment-ready)
│   └── saas_app_v1.py

└── requirements.txt                         # Project dependencies


## Features
- Daily scraping of ISW reports and Telegram data
- Weather forecast integration per city
- Telegram text vectorization (TF-IDF)
- ISW text vectorization (TF-IDF)
- Dataset merging for machine learning
- Multiple model training pipelines (LogReg, CatBoost, RF, SGD)
- Visualization-ready notebooks

## How to run
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/war-alert-system.git
   cd war-alert-system```

2. **Install dependencies:**
```bash
  pip install -r requirements.txt```
Contents of requirements.txt:
```argparse
apscheduler
pandas
requests
telethon
aiohttp
python-dotenv
numpy
matplotlib
seaborn
scikit-learn
gensim
nltk
tqdm
emoji
spacy
langdetect
catboost```
```

3. **Run collection scripts:**
  3.1. D C
   Use bash scripts in daily_data_collection/ or run Python scripts directly.

6. **Train models:**
Open and run notebooks from the models/ directory.
