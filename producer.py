from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_data():
    sensors = ['S1', 'S2', 'S3']
    while True:
        for sensor_id in sensors:
            data = {
                'sensor_id': sensor_id,
                'temperature': random.uniform(60, 100) 
            }
            producer.send('sensor-suhu', value=data)
            print(f"Sent data: {data}")
        time.sleep(1)

if __name__ == "__main__":
    generate_data()
