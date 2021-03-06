import arcpy
import os
import sys
import math
import time


from klasy_graf import Node, Edge, Graph
from Priority_queue import Priority_queue

#skjz2 = arcpy.env.workspace = "E:\\studia\\geoinformatyka\\sem_5_powt\\PAG\\lab\\projekt\\kujawsko_pomorskie_pow_torunski\\L4_2_BDOT10k__OT_SKJZ_L.shp"

arcpy.env.workspace = "E:\\studia\\geoinformatyka\\sem_5_powt\\PAG\\lab\\projekt\\kujawsko_pomorskie_m_Torun"

graph1 = Graph()

skjz = "L4_1_BDOT10k__OT_SKJZ_L.shp"


id_edge = 0



#zapisanie odcinkow do klasy Edge i wezlow do klasy Node
cursor = arcpy.SearchCursor(skjz)
shapeName = arcpy.Describe (skjz).shapeFieldName
for row in cursor:
    feat = row.getValue(shapeName)
    xy1 = feat.firstPoint
    xy2 = feat.lastPoint
    startx = xy1.X
    starty = xy1.Y
    endx = xy2.X
    endy = xy2.Y
    cost_length = feat.length
    mat = row.materialNa
    vel = Edge.vel_tab[mat]
    dir = row.direction
    start_id = str(startx)[:6] + str(starty)[:6]
    end_id = str(endx)[:6] + str(endy)[:6]
    if start_id not in graph1.node.keys():
        start_node = Node(start_id, startx, starty)
        graph1.node[start_id] = start_node
    else:
        start_node = graph1.get_node(start_id)
    if end_id not in graph1.node.keys():
        end_node = Node(end_id, endx, endy)
        graph1.node[end_id] = end_node
    else:
        end_node = graph1.get_node(end_id)
    single_edge = Edge(id_edge, start_node, end_node, cost_length, vel, dir)
    id_edge += 1
    graph1.edge[id_edge] = single_edge

for i, item in graph1.edge.iteritems():
    #odczytuje ID punktu poczatkowego i koncowego
    start = item.n_from.getID()
    end = item.n_to.getID()
    #przypisueje wierzcholkowi z poczatku krawedzi krawedz do sasiada z konca krawedzi i odwrotnie
    if item.get_dir() < 2:
        graph1.node[start].edges.append(item)
    if item.get_dir() % 2 == 0:
        graph1.node[end].edges.append(item)
    #bez kierunkowosci
    #graph1.node[start].edges.append(item)
    #graph1.node[end].edges.append(item)

#wprowadzenie punktu poczatkowego i punktu koncowego
start_in = str(473669572019)
end_in = str(473765572109)
#print('ID punktu startowego:')
#start_in = str(input())
#print('ID punktu koncowego:')
#end_in = str(input())

start = graph1.get_node(start_in)
end = graph1.get_node(end_in)
x_start, y_start, x_end, y_end = start.getX(), start.getY(), end.getX(), end.getY()

#heurestyka - odleglosc
def heur_length(node, end):
    x_end, y_end = end.getX(), end.getY()
    node.set_est_dist(math.sqrt((x_end - node.getX()) * (x_end - node.getX()) + (y_end - node.getY()) * (y_end - node.getY())))

#heurestyka - czas
def heur_time(node, end):
    x_end, y_end = end.getX(), end.getY()
    node.set_est_dist(math.sqrt((x_end - node.getX()) * (x_end - node.getX()) + (y_end - node.getY()) * (y_end - node.getY())) * 60 / 1000 / 70)

#zapis do pliku
outFile1 = open(os.path.join(sys.path[0], "edgesList.txt"), "w")

for edge in graph1.edge.values():
    outFile1.write("{0}, {1}, {2}, {3} \n".format(str(edge.getID()), str(edge.n_from.getID()), str(edge.n_to.getID()), str(edge.cost_length())))

outFile1.close()

outFile2 = open(os.path.join(sys.path[0], "verticesList.txt"), "w")

for node in graph1.node.values():
    outFile2.write("{0}, {1}, {2}, est dist: {3} \n".format(str(node.getID()), str(node.getX()), str(node.getY()), str(node.get_est_dist())))
    for edge in node.edges:
        outFile2.write(" " + str(edge.getID()))
    outFile2.write("\n")

outFile2.close()


#A gwiazdka
def Astar(G, s, e, p, opt):
    visits = 0
    visited = 0
    S = set()
    Q = Priority_queue()
    g = {}
    g[s.getID()] = 0
    p[s.getID()] = None
    Q.insert((0, s.getID()))
    while not Q.isempty():
        u_id = Q.getmin()[1]
        S.add(u_id)
        u = G.get_node(u_id)
        if u.getID() == e.getID():
            print("Koszt najkrotszej sciezki: " + str(g[u.getID()]))
            print("Liczba odwiedzonych wierzcholkow: " + str(visited))
            print("Liczba odwiedzin wierzcholkow: " + str(visits))
            break
        for edge in u.get_edges():
            v = edge.get_end(u)
            if opt == 't':
                heur_time(v, e)
                edge_cost = edge.cost_time()
            elif opt == 'l':
                heur_length(v, e)
                edge_cost = edge.cost_length()
            v_id = v.getID()
            if v_id not in S:
                visits += 1
                if v_id not in Q.dic:
                    visited += 1
                    p[v_id] = u_id
                    g[v_id] = g[u_id] + edge_cost
                    v_f = g[v_id] + v.get_est_dist()
                    Q.insert((v_f, v_id))
                if g[v_id] > g[u_id] + edge_cost:
                    p[v_id] = u_id
                    g[v_id] = g[u_id] + edge_cost
                    v_f = g[v_id] + v.estDist
                    Q.decrease((v_f, v_id))

#Dijkstra
def Dijkstra(G, s, e, p, opt):
    d = {}
    Q = Priority_queue()
    S = set()
    visits = 0
    visited = 0
    d[s.getID()] = 0
    p[s.getID()] = None
    Q.insert((0, s.getID()))
    while not Q.isempty():
        u_id = Q.getmin()[1]
        S.add(u_id)
        u = G.get_node(u_id)
        if u == e:
            print("Koszt najkrotszej sciezki: " + str(d[u.getID()]))
            print("Liczba odwiedzonych wierzcholkow: " + str(visited))
            print("Liczba odwiedzin wierzcholkow: " + str(visits))
            break
        for edge in u.edges:
            v = edge.get_end(u)
            if opt == 't':
                heur_time(v, e)
                edge_cost = edge.cost_time()
            elif opt == 'l':
                heur_length(v, e)
                edge_cost = edge.cost_length()
            v_id = v.getID()
            if v_id not in S:
                visits += 1
                if v_id not in Q.dic:
                    visited += 1
                    p[v_id] = u_id
                    d[v_id] = d[u_id] + edge_cost
                    Q.insert((d[v_id], v_id))
                if d[v_id] > d[u_id] + edge_cost:
                    d[v_id] = d[u_id] + edge_cost
                    Q.decrease((d[v_id], v_id))
                    p[v_id] = u_id

pop = {}

start_time = time.time()
Astar(graph1, start, end, pop, 'l')
end_time = time.time()
print "Czas dzialania algorytmu: " + str(end_time - start_time)



#tworzenie warstwy z wyznaczona trasa
arcpy.Delete_management("navigation.shp")

out_path = arcpy.env.workspace
out_name = "navigation.shp"
geometry_type = "POLYLINE"

feature_class = arcpy.CreateFeatureclass_management(out_path, out_name, geometry_type, skjz, "DISABLED", "DISABLED", skjz)

#array = arcpy.Array()
array2 = arcpy.Array()
with arcpy.da.InsertCursor(feature_class, ["SHAPE@"]) as cursor:
    i = end.getID()
    while i != None:
        my_node = graph1.get_node(i)
        array2.add(arcpy.Point(my_node.getX(), my_node.getY()))
        i = pop[i]
    #array.add(arcpy.Point(x_end, y_end))
    #array.add(arcpy.Point(x_start, y_start))
    #cursor.insertRow([arcpy.Polyline(array)])
    cursor.insertRow([arcpy.Polyline(array2)])
