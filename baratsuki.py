# !/usr/bin/python
# coding: UTF-8
#add networkx

import networkx as nx


import random

# from coupling import coupling
from matplotlib.pyplot import ylim, title, xlim

from clusteredNet import *
from coupling import coupling
from gameModel import *
from opinionModel import *
from makeGraph import makeGraph_fromFile, makeGraph_fromFile, printGstate
from matplotlib import pyplot as plt
from publicGoodsGame import publicGoods_game


activistRate = 0.0
nodeNum = 500
kaisu = 800
# couplingStrength = 0.1
opinionLayerStrength = 0.5


#--------------層の生成

OLnetwork = 'RegularNetwork.csv'
GLnetwork = 'BAnetwork2.csv'

BA = 'BAnetwork.csv'


#GLの層
gameLayer_info = makeGraph_fromFile(nodeNum,GLnetwork, 'GL',activistRate)
gameLayer = gameLayer_info[0]
strategyList = gameLayer_info[2]


#OLの層
opinionLayer_info = makeGraph_fromFile(nodeNum,'BAnetwork.csv', 'ON',activistRate)
opinionLayer = opinionLayer_info[0]
opinionList = opinionLayer_info[1]


#---各層の初期値をいれる--

numOfCList_gameLayer =[]
numOfCList_opinionLayer=[]

numOfCList_opinionLayer.append(countC_of_opinionLayer(opinionLayer))
numOfCList_gameLayer.append(countC_of_gameLayer(gameLayer))
#--------------------------

g= -0.5
s = 1.5

#それぞれのノードの層間の強さにばらつきを持たせる
for nodeNum in range(nx.number_of_nodes(gameLayer)):
    gameLayer.node[nodeNum]['couplingStrength'] = random.random()*0.4
    # gameLayer.node[nodeNum]['couplingStrength'] = 0


#ステップ開始

for num in range(kaisu):
    rand = random.random()
    gameInfo = game(gameLayer,g,s)
    gameLayer = gameInfo[0]
    strategyList = gameInfo[1]
    newOpinionList = []

    for nodeNum in range(nx.number_of_nodes(gameLayer)):
        #GameModelを動かす
        gameNode = gameLayer.node[nodeNum]  # ランダムにノードを選択
        copyNode_list = gameLayer.neighbors(nodeNum)  # コピー相手の候補リストを作る
        if copyNode_list != []:
            copyNodeNum = random.choice(copyNode_list)  # 候補リストの中からランダムに選択
            copyNode = gameLayer.node[copyNodeNum]  # コピー相手の決定
            p = (1.0 - math.tanh(gameNode['point'] - copyNode['point'])) * 0.1  # どのくらいの確率で戦略をコピーするのか
            x = random.random()
            if x < p:
                gameNode['strategy'] = strategyList[copyNodeNum]  # strategyListから戦略をコピー
        # node['point'] = 0

        #OpinionModelを動かす
        opinionNode = opinionLayer.node[nodeNum]
        if opinionNode['activist'] != 1:
            copyNode_list = opinionLayer.neighbors(nodeNum)  # コピー相手の候補リストを作る
            if copyNode_list != []:
                copyNodeNum = random.choice(copyNode_list)  # 候補リストの中からランダムに選択
                copyNode = opinionLayer.node[copyNodeNum]
                if copyNode['activist'] == 1:
                    opinionNode['opinion'] = opinionList[copyNodeNum]

                else:
                    if opinionList[copyNodeNum] == 1:
                        opinionNode['opinion'] = opinionList[copyNodeNum]
                    else:
                        rand = random.random()
                        if rand< 0.85:   #biaseをかける
                            opinionNode['opinion'] = opinionList[copyNodeNum]

        #Couplingするかどうか
        rand = random.random()
        if rand < gameNode['couplingStrength']:
            if nodeNum %2 == 0:
                gameLayer.node[nodeNum]['strategy'] = opinionLayer.node[nodeNum]['opinion']
            else:
                opinionLayer.node[nodeNum]['opinion'] = gameLayer.node[nodeNum]['strategy']

        newOpinionList.append(opinionNode['opinion'])
    opinionList = newOpinionList

    numOfCList_gameLayer.append(countC_of_gameLayer(gameLayer))
    numOfCList_opinionLayer.append(countC_of_opinionLayer(opinionLayer))


plt.plot(numOfCList_gameLayer,label="GameLayer")
plt.plot(numOfCList_opinionLayer,label="OpinionLayer")
plt.xlabel("Time Step")
plt.ylabel("Number of Cooperators")

ylim(0,nodeNum*1.03)
xlim(0,kaisu)
plt.legend(loc="lower right")
plt.show()

