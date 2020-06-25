from flask import Flask, request, jsonify
from controller import *

app = Flask(__name__)

@app.route('/api/predictor', methods=['POST'])
def tampered_image_processing():
    try:
        requested_model = request.form['model']
        
        # Load the model
        model = load_model(choose_model(requested_model))
        
        # Process file
        filepath = files_handler(request.files['img'])
        img = load(filepath)
        
        result = process_prediction(model, img)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({
            'message': e.args
        })
   
if __name__ == "__main__":
    app.run(threaded=False)