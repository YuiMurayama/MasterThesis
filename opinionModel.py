# !/usr/bin/python
# coding: UTF-8
#意見交換のメソッド
import networkx as nx
import random
import time
from matplotlib import pyplot as plt
#意見を数えるメソッド
from numpy.random import randint


def countC_of_opinionLayer(G):
    numOf0 = 0
    numOf1 = 0
    for nodeNum in range(nx.number_of_nodes(G)):

        # print G.node[nodeNum]['opinion']
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
                if copyNode['activist'] == 1:
                    # print 'activist'
                    node['opinion'] = opinionList[copyNodeNum]

                else:
                    rand=random.random()
                    if rand< 0.6:
                        node['opinion'] = opinionList[copyNodeNum]
                    # if opinionList[copyNodeNum] == 0:
                    #     node['opinion'] = opinionList[copyNodeNum]
                    # else:
                    #     rand = random.random()
                    #     if rand< 1.1:   #biaseをかける1以下ならCになりやすくなるよ
                    #         node['opinion'] = opinionList[copyNodeNum]
        # else:
            # print 'activist',node['activist']
                        # print 'こうかん'
        newOpinionList.append(node['opinion'])
    opinionList = newOpinionList
    return G,opinionList






def majorityGame(G,opinionList):
    newOpinionList=[]
    # print 'opinionlist',opinionList
    for nodeNum in range(nx.number_of_nodes(G)):
        node = G.node[nodeNum]  # ランダムにノードを選択
        copyNode_list = G.neighbors(nodeNum)  # コピー相手の候補リストを作る
        if copyNode_list != []:
            numOfC = 0
            numOfD = 0
            for num in range(len(copyNode_list)):
                if G.node[copyNode_list[num]]['opinion'] == 0:
                    numOfC +=1
                else:
                    numOfD +=1
                # print numOfC,numOfD
                if numOfC < numOfD:
                    node['opinion'] = 1
                elif numOfC > numOfD:
                    node['opinion'] = 0
                else:
                    node['opinion'] = randint(2)
        newOpinionList.append(node['opinion'])
    opinionList = newOpinionList
    return G,opinionList
