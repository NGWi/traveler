from flask import Flask, request, jsonify
from flask_cors import CORS
import main  # Main module of traveler repo

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

@app.route('/solve-tsp', methods=['POST'])
def solve_tsp():
    try:
        # Get locations from request JSON
        data = request.get_json()
        locations = data.get('locations', [])
        designated_end = data.get('designated_end', False)
        # Validate input
        if not locations or len(locations) < 2:
            return jsonify({"error": "At least 2 locations required"}), 400

        # Get distance matrix
        distance_matrix = main.get_distance_matrix(locations)
        if not distance_matrix:
            return jsonify({"error": "Failed to calculate distance matrix"}), 500
        # Get fastest route
        result = main.get_fastest_route(distance_matrix, designated_end)
        if not result:
            return jsonify({"error": "Failed to calculate route"}), 500

        time, path = result
        
        # Return locations in order instead of indices
        ordered_locations = [locations[i] for i in path]

        return jsonify({
            "total_time": time,
            "optimal_route": ordered_locations,
            "distance_matrix": distance_matrix
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)