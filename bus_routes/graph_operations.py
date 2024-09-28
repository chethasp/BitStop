import csv
from calculate_distances import get_distance


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
