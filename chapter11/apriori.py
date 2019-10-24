# -*- encoding: utf-8 -*-
"""
@File    : apriori.py
@Time    : 2019/10/20 0020 17:25
@Author  : xxx
@Email   : no email
@Software: PyCharm
"""

def loadDataSet():
    return [[1,3,4],[2,3,5],[1,2,3,5],[2,5]]

def createC1(dataSet):
    C1=[]
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return list(map(frozenset,C1))
    # return [frozenset(var) for var in C1]

def scanD(D,Ck,minSupport):
    ssCnt={}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if can not in ssCnt:
                    ssCnt[can]=1
                else:
                    ssCnt[can] += 1
    numItems=float(len(D))
    retList=[]
    supportData={}
    for key in ssCnt:
        support=ssCnt[key]/numItems
        if support>=minSupport:
            retList.insert(0,key)
        supportData[key]=support
    return retList,supportData

def aprioriGen(Lk,k):
    retList=[]
    lenLk=len(Lk)
    for i in range(lenLk):
        for j in range(i+1,lenLk):
            L1=list(Lk[i])[:k-2]
            L2=list(Lk[j])[:k-2]
            L1.sort()
            L2.sort()
            if L1==L2:
                retList.append(Lk[i]|Lk[j])
    return retList

def apriori(dataSet,minSupport=0.5):
    C1=createC1(dataSet)
    D=list(map(set,dataSet))
    L1,supportData=scanD(D,C1,minSupport)
    L=[L1]
    k=2
    while (len(L[k-2])>0):
        Ck=aprioriGen(L[k-2],k)
        Lk,supK=scanD(D,Ck,minSupport)
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L,supportData

def generateRules(L,supportData,minConf=0.7):
    bigRuleList=[]
    for i in range(1,len(L)):
        for freqSet in L[i]:
            H1=[frozenset([item]) for item in freqSet]
            if (i>1):
                rulesFromConseq(freqSet,H1,supportData,bigRuleList,minConf)
            else:
                calcConf(freqSet,H1,supportData,bigRuleList,minConf)
    return bigRuleList

def calcConf(freqSet,H,supportData,br1,minConf=0.7):
    prunedH=[]
    for conseq in H:
        conf=supportData[freqSet]/supportData[freqSet-conseq]
        if conf>=minConf:
            print(freqSet-conseq,"--->",conseq,"conf:",conf)
            br1.append((freqSet-conseq,conseq,conf))
            prunedH.append(conseq)
    return prunedH





def rulesFromConseq(freqSet,H,supportData,br1,minConf=0.7):
    m=len(H[0])
    if (len(freqSet))>m+1:
        Hmp1=aprioriGen(H,m+1)
        Hmp1=calcConf(freqSet,Hmp1,supportData,br1,minConf)
        if (len(Hmp1)>1):
            rulesFromConseq(freqSet,Hmp1,supportData,br1,minConf)

# https://blog.csdn.net/zoinsung_lee/article/details/80199817
from time import sleep
from votesmart import votesmart
def getTransList(actionIdList,billTitleList):
    itemMeaning=['Republican','Democratic']
    for billTitle in billTitleList:
        itemMeaning.append('%s -- Nay'%billTitle)
        itemMeaning.append('%s -- Yea'%billTitle)
    transDict={}
    voteCount=2
    for actionId in actionIdList:
        sleep(3)
        print("getting votes for actionId: %d"%actionId)
        try:
            voteList=votesmart.votes.getBillActionVotes(actionId)
            for vote in voteList:
                if not transDict.has_key(vote.candidateName):
                    transDict[vote.candidateName]=[]
                    if vote.officeParties=='Democratic':
                        transDict[vote.candidateName].append(1)
                    elif vote.officeParties=='Republican':
                        transDict[vote.candidateName].append(0)
                if vote.action=='Nay':
                    transDict[vote.candidateName].append(voteCount)
                elif vote.action=='Yea':
                    transDict[vote.candidateName].append(voteCount+1)
        except:
            print("problem getting actionId: %d"%actionId)
        voteCount+=2
    return transDict,itemMeaning



if __name__=='__main__':
    print("hello world")
    dataSet=loadDataSet()
    # C1=createC1(dataSet)
    # print(C1)
    # D=list(map(set,dataSet))
    # print(D)
    # L1,supportData0=scanD(D,C1,0.5)
    # print(L1)

    # L,suppData=apriori(dataSet)
    # print(L)
    # print(L[0])
    # print(aprioriGen(L[0],2))
    # L,suppData=apriori(dataSet,minSupport=0.7)
    # print(L)

    # L,supportData=apriori(dataSet,minSupport=0.5)
    # print(generateRules(L,supportData,minConf=0.7))
    # print(generateRules(L, supportData, minConf=0.5))

    mushDatSet=[line.split() for line in open('dataset/mushroom.dat').readlines()]
    L,sippoerData=apriori(mushDatSet,minSupport=0.3)
    for item in L[1]:
        if item.intersection('2'):
            print(item)
    for item in L[3]:
        if item.intersection('2'):
            print(item)



