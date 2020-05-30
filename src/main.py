import pandas as pd
import os
import networkx as nx
import matplotlib.pyplot as plt
from pathfinder import PathFinder

if __name__ == '__main__':
    print('Reading csv...')
    # Reading road data files to pandas
    dataPath = os.path.join(os.getcwd(), os.pardir, 'data')
    dfNode = pd.read_csv(os.path.join(dataPath, 'OL_node.csv'), delim_whitespace=True, names=['idNode', 'x', 'y'])
    dfEdge = pd.read_csv(os.path.join(dataPath, 'OL_edge.csv'), delim_whitespace=True, names=['idEdge', 'idNodeStart', 'idNodeEnd', 'distance'])

    pathFinder = PathFinder(dfNode, dfEdge)

    print('Creating Subgraph...')
    # Dummy user input
    requestedNodes = [1, 3, 19, 20, 30, 22, 39, 14]
    addNode = []
    for i in range(len(requestedNodes)):
        # print('i: ', requestedNodes[i])
        for j in range(i + 1, len(requestedNodes)):
            # print('j: ', requestedNodes[j])
            paths = pathFinder.search(requestedNodes[i], requestedNodes[j], 2)
            for path in paths:
               addNode.extend(path) 
               addNode = list(dict.fromkeys(addNode))

    requestedNodes.extend(addNode)

    newDfEdge = dfEdge.loc[(dfEdge['idNodeStart'].isin(requestedNodes)) & (dfEdge['idNodeEnd'].isin(requestedNodes))]

    # Alternatives for positioning nodes according to its coordinates (better used for full graph)

    # pos ={}
    # for node in requestedNodes:
    #     nodePosition = dfNode.loc[dfNode['idNode'] == node]
    #     x = int(nodePosition['x'])
    #     y = int(nodePosition['y'])
    #     pos[node] = (x, y)

    G = nx.from_pandas_edgelist(newDfEdge, 'idNodeStart', 'idNodeEnd')

    print('Drawing Subgraph...')
    # plt.figure(3,figsize=(24, 24))

    # Maximize figure windows (Currently work on Windows OS)
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    nx.draw(G, pos=nx.spring_layout(G), with_labels=True, dpi=100)
    plt.show()

    print('Done')

    
    

    