"""
Kafka consumers for processing user activity events.
"""
from kafka import KafkaConsumer
from django.conf import settings
import json
import logging
from lms.achievement_engine import AchievementEngine

logger = logging.getLogger(__name__)


class UserActivityConsumer:
    """Consumer for user activity events"""
    
    def __init__(self):
        try:
            self.consumer = KafkaConsumer(
                settings.KAFKA_TOPIC_USER_ACTIVITY,
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                group_id='lms_achievement_processor',
                auto_offset_reset='earliest',
                enable_auto_commit=True
            )
            logger.info(f"Kafka consumer connected to topic: {settings.KAFKA_TOPIC_USER_ACTIVITY}")
        except Exception as e:
            logger.error(f"Failed to create Kafka consumer: {e}")
            self.consumer = None
    
    def start_consuming(self):
        """Start consuming messages"""
        if self.consumer is None:
            logger.error("Consumer not initialized")
            return
        
        logger.info("Starting to consume user activity events...")
        
        try:
            for message in self.consumer:
                self.process_message(message.value)
        except KeyboardInterrupt:
            logger.info("Consumer stopped by user")
        except Exception as e:
            logger.error(f"Error consuming messages: {e}")
        finally:
            self.close()
    
    def process_message(self, event_data):
        """Process a single event message"""
        try:
            event_type = event_data.get('event_type')
            user_id = event_data.get('user_id')
            
            logger.info(f"Processing event: {event_type} for user {user_id}")
            
            # Process achievement logic
            AchievementEngine.check_and_award_achievements(
                user_id=user_id,
                event_type=event_type,
                event_data=event_data
            )
            
            # Additional processing can be added here
            # - Analytics
            # - Logging
            # - Notifications
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
    
    def close(self):
        """Close consumer"""
        if self.consumer:
            self.consumer.close()
            logger.info("Consumer closed")


def start_consumer():
    """Start the Kafka consumer"""
    consumer = UserActivityConsumer()
    consumer.start_consuming()
