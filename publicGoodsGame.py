# !/usr/bin/python
# coding: UTF-8
#add networkx
import math
import networkx as nx
import random
from matplotlib import pyplot as plt

#近隣とゲームをして戦略からそのポイントが決まる
from makeGraph import makeGraph_fromFile


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

#リストにいるプレイヤーの中からcooperatorの数を返す
def countCooperatorofList(G,playerList):
    numOfCooperator = 0
    for nodeNum in range(len(playerList)):
        if G.node[playerList[nodeNum]]['strategy'] == 1:
            numOfCooperator += 1
    return numOfCooperator


def getPayoff(G,p1,r,c,gamePlayer_List):
    numOfC = countCooperatorofList(G, gamePlayer_List)
    # print 'Cの数は', numOfC
    # print 'playerは', len(gamePlayer_List)

    if p1['strategy'] == 1:
        p1['point'] += r * numOfC * c / len(gamePlayer_List) - c
    else:
        p1['point'] += r * numOfC * c / len(gamePlayer_List)

    return p1['point']


def publicGoodGame(G,r,c):
    strategyList = []
    for nodeNum in range(nx.number_of_nodes(G)):
        # print ''
        p1 = G.node[nodeNum]
        neighbors_List = G.neighbors(nodeNum)

        # print '初期値',p1['point']
        for neighborNum in range(len(neighbors_List)):
            gamePlayer_List= G.neighbors(neighbors_List[neighborNum])
            # print gamePlayer_List
            gamePlayer_List.append(neighbors_List[neighborNum])
            # print gamePlayer_List
            p1['point'] = getPayoff(G,p1,r,c,gamePlayer_List)
            # print '後の点',p1['point']

        gamePlayer_List = neighbors_List
        gamePlayer_List.append(nodeNum)
        # print gamePlayer_List
        p1['point'] = getPayoff(G,p1,r,c,gamePlayer_List)
        strategyList.append(p1['strategy'])
        print '最終',p1['point']
    return G,strategyList


#戦略をコピーする
def copyStrategy(G,strategyList):
    for nodeNum in range(nx.number_of_nodes(G)):
        node = G.node[nodeNum]  # ランダムにノードを選択
        copyNode_list = G.neighbors(nodeNum)    #コピー相手の候補リストを作る
        if copyNode_list != []:
            copyNodeNum =random.choice(copyNode_list)   #候補リストの中からランダムに選択
            copyNode = G.node[copyNodeNum]              #コピー相手の決定
            p = (1.0-math.tanh(node['point']-copyNode['point']))*0.5   #どのくらいの確率で戦略をコピーするのか
            # print 'tanh', math.tanh(node['point'] - copyNode['point']),'pは',p
            x = random.random()
            if x < p:
                node['strategy'] = strategyList[copyNodeNum]    #strategyListから戦略をコピー
        node['point'] = 0   #全てのポイントをリセットする!!!
    return G


gameLayer_info = makeGraph_fromFile(10, 'test.csv', 'GL', 0.0)
gameLayer = gameLayer_info[0]
strategyList = gameLayer_info[2]

Gset = publicGoodGame(gameLayer, 1.1, 1)
G = Gset[0]
strategyList = Gset[1]
G = copyStrategy(G,strategyList)


for nodeNum in range(nx.number_of_nodes(G)):
    print G.node[nodeNum]['strategy']




# pos = nx.spring_layout(gameLayer)  # グラフ形式を選択。ここではスプリングモデルでやってみる
# nx.draw(gameLayer, pos, with_labels=True)  # グラフ描画。 オプションでノードのラベル付きにしている
# plt.show()


#
#
# def gameStep(G,s,t):
#     Gset = game(G,s,t)
#     G = Gset[0]
#     strategyList = Gset[1]
#     G =copyStrategy(G,strategyList)
#     # print calStrategyNum(G)
#     return G