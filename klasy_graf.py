#creating Graph
class Node:
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.ID = 0
        self.estDist = None
        self.estTime = None
        self.edges = []

    def __repr__(self):
        return "Node(%s, %s, %s)" % (self.ID, self.X, self.Y)

    def __eq__(self, other):
        if isinstance(other, Node):
            return ((self.X == other.X) and (self.Y == other.Y))
        else:
            return False

    def __ne__(self, other):
        return (not self.__eq__(other))

    def __hash__(self):
        return hash(self.__repr__())


    def getX (self):
        return self.X

    def getY (self):
        return self.Y

    def getID (self):
        return self.ID

    def setID (self, id):
        self.ID = id




class Edge:
    def __init__(self, ID, node_from, node_to, length):
        self.ID = ID
        self.n_from = node_from
        self.n_to = node_to
        self.length = length #metry
        self.time = None #minuty

class Graph:
    def __init__(self):
        self.edge = []
        self.node = []

