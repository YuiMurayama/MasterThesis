# !/usr/bin/python
# coding: UTF-8
#add networkx

import networkx as nx
import random

# from coupling import coupling
from matplotlib.pyplot import ylim, title, xlim
from coupling import coupling
from gameModel import gameStep, countC_of_gameLayer, makePointList
from opinionModel import opinionExchange, countC_of_opinionLayer
from makeGraph import makeGraph_fromFile, makeGraph_fromFile, printGstate
from matplotlib import pyplot as plt

activistRate = 100000
nodeNum = 500
kaisu = 2000
couplingStrength = 0.0


#--------------層の生成


OLnetwork = 'RegularNetwork.csv'
GLnetwork = 'BAnetwork2.csv'


BA = 'BAnetwork.csv'

#GLの層
gameLayer_info = makeGraph_fromFile(nodeNum,GLnetwork, 'GL',activistRate)
gameLayer = gameLayer_info[0]
strategyList = gameLayer_info[2]


#OLの層
opinionLayer_info = makeGraph_fromFile(nodeNum,OLnetwork, 'ON',activistRate)
opinionLayer = opinionLayer_info[0]
opinionList = opinionLayer_info[1]

#---------------------------

# #各層のCの数を数えるリスト
numOfCList_gameLayer =[]
numOfCList_opinionLayer=[]

# #初期のCooperatorの数をリストに加える

originC_opinionLayer =countC_of_opinionLayer(opinionLayer)
originC_gameLayer =countC_of_gameLayer(gameLayer)


numOfCList_opinionLayer.append(originC_opinionLayer)
numOfCList_gameLayer.append(originC_gameLayer)


#-------------------------


for num in range(kaisu):
    rand = random.random()
    # printGstate(opinionLayer, gameLayer)
    # print countC_of_opinionLayer(opinionLayer)
    if rand < couplingStrength:
        coupling_info =coupling(gameLayer, opinionLayer, opinionList)
        gameLayer = coupling_info[0]
        opinionLayer = coupling_info[1]
        opinionList = coupling_info[2]

    else:
        gameLayer = gameStep(gameLayer,-0.5,1.5)
        opinionLayerset = opinionExchange(opinionLayer,opinionList)
        opinionLayer = opinionLayerset[0]
        opinionList = opinionLayerset[1]

    numOfCList_gameLayer.append(countC_of_gameLayer(gameLayer))
    numOfCList_opinionLayer.append(countC_of_opinionLayer(opinionLayer))


print 'game', numOfCList_gameLayer
print 'opinion',numOfCList_opinionLayer


# plt.plot(numOfCList_gameLayer,label="GameLayer")
plt.plot(numOfCList_opinionLayer,label="OpinionLayer")
plt.xlabel("Time Step")
plt.ylabel("Number of Cooperators")

ylim(0,nodeNum*1.03)
xlim(0,kaisu)
plt.legend(loc="lower right")
plt.show()

