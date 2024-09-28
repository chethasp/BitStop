class Node:
    def __init__(self, address, weight=1):
        """
        Initializes a new node with an address and a busyness weight.
        
        Parameters:
        - address (str): Unique identifier for the node (e.g., address or name).
        - weight (int or float): Busyness or importance of the node. Default is 1.
        """
        self.address = address
        self.weight = weight
        self.connections = {}  # Dictionary to hold connections {node: travel_time}
        
    def add_connection(self, node, weight):
        """
        Adds a connection from this node to another node.
        
        Parameters:
        - node (Node): The node to which this node is connected.
        - weight (int or float): Travel time or weight of the edge connecting the nodes.
        """
        self.connections[node] = weight

    def __str__(self):
        """
        Returns a string representation of the node and its connections.
        """
        connections_str = ', '.join([f"{neighbor.address} ({weight})" for neighbor, weight in self.connections.items()])
        return f"Node({self.address}, Weight={self.weight}, Connections=[{connections_str}])"

# Example usage
# Creating nodes
node_a = Node("A", weight=5)
node_b = Node("B", weight=2)
node_c = Node("C", weight=8)

# Adding connections
node_a.add_connection(node_b, 3)
node_a.add_connection(node_c, 5)
node_b.add_connection(node_c, 1)

# Display the nodes and their connections
print(node_a)
print(node_b)
print(node_c)

#Node(A, Weight=5, Connections=[B (3), C (5)])
#Node(B, Weight=2, Connections=[C (1)])
#Node(C, Weight=8, Connections=[])
