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
from copy import deepcopy

if __name__ == '__main__':
    print('Welcome to Logistic Routing Problem Program! \nThis problem is a Multiple Traveling Salesman Problem (mTSP) that will be solved using Ant Colony Optimization.')
    townChoice = int(input('Please choose a town to be the test case!\n1. Oldenburgh\n2. San Fransisco\n'))
    selectedTown = 'OL' if townChoice == 1 else 'SF'

    # Reading road data files
    dataPath = os.path.join(os.getcwd(), os.pardir, 'data')

    nodeFile = os.path.join(dataPath, selectedTown + '_node.txt')
    edgeFile = os.path.join(dataPath, selectedTown + '_edge.txt')
    pathFinder = A_Star(nodeFile, edgeFile)

    maxNode = len(pathFinder.getNodeDict().keys()) - 1
    inputChoice = int(input('How do you want to input the nodes?\n1. Input Manually\n2. Input Random Nodes\n'))
    n = int(input('Please enter the maximum number of nodes: '))
    requestedNodes = []
    print('The first node generated/inputted will be the depot')
    
    # Generate or take user input to get list of nodes
    if (inputChoice == 1):
        print(f'Maximum node number: {maxNode}')
        while len(requestedNodes) < n:
            nodeInput = int(input('Please enter a new node:'))
            if (nodeInput < maxNode and nodeInput not in requestedNodes):
                requestedNodes.append(nodeInput)
            else:
                print('Please enter a unique node and below the maximum node')
    else:
        bound = int(input('Do you want to bound the generated random numbers to a range to speed up time? (The generated nodes will be in a range of 250)\n1. Yes\n2. No\n'))
        if (bound == 1):
            lowerBound = random.randint(0, maxNode - 250)
            nodeList = list(range(lowerBound, lowerBound + 250))
        else:
            nodeList = list(range(maxNode))
        random.shuffle(nodeList)
        while len(requestedNodes) < n:
            nodeInput = nodeList.pop()
            requestedNodes.append(nodeInput)

    salesmanCount = int(input('Please enter the number of salesmen: '))
    while (salesmanCount > (n / 2) - 1):
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

    distanceMatrix = [[0 for j in range(len(requestedNodes))] for i in range(len(requestedNodes))]
    pathMatrix = [[0 for j in range(len(requestedNodes))] for i in range(len(requestedNodes))]
    
    # Creating distance matrix
    for i in range(len(requestedNodes)):
        for j in range(i, len(requestedNodes)):
            path, cost = pathFinder.search(requestedNodes[i], requestedNodes[j])
            distanceMatrix[i][j] = distanceMatrix[j][i] = cost
            pathMatrix[i][j] = path
            pathMatrix[j][i] = path[::-1]

    # Printing distance matrix
    distanceMatrixDisplayed = deepcopy(distanceMatrix)
    for i in range(len(distanceMatrixDisplayed)):
        distanceMatrixDisplayed[i].insert(0, str(requestedNodes[i]) + '|')
    distanceMatrixDisplayed.insert(0, ['-' for i in range(len(requestedNodes) + 1)])
    distanceMatrixDisplayed.insert(0, [''] + list(requestedNodes))
    s = [[str(e) for e in row] for row in distanceMatrixDisplayed]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]

    print('Distance matrix generated: ')
    print('\n'.join(table))

    # Creating subgraph
    userInput = input('Press any key to display subgraph...')
    subgraph = nx.Graph()
    subgraph.add_nodes_from(requestedNodes)
    for i in range(len(distanceMatrix)):
        for j in range(len(distanceMatrix[i])):
            subgraph.add_edge(requestedNodes[i], requestedNodes[j], labels=distanceMatrix[i][j], color='black')

    print('Displaying Subgraph...')
    labels = nx.get_edge_attributes(subgraph, 'labels')
    colors = nx.get_edge_attributes(subgraph, 'color')
    
    nx.draw(subgraph, pos=nx.kamada_kawai_layout(subgraph), with_labels=True, dpi=100)
    plt.show()
    print('Click x to close the graph and continue...')

    # Using ACO to find solution for mTSP
    aco = ACO(30, salesmanCount, 1, 1, 0, distanceMatrix)
    paths, cost = aco.solve()
    print('Paths generated: ')
    for i in range(len(paths)):
        print('Salesman ', i + 1, 'Path: ', '-'.join(str(x) for x in paths[i]), ' Cost: ', cost[i])
    print(f'Total cost: {sum(cost)}')
    
    colorList = ['green', 'blue', 'red', 'indigo', 'pink', 'orange', 'darkgreen', 'magenta', 'brown', 'purple']
    
    # Displaying mTSP solution on subgraph
    print('Drawing salesmen path on subgraph...')
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

    userInput = input('Press any key to display colored subgraph...')
    print('Displaying colored subgraph...')
    nx.draw(subgraph, pos=nx.kamada_kawai_layout(subgraph), with_labels=True, dpi=100)
    nx.draw_networkx_edges(subgraph, pos=nx.kamada_kawai_layout(subgraph), edge_color=colors)
    nx.draw_networkx_edge_labels(subgraph, pos=nx.kamada_kawai_layout(subgraph), edge_labels=labels, label_pos=0.5)
    plt.legend(subgraphPatch, subgraphLabels, loc='best')
    plt.show()
    print('Click x to close the graph and continue...')

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

    pos=nx.kamada_kawai_layout(resultRoadGraph)

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
    userInput = input('Press any key to display road graph...')
    print('Displaying road graph...')
    plt.legend(resultRoadPatch, resultRoadLabels, loc='best')
    plt.show()
    print('Use full screen for better view!')
    print('Click x to close the graph and continue...')

    print('Thank you!')

    
    

    