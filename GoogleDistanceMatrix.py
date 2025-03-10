from os import environ
from sys import argv
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

def main():
    locations = argv[1:]  # Get locations from command line arguments
    # Geocode all locations
    api_key = environ['GM_KEY']
    geocoded = []
    for loc in locations:
        coords = get_coordinates(loc, api_key)
        if coords:
            geocoded.append({"waypoint": {"location": {"latLng": coords}}})
        else:
            print(f"Failed to geocode: {loc}")
            return
            
    url = "https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-FieldMask": "originIndex,destinationIndex,duration",
        "X-Goog-Api-Key": api_key
    }

    # locations = [
    #     "San Francisco, CA",
    #     "Los Angeles, CA",
    #     "New York, NY",
    #     "Chicago, IL"
    # ]


    # Build payload
    payload = {
        "origins": geocoded,
        "destinations": geocoded,
        "travelMode": "DRIVE"
    }

    # Get distance matrix
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        print(f"API Error: {response.text}")
        return

    data = response.json()
    # Initialize matrix with zeros
    n = len(locations)
    matrix = [[0] * n for _ in range(n)]
    
    # Populate matrix from API response
    for entry in data:
        i = entry["originIndex"]
        j = entry["destinationIndex"]
        matrix[i][j] = int(entry["duration"][:-1])

    print(json.dumps(matrix))  # Output as JSON to be passed

if __name__ == "__main__":
    main()