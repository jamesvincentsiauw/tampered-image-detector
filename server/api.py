from flask import Flask, request, jsonify
from healthcheck import HealthCheck, EnvironmentDump
from controller import *

app = Flask(__name__)
app.config["DEBUG"] = False

# Configure Healthcheck
health = HealthCheck()
envdump = EnvironmentDump()

@app.route('/api/predictor', methods=['POST'])
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


# Add a flask route to expose information
app.add_url_rule("/health", "healthcheck", view_func=lambda: health.run())
app.add_url_rule("/environment", "environment", view_func=lambda: envdump.run())
   
    
if __name__ == "__main__":
    app.run(threaded=False)