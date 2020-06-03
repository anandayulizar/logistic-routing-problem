from random import randint

class ACO(object):
    def __init__(self, num_iteration, alpha, beta, rho, distanceMatrix):
        self.num_iteration  = num_iteration
        self.alpha  = alpha
        self.beta  = beta
        self.rho  = rho
        self.globalPheromone = [[1 for j in range(len(distanceMatrix))] for i in range(len(distanceMatrix))]
        self.deltaPheromone = [[0 for j in range(len(distanceMatrix))] for i in range(len(distanceMatrix))]
        self.distanceMatrix = distanceMatrix

    def getProbability(self, i, j, visitedCity):
        tau = self.globalPheromone[i][j]
        eta = 1 / self.distanceMatrix[i][j]
        upper = (tau ** self.alpha) * (eta ** self.beta)
        down = 0
        # print('loop buat down')
        for city in range(len(self.distanceMatrix)):
            
            if city not in visitedCity:
                # print(city)
                tau = self.globalPheromone[i][city]
                eta = 1 / self.distanceMatrix[i][j]
                # print('tau: ', tau, 'eta: ', eta)
                down += (tau ** self.alpha) * (eta ** self.beta)

        return upper / down

    def rouletteWheel(self, probabilityArr):
        rouletteIdx = []
        rouletteArr = []
        for i in range(len(probabilityArr)):
            if probabilityArr[i] != 0:
                rouletteIdx.append(i)
                addition = 0
                for j in range(i + 1, len(probabilityArr)):
                    addition += probabilityArr[j]
                rouletteArr.append(addition)
            else:
                probabilityArr[i] = float('inf')

        choice = randint(1, 101) / 100

        ret = rouletteIdx[len(rouletteIdx) - 1]
        # print(probabilityArr)
        # print(choice)
        for i in range(len(rouletteArr)):
            if (choice > rouletteArr[i]):
                ret = rouletteIdx[i - 1]
            elif (choice == rouletteArr[i]):
                ret = rouletteIdx[i]
        
        
        return ret

    def updateGlobalPheromone(self):
        for i in range(len(self.globalPheromone)):
            for j in range(len(self.globalPheromone)):
                self.globalPheromone[i][j] *= self.rho
                self.globalPheromone[i][j] += self.deltaPheromone[i][j]

    def resetDeltaPheromone(self):
        self.deltaPheromone = [[0 for j in range(len(self.distanceMatrix))] for i in range(len(self.distanceMatrix))]

    def solve(self):
        path = []
        cost = 0 # represents infinity
        
        n = len(self.distanceMatrix)

        for city in range(n):
            currentCity = city
            visitedCity = []
            visitedCity.append(currentCity)
            while len(visitedCity) < n:
                # print(visitedCity)
                probabilityArr = []
                for city in range(len(self.distanceMatrix[currentCity])):
                    if (city in visitedCity):
                        probabilityArr.append(0)
                    else:
                        probabilityArr.append(self.getProbability(currentCity, city, visitedCity))


                nextCity = self.rouletteWheel(probabilityArr)
                # print('current: ', currentCity, 'next: ', nextCity)
                self.deltaPheromone[currentCity][nextCity] += 1 / self.distanceMatrix[currentCity][nextCity]
                currentCity = nextCity
                visitedCity.append(currentCity)

            visitedCity.append(0)

        self.updateGlobalPheromone()
        self.resetDeltaPheromone()

        for iteration in range(1, self.num_iteration):
            # print('iterasi: ', iteration)
            for ant in range(n):
                visitedCity = []
                currentCity = 0
                visitedCity.append(0)
                while len(visitedCity) < n:
                    # print(visitedCity)
                    probabilityArr = []
                    for city in range(len(self.distanceMatrix[currentCity])):
                        if (city in visitedCity):
                            probabilityArr.append(0)
                        else:
                            probabilityArr.append(self.getProbability(currentCity, city, visitedCity))


                    nextCity = self.rouletteWheel(probabilityArr)
                    # print('current: ', currentCity, 'next: ', nextCity)
                    self.deltaPheromone[currentCity][nextCity] += 1 / self.distanceMatrix[currentCity][nextCity]
                    currentCity = nextCity
                    visitedCity.append(currentCity)

                visitedCity.append(0)

            self.updateGlobalPheromone()
            self.resetDeltaPheromone()

        visitedCity = []
        currentCity = 0
        visitedCity.append(0)
        while len(visitedCity) < n:
            # print(visitedCity)
            probabilityArr = []
            for city in range(len(self.distanceMatrix[currentCity])):
                if (city in visitedCity):
                    probabilityArr.append(0)
                else:
                    probabilityArr.append(self.getProbability(currentCity, city, visitedCity))


            nextCity = self.rouletteWheel(probabilityArr)
            # print('current: ', currentCity, 'next: ', nextCity)
            self.deltaPheromone[currentCity][nextCity] += 1 / self.distanceMatrix[currentCity][nextCity]
            currentCity = nextCity
            visitedCity.append(currentCity)

        visitedCity.append(0)

        path = visitedCity
        # print(path)
        for i in range(len(visitedCity) - 1):
            print(self.distanceMatrix[path[i]][path[i+1]])
            cost += self.distanceMatrix[path[i]][path[i+1]]
        '''
        for t=1 to num_iteration do
            for k=1 to ant_count do
                repeat until ant k has completed a tour
                    select the city to be visited next with
                    probability pij
                calculate Lk
            update trail levels
        '''

        return path, cost



if __name__ == "__main__":
    print('Creating distance matrix...')
    distanceMatrix = [[0, 20, 30, 10, 11], [15, 0, 16, 4, 2], [3, 5, 0, 2, 4], [19, 6, 18, 0, 3], [16, 4, 7, 16, 0]]
    # distanceMatrix = [[0, 12, 10, 5], [12, 0, 9, 8], [10, 9, 0, 15], [5, 8, 15, 0]]
    # distanceMatrix = [[[[0, 2, 7, 8], [6, 0, 3, 7], [5, 8, 0, 4], [7, 6, 9, 0]]]]
    
    print(distanceMatrix)

    aco = ACO(10, 1, 1, 0, distanceMatrix)
    path, cost = aco.solve()
    print('Cost: ', cost)
    print('Path: ', path)