from itertools import combinations
import sys
import json

def tsp_held_karp(distances, end_loc=None): # function can theoretically accept end as an index
    n = len(distances)
    if n <= 1:
        print("Invalid input. The number of locations must be at least 2.")
        return None, None
    if end_loc is None:
        end_loc = n - 1
    if end_loc < 0 or end_loc >= n:
        print("Invalid end location")
        return None, None

    sub_routes = dict()
    valid_locations = [loc for loc in range(1,n) if loc != end_loc]

    # Base case: start from 0 to other locations (excluding end_loc)
    for location in valid_locations:
        sub_routes[(1 << location, location)] = (distances[0][location], 0)

    # Iterate through subset sizes
    for subset_size in range(2, len(valid_locations) + 1):
        for subset in combinations(valid_locations, subset_size):
            subset_mask = sum(1 << loc for loc in subset)
            for location in subset:
                prev_mask = subset_mask ^ (1 << location)
                min_cost = float('inf')
                parent = None
                
                for p in subset:
                    if p == location:
                        continue
                    if (prev_mask, p) in sub_routes:
                        cost = sub_routes[(prev_mask, p)][0] + distances[p][location]
                        if cost < min_cost:
                            min_cost = cost
                            parent = p
                
                if min_cost != float('inf'):
                    sub_routes[(subset_mask, location)] = (min_cost, parent)

    # Calculate all_visited mask (all locations except 0 and end_loc)
    all_visited = sum(1 << loc for loc in valid_locations)

    # Find minimum cost to reach end location
    min_total = float('inf')
    last_location = None
    
    for location in valid_locations:
        if (all_visited, location) in sub_routes:
            cost = sub_routes[(all_visited, location)][0] + distances[location][end_loc]
            if cost < min_total:
                min_total = cost
                last_location = location

    # Reconstruct path
    if last_location is None:
        return None, None

    # Start from end location and work backwards
    path = []
    current = last_location
    mask = all_visited

    # Build path from end to start
    while mask:
        path.append(current)
        parent = sub_routes[(mask, current)][1]
        mask ^= (1 << current)  # Remove current from mask
        current = parent

    # Add the start location (0) at the beginning
    path.append(0)
    # Reverse to get correct order: start -> ... -> end
    path.reverse()
    # Add the final end location
    path.append(end_loc)

    return min_total, path

def convert_seconds(seconds):
    res = ""
    if seconds > 3600 * 24:
        days = seconds // (3600 * 24)
        res += f"{days} days "
        seconds %= (3600 * 24)
    if seconds > 3600:
        hours = seconds // 3600
        res += f"{hours} hours "
        seconds %= 3600
    minutes = seconds // 60
    res += f"{minutes} minutes"
    return res.strip()

def main():
    # Example usage
    # distance_matrix = [
    #     [0, 10, 15, 20],
    #     [10, 0, 35, 30],
    #     [15, 35, 0, 25],
    #     [20, 30, 25, 0],
    # ]
    # use_end_point = True

    input_data = sys.stdin.read()
    
    try:
        data = json.loads(input_data)
        distance_matrix = data['matrix']
        designated_end = data.get('designated_end', True)
    except Exception as e:
        print(json.dumps({"error": f"Invalid input: {str(e)}"}))
        return

    end_loc = len(distance_matrix) - 1 if designated_end else 0
    time, path = tsp_held_karp(distance_matrix, end_loc)
    
    if time is None or path is None:
        print(json.dumps({"error": "No valid path found"}))
        return
    
    print(json.dumps({
        "total_time": convert_seconds(time),
        "optimal_route": path
    }))

if __name__ == "__main__":
    main()