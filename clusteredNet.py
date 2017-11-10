# !/usr/bin/python
# coding: UTF-8

from __future__ import division

from itertools import count

import numpy as np
import networkx as nx
import pylab
from matplotlib import pyplot as plt


from opinionModel import *


class MLW_graph(object):
    def __init__(self, local_graph=nx.complete_graph(8), p1=0.0, p2=0.28, p3=0.39, p4=0.43, e1=2, e2=2, e3=2, e4=2,
                 N_lw=2, N=100,state = 'n'):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.e1 = e1
        self.e2 = e2
        self.e3 = e3
        self.e4 = e4
        self.state = state
        self.N_lw = N_lw
        self.local_graph = local_graph

        # 初期グラフの作成
        G_lst = [local_graph.copy() for i in range(N_lw)]
        self.G = self.compose(self.relabel(self.set_cluster_label(G_lst)))

        while (len(self.G) < N):
            r = np.random.rand()
            if 0 <= r < self.p1:
                print("a")
                N_lw += 1
                self.add_local_graph()

            elif self.p1 <= r < self.p2:
                # print("b")
                self.add_new_node_to_lw(1)

            elif self.p2 <= r < self.p3:
                # print("c")
                self.add_edge_within_lw(1)

            elif self.p3 <= r < self.p4:
                # print("d")
                self.delete_edge_within_lw(1)

            # else:
            #     # print("e")
            #     self.add_edge_among_lw(1)

            elif self.p4 <= r < 0.7:
                self.add_edge_among_lw(1)

    def get_G(self):
        return self.G

    def add_local_graph(self):
        """action a
        """
        g = self.local_graph.copy()
        nx.set_node_attributes(g, "cluster", self.N_lw)
        nx.set_node_attributes(g, "opinion", self.N_lw)
        nx.set_node_attributes(g, "activist", 0)

        # 分極してないばあい
        if self.state == 'n':
            for nodeNum in range(nx.number_of_nodes(G)):
                G.node[nodeNum]['opinion'] = randint(2)


        self.G = self.compose(self.G, g)

    def add_new_node_to_lw(self, alpha):
        """action b
        """
        obj_cluster = np.random.randint(self.N_lw)
        # 対象のノードリストを取得
        obj_nodes = [n for n, d in self.G.nodes(data=True) if d["cluster"] == obj_cluster]
        # 対象ノードの次数
        obj_degree = np.array([self.G.degree(n) + alpha for n in obj_nodes])
        obj_prob = obj_degree / np.sum(obj_degree)

        # 新規ノードの追加
        node_id = len(self.G)
        self.G.add_node(node_id, cluster=obj_cluster, opinion= randint(2),activist = 0)
        # ここ


        # 新規エッジの追加
        add_edge = np.random.choice(obj_nodes, self.e1, p=obj_prob, replace=False)
        for n in add_edge:
            # print("add edge :", node_id, n)
            self.G.add_edge(node_id, n)

    def add_edge_within_lw(self, alpha):
        """action c
        """
        obj_cluster = np.random.randint(self.N_lw)
        # 対象のノードリストを取得
        obj_nodes = [n for n, d in self.G.nodes(data=True) if d["cluster"] == obj_cluster]

        for i in range(self.e2):
            node_from = np.random.choice(obj_nodes)
            obj = self.unlinked_nodes(node_from, obj_nodes)
            if len(obj) == 0:
                continue
            # 対象ノードの次数
            obj_degree = np.array([self.G.degree(n) + alpha for n in obj])
            obj_prob = obj_degree / np.sum(obj_degree)
            node_to = np.random.choice(obj, p=obj_prob)

            # print("add edge :", node_from, node_to)
            self.G.add_edge(node_from, node_to)

    def unlinked_nodes(self, node_id, obj_nodes):
        ret = [p for p in obj_nodes if (not self.G.has_edge(node_id, p)) or (not p == node_id)]
        return ret

    def delete_edge_within_lw(self, alpha):
        """action d
        """
        obj_cluster = np.random.randint(self.N_lw)
        # 対象のノードリストを取得
        obj_nodes = [n for n, d in self.G.nodes(data=True) if d["cluster"] == obj_cluster]
        for i in range(self.e3):
            node_from = np.random.choice(obj_nodes)
            # 対象ノードの次数
            obj_degree = np.array([self.G.degree(n) + alpha for n in obj_nodes])
            obj_prob = (1 - (obj_degree / np.sum(obj_degree))) / (len(obj_nodes) - 1)
            node_to = np.random.choice(obj_nodes, p=obj_prob)

            while (not self.G.has_edge(node_from, node_to)):
                node_to = np.random.choice(obj_nodes, p=obj_prob)

            # print("delete edge :", node_from, node_to)
            self.G.remove_edge(node_from, node_to)

    def add_edge_among_lw(self, alpha):
        """action e
        """
        obj_clusters = np.random.choice(range(self.N_lw), 2, replace=False)
        obj_nodes0 = [n for n, d in self.G.nodes(data=True) if d["cluster"] == obj_clusters[0]]
        obj_nodes1 = [n for n, d in self.G.nodes(data=True) if d["cluster"] == obj_clusters[1]]

        for i in range(self.e4):
            obj_degree0 = np.array([self.G.degree(n) + alpha for n in obj_nodes0])
            obj_prob0 = obj_degree0 / np.sum(obj_degree0)
            obj_degree1 = np.array([self.G.degree(n) + alpha for n in obj_nodes1])
            obj_prob1 = obj_degree1 / np.sum(obj_degree1)

            node0 = np.random.choice(obj_nodes0, p=obj_prob0)
            node1 = np.random.choice(obj_nodes1, p=obj_prob1)

            while (self.G.has_edge(node0, node1)):
                node0 = np.random.choice(obj_nodes0, p=obj_prob0)
                node1 = np.random.choice(obj_nodes1, p=obj_prob1)

            self.G.add_edge(node0, node1)
            # print("add edge: ", node0, node1)

    def set_cluster_label(self, G_lst):
        for i, G in enumerate(G_lst):
            nx.set_node_attributes(G, "cluster", i)
            nx.set_node_attributes(G, "opinion", i)
            nx.set_node_attributes(G, "activist",0)

            # 分極していない場合
            if self.state == 'n':
                for nodeNum in range(nx.number_of_nodes(G)):
                    G.node[nodeNum]['opinion'] = randint(2)

        return G_lst


    def relabel(self, G_lst):
        """ノードのラベルを振り直す
        """
        init_node_num = 0
        for i, G in enumerate(G_lst):
            node_num = len(G)
            map_from = range(node_num)
            map_to = range(init_node_num, init_node_num + node_num)
            mapping = dict(zip(map_from, map_to))
            G = nx.relabel_nodes(G, mapping)
            G_lst[i] = G
            init_node_num += node_num
        return G_lst

    def compose(self, G_lst):
        """グラフを合体
        """
        ret_G = nx.Graph()
        for G in G_lst:
            ret_G = nx.compose(ret_G, G)
        return ret_G


def makeClusterG (allNodeNum,firstNodeNum,state,filename):
    G = MLW_graph(N=allNodeNum,local_graph=nx.complete_graph(firstNodeNum),state = state).get_G()
    nx.write_gpickle(G,filename)


def makeClusterList(G):
    clusterList_a = []
    clusterList_b = []
    for nodeNum in range(nx.number_of_nodes(G)):
        if G.node[nodeNum]['opinion'] == 0:
            clusterList_a.append(nodeNum)
        else:
            clusterList_b.append(nodeNum)
    return clusterList_a, clusterList_b


def printClusteredG(G):
    clusterList = makeClusterList(G)
    clusterList_a = clusterList[0]
    clusterList_b = clusterList[1]
    pos = nx.spring_layout(G)  # グラフ形式を選択。ここではスプリングモデルでやってみる
    nx.draw_networkx_nodes(G, pos, clusterList_a, node_size=20, node_color='b')
    nx.draw_networkx_nodes(G, pos, clusterList_b, node_size=20, node_color='r')
    nx.draw_networkx_edges(G, pos, width=0.1)
    pylab.xticks([])
    pylab.yticks([])
    pylab.show()

def makeClusteredInfor(filename):
    G = nx.read_gpickle(filename)
    opinionList =[]
    for nodeNum in range(nx.number_of_nodes(G)):
        opinionList.append(G.node[nodeNum]['opinion'])
    return G,opinionList

# G = makeClusterG(500,230,'b','clusteredNet.gpickle')
#
#
# opinionLayer_info = makeClusteredInfor('clusteredNet.gpickle')
# opinionLayer = opinionLayer_info[0]
# opinionList = opinionLayer_info[1]
#
#
# printClusteredG(opinionLayer)
#
# for num in range(1):
#     majorityGame(opinionLayer,opinionList)
#
# printClusteredG(opinionLayer)

