from typing import Dict, Any, List
import json
from datetime import datetime
from confluent_kafka import Consumer, KafkaError
import logging
from collections import defaultdict
from sqlalchemy.orm import Session
from app.models import SymbolAverage, RawMarketData, ProcessedPricePoint
from app.core.database import SessionLocal
import os
from collections import deque

logger = logging.getLogger(__name__)

class KafkaPriceConsumer:
    def __init__(self):
        self.consumer = Consumer({
            'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
            'group.id': 'market-data-consumer',
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': True
        })
        self.topic = 'price-events'
        self.price_history = {}  # symbol -> deque(maxlen=5)
        self.db = SessionLocal()

    def calculate_moving_average(self, symbol: str, price: float) -> float:
        """Calculate 5-point moving average for a symbol."""
        if symbol not in self.price_history:
            self.price_history[symbol] = deque(maxlen=5)
        
        self.price_history[symbol].append(price)
        
        if len(self.price_history[symbol]) < 5:
            logger.debug(f"Not enough data points for {symbol}. Current points: {len(self.price_history[symbol])}")
            return None  # Not enough data points yet
            
        return sum(self.price_history[symbol]) / 5

    def update_symbol_average(self, symbol: str, average: float):
        """Update the moving average in the database."""
        try:
            # Try to get existing record
            symbol_avg = self.db.query(SymbolAverage).filter_by(symbol=symbol).first()
            
            if symbol_avg:
                # Update existing record
                symbol_avg.average = average
                symbol_avg.updated_at = datetime.utcnow()
                logger.info(f"Updated existing moving average for {symbol}: {average}")
            else:
                # Create new record
                symbol_avg = SymbolAverage(
                    symbol=symbol,
                    average=average
                )
                self.db.add(symbol_avg)
                logger.info(f"Created new moving average for {symbol}: {average}")
            
            self.db.commit()
            logger.info(f"Committed moving average for {symbol}: {average}")
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating moving average: {str(e)}")
            raise

    def store_processed_price_point(self, symbol: str, price: float, timestamp: datetime, provider: str):
        """Store processed price point with additional metrics."""
        try:
            # Get previous price point for this symbol
            prev_price_point = self.db.query(ProcessedPricePoint)\
                .filter_by(symbol=symbol)\
                .order_by(ProcessedPricePoint.timestamp.desc())\
                .first()

            # Calculate price change
            price_change = None
            if prev_price_point:
                price_change = price - prev_price_point.price

            # Create new processed price point
            processed_point = ProcessedPricePoint(
                symbol=symbol,
                price=price,
                timestamp=timestamp,
                provider=provider,
                price_change=price_change,
                # Additional metrics can be added here as they become available
                volume=None,
                high_price=None,
                low_price=None,
                open_price=None,
                close_price=None
            )

            self.db.add(processed_point)
            self.db.commit()
            logger.info(f"Stored processed price point for {symbol}: {price}")

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error storing processed price point: {str(e)}")
            raise

    def process_message(self, message):
        """Process a price update message."""
        try:
            # Parse message
            data = json.loads(message.value().decode('utf-8'))
            symbol = data['symbol']
            price = float(data['price'])
            timestamp = datetime.fromisoformat(data['timestamp'])
            provider = data.get('source', 'yfinance')
            
            # Store raw market data
            raw_data = RawMarketData(
                symbol=symbol,
                price=price,
                timestamp=timestamp,
                provider=provider
            )
            self.db.add(raw_data)
            self.db.commit()
            
            # Store processed price point
            self.store_processed_price_point(symbol, price, timestamp, provider)
            
            # Calculate moving average
            average = self.calculate_moving_average(symbol, price)
            
            if average is not None:
                # Upsert to symbol_averages
                self.update_symbol_average(symbol, average)
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            raise

    def start_consuming(self):
        """Start consuming messages from Kafka."""
        try:
            self.consumer.subscribe([self.topic])
            logger.info(f"Started consuming from topic: {self.topic}")
            
            while True:
                msg = self.consumer.poll(1.0)
                
                if msg is None:
                    logger.debug("No message received")
                    continue
                    
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        logger.debug("Reached end of partition")
                        continue
                    else:
                        logger.error(f"Consumer error: {msg.error()}")
                        continue
                
                logger.info(f"Received message: {msg.value().decode('utf-8')}")
                self.process_message(msg)
                
        except KeyboardInterrupt:
            logger.info("Stopping consumer...")
        finally:
            self.consumer.close()
            self.db.close()

if __name__ == "__main__":
    consumer = KafkaPriceConsumer()
    consumer.start_consuming() 