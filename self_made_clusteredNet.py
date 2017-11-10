# !/usr/bin/python
# coding: UTF-8


import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
from numpy.random import *




def self_clusteredNet(clusterNum,nodeNum,intraEdgeNum):
    clusterG_list =[]

    numOfnode_inCluster = nodeNum / clusterNum
    #クラスター内の生成
    #BAモデルで意見は交互に0,1
    for i in range(clusterNum):
        G = nx.barabasi_albert_graph(numOfnode_inCluster,10)
        clusterG_list.append(G)
        if i % 2 == 0:
            nx.set_node_attributes(G, 'opinion', 1)

        else:
            nx.set_node_attributes(G, 'opinion', 0)

    #クラスター間のエッジ生成

    for i in range(intraEdgeNum):
        startNodeNum = randint(numOfnode_inCluster)
        endNodeNum = randint(numOfnode_inCluster)
