# !/usr/bin/python
# coding: UTF-8

from makeEdges import *


import matplotlib.pyplot as plt



makeRegular_edges('regularSample.csv',20)
edgeFile = 'regularSample.csv'


G = nx.Graph()
f_coords = open(edgeFile)
edgeLines = f_coords.readlines()
opinionList = []
strategyList = []

# エッジを貼る
f_edge = open(edgeFile)
edgeLines = f_edge.readlines()
f_edge.close()
for line in edgeLines:
    edgeList = line.split(',')
    G.add_edge(int(edgeList[0])+1, int(edgeList[1])+1)



plt.figure(figsize=(5, 5))
pos = nx.circular_layout(G)
# nx.draw_networkx(G, pos)
nx.draw_networkx_nodes(G, pos,node_size= 500, node_color='w',alpha=1)
nx.draw_networkx_labels(G, pos,label_color = 'k',fontsize=3, font_family="Yu Gothic", font_weight="bold")
nx.draw_networkx_edges(G, pos, alpha=1, edge_color='k')


plt.show()