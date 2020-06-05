import pandas as pd
import os
from heapq import heappush, heappop
from scipy.spatial import distance
import networkx as nx
import matplotlib.pyplot as plt
import time
import loader

class A_Star(object):
    def __init__(self, nodeFile, edgeFile):
        self.nodeDict = loader.loadNodes(nodeFile)
        self.neighborDict, self.distanceDict = loader.loadEdges(edgeFile, self.nodeDict)

    def getNodeDict(self):
        return self.nodeDict
        
    def getDistanceDict(self):
        return self.distanceDict

    def getNeighborDict(self):
        return self.neighborDict

    def search(self, initial, goal):

        # count is the max number of path to search from initial to goal
        node = (0, initial, [], 0) # fCost, node, path, gCost
        heap = [node]

        goalCoordinates = self.nodeDict[goal]
        goalX = goalCoordinates[0]
        goalY = goalCoordinates[1]

        reachGoal = False
        expanseNode = ()
        while (not reachGoal):
            expanseNode = heappop(heap)
            currentTown = expanseNode[1]

            if (currentTown != goal):
                # dfNeighboring = self.dfEdge.loc[(self.dfEdge['idNodeStart'] == currentTown) | (self.dfEdge['idNodeEnd'] == currentTown)]
                neighboringNodes = self.neighborDict[currentTown]
                # for index, row in dfNeighboring.iterrows():
                for neighborTown in neighboringNodes:
                    # neighborTown = row['idNodeEnd'] if row['idNodeStart'] == currentTown else row['idNodeStart']

                    if (neighborTown not in expanseNode[2]):
                        d = self.distanceDict[(currentTown, neighborTown)] if (currentTown, neighborTown) in self.distanceDict.keys() else self.distanceDict[(neighborTown,currentTown)]
                        gCost = expanseNode[3] + d
                        nodeCoordinates = self.nodeDict[neighborTown]
                        nodeX = nodeCoordinates[0]
                        nodeY = nodeCoordinates[1]
                        hCost = distance.euclidean((nodeX, nodeY), (goalX, goalY))
                        fCost = gCost + hCost
                        path = []
                        path.extend(expanseNode[2])
                        path.append(currentTown)
                        heappush(heap, (fCost, neighborTown, path, gCost))
            
            else:
                expanseNode[2].append(currentTown)
                reachGoal = True

        return expanseNode[2], round(expanseNode[3])

if __name__ == "__main__":
    # Testing pathfinder with dummy data from Mr. Rinaldi Munir's presentation 'Route/Path Planning using A Star and UCS'
    dataPath = os.path.join(os.getcwd(), os.pardir, 'data')
    pathFinder = A_Star(os.path.join(dataPath, 'OL_node.txt'), os.path.join(dataPath, 'OL_edge.txt'))
    
    path, cost = pathFinder.search(1, 90)
    print(f'Path: {path}')
    print(f'Cost: {cost}')
    print('Done')