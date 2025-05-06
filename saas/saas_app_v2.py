from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib
from datetime import datetime, timedelta

app = Flask(__name__, template_folder='templates')

model = joblib.load('6__catboost_classifier__v1.pkl')

df = pd.read_csv('subset_missing_alarms.xls')
df_copy = df.copy()
x = df.drop(['alarms', 'city_address', 'datetime'], axis=1)
preds = model.predict(x)
df_copy['alarms'] = preds
df_copy.to_csv('result.csv', index=False)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_alarm', methods=['POST'])
def get_alarm():
    data = request.get_json()
    city = data.get('city_address')
    dt = data.get('datetime')

    if not city or not dt:
        return jsonify({'error': 'Both city_address and datetime are required'}), 400

    try:
        result_df = pd.read_csv('result.csv')
        match = result_df[(result_df['datetime'] == dt) & (result_df['city_address'] == city)]

        if match.empty:
            return jsonify({'error': 'No matching row found'}), 404

        alarm_value = int(match.iloc[0]['alarms'])
        return jsonify({'datetime': dt, 'city_address': city, 'alarm': alarm_value})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/24hour', methods=['POST'])
def forecast_24hour():
    data = request.get_json()
    city = data.get('city_address')
    dt = data.get('datetime')

    if not city or not dt:
        return jsonify({'error': 'Both city_address and datetime are required'}), 400

    try:
        dt_start = pd.to_datetime(dt)
        dt_end = dt_start + timedelta(hours=24)

        result_df = pd.read_csv('result.csv')
        result_df['datetime'] = pd.to_datetime(result_df['datetime'])

        window = result_df[
            (result_df['city_address'] == city) &
            (result_df['datetime'] >= dt_start) &
            (result_df['datetime'] < dt_end)
        ]

        if window.empty:
            return jsonify({'error': 'No data available for this window'}), 404

        result = window[['datetime', 'city_address', 'alarms']].to_dict(orient='records')
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/day_predict', methods=['POST'])
def forecast_day():
    data = request.get_json()
    city = data.get('city_address')
    dt = data.get('datetime')

    if not city or not dt:
        return jsonify({'error': 'Both city_address and datetime are required'}), 400

    try:
        dt_start = pd.to_datetime(dt)
        dt_end = dt_start.replace(hour=23, minute=0, second=0, microsecond=0)

        result_df = pd.read_csv('result.csv')
        result_df['datetime'] = pd.to_datetime(result_df['datetime'])

        window = result_df[
            (result_df['city_address'] == city) &
            (result_df['datetime'] >= dt_start) &
            (result_df['datetime'] <= dt_end)
        ]

        if window.empty:
            return jsonify({'error': 'No data available for this window'}), 404

        result = window[['datetime', 'city_address', 'alarms']].to_dict(orient='records')
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
