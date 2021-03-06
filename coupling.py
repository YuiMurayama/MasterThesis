# !/usr/bin/python
# coding: UTF-8
#add networkx


import random
import networkx as nx


def coupling(gameLayer,opinionLayer,opinionList,opinionLayerStrength):
    newOpinionList = []
    for nodeNum in range(nx.number_of_nodes(opinionLayer) ):
        rand_of_copy = random.random()
        rand_of_whichLayer = random.random()

        # どちらからどちらへコピーするかの確率

        if rand_of_copy < 0.5:
            # if rand_of_whichLayer <= opinionLayerStrength:
            if rand_of_whichLayer <= gameLayer.node[nodeNum]['biase']:
                gameLayer.node[nodeNum]['strategy'] = opinionLayer.node[nodeNum]['opinion']
            else:
                if opinionLayer.node[nodeNum]['activist'] != 1:
                    opinionLayer.node[nodeNum]['opinion'] = gameLayer.node[nodeNum]['strategy']


        # if rand_of_copy < gameLayer.node[nodeNum]['biase']:
        #     if nodeNum %2 == 0:
        #         gameLayer.node[nodeNum]['strategy'] = opinionLayer.node[nodeNum]['opinion']
        #     else:
        #         if opinionLayer.node[nodeNum]['activist'] != 1:
        #             opinionLayer.node[nodeNum]['opinion'] = gameLayer.node[nodeNum]['strategy']



        newOpinionList.append(opinionLayer.node[nodeNum]['opinion'])

    return (gameLayer, opinionLayer, newOpinionList)

