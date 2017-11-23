# !/usr/bin/python
# coding: UTF-8
#add networkx
import math
import networkx as nx
import random


#近隣とゲームをして戦略からそのポイントが決まる
def game(G, s, t):
    strategyList = []
    for nodeNum in range(nx.number_of_nodes(G)):
        p1 = G.node[nodeNum]#ランダムにノードを選択
        p2_list =G.neighbors(nodeNum)
        if p2_list != []:
            p2 = G.node[random.choice(p2_list)]
            if p1['strategy'] == 1 and p2['strategy'] == 1:
                p1['point'] += 1
                p2['point'] += 1
            elif p1['strategy'] == 0 and p2['strategy'] == 1:
                p1['point'] += t
                p2['point'] += s
            elif p1['strategy'] == 1 and p2['strategy'] == 0:
                p1['point'] += s
                p2['point'] += t
            else:
                p1['point'] += 0
                p2['point'] += 0
        strategyList.append(p1['strategy'])
    # print strategyList
    return G,strategyList




def makePointList(G):
    pointList =[]
    for nodeNum in range(nx.number_of_nodes(G)):
        pointList.append(G.node[nodeNum]['point'])
    # print pointList
    return pointList


#戦略をコピーする
def copyStrategy(G,strategyList,toleranceNum):
    for nodeNum in range(nx.number_of_nodes(G)):
        node = G.node[nodeNum]  # ランダムにノードを選択
        copyNode_list = G.neighbors(nodeNum)    #コピー相手の候補リストを作る

        if copyNode_list != []:

            copyNodeNum =random.choice(copyNode_list)   #候補リストの中からランダムに選択
            copyNode = G.node[copyNodeNum]              #コピー相手の決定
            p = (1.0-math.tanh(node['point']-copyNode['point']))*0.1   #どのくらいの確率で戦略をコピーするのか
            # print 'tanh', math.tanh(node['point'] - copyNode['point']),'pは',p
            x = random.random()
            if x < p:
                if node['strategy'] == 1 and strategyList[copyNodeNum] == 0:
                    if node['tolerance'] < toleranceNum:
                        node['tolerance'] += 1
                    else:
                        node['strategy'] = strategyList[copyNodeNum]
                        node['tolerance'] = 0

                else:
                    node['strategy'] = strategyList[copyNodeNum]    #strategyListから戦略をコピー


        #ここにtorelanceのコードを入れる


        node['point'] = 0   #全てのポイントをリセットする!!!

    return G

#CとDの数を数える
def countC_of_gameLayer(G):
    nodeNumArrayOfC =[]
    nodeNumArrayOfD =[]
    numOfCooperator = 0
    numOfDefector = 0
    for nodeNum in range(nx.number_of_nodes(G)):
        if G.node[nodeNum]['strategy'] == 1:
            numOfCooperator += 1
            nodeNumArrayOfC.append(nodeNum)
        if G.node[nodeNum]['strategy'] == 0:
            numOfDefector += 1
            nodeNumArrayOfD.append(nodeNum)
    return numOfCooperator
    # return (nodeNumArrayOfC,nodeNumArrayOfD)



#ペイオフと戦略コピーをまとめたものこれが全部！
#G,s,tを入れるとGMを実行して返してくれる

def gameStep(G,s,t,toleranceNum):
    Gset = game(G,s,t)
    G = Gset[0]
    strategyList = Gset[1]
    G =copyStrategy(G,strategyList,toleranceNum)
    # print calStrategyNum(G)
    return G