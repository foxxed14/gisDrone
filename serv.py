from flask import Flask, request, render_template_string
import folium
import folium.plugins
from datetime import datetime

app = Flask(__name__)

# Список для хранения данных
data_points = []

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

    m = folium.Map(location=[float(data_points[-1]['latitude']), float(data_points[-1]['longitude'])], zoom_start=10)
    features = []

    coordinates = []
    for point in data_points:
        coordinates.append([float(point['latitude']), float(point['longitude'])])
        
        # Добавление точек
        feature_point = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [float(point['longitude']), float(point['latitude'])]
            },
            'properties': {
                'time': point['timestamp'],
                'style': {'color': 'red'},
                'icon': 'circle',
                'popup': f"Temperature: {point['temperature']}°C\nPressure: {point['pressure']} hPa\nHumidity: {point['humidity']}%",
            }
        }
        features.append(feature_point)
    
    # Добавление линий
    folium.PolyLine(coordinates, color="blue", weight=2.5, opacity=1).add_to(m)

    feature_collection = {
        'type': 'FeatureCollection',
        'features': features,
    }

    folium.plugins.TimestampedGeoJson(
        feature_collection,
        period='PT1S',
        add_last_point=True,   
        auto_play=True,        
        loop=False,
        max_speed=1,
        loop_button=True,
        date_options='YYYY/MM/DD HH:mm:ss',
        time_slider_drag_update=True
    ).add_to(m)

    return render_template_string('<html><body>{{ m | safe }}</body></html>', m=m._repr_html_())


if __name__ == '__main__':
    app.run(debug=True)
