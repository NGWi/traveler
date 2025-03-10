import subprocess
import json

def get_distance_matrix(locations):
    try:
        output = subprocess.check_output(
            ["python", "GoogleDistanceMatrix.py"] + locations, 
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        distance_matrix = json.loads(output.strip())  # Assuming the output is a JSON string
        return distance_matrix
    except subprocess.CalledProcessError as e:
        print(f"Error while calling GoogleDistanceMatrix.py: {e.stderr}")
    except SyntaxError:
        print("Invalid matrix format")
    return None

def get_fastest_route(distance_matrix):
    try:
        # Serialize the distance matrix to JSON
        matrix_json = json.dumps(distance_matrix)

        # Call travelingSalesman.py and pass the distance matrix as input
        process = subprocess.Popen(
            ['python', 'travelingSalesman.py'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # Send the matrix JSON to the subprocess
        stdout, stderr = process.communicate(input=matrix_json)
        if process.returncode != 0:
            print(f"Error in travelingSalesman.py: {stderr}")
            return None
        
        # Assuming travelingSalesman.py returns a JSON string
        result = json.loads(stdout.strip())
        return result
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def main(): 
    # Sample user_input:
    user_input = ["San Francisco, CA", "Los Angeles, CA", "New York, NY", "Chicago, IL"]
    
    # Get distance matrix
    distance_matrix = get_distance_matrix(user_input)
    
    if distance_matrix is None:
        print("Failed to retrieve the distance matrix.")
        return

    # Sample data:
    # distance_matrix = [ [0, 20924, 152768, 110588],
    #                     [21116, 0, 146201, 104021],
    #                     [153269, 146469, 0, 43370],
    #                     [111089, 104289, 43514, 0]]

    # Get fastest route
    fastest_route = get_fastest_route(distance_matrix)
    
    if fastest_route is None:
        print("Failed to retrieve the fastest route.")
        return
    
    time, path = fastest_route  # Assuming result is a tuple of (time, path)
    
    print(f"Minimum time: {time}")
    print(f"Optimal path: {path}")

if __name__ == "__main__":
    main()