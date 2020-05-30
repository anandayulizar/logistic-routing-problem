import pandas as pd
import os
import networkx as nx
import matplotlib.pyplot as plt
from pathfinder import A_Star

if __name__ == '__main__':
    print('Reading csv...')
    # Reading road data files to pandas
    dataPath = os.path.join(os.getcwd(), os.pardir, 'data')
    dfNode = pd.read_csv(os.path.join(dataPath, 'OL_node.csv'), delim_whitespace=True, names=['idNode', 'x', 'y'])
    dfEdge = pd.read_csv(os.path.join(dataPath, 'OL_edge.csv'), delim_whitespace=True, names=['idEdge', 'idNodeStart', 'idNodeEnd', 'distance'])

    pathFinder = A_Star(dfNode, dfEdge)

    distanceMatrix = {}
    print('Creating Subgraph...')
    # Dummy user input
    requestedNodes = [1, 3, 19, 20, 30, 22, 39, 14]
    addNode = []
    for i in range(len(requestedNodes)):
        # print('i: ', requestedNodes[i])
        distanceMatrix[requestedNodes[i]] = {}
        for j in range(i + 1, len(requestedNodes)):
            # print('j: ', requestedNodes[j])
            cost = pathFinder.search(requestedNodes[i], requestedNodes[j], 2)
            distanceMatrix[requestedNodes[i]][requestedNodes[j]] = cost
            # Tambahin buat matrix tar

    G = nx.Graph()
    # dfDistanceMatrix = pd.DataFrame(columns=['idNodeStart', 'idNodeEnd', 'distance'])
    for city1, v in distanceMatrix.items():
        G.add_node(city1)
        for city2, d in v.items():
            G.add_node(city2)
            G.add_edge(city1, city2, labels=d)
            # dfDistanceMatrix = dfDistanceMatrix.append({'idNodeStart': city1, 'idNodeEnd': city2, 'distance': d}, ignore_index=True)
    # print(dfDistanceMatrix)

    # Alternatives for positioning nodes according to its coordinates (better used for full graph)

    # pos ={}
    # for node in requestedNodes:
    #     nodePosition = dfNode.loc[dfNode['idNode'] == node]
    #     x = int(nodePosition['x'])
    #     y = int(nodePosition['y'])
    #     pos[node] = (x, y)

    # G = nx.from_pandas_edgelist(dfDistanceMatrix, 'idNodeStart', 'idNodeEnd')

    print('Drawing Subgraph...')
    # plt.figure(3,figsize=(24, 24))

    # Maximize figure windows (Currently work on Windows OS)
    # mng = plt.get_current_fig_manager()
    # mng.window.state('zoomed')
    labels = nx.get_edge_attributes(G, 'labels')
    nx.draw(G, pos=nx.kamada_kawai_layout(G), with_labels=True, dpi=100)
    nx.draw_networkx_edge_labels(G, pos=nx.kamada_kawai_layout(G), edge_labels=labels, label_pos=0.25)
    plt.show()

    print('Done')

    
    

    