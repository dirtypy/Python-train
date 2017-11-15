#!/usr/bin/python3
#coding=gbk

'''
naive bayes ?���ر�Ҷ˹
@author: sean
@since 2017-05-31
'''

from imp import reload

from numpy import *

# ����׼������
def loadDataSet():
    postingList=[
        ['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
        ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
        ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
        ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
        ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
        ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']
    ]
    classVec=[0,1,0,1,0,1] # 0 ��ʾ ������������ 1 ��ʾ ������������
    return postingList,classVec

# �������ڹ����ֵ� ���ֵ��ڵĵ��ʲ��ظ���
def createVocabList(dataSet):
    vocabSet=set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)
    # return vocabSet

# ��ʶ���ʳ��ֵĴ���
def setOfWords2Vec(vocabList,inputSet):
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
            # returnVec[vocabList.index(word)]=1
        else: print "the word : %s is not in my Vocabulary! " %word
    return returnVec

# ���ر�Ҷ˹ ѵ������
# p0Vec p1Vec �� �����赥������ / ���赥������ pAbusive �����������������ĸ���
def trainNB0(trainMatrix,trainCategory):
    numTrainDocs = len(trainMatrix) # ��ȡ��������
    numWords = len(trainMatrix[0]) # ��ΪtrainMatrix ���� ������ ���� ά�ȶ���һ����
    pAbusive = sum(trainCategory)/float(numTrainDocs) # sum([1,0])/len([1,0])  1/2 �����ĵ��ڰ������赥�ʵĸ���
    p0Num = zeros(numWords); p1Num = zeros(numWords)
    p0Denom = 0.0 ; p1Denom = 0.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1 :
            p1Num += trainMatrix[i] # �������
            p1Denom += sum(trainMatrix[i]) # ��¼�����ĵ��ʸ���
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p1Vec = p1Num/p1Denom
    p0Vec = p0Num/p0Denom
    return p0Vec,p1Vec,pAbusive


