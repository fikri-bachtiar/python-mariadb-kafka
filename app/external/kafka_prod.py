from kafka import KafkaProducer

# from app.config import settings

producer = KafkaProducer(bootstrap_servers="127.0.0.1:29092")
