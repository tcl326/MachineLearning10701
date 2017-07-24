import gen_synthetic as synthData
import math
import numpy as np
from operator import itemgetter

def getData(n, p, sigma):
    X,Y = synthData.gen_synthetic(n,p,sigma)
    data = np.concatenate((X,Y),axis=1)
    nData = np.split(data,10)
    return nData

def euclideanDistance(sample1, sample2, dimensionality):
    distance = 0
    for x in range(dimensionality):
        distance += (sample1[x]-sample2[x])**2
    return math.sqrt(distance)

def getNeighbours(trainingSet, testingSample, k):
    distances = []
    neighbours = []
    dimensionality = len(testingSample)-1
    for x in trainingSet:
        dist = euclideanDistance(testingSample,x,dimensionality)
        distances.append((x,dist))
    sortedByDist = sorted(distances,key=itemgetter(1))
    for i in range(k):
        neighbours.append(sortedByDist[i][0])
    return neighbours

def getDecision(neighbours):
    voteDict = {}
    for x in neighbours:
        response = x[-1]
        if response in voteDict:
            voteDict[response] += 1
        else:
            voteDict[response] = 1
    sortedVote = sorted(voteDict.items(), key=itemgetter(1))
    return sortedVote[-1][0]

def getAccuracy(predictions, data):
    return np.sum(np.equal(predictions,data[:,-1]))/float(len(predictions))*100

def main():
    predictions=[]
    n = 1000
    p = 10
    sigma = 0.001
    k = 50;
    data = getData(n,p,sigma)
    for i in range(len(data)):
        testingSet = data[i]
        trainingSet = np.vstack([data[x] for x in range(len(data)) if x!=i])
        for j in testingSet:
            neighbours = getNeighbours(trainingSet,j,k)
            result = getDecision(neighbours)
            predictions.append(result)
            print ('predicted=' + str(result) + ', actual=' + str(j[-1]))
    print getAccuracy(predictions,np.vstack(data))


    # print euclideanDistance([2,2],[1,1],len([2,2]))

main()

# trainSet = [[2, 2, 2, 'a'], [4, 4, 4, 'b']]
# testInstance = [5, 5, 5]
# k = 1
# neighbors = getNeighbours(trainSet, testInstance, 1)
# print(neighbors)
