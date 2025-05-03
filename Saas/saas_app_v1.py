from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import joblib

app = Flask(__name__)
CORS(app)

model = joblib.load('catboost_model.pkl')

df = pd.read_csv('subset_missing_alarms.xls')

df_copy = df.copy()

x = df.drop(['alarms', 'city_address', 'datetime'], axis=1)

preds = model.predict(x)

df_copy['alarms'] = preds

df_copy.to_csv('result.csv', index=False)

@app.route('/')
def home():
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
