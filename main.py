from GoogleDistanceMatrix import get_matrix
from travelingSalesman import tsp_held_karp, convert_seconds


def get_distance_matrix(locations):
    try:
        matrix = get_matrix(locations)
        if not matrix:
            print("Failed to get distance matrix from API")
            return None
        return matrix
    except Exception as e:
        print(f"Error while getting distance matrix: {str(e)}")
        return None


def get_fastest_route(distance_matrix, designated_end=False):
    try:
        end_loc = len(distance_matrix) - 1 if designated_end else 0
        time, path = tsp_held_karp(distance_matrix, end_loc)

        if time is None or path is None:
            print("No valid path found")
            return None

        return (convert_seconds(time), path)

    except Exception as e:
        print(f"Route Error: {str(e)}")
        return None


def main():
    # Sample user_input:
    sample_input = [
        "San Francisco, CA",
        "Los Angeles, CA",
        "New York, NY",
        "Chicago, IL",
    ]

    # Get distance matrix
    distance_matrix = get_distance_matrix(sample_input)

    if distance_matrix is None:
        print("Failed to retrieve the distance matrix.")
        return

    # Sample data:
    # distance_matrix = [ [0, 20924, 152768, 110588],
    #                     [21116, 0, 146201, 104021],
    #                     [153269, 146469, 0, 43370],
    #                     [111089, 104289, 43514, 0]]

    # Get fastest route
    fastest_route = get_fastest_route(
        distance_matrix, designated_end=True
    )  # Default False for backwards compatiibility

    if fastest_route is None:
        print("Failed to retrieve the fastest route.")
        return

    time, path = fastest_route  # Assuming result is a tuple of (time, path)

    print(f"Minimum time: {time}")
    print(f"Optimal path: {path}")


if __name__ == "__main__":
    main()
