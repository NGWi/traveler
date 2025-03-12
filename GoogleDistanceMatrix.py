from os import environ
import requests
import json


def get_coordinates(address, api_key):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": api_key}
    response = requests.get(base_url, params=params)
    data = response.json()
    if data["results"]:
        location = data["results"][0]["geometry"]["location"]
        return {"latitude": location["lat"], "longitude": location["lng"]}
    return None


def get_matrix(locations):
    """Get distance matrix from Google Maps API."""
    api_key = environ["GM_KEY"]
    geocoded = []
    for loc in locations:
        coords = get_coordinates(loc, api_key)
        if coords:
            geocoded.append({"waypoint": {"location": {"latLng": coords}}})
        else:
            print(f"Failed to geocode: {loc}")
            return None

    url = "https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-FieldMask": "originIndex,destinationIndex,duration",
        "X-Goog-Api-Key": api_key,
    }

    total = len(geocoded)
    payload = {
        "origins": geocoded,
        "destinations": geocoded,
        "travelMode": "DRIVE",
        "routingPreference": (
            "TRAFFIC_AWARE_OPTIMAL" if total <= 10 else "TRAFFIC_AWARE"
        ),
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        print(f"API Error: {response.text}")
        return None
    data = response.json()

    # Initialize matrix with zeros
    matrix = [[0] * total for _ in range(total)]
    # Populate matrix from API response
    for entry in data:
        i = entry["originIndex"]
        j = entry["destinationIndex"]
        matrix[i][j] = int(entry["duration"][:-1])

    return matrix


def main():
    from sys import argv

    locations = argv[1:]  # Get locations from command line arguments
    matrix = get_matrix(locations)
    if matrix:
        print(json.dumps(matrix))


if __name__ == "__main__":
    main()
