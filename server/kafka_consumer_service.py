import base64
import json
import re
import urllib.request
import os
import uuid
from controller import *
from config.kafka_producer_config import producer
from kafka import KafkaConsumer
from keras.models import load_model
from dotenv import load_dotenv

load_dotenv()
server = os.getenv('KAFKA_IP_SERVER')
topic = 'streaming-tampered-image'
client_topic = 'streaming-tampered-image-response'
bootstrap_servers = [server]
consumer_timeout = 1000
group_id = 'topic-group'

consumer = KafkaConsumer(
    bootstrap_servers=bootstrap_servers,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    )
consumer.subscribe(topic)
print("Listening to Topic: ", topic)

def produce_to_client(topic, data):
    try:
        producer().send(
            topic=topic,
            value=data,
                key=str(uuid.uuid4())
            ).add_callback(success).add_errback(error)

        producer().flush()

        return 'Send Produce Topic Success'
    except:
        print(e)
        return 'Send Produce Topic Failed'


# Kafka success message
def success(rec):
    print('> message delivered to %s with partition %d and offset %d' % (rec.topic, rec.partition, rec.offset))


# Kafka exception message
def error(exception):
    print('> message unsent with exception:', exception)

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

                    result = process_prediction(model, img)

                    produce_to_client(topic=client_topic, data=result)
            except Exception as e:
                print(e)
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
