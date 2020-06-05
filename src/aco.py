from random import uniform

class ACO(object):
    def __init__(self, num_iteration, salesman_count, alpha, beta, rho, distanceMatrix):
        self.num_iteration  = num_iteration
        self.salesman_count  = salesman_count
        self.alpha  = alpha
        self.beta  = beta
        self.rho  = rho
        self.distanceMatrix = distanceMatrix
        self.n = len(distanceMatrix)
        self.globalPheromone = [[1 for j in range(self.n)] for i in range(self.n)]
        self.deltaPheromone = [[0 for j in range(self.n)] for i in range(self.n)]

    def getProbability(self, i, j, visitedCity):
        tau = self.globalPheromone[i][j]
        eta = 1 / self.distanceMatrix[i][j]
        upper = (tau ** self.alpha) * (eta ** self.beta)
        down = 0
        for city in range(self.n):
            
            if city not in visitedCity and city != i:
                tau = self.globalPheromone[i][city]
                eta = 1 / self.distanceMatrix[i][city]
                down += (tau ** self.alpha) * (eta ** self.beta)

        return upper / down

    def rouletteWheel(self, probabilityArr):
        rouletteIdx = []
        rouletteArr = []
        for i in range(len(probabilityArr)):
            if probabilityArr[i] != 0:
                rouletteIdx.append(i)
                addition = 0
                for j in range(i, len(probabilityArr)):
                    addition += probabilityArr[j]
                rouletteArr.append(addition)
            else:
                probabilityArr[i] = float('inf')

        choice = uniform(0, rouletteArr[0])

        ret = rouletteIdx[len(rouletteIdx) - 1]
        for i in range(len(rouletteArr)):
            if (choice > rouletteArr[i]):
                ret = rouletteIdx[i - 1]
            elif (choice == rouletteArr[i]):
                ret = rouletteIdx[i]
        
        return ret

    def updateGlobalPheromone(self):
        for i in range(len(self.globalPheromone)):
            for j in range(len(self.globalPheromone)):
                self.globalPheromone[i][j] *= (1 - self.rho)
                self.globalPheromone[i][j] += self.deltaPheromone[i][j]

    def resetDeltaPheromone(self):
        self.deltaPheromone = [[0 for j in range(self.n)] for i in range(self.n)]

    def solve(self):
        paths = []
        cost = 0

        for iteration in range(self.num_iteration):
            pathList = [[] for i in range(self.salesman_count)]
            visitedCity = []
            for salesman in range(self.salesman_count):
                currentCity = 0
                pathList[salesman].append(0)
                
                while ((len(visitedCity) < self.n - 1) and ((len(pathList[salesman]) < self.n - len(visitedCity) - (2 * (self.salesman_count - salesman - 1))) or (salesman == self.salesman_count - 1)) and (currentCity != 0 or len(pathList[salesman]) == 1)) :
                    probabilityArr = []
                    for city in range(len(self.distanceMatrix[currentCity])):
                        if ((city in visitedCity) or (city == 0 and (len(pathList[salesman]) < 3 or salesman == self.salesman_count - 1))):
                            probabilityArr.append(0)
                        else:
                            probabilityArr.append(self.getProbability(currentCity, city, visitedCity))

                    nextCity = self.rouletteWheel(probabilityArr)
                    self.deltaPheromone[currentCity][nextCity] += 1 / self.distanceMatrix[currentCity][nextCity]
                    currentCity = nextCity
                    if currentCity != 0:
                        visitedCity.append(currentCity)
                    pathList[salesman].append(currentCity)

                if currentCity != 0:
                    pathList[salesman].append(0)

            paths = pathList

            self.updateGlobalPheromone()
            self.resetDeltaPheromone()

        cost = [0 for i in range(len(paths))]
        for i in range(len(paths)):
            for j in range(len(paths[i]) - 1):
                cost[i] += self.distanceMatrix[paths[i][j]][paths[i][j+1]]

        return paths, cost



if __name__ == "__main__":
    print('Creating distance matrix...')
    distanceMatrix = [[0, 20, 30, 10, 11], [15, 0, 16, 4, 2], [3, 5, 0, 2, 4], [19, 6, 18, 0, 3], [16, 4, 7, 16, 0]]
    # distanceMatrix = [[0, 12, 10, 5], [12, 0, 9, 8], [10, 9, 0, 15], [5, 8, 15, 0]]
    # distanceMatrix = [[[[0, 2, 7, 8], [6, 0, 3, 7], [5, 8, 0, 4], [7, 6, 9, 0]]]]
    
    print(distanceMatrix)
    print('#' * 150)

    aco = ACO(5, 1, 1, 1, 0, distanceMatrix)
    path, cost = aco.solve()
    print('Cost: ', cost)
    print('Path: ', path)