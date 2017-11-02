# !/usr/bin/python
# coding: UTF-8
#意見交換のメソッド
import networkx as nx
import random
import time
from matplotlib import pyplot as plt
#意見を数えるメソッド

def countC_of_opinionLayer(G):
    numOf0 = 0
    numOf1 = 0
    for nodeNum in range(nx.number_of_nodes(G)):
        if G.node[nodeNum]['opinion'] < 0.2:
            numOf0 += 1
        if G.node[nodeNum]['opinion'] > 0.8:
            numOf1 += 1
    return numOf1


def printGstate(opinionLayer):
    Gstate_opinion =[]
    Gstate_strategy=[]
    for nodeNum in range(nx.number_of_nodes(opinionLayer)):
        Gstate_opinion.append(opinionLayer.node[nodeNum]['opinion'])
    print "Oは",Gstate_opinion
    # print "Gは",Gstate_strategy



#意見交換のメソッド
#全てのオピニオンを近隣と交換させる徒
def opinionExchange(G,opinionList):
    newOpinionList=[]
    # print 'opinionlist',opinionList
    for nodeNum in range(nx.number_of_nodes(G)):
        node = G.node[nodeNum]  # ランダムにノードを選択

        if node['activist'] != 1:
            copyNode_list = G.neighbors(nodeNum)  # コピー相手の候補リストを作る
            if copyNode_list != []:
                copyNodeNum = random.choice(copyNode_list)  # 候補リストの中からランダムに選択
                copyNode = G.node[copyNodeNum]
                # print nodeNum, 'と', copyNodeNum
                if copyNode['activist'] == 1:
                    node['opinion'] = opinionList[copyNodeNum]
                    # print 'こうかん'
                else:
                    rand = random.random()
                    if rand< 0.5:
                        node['opinion'] = opinionList[copyNodeNum]
                        # print 'こうかん'
        newOpinionList.append(node['opinion'])
    opinionList = newOpinionList

    return G,opinionList