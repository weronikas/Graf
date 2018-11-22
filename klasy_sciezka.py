#creating Graph
from collections import defaultdict

class Node:
    def __init__(self, id, X, Y, estDist):
        self.ID = id
        self.X = X
        self.Y = Y
        self.estDist = estDist
        self.edges = []

class Edge:
    def __init__(self, node_from, node_to, cost):
        self.n_from = node_from
        self.n_to = node_to
        self.cost = cost

    def __str__(self):
        return self.cost

class Graph:
    def __init__(self):
        self.edge = []
        self.node = []

