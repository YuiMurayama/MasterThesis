# !/usr/bin/python
# coding: UTF-8
#add networkx

from matplotlib import pyplot as plt
import networkx as nx

G = nx.Graph()
f_coords = open('test.csv')
edgeLines = f_coords.readlines()

# エッジを貼る
f_edge = open('test.csv')
edgeLines = f_edge.readlines()
f_edge.close()
for line in edgeLines:
    edgeList = line.split(',')
    G.add_edge(int(edgeList[0]), int(edgeList[1]))


pos = nx.circular_layout(G)
nx.draw_networkx_nodes(G, pos, node_size=500, node_color="w")
nx.draw_networkx_edges(G, pos, width=0.6)
# nx.draw_networkx_edge_labels(G, pos,edge_labels)
nx.draw_networkx_labels(G, pos ,font_size=10, font_color="k")


plt.show()