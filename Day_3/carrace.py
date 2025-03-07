from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/process_cars', methods=['POST'])
def process_cars(): 
    
    if 'Authorization' not in request.headers or 'carrace' not in request.headers['Authorization']:
        return jsonify({"error": "Unauthorized request"}), 401 
    try:
        data = request.json
        cars = data['car']  
    except (KeyError, TypeError):
        return jsonify({"error": "Invalid input format"}), 400
    
    
    if not cars:
        return jsonify({"error": "Empty car list"}), 400
    
    # Extract car names and check for required fields
    car_names = []
    for car in cars:
        if 'Name' not in car:
            return jsonify({"error": "Missing 'Name' field in car entry"}), 400
        car_names.append(car['Name'])
    
    
    output = {
        "Car List": car_names
    }
    
    return jsonify(output)

@app.route('/test', methods=['GET'])
def test():
    return "Flask app is running!"

@app.errorhandler(500)
def handle_server_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
