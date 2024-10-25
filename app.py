from flask import Flask, jsonify
from flight_data_forge import generate_flight_data
from process_flight_data import process_flight_data

app = Flask(__name__)

@app.route('/generate-flights', methods=['POST'])
def generate_flights():
    message = generate_flight_data()
    return jsonify({"message": message})

@app.route('/process-flights', methods=['GET'])
def process_flights():
    result = process_flight_data()
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
