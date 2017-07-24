import json
import csv
import math

def readCSVFile(fileNameString):
    print fileNameString
    with open(fileNameString,'rb') as csvFile:
        reader = csv.reader(csvFile)
        content = list(reader)
    return content

def getUniqueVocab():
    return readCSVFile('uniqueVocab.csv')

def getPosTestBagOfWords():
    return readCSVFile('posTestBOW.csv')

def getNegTestBagOfWords():
    return readCSVFile('negTestBOW.csv')

def readJson(filename):
    with open(filename) as jsonFile:
        data = json.load(jsonFile)
    return data

def getPriorProbabilityDictionary():
    return readJson('priorProbabilityLaplace0.0001Dictionary.json')

def getWordClassCount():
    return readJson('vocabClassCount.json')

def getNumInstancesInClass(vocabClassCountDictionary, className):
    count = 0
    for key, value in vocabClassCountDictionary.iteritems():
        count += value[className]
    print count
    return count

def getLogPosterior(wordString, className, classProb, classCount, priorProbabilityDictionary):
    if wordString in priorProbabilityDictionary:
        return math.log(priorProbabilityDictionary[wordString][className]*classProb)
    else:
        return math.log(0.0001/float(len(priorProbabilityDictionary)*0.0001+classCount)*classProb)

def getClassProb(vocabClassCountDictionary, className):
    countClass = 0
    countNotClass = 0
    for key, value in vocabClassCountDictionary.iteritems():
        for cl, count in value.iteritems():
            if cl == className:
                countClass += count
            else:
                countNotClass += count

    # print count
    return countClass/float(countClass + countNotClass)

def classify(bagOfWords, negClassProb, posClassProb, priorProbabilityDictionary):
    posLogProbability = 0
    negLogProbability = 0
    posCount = 5590615
    negCount = 5561198
    for word in bagOfWords:
        # print word
        posLogProbability += getLogPosterior(word, 'pos', posClassProb, posCount, priorProbabilityDictionary)
        negLogProbability += getLogPosterior(word, 'neg', negClassProb, negCount, priorProbabilityDictionary)
    if posLogProbability > negLogProbability:
        return 'pos'
    else:
        return 'neg'

negBagsOfWords = getNegTestBagOfWords()
posBagsOfWords = getPosTestBagOfWords()
negClassProb = getClassProb(getWordClassCount(), 'neg')
posClassProb = getClassProb(getWordClassCount(), 'pos')
priorProbabilityLaplace1Dictionary = getPriorProbabilityDictionary()
trueNeg = 0
falsePos = 0
truePos = 0
falseNeg = 0
for bag in negBagsOfWords:
    if classify(bag, negClassProb, posClassProb, priorProbabilityLaplace1Dictionary) == 'neg':
        trueNeg += 1
    else:
        falsePos += 1

for bag in posBagsOfWords:
    if classify(bag, negClassProb, posClassProb, priorProbabilityLaplace1Dictionary) == 'pos':
        truePos += 1
    else:
        falseNeg += 1

print trueNeg, falsePos, truePos, falseNeg
#
# print classify(getNegTestBagOfWords()[5], getClassProb(getWordClassCount(), 'neg'), getClassProb(getWordClassCount(), 'pos'), getPriorProbabilityDictionary())
