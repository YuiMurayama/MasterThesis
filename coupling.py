# !/usr/bin/python
# coding: UTF-8
#add networkx


import random
import networkx as nx


def coupling(gameLayer,opinionLayer,opinionList):
    newOpinionList = []
    for nodeNum in range(nx.number_of_nodes(opinionLayer) ):
        rand_of_copy = random.random()
        rand_of_whichLayer = random.random()
        # どちらからどちらへコピーするかの確率
        if rand_of_copy < 0.5:
            if rand_of_whichLayer <= 0.5:
                gameLayer.node[nodeNum]['strategy'] = opinionLayer.node[nodeNum]['opinion']
            else:
                if opinionLayer.node[nodeNum]['activist'] != 1:
                    opinionLayer.node[nodeNum]['opinion'] = gameLayer.node[nodeNum]['strategy']

        newOpinionList.append(opinionLayer.node[nodeNum]['opinion'])

    return (gameLayer, opinionLayer, newOpinionList)

