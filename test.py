# !/usr/bin/python
# coding: UTF-8
#add networkx

from matplotlib import pyplot as plt
import networkx as nx

import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import networkx as nx
import random

#ネットワーク
graph = nx.Graph()
def get_fig(node_number):
    graph.add_node(node_number, Position=(random.randrange(0, 100), random.randrange(0, 100)))
    graph.add_edge(node_number, random.choice(graph.nodes()))
    nx.draw(graph, pos=nx.get_node_attributes(graph,'Position'))

fig = plt.figure(figsize=(5,4))

anim = animation.FuncAnimation(fig, get_fig, frames=30)
anim.save('demoanimation.gif', writer='imagemagick', fps=4);