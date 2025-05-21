from kafka import KafkaProducer
import json
import random
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

gudang_ids = ['G1', 'G2', 'G3']

while True:
    for gudang in gudang_ids:
        kelembaban = random.randint(60, 80)
        data = {"gudang_id": gudang, "kelembaban": kelembaban}
        producer.send('sensor-kelembaban-gudang', value=data)
        print(f"Sent Kelembaban: {data}")
    time.sleep(1)
