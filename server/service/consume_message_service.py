import re, base64, json
from kafka import KafkaConsumer
# from controller import *

topic = 'tampered-image'
bootstrap_servers = ['localhost:9092']
consumer_timeout = 1000
group_id = 'topic-group'

consumer = KafkaConsumer(bootstrap_servers=bootstrap_servers)
consumer.subscribe(topic)

for message in consumer:
    # print(
    #     "> consuming message from %s partition=%d with offset=%d and key=%s" % (
    #         message.topic, message.partition, message.offset, message.key
    #     )
    # )
    print(message.value)
    try:
        if message is None:
            print('No Message Received')
            continue
        else:
            parsed_string = re.sub(r"[“|”|‛|’|‘|`|´|″|′|']", '"', str(message.value))
            json_image = json.loads(parsed_string)
            print(base64.b64decode(json_image['img']))
    except Exception as e:
        print(e.args)

# To consume latest messages and auto-commit offsets
# consumer.subscribe(topic)

# running = True
# while True:
#     try:
#         for message in consumer:
#             print(
#               "> consuming message from %s partition=%d with offset=%d and key=%s" % (
#                 message.topic, message.partition, message.offset, message.key
#               )
#             )
#             if message is None:
#                 continue
#             else:
#                 print(message)
#     except KeyboardInterrupt:
#         pass
#     finally:
#         consumer.close()
