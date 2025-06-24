from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib  # Import joblib for model loading

app = Flask(__name__)
CORS(app)

# Load the trained model once at startup
model = joblib.load('trained_model.pkl')

@app.route('/check', methods=['POST'])
def classify_statement():
    try:
        # Get the JSON data from the request
        data = request.get_json()
        user_input = data.get('input_string')

        # Use the loaded model to predict
        prediction = model.predict([user_input])[0]
        result = "Real" if prediction == 0 else "Fake"  # Adjust prediction based on your model's labeling

        return jsonify({"result": result})
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred while processing the request."}), 500

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message": "Connected through Flask"})

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
