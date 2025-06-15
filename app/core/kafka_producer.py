from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_polling_job(job: dict, topic: str = "polling_jobs"):
    producer.send(topic, value=job)
    producer.flush()
