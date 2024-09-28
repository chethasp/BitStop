import networkx as nx
import numpy as np
import random
import pandas as pd
import math 
import matplotlib.pyplot as plt

def get_duration_from_csv(venue1_name, venue2_name, csv_file='static/durations.csv'):
    # Load the durations data from the CSV file
    durations_df = pd.read_csv(csv_file)

    # Iterate through the rows to find the matching venue pairs
    for index, row in durations_df.iterrows():
        if (row['venue_name1'] == venue1_name and row['venue_name2'] == venue2_name) or \
           (row['venue_name1'] == venue2_name and row['venue_name2'] == venue1_name):
            return row['Duration (minutes)']

    # Return a default value if no match is found
    return float('inf')  # Indicates no connection

def create_graph():
    G = nx.Graph()

    # Load foot traffic data from CSV
    venues = pd.read_csv('static/foot_traffic_sites.csv')
    
    # Adding nodes with normalized foot traffic weights and positions
    foot_traffic = venues['foot_traffic'].values  # Assuming 'foot_traffic' column exists
    min_val, max_val = min(foot_traffic), max(foot_traffic)

    for i in range(len(foot_traffic)):
        normalized_weight = 1 + 44 * (foot_traffic[i] - min_val) / (max_val - min_val)
        # Extract latitude and longitude
        latitude = venues.iloc[i]['latitude']  # Assuming 'latitude' column exists
        longitude = venues.iloc[i]['longitude']  # Assuming 'longitude' column exists
        G.add_node(i, weight=normalized_weight, pos=(longitude, latitude))  # Store position as (longitude, latitude)

    # Initialize an edge counter
    edge_count = 0
    
    # Adding edges with weights based on driving duration
    penalty_factor = 22  # Adjust this value to increase or decrease the penalty for longer routes
    for i in range(len(foot_traffic)):
        for j in range(i + 1, len(foot_traffic)):
            duration = get_duration_from_csv(venues.iloc[i]['venue_name'], venues.iloc[j]['venue_name'])
            if duration != float('inf'):  # Only add edges with valid durations
                # Calculate edge weight with a penalty
                edge_weight = max(duration * penalty_factor, 1)  # Ensure weight is positive
                G.add_edge(i, j, weight=edge_weight)
                edge_count += 1  # Increment the edge counter
                print(f"Adding edge between {venues.iloc[i]['venue_name']} and {venues.iloc[j]['venue_name']} with duration {duration} (weighted: {edge_weight})")

    # Print the total number of edges created
    print(f"Total edges created: {edge_count}")

    return G, venues  # Return venues DataFrame for plotting



def generate_initial_routes(G, num_routes=100):
    all_nodes = list(G.nodes)
    initial_routes = []

    for _ in range(num_routes):
        route_size = random.randint(5, 10)  # Random size between 5 and 13
        route = random.sample(all_nodes, k=route_size)  # Sample unique nodes for the route
        initial_routes.append(route)

    return initial_routes

def calculate_cost(routes, G):
    total_travel_time = 0
    uncovered_nodes = set(G.nodes)  # Track all uncovered nodes, not just high-traffic nodes
    overlap_penalty = 0

    for route in routes:
        # Calculate travel time for each route
        for i in range(len(route) - 1):
            # Check if the edge exists before accessing its weight
            if G.has_edge(route[i], route[i + 1]):
                total_travel_time += G[route[i]][route[i + 1]]['weight']
            else:
                # If the edge doesn't exist, you can either skip it or add a penalty
                total_travel_time += float('inf')  # Add an infinite penalty for non-existing edges

        # Track covered nodes
        uncovered_nodes -= set(route)

    # Add overlap penalty
    all_visited_nodes = [node for route in routes for node in route]
    overlap_penalty = len(all_visited_nodes) - len(set(all_visited_nodes))

    # Increase penalty for uncovered nodes (including low-traffic nodes)
    cost = total_travel_time + 200 * len(uncovered_nodes) + 50 * overlap_penalty  # Increased penalty for uncovered nodes

    return cost


# Step 4: Genetic Algorithm (GA)
def genetic_algorithm(G, initial_routes, num_generations=100):
    population = initial_routes
    population_size = len(initial_routes)

    for generation in range(num_generations):
        # Calculate fitness for each individual
        fitness = [1 / calculate_cost([route], G) for route in population]

        # Ensure fitness list is not empty to avoid division by zero
        if sum(fitness) == 0:
            continue  # Skip this generation if fitness is zero for all

        # Selection: Select parents based on fitness
        parents = random.choices(population, weights=fitness, k=min(population_size, 2))  # Select at most 2 parents

        # Crossover: Create new routes by combining parents
        offspring = []
        for i in range(0, len(parents), 2):
            if i + 1 < len(parents):
                parent1, parent2 = parents[i], parents[i + 1]
                
                # Check if parents have more than one node
                if len(parent1) > 1 and len(parent2) > 1:
                    crossover_point = random.randint(1, min(len(parent1), len(parent2)) - 1)
                    child = parent1[:crossover_point] + parent2[crossover_point:]
                    offspring.append(child)
                else:
                    # If either parent has 1 node, just add them directly to offspring
                    offspring.append(parent1)
                    offspring.append(parent2)

        # Mutation: Randomly modify some routes
        for route in offspring:
            if random.random() < 0.1:  # Mutation probability
                idx = random.randint(0, len(route) - 1)
                new_node = random.choice(list(G.nodes))
                route[idx] = new_node

        # Update population
        population += offspring
        population = sorted(population, key=lambda r: calculate_cost([r], G))[:population_size]

    # Return the best routes
    return sorted(population, key=lambda r: calculate_cost([r], G))[:5]

def simulated_annealing(G, route, initial_temp=1000, cooling_rate=0.95, num_iterations=100):
    current_route = route
    current_cost = calculate_cost([current_route], G)
    temp = initial_temp

    for i in range(num_iterations):
        # Generate a neighboring route
        new_route = current_route[:]
        
        # Check if the route has at least 2 nodes to swap
        if len(new_route) < 2:
            continue  # Skip iteration if there aren't enough nodes to swap

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

def optimize_routes(G, initial_routes):
    # Step 1: Use Genetic Algorithm for initial optimization
    optimized_routes = genetic_algorithm(G, initial_routes)

    # Ensure all nodes are still covered after optimization
    covered_nodes = set(node for route in optimized_routes for node in route)
    uncovered_nodes = set(G.nodes) - covered_nodes

    # If there are uncovered nodes, add them to routes
    for uncovered in uncovered_nodes:
        # Again, you can choose your strategy here
        optimized_routes[0].append(uncovered)  # Add uncovered nodes to the first route

    return optimized_routes

def plot_routes(G, routes, venues):
    # Extract positions from the graph
    pos = nx.get_node_attributes(G, 'pos')

    # Define a list of colors for different routes
    colors = ['red', 'green', 'blue', 'purple', 'orange', 'cyan', 'magenta', 'yellow', 'pink', 'brown']

    # Draw the nodes of the graph
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color='lightblue')
    nx.draw_networkx_labels(G, pos, font_size=10, font_color='black')

    # Iterate over the routes and draw each one in a different color
    for idx, route in enumerate(routes):
        edges = [(route[i], route[i + 1]) for i in range(len(route) - 1)]
        # Use modulo to cycle through colors if there are more routes than colors
        color = colors[idx % len(colors)]
        nx.draw_networkx_edges(G, pos, edgelist=edges, width=2, alpha=0.7, edge_color=color)

    # Show the plot
    plt.title("Optimized Bus Routes")
    plt.axis('off')  # Hide axes for better visualization
    plt.show()

if __name__ == "__main__":
    G, venues = create_graph()  # Get both graph and venues
    initial_routes = generate_initial_routes(G)
    optimized_routes = optimize_routes(G, initial_routes)

    # Print the optimized routes along with their costs
    for idx, route in enumerate(optimized_routes):
        route_cost = calculate_cost([route], G)  # Calculate the cost of the route
        print(f"Route {idx + 1}: {route} | Cost: {route_cost}")

    # Plot the optimized routes
    plot_routes(G, optimized_routes, venues)  # Pass venues to plotting function

