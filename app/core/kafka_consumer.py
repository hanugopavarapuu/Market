import json
from kafka import KafkaConsumer
from app.core.database import SessionLocal
from app.models import RawMarketData
from app.services.market_provider import fetch_price_yfinance
from datetime import datetime

KAFKA_TOPIC = "polling_jobs"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092" 
def consume_messages():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',
        group_id="market_data_service_group",
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        enable_auto_commit=True
    )

    db = SessionLocal()
    print(f"✅ Listening to topic: {KAFKA_TOPIC}")

    try:
        for message in consumer:
            print("📥 Kafka message received")
            job = message.value
            job_id = job.get("job_id")
            symbols = job.get("symbols", [])
            interval = job.get("interval")
            provider = job.get("provider", "yfinance")
            print(f"Job: {job}")

            for symbol in symbols:
                data = fetch_price_yfinance(symbol)
                if data["price"] is None:
                    print(f"⚠️ Price not found for {symbol}")
                    continue

                raw_data = RawMarketData(
                    symbol=symbol,
                    price=data["price"],
                    timestamp=datetime.fromisoformat(data["timestamp"]),
                    provider=provider,
                    raw_response=json.dumps(data)  
                )
                db.add(raw_data)
                print(f"📊 {symbol}: {data['price']} at {data['timestamp']}")

            db.commit()
    except Exception as e:
        print(f"❌ Error in consumer: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    consume_messages()
