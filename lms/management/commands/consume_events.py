"""
Django management command to run Kafka consumer for user activity events.
"""
from django.core.management.base import BaseCommand
from lms.consumers import start_consumer
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Start Kafka consumer for processing user activity events'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Kafka consumer...'))
        self.stdout.write('Press Ctrl+C to stop')
        
        try:
            start_consumer()
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('\nConsumer stopped'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
            logger.error(f'Consumer error: {e}')
