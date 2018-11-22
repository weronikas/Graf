
from  klasy_sciezka import Node, Graph, Edge
import sys
import os
import math
import heapq
from Priority_queue import Priority_queue

graph1 = Graph()



x_coor, y_coor, est_dist = 0, 0, 0
buffer = []
num_lines = 0
with open(os.path.join(sys.path[0],"graf40.txt"),'r') as inFile:
    for line in inFile:
        costs = [int(x) for x in line.split()]
        buffer.append(costs)
        num_lines += 1
num = 0
#wczytanie krawedzi i wezlow
for list in buffer:
    for point in list:
        single_node = Node(num, x_coor, y_coor, est_dist)
        num += 1
        graph1.node.append(single_node)
        #krawedzie poziome
        if ((x_coor > 0) and (x_coor < (len(costs)))):
            edge_cost = (buffer[y_coor][x_coor - 1] + buffer[y_coor][x_coor]) / 2
            n_from = graph1.node[- 2]
            n_to =  graph1.node[- 1]
            single_edge = Edge(n_from, n_to, edge_cost)
            graph1.edge.append(single_edge)
            n_from.edges.append(single_edge)
            n_to.edges.append(single_edge)
        # krawedzie pionowe
        if (y_coor > 0) and (y_coor < (num_lines)):
            edge_cost = (buffer[y_coor - 1][x_coor] + buffer[y_coor][x_coor]) / 2
            n_from, n_to = graph1.node[- 1 - len(costs)], graph1.node[ - 1]
            single_edge = Edge(n_from, n_to, edge_cost)
            graph1.edge.append(single_edge)
            n_from.edges.append(single_edge)
            n_to.edges.append(single_edge)
        x_coor += 1
    x_coor = 0
    y_coor += 1

end = graph1.node[num - 1]
start = graph1.node[0]


#heurestyka - odleglosc
for node in graph1.node:
    node.estDist = math.sqrt((end.X - node.X) * (end.X - node.X) + (end.Y - node.Y) * (end.Y - node.Y))

#A*
def Astar(s, e):
    visits = 0
    visited = 0
    S = []
    Q = []
    heapq.heapify(Q)
    p = {}
    g = {}
    f = {}
    g[s] = 0
    p[s] = None
    u = s
    Q.append(u)
    while len(Q) != 0:
#        print(str(u.X) + ' ' + str(u.Y) + ' ' + str(g[u]))
        S.append(u)
        Q.remove(u)
        for edge in u.edges:
            if edge.n_from == u:
                v = edge.n_to
            else:
                v = edge.n_from
            if v not in S:
#                print('Sasiad' + ' ' + str(v.X) + ' ' + str(v.Y))
                visits += 1
                if v not in Q:
                    visited += 1
                    Q.append(v)
                if v in g:
                    if g[v] > g[u] + edge.cost:
                        g[v] = g[u] + edge.cost
                        f[v] = g[v] + v.estDist
                        p[v] = u
                else:
                    g[v] = g[u] + edge.cost
                    f[v] = g[v] + v.estDist
                    p[v] = u
        u = Q[0]
        for node in Q:
            if f[u] > f[node]:
                u = node
        if u == e:
            S.append(u)
            print("Koszt najkrotszej sciezki: " + str(g[u]))
            print("Liczba odwiedzonych wierzcholkow: " + str(visited))
            print("Liczba odwiedzin wierzcholkow: " + str(visits))
            break


def Astar2(G, s, e):
    visits = 0
    visited = 0
    S = {}
    Q = Priority_queue()
    p = {}
    g = {}
    g[s.ID] = 0
    p[s.ID] = None
    Q.insert((0, s.ID), None)
    u = s
    while not Q.isempty():
#        print(str(u.X) + ' ' + str(u.Y) + ' ' + str(g[u]))
        u_id = Q.getmin()[1]
        S[u_id] = True

        # do zmiany
        for node in G.node:
            if node.ID == u_id:
                u = node
        if u == e:
            print("Koszt najkrotszej sciezki: " + str(g[u.ID]))
            print("Liczba odwiedzonych wierzcholkow: " + str(visited))
            print("Liczba odwiedzin wierzcholkow: " + str(visits))
            break
        for edge in u.edges:
            if edge.n_from == u:
                v = edge.n_to
            else:
                v = edge.n_from
            if v.ID not in S:
#                print('Sasiad' + ' ' + str(v.X) + ' ' + str(v.Y))
                visits += 1
                if v.ID not in Q.dic:
                    visited += 1
                    #p[v.ID] = u.ID
                    g[v.ID] = g[u.ID] + edge.cost
                    v_f = g[v.ID] + v.estDist
                    Q.insert((v_f, v.ID), u.ID)

#Dijkstra
def Dijkstra(G, s, e):
    d = {} #najkrotsza sciezka
    p = {} #poprzednik
    d[s] = 0
    p[s] = None
    Q = []
    S = []
    visits = 0
    visited = 0
    u = s
    Q.append(u)
    while len(Q) != 0:
#        print(str(u.X) + ' ' + str(u.Y) + ' ' + str(d[u]))
        Q.remove(u)
        S.append(u)
        for edge in u.edges:
            if edge.n_from == u:
                v = edge.n_to
            else:
                v = edge.n_from
            if v not in S:
#                print('Sasiad' + ' '+ str(v.X) + ' ' + str(v.Y))
                visits += 1
                if v not in Q:
                    visited += 1
                    Q.append(v)
                if v in d:
                    if d[v] > d[u] + edge.cost:
                        d[v] = d[u] + edge.cost
                        p[v] = u
                else:
                    d[v] = d[u] + edge.cost
                    p[v] = u
        u = Q[0]
        for node in Q:
            if d[u] > d[node]:
                u = node
        if u == e:
            S.append(u)
            print("Koszt najkrotszej sciezki: " + str(d[e]))
            print("Liczba odwiedzonych wierzcholkow: " + str(visited))
            print("Liczba odwiedzin wierzcholkow: " + str(visits))
            break

def Dijkstra2(G, s, e):
    d = {}
    Q = Priority_queue()
    S = {}
    visits = 0
    visited = 0
    u = s
    d[u.ID] = 0
    Q.insert((0, u.ID), None)
    while not Q.isempty():
#        print(str(u.X) + ' ' + str(u.Y) + ' ' + str(d[u.ID]))
        u_id = Q.getmin()[1]
        S[u_id] = True

        # do zmiany
        for node in G.node:
            if node.ID == u_id:
                u = node
        if u == e:
            print("Koszt najkrotszej sciezki: " + str(d[u.ID]))
            print("Liczba odwiedzonych wierzcholkow: " + str(visited))
            print("Liczba odwiedzin wierzcholkow: " + str(visits))
            break

        for edge in u.edges:
            if edge.n_from == u:
                v = edge.n_to
            else:
                v = edge.n_from
            if v.ID not in S:
#                print('Sasiad' + ' '+ str(v.X) + ' ' + str(v.Y))
                visits += 1
                if v.ID not in Q.dic:
                    visited += 1
                    d[v.ID] = d[u.ID] + edge.cost
                    Q.insert((d[v.ID], v.ID), u.ID)


Dijkstra2(graph1, start, end)
Astar2(graph1, start, end)