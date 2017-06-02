#!/usr/bin/python3
#coding=gbk

'''
ID3
@author: sean
@since 2017-05-31
'''

from math import log
import  operator

# ���ɲ���ʹ�õ�dataSet
def createDataSet():
    dataSet = [[1,1,'yes'],
               [1,1,'yes'],
               [1,0,'no'],
               [0,1,'no'],
               [0,1,'no']]
    labels = ['no surfacing','flippers']
    return dataSet, labels

# �� Entropy
# ������ũ�صĹ�ʽ �����ص�ֵ
def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    # ͳ��ÿ������ֵ���ֵĴ���
    for featVec in dataSet:
        currentLabels = featVec[-1]
        if currentLabels not in labelCounts.keys():
            labelCounts[currentLabels] = 0
        labelCounts[currentLabels] += 1
    shannonEnt = 0.0
    # ���ݹ�ʽ������ũ�ص�ֵ
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob * log(prob,2)
    return shannonEnt

# �������ݼ�
# ���ǽ� axis��Ϊvalue�Ķ����ȡ���� ��Ϊһ����������س���
def splitDataSet(dataSet,axis,value):
    resultDataSet=[]
    for featVec in dataSet:
        if featVec[axis] == value:
            # ������������Ժϳ�һ�� ����д���Ը����� ��߽���axis �е�ֵɾ���ˣ�
            tmpDataSet = featVec[:axis]
            tmpDataSet.extend(featVec[axis+1:])
            resultDataSet.append(tmpDataSet)
    return resultDataSet

# ѡ����õ����ݼ����ַ�ʽ
def chooseBeastFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1 # ǰ�������������� ���һ���Ǿ�������
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0 ; bestFeatures = -1;
    # range(num) Ϊ [0,1,2,3,...]
    for i in range(numFeatures):
        featList = [example[i]  for example in dataSet ] # for example in dataSet : featList = example[i] ÿ�������ĵ�i�ж���ֵ��featList
        uniqueVals = set(featList) # ȥ���ظ��ģ�����Ωһ������
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet,i,value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob*calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        if(infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeatures = i
    return bestFeatures

# ѡ�ٳ������Ŀ ����һ��(���� ���ִ�������һ��� ����)
def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.items(),key = operator.itemgetter(1),reverse = True)
    return sortedClassCount[0][0]

# ������ ��Ҳ���Ǵ���һ����������������(һ���������� ÿ��ѡȡ�� ������ ��Ҫ���������� �� �����������������Ŀ����� ���з���)
def createTree(dataSet,labels):
    classList = [example[-1] for example in dataSet ] # ���������������һ�и�ֵ�� classList����
    if classList.count(classList[0]) == len(dataSet):
        return classList[0] # ������е�����ǩ����ͬ ��ô�� �����ټ���������
    if len(dataSet[0])==1:
        return majorityCnt(dataSet) # ��� ֻ��һ�������� ��ôʹ�� ������������ԭ�� ����ѡ��
    # ѡ��� ����Ҫ������
    bestFeat = chooseBeastFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    # �������Ľ�� ɾ���Ѿ�ʹ�ù���ı�ǩ
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues) # ͨ��set���� ����Ψһ��
    for value in uniqueVals:
        subLables = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet,bestFeat,value),subLables)
    return myTree

# ���л��� �������浽����
def storeTree(inputTree,filename):
    import  pickle
    fw = open(filename,'w')
    pickle.dump(inputTree,fw)
    fw.close()

# ��ȡ�ļ����㱣������νṹ
def grabTree(filename):
    import  pickle
    fr = open(filename)
    return pickle.load(fr)

# ��ʵ����д�е����⣬�Ǿ��ǵ��ж� ������ ����������ϵ�ʱ�� ���µĲ��������޷���ֵ
# ���ڽ���ж�˳��������� ��������ճ�����
def classify(inputTree,featLabels,testVec):
    firstStr = inputTree.keys()[0] # ��ȡ������ַ���
    secondDict = inputTree[firstStr] # ��ȡ���ĸ��ڵ�
    featIndex = featLabels.index(firstStr) # ��ȡ �ַ��������ڲ����������к�
    for key in secondDict.keys():
        # �жϲ������� ���� ����������һ��
        if key == testVec[featIndex]:
            if type(secondDict[key]).__name__ == 'dist': # ͨ���ж� ���Ƿ�Ϊ �ֵ��������� �ж��Ƿ�Ϊ���ڵ� / Java�ڿ����ж� ������ �Ƿ�Ϊ�ս����ж��Ƿ�Ϊ�����
                channelLabel = classify(secondDict[key],featLabels,testVec)
            else:
               # channelLabel = key
                channelLabel = secondDict[key]
    return channelLabel









