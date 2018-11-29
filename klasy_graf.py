from collections import defaultdict

#creating Graph
class Node:
    def __init__(self, ID, X, Y):
        self.X = X
        self.Y = Y
        self.ID = ID
        self.estDist = 'rrr'
        self.estTime = None
        self.edges = []

    def get_neighbours (self):
        neighbours = []
        for edge in self.edges:
            item = (edge, edge.get_end(self))
            neighbours.append(item)
        return neighbours


    def getX (self):
        return self.X

    def getY (self):
        return self.Y

    def getID (self):
        return self.ID

    def get_edges(self):
        return self.edges

    def get_est_dist(self):
        return self.estDist

    def set_est_dist (self, dist):
        self.estDist = dist


class Edge:
    def __init__(self, ID, node_from, node_to, length):
        self.ID = ID
        self.n_from = node_from
        self.n_to = node_to
        self.length = length #metry
        self.velocity = None
        self.direction = None

    def get_end (self, vertex):
        if vertex.ID == self.n_from.ID:
           return  self.n_to
        if vertex.ID == self.n_to.ID:
            return self.n_from
        else:
            print "Podany wierzcholek nie jest zadnym z koncow krawedzi"
            print("Vertex: {0}, n_from: {1}, n_to: {2} \n".format(str(vertex.getID()), str(self.n_from.getID()), str(self.n_to.getID())))


    def cost_length (self):
        return self.length

    def cost_time (self):
        time = (self.length * 3600) / (self.velocity * 1000)
        return time

    def getID (self):
        return self.ID


class Graph:
    def __init__(self):
        self.edge = {}
        self.node = {}

    def get_node (self, id):
        return self.node[id]

    def get_edge (self, id):
        return self.edge[id]

    def closest_node (self, x, y):
        pass

