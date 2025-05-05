# Air Alarm Prediction System

## General Description
This repository contains a modular system for collecting, processing, analyzing, and modeling war-related alerts and contextual data in Ukraine. 
The goal is to combine air alarm data, weather, ISW (Institute for the Study of War) reports, and Telegram signals to identify patterns and potentially predict risks.

Predictions are based on the analysis of:
1. ISW reports
2. Weather conditions
3. Regional alarms
4. Additional open sources (Telegram, national holidays, distances to military airfields)

## System Architecture
```
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
│   │   ├── get_weather.py                   # old
│   │   └── daily_weather.py                 # old
│   │   └── daily_weather_forecast.py     

├── data_collection/                         # One-time or manual data scraping scripts
│   ├── extra_data/                          # Additional static datasets
│   │   ├── Holiday_Risk_Factor_Assigment.ipynb
│   │   ├── combined_df_ukr.csv
│   │   ├── distances.csv
│   │   └── distances.py
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
│   │   ├── merging_extra_data.ipynb
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
│   ├── saas_app_v1.py                       # old version
│   ├── saas_app_v2.py
│   └── templates/
│       └── index.html

└── requirements.txt                         # Project dependencies
```

## Features
- Daily scraping of ISW reports and Telegram data
- Weather forecast integration per city
- Telegram text vectorization (TF-IDF)
- ISW text vectorization (TF-IDF)
- Dataset merging for machine learning
- Multiple model training pipelines (LogReg, CatBoost, RF, SGD)
- Visualization-ready notebooks

## How to run
**1. Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/war-alert-system.git
   cd war-alert-system
   ```

**2. Install dependencies:**
```bash
  pip install -r requirements.txt
```
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
catboost
```
---
**3. General and Daily Data Collections**  
Depending on your objectives, you can choose between two data collection modes: General Data Collection or Daily Data Collection. Both include steps for downloading, preprocessing, and merging data into a unified dataset.  
For model training, we used General Data Collection, while Daily Data Collection was used primarily for testing and integration with the SaaS interface to simulate real-time predictions.  

**3.1. General Data Collection**  
**3.1.1. Data Download**  
You can retrieve historical data from the following sources by running the corresponding scripts:  

**ISW Articles**  
```bash  
   data_collection/get_isw_data.sh
```
**Telegram Channels**
     
 *Original repo*: https://github.com/unnohwn/telegram-scraper
```bash  
   data_collection/get_telegram_data.sh  
```

**Additional Data**
   
To improve prediction quality, we incorporated external public datasets:

**Risk Factors Based on Holidays and Memorial Dates in Ukraine**
      Run the notebook:

```bash
jupyter notebook data_collection/extra_data/Holiday_Risk_Factor_Assigment.ipynb  
``` 
**Distance Calculation Between Ukrainian Cities and Airfields**
      Run the script:
```bash
python data_collection/extra_data/distances.py
```
   
   Example datasets are available:
   1. combined_df_ukr.csv
   2. distances.csv

**3.1.2. Data Preprocessing**

**ISW**  
Several preprocessing strategies were tested (e.g., removing stop words and digits). The final version is in:  
```bash
jupyter notebook data_processing/isw_processing/isw_data_cleaning_without_stopwords.ipynb
```
**Telegram**  
Preprocessing:  
```bash
python data_processing/telegram_processing/telegram_parser.py
```
Vectorization (TF-IDF):  
```bash
python data_processing/telegram_processing/telegram_vectoriser.py
```
Merging:
```bash
python data_processing/telegram_processing/merge_preparation.py
```

**Weather**  
```bash
jupyter notebook data_processing/weather_data/Weather_data_cleaning.ipynb
```

**Air Alarm Data**  
The alarm data was provided manually before project start. Preprocess it using:  
```bash
jupyter notebook data_processing/alarm_parser/alarm_data_cleaning.ipynb
```

**3.1.3. Merging All Data**  
Merge all cleaned datasets into a final training set:  
```bash
jupyter notebook data_processing/merge/Data_merge.ipynb
```

Run the notebook to process and analyze weather data as well as holiday data in Ukraine. It loads data from CSV files, processes dates, calculates risks associated with holidays, and saves the results in a new CSV file that contains information about weather conditions and holidays for various cities:
```bash
jupyter notebook data_processing/merge/merging_extra_data.ipynb
```

**3.1.4. Additional Tools**

**Others:**
**1. Parse External Links from ISW Articles**  
To extract links to external sources (including Telegram channels) mentioned in ISW articles:  
```bash
jupyter notebook data_processing/isw_processing/isw_link_parser.ipynb
```

**2. Data Analysis Notebooks**  
A variety of exploratory data analyses are available in the analysis/ directory. These help visualize dataset distributions, correlation, and quality before training.

---
**3.2. Daily Data Collection**  
This mode fetches and processes real-time data for daily model predictions. Each dataset includes a download and preprocessing stage.

**3.2.1. ISW Articles**  
Download:  
```bash
python daily_data_collection/daily_isw_scrap_process/daily_isw_scrapper_v_final.py
``` 
Preprocessing:  
```bash
python daily_data_collection/daily_isw_scrap_process/preprocess_isw.py
```

**3.2.2. Telegram**  
Download:  
```bash
bash daily_data_collection/get_hour_telegram_data/get_hour_telegram_data.sh
```
Preprocessing:  
```bash
bash daily_data_collection/get_hour_telegram_data/clear_daily_telegram_data.sh
```

**3.2.3. Weather**  
Download:  
```bash
python daily_data_collection/weather_forecast/daily_weather_forecast.py
``` 

**3.2.4. Final Dataset Merge & Preprocessing**  
Merge all daily datasets:  
```bash
python daily_data_collection/daily_merge_process_final_dataset/merge_final_dataset.py
```
Preprocess the merged dataset:  
```bash
python daily_data_collection/daily_merge_process_final_dataset/preprocess_final_dataset.py
```
Sample daily CSV datasets are also included for demonstration and merging purposes.

--- 

**4. Train Models**  
We experimented with five models:  
- Linear Regression  
- Logistic Regression  
- CatBoost Classifier  
- Random Forest Classifier  
- Stochastic Gradient Descent Classifier

The final deployed ensemble combines the best two models:  
**CatBoost Classifier and Random Forest Classifier**

To replicate the training and ensemble:  
1. Train both base models on the same dataset.  
2. Use an unseen dataset for objective ensemble evaluation.

```bash
 jupyter notebook models/ensemble_model/models_for_ensemble.ipynb  
 jupyter notebook models/ensemble_model/ensemble_model.ipynb
```
**Optional: Individual Model Notebooks**

Linear Regression: 
```bash
models/linear_regression/Linear.ipynb
```
Logistic Regression (v1): 
```bash
models/logistic_regression/Logistic_regression_DS.ipynb
```
Logistic Regression (v2): 
```bash
models/logistic_regression/Logistic_regression_v2.ipynb
```
Stochastic Gradient Descent Classifier: 
```bash
models/stochastic_gradient_descent_classifier/SGD_classifier.ipynb
```
Cat Boost Classifier: 
```bash
models/cat_boost_model/cat_boost_classifier.ipynb
```
Random Forest Classifier: 
```bash
models/random_forest_classifier/random_forest_classifier.ipynb
```

**5. Saas**
