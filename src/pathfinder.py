import pandas as pd
import os
from heapq import heappush, heappop
from scipy.spatial import distance
import networkx as nx
import matplotlib.pyplot as plt

class PathFinder(object):
    def __init__(self, dfNode, dfEdge):
        self.dfEdge = dfEdge
        self.dfNode = dfNode

    def search(self, initial, goal, count):
        # count is the max number of path to search from initial to goal
        node = (0, initial, [], 0) # fCost, node, path, gCost
        heap = []
        heappush(heap, node)

        goalInfo = self.dfNode.loc[self.dfNode['idNode'] == goal]
        goalX = int(goalInfo['x'])
        goalY = int(goalInfo['y'])
        pathList = []
        while (len(heap) > 0 and len(pathList) < count):
            expanseNode = heappop(heap)
            currentTown = expanseNode[1]
            # print('Current Town: ', currentTown)

            if (currentTown != goal):
                dfNeighboring = self.dfEdge.loc[(self.dfEdge['idNodeStart'] == currentTown) | (self.dfEdge['idNodeEnd'] == currentTown)]
                for index, row in dfNeighboring.iterrows():
                    neighborTown = row['idNodeEnd'] if row['idNodeStart'] == currentTown else row['idNodeStart']

                    if (neighborTown not in expanseNode[2]):
                        gCost = expanseNode[3] + int(row['distance'])
                        nodeInfo = self.dfNode.loc[self.dfNode['idNode'] == neighborTown]
                        nodeX = int(nodeInfo['x'])
                        nodeY = int(nodeInfo['y'])
                        hCost = distance.euclidean((nodeX, nodeY), (goalX, goalY))
                        fCost = gCost + hCost
                        path = []
                        for town in expanseNode[2]:
                            path.append(town)
                        path.append(currentTown)
                        heappush(heap, (fCost, neighborTown, path, gCost))
            
            else:
                expanseNode[2].append(currentTown)
                # print('Path: ', expanseNode[2])
                pathList.append(expanseNode[2])

        return pathList

if __name__ == "__main__":
    # Testing pathfinder with dummy data from Rinaldi Munir's presentation
    dataPath = os.path.join(os.getcwd(), os.pardir, 'data')
    print('Reading csv...')
    dfNode = pd.read_csv(os.path.join(dataPath, 'dummy_node.csv'), delim_whitespace=True, names=['idNode', 'x', 'y'])
    dfEdge = pd.read_csv(os.path.join(dataPath, 'dummy_edge.csv'), delim_whitespace=True, names=['idEdge', 'idNodeStart', 'idNodeEnd', 'distance'])
    # print(dfNode)
    # print(dfEdge)

    pathFinder = PathFinder(dfNode, dfEdge)
    print('List of path:')
    print(pathFinder.search('A', 'B', 2))

    G = nx.from_pandas_edgelist(dfEdge, 'idNodeStart', 'idNodeEnd')

    print('Drawing graph...')
    nx.draw(G, pos=nx.spring_layout(G), with_labels=True)
    plt.show()

    print('Done')