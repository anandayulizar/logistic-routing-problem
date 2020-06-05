import os

def loadNodes(filename):
    with open(filename) as file:
        nodeList = file.read().split('\n')
        nodeDict = {}
        for node in nodeList:
            coordinates = node.split(' ')
            if (len(coordinates) != 3):
                continue
            nodeDict[int(coordinates[0])] = (float(coordinates[1]), float(coordinates[2]))
        
    return nodeDict

def loadEdges(filename, nodeDict):
    with open(filename) as file:
        edgeList = file.read().split('\n')
        neighborDict = {}
        for node in nodeDict.keys():
            neighborDict[node] = []

        distanceDict = {}
        for edge in edgeList:
            connection = edge.split(' ')
            if (len(connection) != 4):
                continue
            neighborDict[int(connection[1])].append(int(connection[2]))
            neighborDict[int(connection[2])].append(int(connection[1]))
            distanceDict[(int(connection[1]), int(connection[2]))] = float(connection[3])

        return neighborDict, distanceDict



if __name__ == "__main__":
    dataPath = os.path.join(os.getcwd(), os.pardir, 'data')
    nodeDict = loadNodes(os.path.join(dataPath, 'OL_node.csv'))
    neighborDict, distanceDict = loadEdges(os.path.join(dataPath, 'OL_edge.csv'), nodeDict)

    # print(distanceDict)

    d = distanceDict[(2209, 2239)] if (2209, 2239) in distanceDict.keys() else distanceDict[(2239,2209)]

    print(d)