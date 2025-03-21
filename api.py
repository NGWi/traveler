import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import main  # Main module of traveler repo

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests


@app.route("/solve-tsp", methods=["POST"])
def solve_tsp():
    try:
        # Get locations from request JSON
        data = request.get_json()
        locations = data.get("locations", [])
        designated_end = data.get("designated_end", False)
        # Validate input
        if not locations or len(locations) < 2:
            return jsonify({"error": "At least 2 locations required"}), 400

        # Get distance matrix
        distance_matrix = main.get_distance_matrix(locations)
        if not distance_matrix:
            return jsonify({"error": "Failed to calculate distance matrix"}), 500
        
        # Check for geocoding error
        if isinstance(distance_matrix, dict) and "error" in distance_matrix:
            return jsonify(distance_matrix), 400
        
        # Get fastest route
        result = main.get_fastest_route(distance_matrix, designated_end)
        if not result:
            return jsonify({"error": "Failed to calculate route"}), 500

        time, path = result


        return jsonify(
            {
                "total_time": time,
                "optimal_route": path,
                "distance_matrix": distance_matrix,
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    if os.environ.get("FLASK_ENV") == "production":
        from gunicorn.app.base import BaseApplication

        class GunicornApp(BaseApplication):
            def __init__(self, app, options=None):
                self.options = options or {}
                self.application = app
                super().__init__()

            def load_config(self):
                for key, value in self.options.items():
                    self.cfg.set(key, value)

            def load(self):
                return self.application

        options = {
            "bind": "0.0.0.0:8000",
            "workers": 1,  # Single worker for free tier
            "worker_class": "sync",  # Safer for memory-intensive operations
            "timeout": 120,  # 2 minutes timeout
            "graceful_timeout": 60,
        }

        GunicornApp(app, options).run()
    else:
        # Development server
        app.run(debug=True, port=5001)
