# !/usr/bin/python
# coding: UTF-8

import networkx as nx
import random

#エッジファイル、どのレイヤーか、activistの割合の指定
def makeGraph_fromFile(nodeNum,edgeFile, layer, activistRate):
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
        G.add_edge(int(edgeList[0]), int(edgeList[1]))

    if layer == 'ON':
        NormalNum = 0
        for node in range(nodeNum):
            rand = random.random()
            # activistなら意見は0.2の確率でしか変えない、意見は1.0

            if activistRate == 0.0:
                activistInter = 1000000
            else:
                activistInter = 1.0/activistRate

            if node % activistInter == 0:
            # if nx.degree(G)[node] >= 60:
                activist = 1
                opinion = 1
            else:
                # activistでないなら意見は変えまくるし意見は0か1をランダムに選ぶ
                activist = 0
                #どのノードが0なんかを固定
                if NormalNum % 2 == 0:
                    opinion = 0
                else:
                    opinion = 1
                NormalNum = NormalNum +1
                # opinion = random.randint(0, 1)
            G.add_node(node,opinion=opinion, activist=activist)
            opinionList.append(opinion)



        # gameModelなら座標と0か1の戦略をもたせる
    else:
        for node in range(nodeNum):
            tolerance = 0
            biase = random.random()
            # biase = 0.5

            if node % 2 == 0:
                strategy = 0

            else:
                strategy = 1
            # strategy = random.randint(0, 1)
            G.add_node(node,point=0,strategy=strategy,biase = biase,tolerance = tolerance)  # 0がcooperation,1がDefection
            strategyList.append(strategy)
    return (G, opinionList, strategyList)


def printGstate(opinionLayer):
    Gstate_opinion =[]
    Gstate_strategy=[]
    for nodeNum in range(nx.number_of_nodes(opinionLayer)):
        Gstate_opinion.append(opinionLayer.node[nodeNum]['opinion'])
    print "Oは",Gstate_opinion
    # print "Gは",Gstate_strategy
