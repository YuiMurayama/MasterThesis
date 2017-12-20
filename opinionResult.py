# !/usr/bin/python
# coding: UTF-8
#add networkx

import networkx as nx


import random
import copy

# from coupling import coupling
from matplotlib.pyplot import ylim, title, xlim

from clusteredNet import *
from coupling import coupling
from gameModel import gameStep, countC_of_gameLayer, makePointList
from opinionModel import *
from makeGraph import makeGraph_fromFile, makeGraph_fromFile, printGstate
from matplotlib import pyplot as plt
from publicGoodsGame import publicGoods_game



activistRate = 0.05
nodeNum = 500
timeStep =200
kaisu = 20
tolerance =0

activistKaisu =  5

#--------------層の生成

network_dir = "./networks/"

OLnetwork = network_dir + 'RegularNetwork.csv'
GLnetwork = network_dir + 'BAnetwork2.csv'

BA = network_dir + 'BAnetwork.csv'


result =[]

for x in range(activistKaisu):
    activistRate = 0.01 * x

    #OLの層
    opinionLayer_info = makeGraph_fromFile(nodeNum,BA, 'ON',activistRate)
    opinionLayer = opinionLayer_info[0]
    opinionList = opinionLayer_info[1]

    #OLがclusterの場合

    # opinionLayer_info = makeClusteredInfor('clusteredNet.gpickle')
    # opinionLayer = opinionLayer_info[0]
    # opinionList = opinionLayer_info[1]

    first_numofC = countC_of_opinionLayer(opinionLayer)
    sumResult =[0]*(timeStep+1)

    first_numofC =countC_of_opinionLayer(opinionLayer)
    sumResult[0] = first_numofC

    firstOpinionLayer = opinionLayer.copy()
    firstOpinionList = copy.deepcopy(opinionList)

    for n in range(kaisu):
        numOfCList_opinionLayer = [0] * (timeStep + 1)
        numOfCList_opinionLayer[0] = first_numofC

        opinionLayer = firstOpinionLayer.copy()
        opinionList= copy.deepcopy(firstOpinionList)
        # print countC_of_opinionLayer(opinionLayer)

        for num in range(timeStep):

            #voter game
            opinionLayerset = opinionExchange(opinionLayer,opinionList)
            opinionLayer = opinionLayerset[0]
            opinionList = opinionLayerset[1]

            #majority vote
            # opinionLayerset = majorityGame(opinionLayer,opinionList)
            # opinionLayer = opinionLayerset[0]
            # opinionList = opinionLayerset[1]
            # sumResult[num+1] += countC_of_opinionLayer(opinionLayer)
            # numOfCList_opinionLayer.append(countC_of_opinionLayer(opinionLayer))
            numOfCList_opinionLayer[num+1]=countC_of_opinionLayer(opinionLayer)
            sumResult[num + 1] += countC_of_opinionLayer(opinionLayer)


        # print numOfCList_opinionLayer
    def calc_ave(n):
        return n/kaisu
    aveResult = list(map(calc_ave,sumResult))
    aveResult[0] = first_numofC

    plt.plot(aveResult, label="activistRate"+str(x*0.01))

    result.append(aveResult)
    # print "ave",aveResult


# print result


plt.xlabel("Time Step")
plt.ylabel("Number of Opinion A")
ylim(200,nodeNum*1.03)
xlim(0, timeStep)
plt.legend(loc="lower right")
plt.show()




