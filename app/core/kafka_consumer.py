from kafka import KafkaConsumer
import json
from app.services.market_provider import fetch_price_yfinance

def start_consumer(topic: str = "polling_jobs"):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers='localhost:9092',
        auto_offset_reset='latest',
        group_id='price-pollers',
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )

    print(f"✅ Listening to topic: {topic}")

    for message in consumer:
        print("📥 Kafka message received")
        job = message.value
        print(f"Job: {job}")

        symbols = job.get("symbols", [])
        provider = job.get("provider", "yfinance")

        for symbol in symbols:
            data = fetch_price_yfinance(symbol)
            print(f"📊 {symbol}: {data['price']} at {data['timestamp']}")

if __name__ == "__main__":
    start_consumer()
