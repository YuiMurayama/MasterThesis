# !/usr/bin/python
# coding: UTF-8
#add networkx

import networkx as nx
import random
import numpy as np

# from coupling import coupling
from matplotlib.pyplot import ylim, title, xlim
from coupling import coupling
from gameModel import gameStep, countC_of_gameLayer, makePointList
from opinionModel import opinionExchange, countC_of_opinionLayer
from makeGraph import makeGraph_fromFile, makeGraph_fromFile, printGstate
from matplotlib import pyplot as plt

result = {}

for n in range(10000,10001):
    numOfCList_opinionLayer =[]
    result[n] = numOfCList_opinionLayer
    activistRate = n
    nodeNum = 500
    kaisu = 600

    #--------------層の生成

    OLnetwork = 'BAnetwork2.csv'
    opinionLayer_info = makeGraph_fromFile(nodeNum,OLnetwork, 'ON',activistRate)
    opinionLayer = opinionLayer_info[0]
    opinionList = opinionLayer_info[1]

    #---------------------------

    originC_opinionLayer =countC_of_opinionLayer(opinionLayer)
    numOfCList_opinionLayer.append(originC_opinionLayer)
    #-------------------------


    for num in range(kaisu):
        rand = random.random()
        opinionLayerset = opinionExchange(opinionLayer,opinionList)
        opinionLayer = opinionLayerset[0]
        opinionList = opinionLayerset[1]
        numOfCList_opinionLayer.append(countC_of_opinionLayer(opinionLayer))


    plt.plot(numOfCList_opinionLayer,label='activistRate ='+str(1.0/n))
    print 'opinion',numOfCList_opinionLayer


# print result


# plt.plot(a,label= 'high degree')

plt.xlabel("Time Step")
plt.ylabel("Number of Cooperators")

ylim(0,nodeNum*1.03)
plt.legend(loc="lower right")
plt.show()

