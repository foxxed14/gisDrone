
import requests
import random
import time

# URL сервера, на который будут отправляться данные
SERVER_URL = "http://localhost:5000/data"

# Начальные координаты
latitude = 50.0
longitude = 50.0

def generate_random_data():
    global latitude, longitude

    temperature = random.uniform(15.0, 25.0)  # Температура от 15 до 25 градусов
    pressure = random.uniform(980, 1050)      # Давление от 980 до 1050 гПа
    humidity = random.uniform(20, 80)         # Влажность от 20% до 80%

    # Изменяем координаты для формирования маршрута
    latitude += random.uniform(-0.05, 0.05)
    longitude += random.uniform(-0.05, 0.05)
    
    return {
        'temperature': temperature,
        'latitude': latitude,
        'longitude': longitude,
        'pressure': pressure,
        'humidity': humidity
    }

if __name__ == "__main__":
    while True:
        data = generate_random_data()
        response = requests.post(SERVER_URL, data=data)
        
        if response.status_code == 200:
            print("Данные успешно отправлены на сервер!")
        else:
            print(f"Ошибка при отправке данных. Статус: {response.status_code}. Ответ: {response.text}")

        # Ожидание 10 секунд перед следующей отправкой
        time.sleep(10)
