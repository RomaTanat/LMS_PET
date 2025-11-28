"""
Kafka event definitions and producers for user activity tracking.
"""
from kafka import KafkaProducer
from django.conf import settings
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class EventProducer:
    """Kafka event producer singleton"""
    _instance = None
    _producer = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._producer is None:
            try:
                self._producer = KafkaProducer(
                    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                    key_serializer=lambda k: k.encode('utf-8') if k else None
                )
                logger.info(f"Kafka producer connected to {settings.KAFKA_BOOTSTRAP_SERVERS}")
            except Exception as e:
                logger.error(f"Failed to connect to Kafka: {e}")
                self._producer = None
    
    def send_event(self, topic, event_data, key=None):
        """Send event to Kafka topic"""
        if self._producer is None:
            logger.warning("Kafka producer not available, event not sent")
            return False
        
        try:
            # Add timestamp if not present
            if 'timestamp' not in event_data:
                event_data['timestamp'] = datetime.utcnow().isoformat()
            
            future = self._producer.send(topic, value=event_data, key=key)
            future.get(timeout=10)  # Wait for confirmation
            logger.info(f"Event sent to {topic}: {event_data.get('event_type')}")
            return True
        except Exception as e:
            logger.error(f"Failed to send event to Kafka: {e}")
            return False
    
    def close(self):
        """Close Kafka producer"""
        if self._producer:
            self._producer.close()


# Event type constants
class EventTypes:
    COURSE_ENROLLED = 'course_enrolled'
    COURSE_COMPLETED = 'course_completed'
    MATERIAL_VIEWED = 'material_viewed'
    TEST_PASSED = 'test_passed'
    TEST_FAILED = 'test_failed'
    LOGIN = 'user_login'
    PROFILE_UPDATED = 'profile_updated'


def send_course_enrolled_event(user_id, course_id, course_title):
    """Send course enrollment event"""
    event_data = {
        'event_type': EventTypes.COURSE_ENROLLED,
        'user_id': user_id,
        'course_id': course_id,
        'course_title': course_title,
    }
    producer = EventProducer()
    producer.send_event(
        settings.KAFKA_TOPIC_USER_ACTIVITY,
        event_data,
        key=f'user_{user_id}'
    )


def send_course_completed_event(user_id, course_id, course_title):
    """Send course completion event"""
    event_data = {
        'event_type': EventTypes.COURSE_COMPLETED,
        'user_id': user_id,
        'course_id': course_id,
        'course_title': course_title,
    }
    producer = EventProducer()
    producer.send_event(
        settings.KAFKA_TOPIC_USER_ACTIVITY,
        event_data,
        key=f'user_{user_id}'
    )


def send_material_viewed_event(user_id, material_id, material_title, course_id):
    """Send material viewed event"""
    event_data = {
        'event_type': EventTypes.MATERIAL_VIEWED,
        'user_id': user_id,
        'material_id': material_id,
        'material_title': material_title,
        'course_id': course_id,
    }
    producer = EventProducer()
    producer.send_event(
        settings.KAFKA_TOPIC_USER_ACTIVITY,
        event_data,
        key=f'user_{user_id}'
    )


def send_test_passed_event(user_id, test_id, score, course_id):
    """Send test passed event"""
    event_data = {
        'event_type': EventTypes.TEST_PASSED,
        'user_id': user_id,
        'test_id': test_id,
        'score': score,
        'course_id': course_id,
    }
    producer = EventProducer()
    producer.send_event(
        settings.KAFKA_TOPIC_USER_ACTIVITY,
        event_data,
        key=f'user_{user_id}'
    )


def send_test_failed_event(user_id, test_id, score, course_id):
    """Send test failed event"""
    event_data = {
        'event_type': EventTypes.TEST_FAILED,
        'user_id': user_id,
        'test_id': test_id,
        'score': score,
        'course_id': course_id,
    }
    producer = EventProducer()
    producer.send_event(
        settings.KAFKA_TOPIC_USER_ACTIVITY,
        event_data,
        key=f'user_{user_id}'
    )


def send_login_event(user_id, username):
    """Send user login event"""
    event_data = {
        'event_type': EventTypes.LOGIN,
        'user_id': user_id,
        'username': username,
    }
    producer = EventProducer()
    producer.send_event(
        settings.KAFKA_TOPIC_USER_ACTIVITY,
        event_data,
        key=f'user_{user_id}'
    )


def send_profile_updated_event(user_id, updated_fields):
    """Send profile updated event"""
    event_data = {
        'event_type': EventTypes.PROFILE_UPDATED,
        'user_id': user_id,
        'updated_fields': updated_fields,
    }
    producer = EventProducer()
    producer.send_event(
        settings.KAFKA_TOPIC_USER_ACTIVITY,
        event_data,
        key=f'user_{user_id}'
    )
