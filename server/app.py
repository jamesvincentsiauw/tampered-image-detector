from flask import Flask, request, jsonify
import connexion
from healthcheck import HealthCheck, EnvironmentDump
from controller import *

# Configure Healthcheck
health = HealthCheck()
envdump = EnvironmentDump()

# Main Method. Will be called by Connexion and Connected with Swagger
def tampered_image_processing():
    try:
        requested_model = request.form['model']

        if choose_model(requested_model) == "error":
            val = {
                'status': "Error",
                'message': 'Model Not Found!'
            }
            return jsonify(val), 400

        # Load the model
        model = load_model(choose_model(requested_model))

        # Process file
        if not request.files['img']:
            return jsonify({
                'message': "Bad Parameter!",
                'status': "Error"
            }), 400
        filepath = files_handler(request.files['img'])
        img = load(filepath)

        result = process_prediction(model, img)
        return jsonify(result), 200
    
    except Exception as e:
        print(e)
        return {
            'status': "Error",
            'message': e.args
        }, 500
    
if __name__ == "__main__":
    # Create the application instance
    app = connexion.App(__name__, specification_dir='openapi/')
    
    # Add a flask route to expose information
    app.add_url_rule("/health", "healthcheck", view_func=lambda: health.run())
    app.add_url_rule("/environment", "environment", view_func=lambda: envdump.run())
    
    # Read the swagger.yml file to configure the endpoints
    app.add_api('swagger.yaml')
    app.run(threaded=False)