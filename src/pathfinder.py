import pandas as pd
import os
from heapq import heappush, heappop
from scipy.spatial import distance
import networkx as nx
import matplotlib.pyplot as plt

class A_Star(object):
    def __init__(self, dfNode, dfEdge):
        self.dfEdge = dfEdge
        self.dfNode = dfNode

    def search(self, initial, goal):

        # count is the max number of path to search from initial to goal
        node = (0, initial, [], 0) # fCost, node, path, gCost
        heap = [node]

        goalInfo = self.dfNode.loc[self.dfNode['idNode'] == goal]
        goalX = int(goalInfo['x'])
        goalY = int(goalInfo['y'])

        reachGoal = False
        expanseNode = ()
        while (not reachGoal):
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
                        path.append(int(currentTown))
                        heappush(heap, (fCost, neighborTown, path, gCost))
            
            else:
                expanseNode[2].append(int(currentTown))
                reachGoal = True

        return expanseNode[2], expanseNode[3]

if __name__ == "__main__":
    # Testing pathfinder with dummy data from Mr. Rinaldi Munir's presentation 'Route/Path Planning using A Star and UCS'
    dataPath = os.path.join(os.getcwd(), os.pardir, 'data')
    print('Reading csv...')
    dfNode = pd.read_csv(os.path.join(dataPath, 'dummy_node.csv'), delim_whitespace=True, names=['idNode', 'x', 'y'])
    dfEdge = pd.read_csv(os.path.join(dataPath, 'dummy_edge.csv'), delim_whitespace=True, names=['idEdge', 'idNodeStart', 'idNodeEnd', 'distance'])
    # print(dfNode)
    # print(dfEdge)

    pathFinder = A_Star(dfNode, dfEdge)
    print('List of path:')
    path, cost = pathFinder.search('A','B')

    print(f'Path: {path}\n Cost: {cost}')

    # G = nx.from_pandas_edgelist(dfEdge, 'idNodeStart', 'idNodeEnd')

    # print('Drawing graph...')
    # nx.draw(G, pos=nx.spring_layout(G), with_labels=True)
    # plt.show()

    # print('Done')