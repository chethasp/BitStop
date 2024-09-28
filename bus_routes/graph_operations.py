import csv
import random
import numpy as np
import networkx as nx
from calculate_distances import get_duration

# Node and Graph classes
class Node:
    def __init__(self, name, address, latitude, longitude, weight=0):
        self.name = name
        self.address = address
        self.weight = weight
        self.latitude = latitude
        self.longitude = longitude
    
    def __str__(self):
        return f"Node info: {self.name}, {self.address}, {self.weight}"

class Graph:
    def __init__(self):
        self.nodes = {}  # key: name, value: node object
        self.edges = {}  # adjacency list for edges

    def add_node(self, name, address, weight, latitude, longitude):
        self.nodes[name] = Node(name, address, latitude, longitude, weight)
        self.edges[name] = {}

    def add_edge(self, name1, name2, weight=1):
        self.edges[name1][name2] = weight
        self.edges[name2][name1] = weight

    def get_node(self, name):
        return self.nodes[name]
    
    def get_edge(self, name1, name2):
        return self.edges[name1][name2]

# Step 1: Create the Graph
def create_graph(csv_file):
    graph = Graph()

    # Load foot traffic data from CSV
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        venues = list(reader)
    
    # Adding nodes with normalized foot traffic weights
    foot_traffic = np.array([int(venue['foot_traffic']) for venue in venues])  # Assuming 'foot_traffic' column exists
    min_val, max_val = min(foot_traffic), max(foot_traffic)

    for venue in venues:
        name = venue['name']
        address = venue['address']
        latitude = float(venue['latitude'])
        longitude = float(venue['longitude'])
        weight = 1 + 44 * (int(venue['foot_traffic']) - min_val) / (max_val - min_val)  # Normalized weight
        graph.add_node(name, address, weight, latitude, longitude)

    # Adding edges with weights based on driving duration
    node_names = list(graph.nodes.keys())
    for i in range(len(node_names)):
        for j in range(i + 1, len(node_names)):
            name1, name2 = node_names[i], node_names[j]
            lat1, lon1 = graph.get_node(name1).latitude, graph.get_node(name1).longitude
            lat2, lon2 = graph.get_node(name2).latitude, graph.get_node(name2).longitude
            duration = get_duration(lat1, lon1, lat2, lon2)
            graph.add_edge(name1, name2, max(duration, 1))  # Ensure weight is positive

    return graph

# Step 2: Generate Initial Routes
def generate_initial_routes(graph, num_routes=5):
    routes = []

    # Greedily generate initial routes based on high foot traffic nodes
    high_traffic_nodes = sorted(graph.nodes.values(), key=lambda x: x.weight, reverse=True)
    selected_nodes = [node.name for node in high_traffic_nodes[:num_routes]]

    for start_node in selected_nodes:
        # Generate a route starting from a high traffic node
        path = nx.single_source_dijkstra_path(graph, start_node)
        route = list(path.values())[0][:10]  # Take up to 10 nodes for a route
        routes.append(route)

    return routes

# Step 3: Cost Function
def calculate_cost(routes, graph):
    total_travel_time = 0
    uncovered_high_traffic_nodes = set(graph.nodes.keys())
    overlap_penalty = 0

    for route in routes:
        if len(route) < 2:
            continue  # Skip routes that don't have enough nodes

        # Calculate travel time for each route
        for i in range(len(route) - 1):
            total_travel_time += graph.get_edge(route[i], route[i + 1])

        # Track covered nodes
        uncovered_high_traffic_nodes -= set(route)

    # Add overlap penalty
    all_visited_nodes = [node for route in routes for node in route]
    overlap_penalty = len(all_visited_nodes) - len(set(all_visited_nodes))

    # Calculate cost
    cost = total_travel_time + 100 * len(uncovered_high_traffic_nodes) + 50 * overlap_penalty
    return cost

# Step 4: Genetic Algorithm (GA)
def genetic_algorithm(graph, initial_routes, num_generations=100):
    population = initial_routes
    population_size = len(initial_routes)

    for generation in range(num_generations):
        # Calculate fitness for each individual
        fitness = [1 / calculate_cost([route], graph) for route in population]

        # Selection: Select parents based on fitness
        parents = random.choices(population, weights=fitness, k=population_size)

        # Crossover: Create new routes by combining parents
        offspring = []
        for i in range(0, len(parents), 2):
            if i + 1 < len(parents):
                parent1, parent2 = parents[i], parents[i + 1]
                crossover_point = random.randint(1, min(len(parent1), len(parent2)) - 1)
                child = parent1[:crossover_point] + parent2[crossover_point:]
                offspring.append(child)

        # Mutation: Randomly modify some routes
        for route in offspring:
            if random.random() < 0.1:  # Mutation probability
                idx = random.randint(0, len(route) - 1)
                new_node = random.choice(list(graph.nodes.keys()))
                route[idx] = new_node

        # Update population
        population = parents + offspring
        population = sorted(population, key=lambda r: calculate_cost([r], graph))[:population_size]

    # Return the best routes
    return sorted(population, key=lambda r: calculate_cost([r], graph))[:5]

# Step 5: Simulated Annealing (SA)
def simulated_annealing(graph, route, initial_temp=1000, cooling_rate=0.95, num_iterations=100):
    current_route = route
    current_cost = calculate_cost([current_route], graph)
    temp = initial_temp

    for i in range(num_iterations):
        # Generate a neighboring route
        new_route = current_route[:]
        idx1, idx2 = random.sample(range(len(new_route)), 2)
        new_route[idx1], new_route[idx2] = new_route[idx2], new_route[idx1]

        # Calculate new cost
        new_cost = calculate_cost([new_route], graph)

        # Acceptance probability
        if new_cost < current_cost or random.random() < np.exp((current_cost - new_cost) / temp):
            current_route = new_route
            current_cost = new_cost

        # Cool down temperature
        temp *= cooling_rate

    return current_route

# Step 6: Finalize Routes
def optimize_routes(graph, initial_routes):
    # Step 1: Use Genetic Algorithm for initial optimization
    optimized_routes = genetic_algorithm(graph, initial_routes)

    # Step 2: Use Simulated Annealing to fine-tune the routes
    final_routes = []
    for route in optimized_routes:
        final_route = simulated_annealing(graph, route)
        final_routes.append(final_route)

    return final_routes

# Main function to run the full program
if __name__ == "__main__":
    graph = create_graph('static/foot_traffic_sites.csv')
    initial_routes = generate_initial_routes(graph)
    optimized_routes = optimize_routes(graph, initial_routes)

    # Print the optimized routes
    for idx, route in enumerate(optimized_routes):
        print(f"Route {idx + 1}: {route}")
