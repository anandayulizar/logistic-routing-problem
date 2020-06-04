import pandas as pd
import os
import networkx as nx
import matplotlib.pyplot as plt
from pathfinder import A_Star
from aco import ACO
import numpy as np
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
from textwrap import wrap

if __name__ == '__main__':
    print('Reading csv...')
    # Reading road data files to pandas
    dataPath = os.path.join(os.getcwd(), os.pardir, 'data')
    dfNode = pd.read_csv(os.path.join(dataPath, 'OL_node.csv'), delim_whitespace=True, names=['idNode', 'x', 'y'])
    dfEdge = pd.read_csv(os.path.join(dataPath, 'OL_edge.csv'), delim_whitespace=True, names=['idEdge', 'idNodeStart', 'idNodeEnd', 'distance'])

    pathFinder = A_Star(dfNode, dfEdge)

    print('Creating Subgraph...')
    # Dummy user input
    requestedNodes = [1, 3, 19, 20, 30, 22, 39, 14]
    distanceMatrix = [[0 for j in range(len(requestedNodes))] for i in range(len(requestedNodes))]
    pathMatrix = [[0 for j in range(len(requestedNodes))] for i in range(len(requestedNodes))]
    for i in range(len(requestedNodes)):
        for j in range(i, len(requestedNodes)):
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

    aco = ACO(50, 2, 1, 1, 0, distanceMatrix)
    paths, cost = aco.solve()
    print('Raw Cost: ', cost)
    print('Raw Paths: ', paths)
    
    print('Drawing salesmen path on subgraph...')
    colorList = ['green', 'blue', 'red', 'indigo', 'pink', 'orange', 'darkgreen', 'magenta', 'brown', 'purple', 'gold']

    subgraphPatch = []
    subgraphLabels = []
    subgraph.remove_edges_from(subgraph.edges())
    for path in paths:
        idx = paths.index(path)
        subgraphPatch.append(Line2D([0], [0], color=colorList[idx], linewidth=3))
        subgraphLabels.append(f'Salesman {idx + 1}, cost: {cost[idx]}')
        for i in range(len(path) - 1):
            subgraph.add_edge(requestedNodes[path[i]], requestedNodes[path[i + 1]], color = colorList[idx], labels=distanceMatrix[path[i]][path[i + 1]])
            # subgraph[requestedNodes[path[i]]][requestedNodes[path[i + 1]]].update({'color' : colorList[idx]})


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

    pos=nx.kamada_kawai_layout(resultRoadGraph)

    nx.draw(resultRoadGraph, pos, with_labels=True, dpi=100, edge_color=(0,0,0,0), node_color=colors)

    rad = 0.1
    resultRoadPatch = []
    resultRoadLabels = []
    for edgeList in edgeLists:
        idx = edgeLists.index(edgeList)
        path = '-'.join(str(x) for x in pathDetails[idx])
        resultRoadPatch.append(Line2D([0], [0], color=colorList[idx], linewidth=3))
        resultRoadLabels.append(f'Salesman {idx + 1}: {path}')
        
        nx.draw_networkx_edges(resultRoadGraph, pos, with_labels=True, edgelist = edgeList, connectionstyle=f'arc3, rad = {rad}', edge_color=colorList[idx])
        rad += 0.25

    resultRoadLabels = [ '\n'.join(wrap(l, 50)) for l in resultRoadLabels]
    print('Displaying road graph')
    print(resultRoadLabels)
    plt.legend(resultRoadPatch, resultRoadLabels, loc='best')
    plt.show()

    print('Finished')

    
    

    