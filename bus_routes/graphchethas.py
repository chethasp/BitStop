import networkx as nx
import numpy as np
import random
import pandas as pd
from calculate_distances import get_duration

# Step 1: Create the Graph
def create_graph():
    G = nx.Graph()

    # Load foot traffic data from CSV
    venues = pd.read_csv('static/foot_traffic_sites.csv')
    
    # Adding nodes with normalized foot traffic weights
    foot_traffic = venues['foot_traffic'].values  # Assuming 'foot_traffic' column exists
    min_val, max_val = min(foot_traffic), max(foot_traffic)

    for i in range(len(foot_traffic)):
        normalized_weight = 1 + 44 * (foot_traffic[i] - min_val) / (max_val - min_val)
        G.add_node(i, weight=normalized_weight)

    # Adding edges with weights based on driving duration
    for i in range(len(foot_traffic)):
        for j in range(i + 1, len(foot_traffic)):
            lat1, lon1 = venues.iloc[i]['latitude'], venues.iloc[i]['longitude']
            lat2, lon2 = venues.iloc[j]['latitude'], venues.iloc[j]['longitude']
            duration = get_duration(lat1, lon1, lat2, lon2)
            G.add_edge(i, j, weight=max(duration, 1))  # Ensure weight is positive

    return G

# Step 2: Generate Initial Routes
def generate_initial_routes(G, num_routes=5):
    routes = []

    # Greedily generate initial routes based on high foot traffic nodes
    high_traffic_nodes = sorted(G.nodes(data=True), key=lambda x: x[1]['weight'], reverse=True)
    selected_nodes = [node[0] for node in high_traffic_nodes[:num_routes]]

    for start_node in selected_nodes:
        # Generate a route starting from a high traffic node
        path = nx.single_source_dijkstra_path(G, start_node)
        route = list(path.values())[0][:10]  # Take up to 10 nodes for a route
        routes.append(route)

    return routes

# Step 3: Cost Function
def calculate_cost(routes, G):
    total_travel_time = 0
    uncovered_high_traffic_nodes = set(G.nodes)
    overlap_penalty = 0

    for route in routes:
        # Calculate travel time for each route
        for i in range(len(route) - 1):
            total_travel_time += G[route[i]][route[i + 1]]['weight']

        # Track covered nodes
        uncovered_high_traffic_nodes -= set(route)

    # Add overlap penalty
    all_visited_nodes = [node for route in routes for node in route]
    overlap_penalty = len(all_visited_nodes) - len(set(all_visited_nodes))

    # Calculate cost
    cost = total_travel_time + 100 * len(uncovered_high_traffic_nodes) + 50 * overlap_penalty
    return cost

# Step 4: Genetic Algorithm (GA)
def genetic_algorithm(G, initial_routes, num_generations=100):
    population = initial_routes
    population_size = len(initial_routes)

    for generation in range(num_generations):
        # Calculate fitness for each individual
        fitness = [1 / calculate_cost([route], G) for route in population]

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
                new_node = random.choice(list(G.nodes))
                route[idx] = new_node

        # Update population
        population = parents + offspring
        population = sorted(population, key=lambda r: calculate_cost([r], G))[:population_size]

    # Return the best routes
    return sorted(population, key=lambda r: calculate_cost([r], G))[:5]

# Step 5: Simulated Annealing (SA)
def simulated_annealing(G, route, initial_temp=1000, cooling_rate=0.95, num_iterations=100):
    current_route = route
    current_cost = calculate_cost([current_route], G)
    temp = initial_temp

    for i in range(num_iterations):
        # Generate a neighboring route
        new_route = current_route[:]
        idx1, idx2 = random.sample(range(len(new_route)), 2)
        new_route[idx1], new_route[idx2] = new_route[idx2], new_route[idx1]

        # Calculate new cost
        new_cost = calculate_cost([new_route], G)

        # Acceptance probability
        if new_cost < current_cost or random.random() < np.exp((current_cost - new_cost) / temp):
            current_route = new_route
            current_cost = new_cost

        # Cool down temperature
        temp *= cooling_rate

    return current_route

# Step 6: Finalize Routes
def optimize_routes(G, initial_routes):
    # Step 1: Use Genetic Algorithm for initial optimization
    optimized_routes = genetic_algorithm(G, initial_routes)

    # Step 2: Use Simulated Annealing to fine-tune the routes
    final_routes = []
    for route in optimized_routes:
        final_route = simulated_annealing(G, route)
        final_routes.append(final_route)

    return final_routes

# Main function to run the full program
if __name__ == "__main__":
    G = create_graph()
    initial_routes = generate_initial_routes(G)
    optimized_routes = optimize_routes(G, initial_routes)

    # Print the optimized routes
    for idx, route in enumerate(optimized_routes):
        print(f"Route {idx + 1}: {route}")
