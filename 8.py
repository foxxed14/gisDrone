from flask import Flask, request, render_template_string
import folium
import folium.plugins
from datetime import datetime
import random

app = Flask(__name__)

# Список для хранения данных
data_points = []

def intersect(p1, q1, p2, q2):
    # Функция для определения пересечения двух отрезков
    # ... (можно реализовать на основе векторного произведения)
    pass

@app.route('/data', methods=['POST'])
def receive_data():
    temperature = request.form.get('temperature')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')
    pressure = request.form.get('pressure')
    humidity = request.form.get('humidity')
    
    # Добавление метки времени к данным
    current_time = datetime.now()
    timestamp = current_time.strftime('%Y-%m-%dT%H:%M:%S')
    
    data_points.append({
        'temperature': temperature,
        'latitude': latitude,
        'longitude': longitude,
        'pressure': pressure,
        'humidity': humidity,
        'timestamp': timestamp
    })

    return "Данные получены", 200

@app.route('/map')
def display_map():
    if not data_points:
        return "Нет данных для отображения на карте"

    m = folium.Map(location=[float(data_points[0]['latitude']), float(data_points[0]['longitude'])], zoom_start=10)
    features = []

    # ... [определение и отображение маршрута, замкнутых областей и т. д.]

    for point in data_points:
        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [float(point['longitude']), float(point['latitude'])]
            },
            'properties': {
                'time': point['timestamp'],
                'style': {'color': 'blue'},
                'icon': 'circle',
                'popup': f"Temperature: {point['temperature']}°C\nPressure: {point['pressure']} hPa\nHumidity: {point['humidity']}%",
            }
        }
        features.append(feature)

    feature_collection = {
        'type': 'FeatureCollection',
        'features': features,
    }

    folium.plugins.TimestampedGeoJson(
        feature_collection,
        period='PT1S',
        add_last_point=True,
        auto_play=False,
        loop=False,
        max_speed=1,
        loop_button=True,
        date_options='YYYY/MM/DD HH:mm:ss',
        time_slider_drag_update=True
    ).add_to(m)

    return render_template_string('<html><body>{{ m | safe }}</body></html>', m=m._repr_html_())

if __name__ == '__main__':
    app.run(debug=True)
