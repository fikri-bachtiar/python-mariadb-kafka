from kafka import KafkaProducer

from app.config import settings

producer = KafkaProducer(
    bootstrap_servers="{}:{}".format(settings.app_kafka_broker_host, settings.app_kafka_broker_port)
)
