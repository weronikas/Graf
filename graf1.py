import arcpy
import os
import sys

from klasy_graf import Node, Edge, Graph

#skjz2 = arcpy.env.workspace = "E:\\studia\\geoinformatyka\\sem_5_powt\\PAG\\lab\\projekt\\kujawsko_pomorskie_pow_torunski\\L4_2_BDOT10k__OT_SKJZ_L.shp"
skjz = arcpy.env.workspace = "E:\\studia\\geoinformatyka\\sem_5_powt\\PAG\\lab\\projekt\\kujawsko_pomorskie_m_Torun"

graph1 = Graph()

#wyszukanie wezlow
skjz = "L4_1_BDOT10k__OT_SKJZ_L.shp"
intersectOutput = "junctions.shp"
splitOutput = "edges.shp"
clusterTolerance = 0.1
arcpy.Intersect_analysis(skjz, intersectOutput, "", "", "point")

id_node = 0
id_edge = 0

"""
cursor = arcpy.SearchCursor(intersectOutput)
shapeName = arcpy.Describe (intersectOutput).shapeFieldName
for row in cursor:
    center = row.getValue(shapeName).centroid
    x = center.X
    y = center.Y
    single_node = Node(id_node, x, y)
    points.add(single_node)
    graph1.node.append(single_node)
    id_node += 1
"""
#podzial drog na odcinki od wezla do wezla
arcpy.SplitLineAtPoint_management(skjz, intersectOutput, splitOutput, clusterTolerance)

#zapisanie odcinkow do klasy Edge i wezlow do klasy Node
cursor = arcpy.SearchCursor(splitOutput)
shapeName = arcpy.Describe (splitOutput).shapeFieldName
for row in cursor:
    feat = row.getValue(shapeName)
    xy1 = feat.firstPoint
    xy2 = feat.lastPoint
    startx = xy1.X
    starty = xy1.Y
    endx = xy2.X
    endy = xy2.Y
    cost = feat.length
    start_id = str(startx)[1:6] + str(starty)[1:6]
    end_id = str(endx)[1:6] + str(endy)[1:6]
    start_node = Node(start_id, startx, starty)
    end_node = Node(end_id, endx, endy)
    if start_node not in graph1.node:
        graph1.node[start_id] = start_node
    else:
        start_node = graph1.node[start_id]
    if end_node not in graph1.node:
        graph1.node[end_id] = end_node
    else:
        end_node = graph1.node[end_id]
    single_edge = Edge(id_edge, start_node, end_node, cost)
    id_edge += 1
    graph1.edge.append(single_edge)

"""
#nadanie ID wezlom
for single_node in nodes:
    single_node.setID(id_node)
    graph1.node.append(single_node)
    id_node += 1
"""
arcpy.Delete_management("junctions.shp")
arcpy.Delete_management("edges.shp")


for item in graph1.edge:
    #odczytuje ID punktu poczatkowego i koncowego
    start = item.n_from.getID()
    end = item.n_to.getID()
    #przypisueje wierzcholkowi o ID poczatku krawedzi sasiada z konca krawedzi i odwrotnie
    start_node = graph1.node[start]
    start_node.edges.append(item)
#    graph1.node[start].edges.append(item.n_to)
    graph1.node[end].edges.append(item)



#zapis do pliku
outFile1 = open(os.path.join(sys.path[0], "edgesList.txt"), "w")

for edge in graph1.edge:
    outFile1.write("{0}, {1}, {2}, {3} \n".format(str(edge.ID), str(edge.n_from.getID()), str(edge.n_to.getID()), str(edge.length)))

outFile1.close()

outFile2 = open(os.path.join(sys.path[0], "verticesList.txt"), "w")

for node in graph1.node.values():
    outFile2.write("{0}, {1}, {2} \n".format(str(node.ID), str(node.X), str(node.Y)))

outFile2.close()