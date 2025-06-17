from typing import Dict, Any
import json
from datetime import datetime
from confluent_kafka import Producer
import logging
import os

logger = logging.getLogger(__name__)

class KafkaPriceProducer:
    def __init__(self):
        self.producer = Producer({
            'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
            'client.id': 'market-data-producer',
            'retries': 3,
            'retry.backoff.ms': 1000,
            'acks': 'all'
        })
        self.topic = 'price-events'
    
    def delivery_report(self, err, msg):
        """Called once for each message produced to indicate delivery result."""
        if err is not None:
            logger.error(f'Message delivery failed: {err}')
        else:
            logger.debug(f'Message delivered to {msg.topic()} [{msg.partition()}]')
    
    def publish_price_update(self, price_data: Dict[str, Any]):
        """
        Publish price update to Kafka topic.
        
        Args:
            price_data: Dict containing price information
                - symbol: str
                - price: float
                - timestamp: str (ISO format)
                - provider: str
        """
        try:
            # Add source field as required by schema
            message = {
                "symbol": price_data["symbol"],
                "price": price_data["price"],
                "timestamp": price_data["timestamp"],
                "source": price_data["provider"],
                "raw_response_id": str(price_data.get("raw_response_id", ""))
            }
            
            # Convert to JSON
            message_json = json.dumps(message)
            
            # Produce message
            self.producer.produce(
                self.topic,
                message_json.encode('utf-8'),
                callback=self.delivery_report
            )
            
            # Trigger any available delivery report callbacks
            self.producer.poll(0)
            
            # Wait for any outstanding messages to be delivered
            self.producer.flush()
            
            logger.info(f"Published price update for {price_data['symbol']}")
            
        except Exception as e:
            logger.error(f"Error publishing price update: {str(e)}")
            raise 