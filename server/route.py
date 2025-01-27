import osmnx as ox
import networkx as nx
import itertools
import numpy as np
from shapely.geometry import LineString

G = ox.load_graphml("route/mumbai_road_network.graphml")
G = ox.add_edge_speeds(G)  # Adds speed limit data
G = ox.add_edge_travel_times(G)  # Adds estimated travel time for edges
# Warehouse Location (Latitude, Longitude)
warehouse_location = (19.116458, 72.902696) 
print(warehouse_location[1], warehouse_location[0])
warehouse_node = ox.distance.nearest_nodes(G, warehouse_location[1], warehouse_location[0])

def optimal_route(delivery_locations):
    delivery_nodes = [ox.distance.nearest_nodes(G, lon, lat) for lat, lon in delivery_locations]
    # Combine warehouse + delivery nodes
    all_nodes = [warehouse_node] + delivery_nodes

    # Compute shortest paths between all locations
    distance_matrix = {}
    shortest_paths = {}
    for i in range(len(all_nodes)):
        for j in range(len(all_nodes)):
            if i != j:
                path = nx.shortest_path(G, all_nodes[i], all_nodes[j], weight="length")
                shortest_paths[(i, j)] = path
                distance_matrix[(i, j)] = nx.shortest_path_length(G, all_nodes[i], all_nodes[j], weight="length")
    print("before",distance_matrix)
    

    # Function to get the distance between two nodes
    def get_distance(u, v):
        return distances.get((u, v), float('inf'))

    # Function to calculate the shortest path using dynamic programming (TSP)
    def tsp(nodes):
        n = len(nodes)
        # DP table to store the shortest path with a bitmask for visited nodes
        dp = {}
        parent = {}

        # Helper function to calculate the DP recursively
        def dp_rec(mask, last):
            if mask == (1 << n) - 1:  # All nodes have been visited
                return get_distance(last, 0)  # Return to the start

            if (mask, last) in dp:
                return dp[(mask, last)]

            best_cost = float('inf')
            for i in range(n):
                if mask & (1 << i) == 0:  # If node i hasn't been visited
                    new_mask = mask | (1 << i)
                    cost = get_distance(nodes[last], nodes[i]) + dp_rec(new_mask, i)
                    if cost < best_cost:
                        best_cost = cost
                        parent[(mask, last)] = i

            dp[(mask, last)] = best_cost
            return best_cost

        # Start the recursion with node 0 and no nodes visited
        start_mask = 1  # Only node 0 is visited initially
        result = dp_rec(start_mask, 0)

        # Reconstruct the path from the parent table
        path = []
        mask = start_mask
        last = 0
        while (mask, last) in parent:
            next_node = parent[(mask, last)]
            path.append(nodes[next_node])
            mask |= (1 << next_node)
            last = next_node

        path.append(0)  # Add the starting node at the end to complete the cycle
        return result, path
    
    distances = distance_matrix

    # Get unique nodes from the distance dictionary
    nodes = set()
    for (u, v) in distances.keys():
        nodes.add(u)
        nodes.add(v)

    # Convert the set to a sorted list
    nodes = sorted(nodes)

    # Compute the shortest distance and the path
    shortest_distance, shortest_path = tsp(nodes)
    if (len(shortest_path) >1):
        shortest_path = [0]+shortest_path
    print("Shortest Distance:", shortest_distance)
    print("Optimal Path:", shortest_path)



    optimized_route = [all_nodes[i] for i in shortest_path]
    # Reconstruct full route with extra lat/lon points along edges
    full_route_nodes = []
    full_route_latlon = []  # Stores all lat/lon points

    for i in range(len(optimized_route) - 1):
        start, end = optimized_route[i], optimized_route[i + 1]
        path = shortest_paths[(all_nodes.index(start), all_nodes.index(end))]  # Get the shortest path

        # Add original nodes to the route (avoid duplicates)
        full_route_nodes.extend(path[:-1])

        # Add extra lat/lon points along edges
        for u, v in zip(path[:-1], path[1:]):
            if G.has_edge(u, v):
                edge_data = G.get_edge_data(u, v)
                if isinstance(edge_data, dict):
                    edge_data = list(edge_data.values())[0]  # Get first edge if multiple exist

                if "geometry" in edge_data:
                    # Use existing road geometry
                    line: LineString = edge_data["geometry"]
                    road_points = list(zip(line.xy[1], line.xy[0]))  # Extract (lat, lon)
                    full_route_latlon.extend(road_points)
                else:
                    # If no geometry, interpolate points between nodes
                    lat1, lon1 = G.nodes[u]['y'], G.nodes[u]['x']
                    lat2, lon2 = G.nodes[v]['y'], G.nodes[v]['x']
                    num_extra_points = 10  # Increase for denser paths
                    for j in np.linspace(0, 1, num_extra_points):
                        full_route_latlon.append((lat1 * (1 - j) + lat2 * j, lon1 * (1 - j) + lon2 * j))

    # Add the final node's lat/lon to the route
    final_lat, final_lon = G.nodes[optimized_route[-1]]['y'], G.nodes[optimized_route[-1]]['x']
    full_route_latlon.append((final_lat, final_lon))


    def compute_route_distances(shortest_route, distance_matrix):
        route_distances = []
        distance = 0
        for i in range(len(shortest_route) - 1):
            if (i==len(shortest_route) - 1):
                break
            start = shortest_route[i]
            end = shortest_route[i + 1]

            distance += distance_matrix.get((start, end))  # Get precomputed distance
         
            # print(start,end,distance,distance/1000)
            route_distances.append(round(distance/1000, 2))
        return route_distances
    distances = compute_route_distances(shortest_path, distance_matrix)
    return full_route_latlon,shortest_path,distances

# delivery_locations = [(19.125914, 72.857195), (19.110758, 72.868224),(19.102111, 72.886025),(19.100309, 72.903522)]
# delivery_locations = [(19.12200913893384,72.8597874644038),(19.141957259861694,72.84297752485146)]
# a,optimized_route,distance = optimal_route(delivery_locations)
# print(optimized_route,distance)
