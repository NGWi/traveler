from itertools import combinations
import numpy as np
import sys
import json


def tsp_held_karp_small(distances, end_loc=None):
    """Original Held-Karp implementation for small routes."""
    n = len(distances)
    if n <= 1:
        print("Invalid input. The number of locations must be at least 2.")
        return None, None
    if n == 2:
        if end_loc == 0:
            return distances[0][1] + distances[1][0], [0, 1, 0]
        else:
            return distances[0][1], [0, 1]
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
    min_total = float("inf")
    last_location = None

    for location in valid_locations:
        if (all_visited, location) in sub_routes:
            cost = sub_routes[(all_visited, location)][0] + distances[location][end_loc]
            if cost < min_total:
                min_total = cost
                last_location = location

    if last_location is None:
        return None, None

    # Reconstruct path
    path = []
    current = last_location
    mask = all_visited

    while mask:
        path.append(current)
        parent = sub_routes[(mask, current)][1]
        mask ^= 1 << current
        current = parent

    path.append(0)
    path.reverse()
    path.append(end_loc)

    return min_total, path


def tsp_held_karp_large(distances, end_loc=None):
    """NumPy-optimized Held-Karp for large routes."""
    n = len(distances)
    if n <= 1:
        print("Invalid input. The number of locations must be at least 2.")
        return None, None
    if n == 2:
        if end_loc == 0:
            return distances[0][1] + distances[1][0], [0, 1, 0]
        else:
            return distances[0][1], [0, 1]
    if end_loc is None:
        end_loc = n - 1
    if end_loc < 0 or end_loc >= n:
        print("Invalid end location")
        return None, None

    # Convert to numpy array for faster operations
    distances = np.array(distances)

    # Pre-compute valid locations and their masks
    valid_locations = np.array([i for i in range(1, n) if i != end_loc])
    location_masks = 1 << valid_locations

    # Initialize dp arrays with infinity
    max_states = 1 << (n - 1)  # 2^(n-1) possible states
    dp = np.full((max_states, n), np.inf)
    parent = np.full((max_states, n), -1, dtype=np.int32)

    # Base case: direct paths from start
    for i, loc in enumerate(valid_locations):
        dp[location_masks[i], loc] = distances[0, loc]

    # Iterate through all possible subset sizes
    for size in range(2, len(valid_locations) + 1):
        # Generate all possible subsets of size 'size'
        for subset in combinations(range(len(valid_locations)), size):
            # Calculate subset mask
            subset_mask = sum(location_masks[i] for i in subset)
            subset_locs = valid_locations[list(subset)]

            # For each possible last location in subset
            for i, last in enumerate(subset_locs):
                # Remove last location from subset
                prev_mask = subset_mask ^ (1 << last)

                # Try all possible previous locations
                prev_locs = np.array(
                    [loc for j, loc in enumerate(subset_locs) if j != i]
                )
                costs = dp[prev_mask, prev_locs] + distances[prev_locs, last]

                # Find minimum cost and its index
                min_idx = np.argmin(costs)
                min_cost = costs[min_idx]

                if min_cost != np.inf:
                    dp[subset_mask, last] = min_cost
                    parent[subset_mask, last] = prev_locs[min_idx]

    # Calculate final costs to end location
    all_visited = sum(1 << loc for loc in valid_locations)
    final_costs = dp[all_visited, valid_locations] + distances[valid_locations, end_loc]

    # Find minimum cost and last location
    min_idx = np.argmin(final_costs)
    min_total = final_costs[min_idx]
    last_location = valid_locations[min_idx]

    if min_total == np.inf:
        return None, None

    # Reconstruct path
    path = []
    current = last_location
    mask = all_visited

    while mask:
        path.append(current)
        current = parent[mask, current]
        mask ^= 1 << path[-1]

    path.append(0)  # Add start location
    path.reverse()
    path.append(end_loc)  # Add end location

    return float(min_total), path


def tsp_held_karp(locations, end_loc=None):
    """Adaptive TSP solver that chooses algorithm based on input size."""
    n = len(locations)
    if end_loc == 0:
        n += 1
    if n <= 17:  # Use original algorithm for small routes
        return tsp_held_karp_small(locations, end_loc)
    else:  # Use NumPy optimization for larger routes
        return tsp_held_karp_large(locations, end_loc)


def convert_seconds(seconds):
    res = ""
    seconds = int(seconds)
    if seconds > 3600 * 24:
        days = seconds // (3600 * 24)
        res += f"{days} days "
        seconds %= 3600 * 24
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
    # designated_end = True

    input_data = sys.stdin.read()

    try:
        data = json.loads(input_data)
        distance_matrix = data["matrix"]
        designated_end = data.get("designated_end", False)
    except Exception as e:
        print(json.dumps({"error": f"Invalid input: {str(e)}"}))
        return

    end_loc = len(distance_matrix) - 1 if designated_end else 0
    time, path = tsp_held_karp(distance_matrix, end_loc)

    if time is None or path is None:
        print(json.dumps({"error": "No valid path found"}))
        return

    print(json.dumps({"total_time": convert_seconds(time), "optimal_route": path}))


if __name__ == "__main__":
    main()
