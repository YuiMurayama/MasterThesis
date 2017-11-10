# !/usr/bin/python
# coding: UTF-8
import csv
import random
import networkx as nx
import numpy as np
from matplotlib import f
from urllib3.filepost import writer
import matplotlib.pylab as plt

from clusteredNet import MLW_graph

nodeNum = 500


#BAネットワークの生成
def makeBA_edges(filename,nodeNum):
    f = open(filename, 'w')
    writer = csv.writer(f, lineterminator='\n')
    G = nx.barabasi_albert_graph(nodeNum,10)
    writer.writerows(G.edges())
    f.close()
    return G


#一次元レギュラーネットワーク
def makeRegular_edges(filename,nodeNum):
    f = open(filename,'w')
    writer = csv.writer(f, lineterminator='\n')

    for node in range(nodeNum-1):
        edge =[node,node+1]
        writer.writerow(edge)
    finalEdge = [nodeNum-1,0]
    writer.writerow(finalEdge)
    f.close()


def makerandomRegular_deges(filename,nodeNum):
    f = open(filename, 'w')
    writer = csv.writer(f, lineterminator='\n')
    list = range(nodeNum)
    random.shuffle(list)
    for node in range(nodeNum - 1):
        edge = [list[node],list[node + 1]]
        writer.writerow(edge)
    finalEdge = [list[nodeNum-1],0]
    writer.writerow(finalEdge)
    f.close()




def makeClustered_edges(filename,nodeNum):
    f = open(filename, 'w')
    writer = csv.writer(f, lineterminator='\n')
    G  = MLW_graph(N=nodeNum).get_G()
    writer.writerows(G.edges())
    f.close()
    return G


makeClustered_edges('clustered_test.csv',30)

makeRegular_edges('test.csv',10)



# makeRegular_edges('RegularNetwork.csv',nodeNum)
# G =makeBA_edges('BAnetwork.csv',nodeNum)

bins = 30
# plt.hist(G.degree().values(), bins=bins)
#
# degree = np.array(G.degree().values())
# print degree
# print len(degree)
# print len(degree[degree>=60])

# plt.xlabel("Edge Number")
# plt.ylabel("Node Number")
#
# plt.show()



# print np.average(nx.degree(G).values())


# makeBA_edges('BAnetwork2.csv',nodeNum)

# randomRegular_deges('randomRegularNetwork.csv',nodeNum)



makeRegular_edges('test.csv',10)


# G   = makeRegular_edges('test.csv',10)
#
#
# pos = nx.spring_layout(G)
#
# nx.draw_networkx_nodes(G, pos, node_size=20, node_color="w")
# # nx.draw_networkx_edges(G, pos, width=0.3)
# # nx.draw_networkx_edge_labels(G, pos,edge_labels)
# # nx.draw_networkx_labels(G, pos ,font_size=6, font_color="r")
#
# plt.xticks([])
# plt.yticks([])
# plt.show()
#


