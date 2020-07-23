from kafka import KafkaProducer
import json
import pickle
import uuid

bootstrap_servers = ['localhost:9092']
producer_timeout = 2000


def producer():
    producer = KafkaProducer(
        acks=1,

        # Acks ='all',
        retries=5,
        compression_type='gzip', # Just use default compression: gzip
        request_timeout_ms=producer_timeout,
        bootstrap_servers=bootstrap_servers,
        key_serializer=str.encode,

        # Config for image
        value_serializer=lambda m: json.dumps(m).encode('utf-8')
        # value_serializer=lambda m: pickle.dumps(m)
    )
    return producer