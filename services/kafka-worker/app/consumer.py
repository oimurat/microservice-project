from kafka import KafkaConsumer, KafkaProducer
import json

consumer = KafkaConsumer("order-topic", bootstrap_servers="kafka:9092")
producer = KafkaProducer(bootstrap_servers="kafka:9092")

for msg in consumer:
    try:
        data = json.loads(msg.value)
        print(f"Processing message: {data}")
        # Simulate processing...
    except Exception as e:
        print(f"Error: {e}")
        producer.send("order-topic.DLT", msg.value)