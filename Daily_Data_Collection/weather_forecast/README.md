# Python_for_DS_air_alarm_project

* **`get_weather.py`**: Цей скрипт отримує прогноз погоди на наступні 24 години для заданого міста та зберігає його у форматі CSV.
* **`daily_weather.py`**: Цей скрипт використовує `schedule` для автоматичного запуску `get_weather.py` щодня о 06:00.

Використання

1.  **Встановлення залежностей:**

    ```bash
    pip install requests python-dotenv schedule
    ```

2.  **Налаштування API-ключа:**

    * Створіть файл `.env` у кореневій директорії проекту.
    * Додайте до файлу ваш API-ключ Visual Crossing:

        ```
        API_KEY="ваш_API_ключ"
        ```

3.  **Запуск `get_weather.py`:**

    * Запустіть скрипт `get_weather.py` для отримання та збереження прогнозу погоди:

        ```bash
        python get_weather.py
        ```

    * Скрипт створить файл CSV з назвою `weather_forecast_YYYY-MM-DD.csv` у поточній директорії.

4.  **Запуск `daily_weather.py`:**

    * Запустіть скрипт `daily_weather.py` для автоматичного запуску `get_weather.py` щодня о 06:00:

        ```bash
        python daily_weather.py
        ```

    * Скрипт буде працювати у фоновому режимі та запускати `get_weather.py` щодня о 06:00.

`get_weather.py`

* Отримує прогноз погоди на наступні 24 години для заданого міста з API Visual Crossing.
* Зберігає дані у форматі CSV з наступними стовпцями:
    * `Time`
    * `Temperature (°C)`
    * `Feels Like (°C)`
    * `Wind Speed (km/h)`
    * `Wind Direction`
    * `Humidity (%)`
    * `Precipitation (mm)`
    * `Cloud Cover (%)`
    * `UV Index`
    * `Conditions`

`daily_weather.py`

* Використовує бібліотеку `schedule` для автоматичного запуску `get_weather.py` щодня о 06:00.
* Працює у фоновому режимі.

Важливо!

* Переконайтеся, що у вас є дійсний API-ключ Visual Crossing.
* Ви можете змінити місто, для якого отримується прогноз, у змінній `CITY` у файлі `get_weather.py`.
* Ви можете змінити час запуску `daily_weather.py`, змінивши рядок `schedule.every().day.at("06:00").do(run_weather_script)` у файлі `daily_weather.py`.
* Не додавайте файл `.env` до вашого Git-репозиторію, оскільки він містить конфіденційну інформацію.
* Для використання скрапера для Telegram, ознайомтеся з інструкціями в репозиторії [telegram-scraper](https://github.com/unnohwn/telegram-scraper).
