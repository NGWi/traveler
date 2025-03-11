# The Traveler App
This project is live at https://the-traveler-fucj.onrender.com/ (Mar 10, 2025)

This backend uses the optimal exact solution to the traveling salesman problem to find the shortest route from a starting location through a set of locations (and, optionally, back to the starting location).

Future plan: Integrate with Google Maps to show the completed route.

To launch the backend:
- Sign up for a Google Maps API key and add it to your Shell environment file as GM_KEY=...
- Install requirements in requirements.txt (e.g., `pip install -r requirements.txt`)
- Run `python api.py` to start the backend.

It is set up to run on port 5001. That can be changed by modifying the last line of `api.py`.
