from random import randint, uniform

class ACO(object):
    def __init__(self, num_iteration, ant_count, alpha, beta, rho, distanceMatrix):
        self.num_iteration  = num_iteration
        self.ant_count  = ant_count
        self.alpha  = alpha
        self.beta  = beta
        self.rho  = rho
        self.distanceMatrix = distanceMatrix
        self.n = len(distanceMatrix)
        self.globalPheromone = [[1 for j in range(self.n)] for i in range(self.n)]
        self.deltaPheromone = [[0 for j in range(self.n)] for i in range(self.n)]

    def getProbability(self, i, j, visitedCity):
        tau = self.globalPheromone[i][j]
        # print('i: ', i, 'j: ', j)
        eta = 1 / self.distanceMatrix[i][j]
        upper = (tau ** self.alpha) * (eta ** self.beta)
        down = 0
        # print('loop buat down')
        # print('visited city: ', visitedCity)
        for city in range(self.n):
            
            if city not in visitedCity:
                # print(city)
                tau = self.globalPheromone[i][city]
                eta = 1 / self.distanceMatrix[i][j]
                # print('tau: ', tau, 'eta: ', eta)
                down += (tau ** self.alpha) * (eta ** self.beta)
        
        # print(upper / down)

        return upper / down

    def rouletteWheel(self, probabilityArr):
        rouletteIdx = []
        rouletteArr = []
        # print('probArr: ', probabilityArr)
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
        # print('choice: ',choice)

        ret = rouletteIdx[len(rouletteIdx) - 1]
        # print('Roulette Arr: ',rouletteArr)
        # print(probabilityArr)
        # print(choice)
        for i in range(len(rouletteArr)):
            if (choice > rouletteArr[i]):
                ret = rouletteIdx[i - 1]
            elif (choice == rouletteArr[i]):
                ret = rouletteIdx[i]

        # ret = 0
        # for i in range(len(probabilityArr)):
        #     if probabilityArr[i] > ret:
        #         ret = i
        
        
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

        # for city in range(self.n):
        #     currentCity = 0
        #     visitedCity = []
        #     visitedCity.append(currentCity)
        #     while len(visitedCity) < self.n:
        #         # print(visitedCity)
        #         probabilityArr = []
        #         for city in range(len(self.distanceMatrix[currentCity])):
        #             if (city in visitedCity):
        #                 probabilityArr.append(0)
        #             else:
        #                 probabilityArr.append(self.getProbability(currentCity, city, visitedCity))


        #         nextCity = self.rouletteWheel(probabilityArr)
        #         # print('current: ', currentCity, 'next: ', nextCity)
        #         self.deltaPheromone[currentCity][nextCity] += 1 / self.distanceMatrix[currentCity][nextCity]
        #         currentCity = nextCity
        #         visitedCity.append(currentCity)

        #     visitedCity.append(0)

        # self.updateGlobalPheromone()
        # self.resetDeltaPheromone()

        for iteration in range(1, self.num_iteration):
            # print('ITERATION: ', iteration)
            # print('iterasi: ', iteration)
            pathList = [[] for i in range(self.ant_count)]
            visitedCity = []
            for ant in range(self.ant_count):
                # print('Ant: ', ant)
                currentCity = 0
                pathList[ant].append(0)
                # print('Jumlah path: ', len(pathList[ant]), 'Maksimal ngambil: ', self.n - len(visitedCity) - (2 * (self.ant_count - ant - 1)))
                # print('self.n: ', self.n, 'self.ant_count: ', self.ant_count, 'ant: ', ant)
                
                while ((len(visitedCity) < self.n - 1) and ((len(pathList[ant]) < self.n - len(visitedCity) - (2 * (self.ant_count - ant - 1))) or (ant == self.ant_count - 1)) and (currentCity != 0 or len(pathList[ant]) == 1)) :
                    # print(visitedCity)
                    
                    probabilityArr = []
                    for city in range(len(self.distanceMatrix[currentCity])):
                        if ((city in visitedCity) or (city == 0 and (len(pathList[ant]) < 3 or ant == self.ant_count - 1))):
                            probabilityArr.append(0)
                        else:
                            probabilityArr.append(self.getProbability(currentCity, city, visitedCity))


                    nextCity = self.rouletteWheel(probabilityArr)
                    # print('current: ', currentCity, 'next: ', nextCity)
                    self.deltaPheromone[currentCity][nextCity] += 1 / self.distanceMatrix[currentCity][nextCity]
                    currentCity = nextCity
                    if currentCity != 0:
                        visitedCity.append(currentCity)
                    pathList[ant].append(currentCity)
                    # print('visited: ', visitedCity)

                if currentCity != 0:
                    # visitedCity.append(0)
                    pathList[ant].append(0)

            paths = pathList

            self.updateGlobalPheromone()
            self.resetDeltaPheromone()

        # print(path)
        # for i in range(len(visitedCity) - 1):
        #     cost += self.distanceMatrix[path[i]][path[i+1]]

        cost = [0 for i in range(len(paths))]
        for i in range(len(paths)):
            for j in range(len(paths[i]) - 1):
                cost[i] += self.distanceMatrix[paths[i][j]][paths[i][j+1]]



        '''
        for t=1 to num_iteration do
            for k=1 to ant_count do
                repeat until ant k has completed a tour
                    select the city to be visited next with
                    probability pij
                calculate Lk
            update trail levels
        '''

        return paths, cost



if __name__ == "__main__":
    print('Creating distance matrix...')
    distanceMatrix = [[0, 20, 30, 10, 11], [15, 0, 16, 4, 2], [3, 5, 0, 2, 4], [19, 6, 18, 0, 3], [16, 4, 7, 16, 0]]
    # distanceMatrix = [[0, 12, 10, 5], [12, 0, 9, 8], [10, 9, 0, 15], [5, 8, 15, 0]]
    # distanceMatrix = [[[[0, 2, 7, 8], [6, 0, 3, 7], [5, 8, 0, 4], [7, 6, 9, 0]]]]
    
    print(distanceMatrix)

    aco = ACO(50, 1, 1, 1, 0, distanceMatrix)
    path, cost = aco.solve()
    print('Cost: ', cost)
    print('Path: ', path)