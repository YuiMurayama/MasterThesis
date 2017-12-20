# !/usr/bin/python
# coding: UTF-8
#add networkx

import networkx as nx


import random

# from coupling import coupling
from matplotlib.pyplot import ylim, title, xlim
from clusteredNet import *
from coupling import coupling
from gameModel import gameStep, countC_of_gameLayer, makePointList
from opinionModel import *
from makeGraph import makeGraph_fromFile, makeGraph_fromFile, printGstate
from matplotlib import pyplot as plt
from publicGoodsGame import publicGoods_game


activistRate = 0.0
nodeNum = 500
timeStep =200
kaisu =10
opinionLayerStrength = 0.5
tolerance =0

#--------------層の生成

network_dir = "./networks/"

OLnetwork = network_dir + 'RegularNetwork.csv'
GLnetwork = network_dir + 'BAnetwork2.csv'

BA = network_dir + 'BAnetwork.csv'


#GLの層
gameLayer_info = makeGraph_fromFile(nodeNum,BA, 'GL',activistRate)
gameLayer = gameLayer_info[0]
strategyList = gameLayer_info[2]

#---------------------------

# #各層の最初のCの数を数えてリストにいれる
numOfCList_gameLayer =[]
numOfCList_opinionLayer=[]

first_numofC=countC_of_gameLayer(gameLayer)
numOfCList_gameLayer.append(first_numofC)

#-------------------------

sumResult =[0]*(timeStep+1)
sumResult[0] = countC_of_gameLayer(gameLayer)

firstGameLayer = gameLayer.copy()
print countC_of_gameLayer(firstGameLayer)


for n in range(kaisu):
    numOfCList_gameLayer = [0] * (timeStep + 1)
    numOfCList_gameLayer[0] = first_numofC

    gameLayer = firstGameLayer.copy()
    # たくろうにあとで
    # print countC_of_gameLayer(firstGameLayer)


    for num in range(timeStep):
        rand = random.random()
        #こちらはGameLayer
        #PGGの場合
        # gameLayer = publicGoods_game(gameLayer,1.1,1)
        #囚人のジレンマの場合
        gameLayer = gameStep(gameLayer, -0.5, 1.5,tolerance)
        numOfCList_gameLayer[num+1] =countC_of_gameLayer(gameLayer)
        sumResult[num+1] += countC_of_gameLayer(gameLayer)


    # print 'game', numOfCList_gameLayer
# print 'opinion',numOfCList_opinionLayer


def calc_ave(n):
    return n/kaisu

aveResult = list(map(calc_ave,sumResult))
aveResult[0] = first_numofC

print aveResult


#
plt.plot(aveResult,label="GameLayer")
plt.xlabel("Time Step")
plt.ylabel("Number of Cooperators")

# ylim(200,nodeNum*1.03)
ylim(-5,nodeNum*0.55)
xlim(0, timeStep)
plt.legend(loc="lower right")

plt.show()