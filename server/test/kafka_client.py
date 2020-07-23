import base64
import json
import re
from kafka import KafkaConsumer

topic = 'streaming-tampered-image-response'
bootstrap_servers = ['localhost:9092']
consumer_timeout = 1000
group_id = 'topic-group'

consumer = KafkaConsumer(
    bootstrap_servers=bootstrap_servers,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    )
consumer.subscribe(topic)

print("Listening to Topic: ", topic)

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

                    print(json_data)
            except Exception as e:
                print(e)
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
