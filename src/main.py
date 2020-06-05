import pandas as pd
import os
import networkx as nx
import matplotlib.pyplot as plt
from pathfinder import A_Star
from aco import ACO
import numpy as np
from matplotlib.lines import Line2D
from textwrap import wrap
import random
import time

if __name__ == '__main__':
    print('Welcome to Logistic Routing Problem Program! \nThis problem is a Multiple Traveling Salesman Problem (mTSP) that will be solved using Ant Colony Optimization.')
    townChoice = int(input('Please choose a town to be the test case!\n1. Oldenburgh\n2. San Fransisco\n'))
    selectedTown = 'OL' if townChoice == 1 else 'SF'

    # Reading road data files to pandas
    dataPath = os.path.join(os.getcwd(), os.pardir, 'data')

    nodeFile = os.path.join(dataPath, selectedTown + '_node.txt')
    edgeFile = os.path.join(dataPath, selectedTown + '_edge.txt')
    pathFinder = A_Star(nodeFile, edgeFile)


    maxNode = len(pathFinder.getNodeDict().keys()) - 1
    inputChoice = int(input('How do you want to input the nodes?\n1. Input Manually\n2. Input Random Nodes\n'))
    n = int(input('Please enter the maximum number of nodes: '))
    requestedNodes = []
    

    if (n == 1):
        while len(requestedNodes) < n:
            nodeInput = int(input('Please enter a new node:'))
            if (nodeInput < maxNode):
                requestedNodes.append(nodeInput)
    else:
        bound = int(input('Do you want to bound the generated random numbers to a range to speed up time? (The generated nodes will be in a range of 500)\n1. Yes\n2. No\n'))
        if (bound == 1):
            lowerBound = random.randint(0, maxNode - 500)
            nodeList = list(range(lowerBound, lowerBound + 500))
        else:
            nodeList = list(range(maxNode))
        random.shuffle(nodeList)
        while len(requestedNodes) < n:
            nodeInput = nodeList.pop()
            requestedNodes.append(nodeInput)

    salesmanCount = int(input('Please enter the number of salesmen: '))
    while (salesmanCount > (n / 2)):
        print('The number of salesman can\'t exceed half of requested nodes')
        salesmanCount = int(input('Please enter the number of salesmen: '))

    alpha = 1
    beta = 1
    rho = 1
    iterCount = 50
    modifyParam = int(input('Do you want to modify ACO parameters? (Default alpha = 1, beta = 1, rho = 1, number of iteration = 50)\n1. Yes\n2. No\n'))
    if modifyParam == 1:
        alpha = int(input('Please enter alpha: '))
        beta = int(input('Please enter beta: '))
        rho = int(input('Please enter rho: '))

    # print('Creating Subgraph...')
    # # Dummy user input
    print(requestedNodes)
    # requestedNodes = [5447, 5454, 5465, 5540, 5495, 5470, 5644, 5627]

    distanceMatrix = [[0 for j in range(len(requestedNodes))] for i in range(len(requestedNodes))]
    pathMatrix = [[0 for j in range(len(requestedNodes))] for i in range(len(requestedNodes))]
    
    for i in range(len(requestedNodes)):
        for j in range(i, len(requestedNodes)):
            print(f'i: {i}, j: {j}')
            path, cost = pathFinder.search(requestedNodes[i], requestedNodes[j])
            distanceMatrix[i][j] = distanceMatrix[j][i] = cost
            pathMatrix[i][j] = path
            pathMatrix[j][i] = path[::-1]

    subgraph = nx.Graph()
    subgraph.add_nodes_from(requestedNodes)
    for i in range(len(distanceMatrix)):
        for j in range(len(distanceMatrix[i])):
            subgraph.add_edge(requestedNodes[i], requestedNodes[j], labels=distanceMatrix[i][j], color='black')

    print('Displaying Subgraph...')
    labels = nx.get_edge_attributes(subgraph, 'labels')
    colors = nx.get_edge_attributes(subgraph, 'color')
    
    nx.draw(subgraph, pos=nx.kamada_kawai_layout(subgraph), with_labels=True, dpi=100)
    nx.draw_networkx_edge_labels(subgraph, pos=nx.kamada_kawai_layout(subgraph), edge_labels=labels, label_pos=0.25)
    plt.show()

    aco = ACO(30, 2, 1, 1, 0, distanceMatrix)
    paths, cost = aco.solve()
    print('Raw Cost: ', cost)
    print('Raw Paths: ', paths)
    
    print('Drawing salesmen path on subgraph...')
    colorList = ['green', 'blue', 'red', 'indigo', 'pink', 'orange', 'darkgreen', 'magenta', 'brown', 'purple']

    subgraphPatch = []
    subgraphLabels = []
    subgraph.remove_edges_from(subgraph.edges())
    for path in paths:
        idx = paths.index(path)
        c = colorList[idx] if idx < len(colorList) else np.random.rand(3,)
        subgraphPatch.append(Line2D([0], [0], color=c, linewidth=3))
        subgraphLabels.append(f'Salesman {idx + 1}, cost: {cost[idx]}')
        for i in range(len(path) - 1):
            subgraph.add_edge(requestedNodes[path[i]], requestedNodes[path[i + 1]], color = colorList[idx], labels=distanceMatrix[path[i]][path[i + 1]])


    colors = nx.get_edge_attributes(subgraph,'color').values()
    labels = nx.get_edge_attributes(subgraph, 'labels')
    subgraphLabels = [ '\n'.join(wrap(l, 20)) for l in subgraphLabels]

    print('Displaying colored subgraph...')
    nx.draw(subgraph, pos=nx.kamada_kawai_layout(subgraph), with_labels=True, dpi=100)
    nx.draw_networkx_edges(subgraph, pos=nx.kamada_kawai_layout(subgraph), edge_labels=labels, label_pos=0.25, edge_color=colors)
    nx.draw_networkx_edge_labels(subgraph, pos=nx.kamada_kawai_layout(subgraph), edge_labels=labels, label_pos=0.25)
    plt.legend(subgraphPatch, subgraphLabels, loc='best')
    plt.show()

    print('Creating road path throughout the town...')
    resultRoadGraph = nx.MultiDiGraph()
        
    pathDetails = []
    edgeLists = []
    for path in paths:
        pathDetail = []
        for i in range(len(path) - 1):
            pathDetail.extend(pathMatrix[path[i]][path[i+1]])
            pathDetail.pop()
        resultRoadGraph.add_nodes_from(pathDetail, color='aquamarine')
        pathDetail.append(requestedNodes[0])
        edgeList = []
        for i in range(len(pathDetail) - 1):
            resultRoadGraph.add_edge(pathDetail[i], pathDetail[i + 1])
            edgeList.append((pathDetail[i], pathDetail[i + 1]))
        pathDetails.append(pathDetail)
        edgeLists.append(edgeList)


    resultRoadGraph.add_nodes_from(requestedNodes, color='crimson')
    colors = nx.get_node_attributes(resultRoadGraph,'color').values()

    pos=nx.spring_layout(resultRoadGraph)

    nx.draw(resultRoadGraph, pos, with_labels=True, dpi=100, edge_color=(0,0,0,0), node_color=colors)

    rad = 0.1
    resultRoadPatch = []
    resultRoadLabels = []
    for edgeList in edgeLists:
        idx = edgeLists.index(edgeList)
        path = '-'.join(str(x) for x in pathDetails[idx])
        c = colorList[idx] if idx < len(colorList) else np.random.rand(3,)
        resultRoadPatch.append(Line2D([0], [0], color=c, linewidth=3))
        resultRoadLabels.append(f'Salesman {idx + 1}: {cost[idx]}')
        
        nx.draw_networkx_edges(resultRoadGraph, pos, with_labels=True, edgelist = edgeList, connectionstyle=f'arc3, rad = {rad}', edge_color=colorList[idx])
        rad += 0.3

    resultRoadLabels = [ '\n'.join(wrap(l, 50)) for l in resultRoadLabels]
    print('Displaying road graph')
    plt.legend(resultRoadPatch, resultRoadLabels, loc='best')
    plt.show()

    print('Finished')

    
    

    