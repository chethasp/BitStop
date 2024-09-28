import csv

class Node:
    def __init__(self, name, address, latitude, longitude, weight=0):
        self.name = name
        self.address = address
        self.weight = weight
        self.latitude = latitude
        self.longitude = longitude
    
    def __str__(self):
        return "Node info: {n}, {a}, {w}".format(n=self.name, a=self.address, w=self.weight)
    
class Graph:
    def __init__(self):
        self.nodes = {} # key: name, value: node object
        self.edges = {} # adjacency list for edges

    def add_node(self, name, address, weight, latitude, longitude):
        self.nodes[name] = Node(name, address,latitude, longitude, weight)
        self.edges[name] = {}

    def add_edge(self, name1, name2, weight=1):
        self.edges[name1][name2] = weight
        self.edges[name2][name1] = weight

    def get_node(self, name):
        return self.nodes[name]
    
    def get_edge(self, name1, name2):
        return self.edges[name1][name2]

graph = Graph()

with open('static/foot_traffic_sites.csv', mode ='r')as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
        if (lines[0] != 'venue_name'):
            graph.add_node(lines[0], lines[1], 1, lines[2], lines[3])
            for node in graph.nodes:
                graph.add_edge(lines[0], graph.nodes[node].name, 1)

print(graph.nodes.keys())
print(graph.edges.values())