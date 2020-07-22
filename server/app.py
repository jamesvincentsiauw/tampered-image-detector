import base64
import uuid
import cv2
import requests
import connexion
from config.kafka_producer_config import producer
from controller import *
from flask import request, jsonify
from healthcheck import HealthCheck
from keras.models import load_model

# Configure Healthcheck
health = HealthCheck()


# Main Method. Will be called by Connexion and Connected with Swagger
def tampered_image_processing():
    try:
        requested_model = request.form['model']

        if choose_model(requested_model) == 'error':
            val = {
                'status': 'error',
                'message': 'Model Not Found!'
            }
            return jsonify(val), 400

        # Load the model
        model = load_model(choose_model(requested_model))

        # Process file
        if not request.files['img']:
            return jsonify({
                'message': 'Bad Parameter! Please upload file',
                'status': 'error'
            }), 400
        filepath = files_handler(request.files['img'])
        if filepath == 'error':
            val = {
                'status': 'error',
                'message': 'Bad Parameter, Check File Extension!'
            }
            return jsonify(val), 400

        img = load(filepath)

        result = process_prediction(model, img)
        return jsonify(result), 200

    except Exception as e:
        print(e)
        return {
            'status': 'error',
            'message': e.args
        }, 500


# Method for Kafka Producer
def produce():
    try:
        topic = 'tampered-image'

        data = {
            'model': 'v2',
            'img': request.args.get('url'),
            'file': 'data/'+str(uuid.uuid4())+'.jpg'
        }

        producer().send(
                topic=topic,
                value=data,
                key=str(uuid.uuid4())
            ).add_callback(success).add_errback(error)

        producer().flush()

        response_message = 'Send Produce Topic Success'
    except Exception as e:
        print(e.args)
        response_message = 'Send Produce Topic Failed'
    return response_message


# Kafka success message
def success(rec):
    print('> message delivered to %s with partition %d and offset %d' % (rec.topic, rec.partition, rec.offset))


# Kafka exception message
def error(exception):
    print('> message unsent with exception:', exception)


if __name__ == '__main__':
    # Create the application instance
    app = connexion.App(__name__, specification_dir='openapi/')

    # Add a flask route to expose information
    app.add_url_rule('/api/predictor/health', 'healthcheck', view_func=lambda: health.run())

    # Read the swagger.yml file to configure the endpoints
    app.add_api('swagger.yaml')
    app.run(threaded=False)
