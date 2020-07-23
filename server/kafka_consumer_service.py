import base64
import json
import re
import urllib.request
import os
from controller import *
from config.kafka_producer_config import producer
from kafka import KafkaConsumer
from keras.models import load_model

topic = 'streaming-tampered-image'
bootstrap_servers = ['localhost:9092']
consumer_timeout = 1000
group_id = 'topic-group'

consumer = KafkaConsumer(
    bootstrap_servers=bootstrap_servers,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    )
consumer.subscribe(topic)

while True:
    try:
        for message in consumer:
            print(
                "> consuming message from %s partition=%d with offset=%d and key=%s" % (
                    message.topic, message.partition, message.offset, message.key
                )
            )
            try:
                if message is None:
                    print('No Message Received')
                    continue
                else:
                    # Parse passed data to json format
                    parsed_string = re.sub(r"[“|”|‛|’|‘|`|´|″|′|']", '"', str(message.value))
                    json_data = json.loads(parsed_string)

                    # check the directory to save the file
                    if not os.path.exists('data/'):
                        # make a directory if it doesn't exist
                        os.makedirs('data')

                    # Retrieve image from URL
                    urllib.request.urlretrieve(json_data['img'], json_data['file'])

                    # Process Prediction
                    model = load_model(choose_model(json_data['model']))
                    img = load(json_data['file'])
                    print(process_prediction(model, img))
            except Exception as e:
                print(e)
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
