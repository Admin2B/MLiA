# -*- encoding: utf-8 -*-
"""
@File    : regTrees.py
@Time    : 2019/10/16 0016 16:51
@Author  : xxx
@Email   : no email
@Software: PyCharm
"""

from numpy import *

def loadDataSet(fileName):
    dataMat=[]
    fr=open(fileName)
    for line in fr.readlines():
        curLine=line.strip().split('\t')
        fltLine=list(map(float,curLine))
        dataMat.append(fltLine)
    return dataMat

def binSplitDataSet(dataSet,feature,value):
    mat0=dataSet[nonzero(dataSet[:,feature]>value)[0],:]
    mat1=dataSet[nonzero(dataSet[:,feature]<=value)[0],:]
    return mat0,mat1

def regLeaf(dataSet):
    return mean(dataSet[:,-1])

def regErr(dataSet):
    return var(dataSet[:,-1])*shape(dataSet)[0]

def chooseBestSplit(dataSet,leafType=regLeaf,errType=regErr,ops=(1,4)):
    tolS=ops[0]
    tolN=ops[1]
    if len(set(dataSet[:,-1].T.tolist()[0] ))==1:
        return None,leafType(dataSet)
    m,n=shape(dataSet)
    S=errType(dataSet)
    bestS=inf
    bestIndex=0
    bestValue=0
    for featIndex in range(n-1):
        #for splitVal in set((dataSet[:, featIndex].T.A.tolist())[0]):
        for splitVal in set((dataSet[:,featIndex].T.A.tolist())[0]):
            mat0,mat1=binSplitDataSet(dataSet,featIndex,splitVal)
            if (shape(mat0)[0]<tolN) or (shape(mat1)[0]<tolN):
                continue
            newS=errType(mat0) + errType(mat1)
            if newS<bestS:
                bestIndex=featIndex
                bestValue=splitVal
                bestS=newS
    if (S-bestS)<tolS:
        return None,leafType(dataSet)
    mat0,mat1=binSplitDataSet(dataSet,bestIndex,bestValue)
    if(shape(mat0)[0]<tolN) or (shape(mat1)[0]<tolN):
        return None,leafType(dataSet)
    return bestIndex,bestValue



def createTree(dataSet, leafType=regLeaf, errType=regErr, ops=(1, 4)):
    feat, val = chooseBestSplit(dataSet, leafType, errType,ops)
    if feat == None:
        return val
    retTree = {}
    retTree['spInd'] = feat
    retTree['spVal'] = val
    lSet, rSet = binSplitDataSet(dataSet, feat, val)
    retTree['left'] = createTree(lSet, leafType, errType, ops)
    retTree['right'] = createTree(rSet, leafType, errType, ops)
    return retTree

def isTree(obj):
    return (type(obj).__name__=='dict')

def getMean(tree):
    if isTree(tree['right']):
        tree['right']=getMean(tree['right'])
    if isTree(tree['left']):
        tree['left'] = getMean(tree['left'])
    return (tree['left']+tree['right'])/2.0

def prune(tree,testData):
    if shape(testData)[0]==0:
        return getMean(tree)
    if (isTree(tree['right']) or isTree(tree['left'])):
        lSet,rSet=binSplitDataSet(testData,tree['spInd'],tree['spVal'])
    if isTree(tree['left']):
        tree['left']=prune(tree['left'],lSet)
    if isTree(tree['right']):
        tree['right'] = prune(tree['right'], rSet)
    if not isTree(tree['left']) and not isTree(tree['right']):
        lSet,rSet=binSplitDataSet(testData,tree['spInd'],tree['spVal'])
        errorNoMerge=sum(power(lSet[:,-1]-tree['left'],2)) + sum(power(rSet[:,-1]-tree['right'],2))
        treeMean=(tree['left']+tree['right'])/2.0
        errorMerge=sum(power(testData[:,-1]-treeMean,2))
        if errorMerge<errorNoMerge:
            print("merging")
            return treeMean
        else:
            return tree
    else:
        return tree

def linearSolve(dataSet):
    m,n=shape(dataSet)
    X=mat(ones((m,n)))
    Y=mat(ones((m,1)))
    X[:,1:n]=dataSet[:,0:n-1]
    Y=dataSet[:,-1]
    xTx=X.T*X
    if linalg.det(xTx)==0.0:
        raise NameError("The matrix is singular, cannot do inverse, try increasing the second value of ops")
    ws=xTx.I*(X.T*Y)
    return ws,X,Y

def modelLeaf(dataSet):
    ws,X,Y=linearSolve(dataSet)
    return ws

def modelErr(dataSet):
    ws,X,Y=linearSolve(dataSet)
    yHat=X*ws
    return sum(power(Y-yHat,2))

def regTreeEval(model,inDat):
    return float(model)

def modelTreeEval(model,inDat):
    n=shape(inDat)[1]
    X=mat(ones((1,n+1)))
    X[:,1:n+1]=inDat
    return float(X*model)

def treeForeCast(tree,inData,modelEval=regTreeEval):
    if not isTree(tree):
        return modelEval(tree,inData)
    if inData[tree['spInd']]>tree['spVal']:
        if isTree(tree['left']):
            return treeForeCast(tree['left'],inData,modelEval)
        else:
            return modelEval(tree['left'],inData)
    else:
        if isTree(tree['right']):
            return treeForeCast(tree['right'],inData,modelEval)
        else:
            return modelEval(tree['right'],inData)

def createForeCast(tree,testData,modelEval=regTreeEval):
    m=len(testData)
    yHat=mat(zeros((m,1)))
    for i in range(m):
        yHat[i,0]=treeForeCast(tree,mat(testData[i]),modelEval)
    return yHat


if __name__=='__main__':
    print("hello")
    # testMat=mat(eye(4))
    # print(testMat)
    # mat0,mat1=binSplitDataSet(testMat,1,0.5)
    # print(mat1)

    # dat=loadDataSet('dataset/sine.txt')
    # datM=mat(dat)
    # print(datM[:,-1].T.tolist())
    # print(set(datM[:-1].T.tolist()[0]))

    # myDat=loadDataSet('dataset/ex00.txt')
    # myMat=mat(myDat)
    # print(createTree(myMat))

    # myDat1=loadDataSet('dataset/ex0.txt')
    # myMat1=mat(myDat1)
    # print(createTree(myMat1))

    # myDat=loadDataSet('dataset/ex00.txt')
    # myMat=mat(myDat)
    # print(createTree(myMat,ops=(0,1)))

    # myDat2=loadDataSet('dataset/ex2.txt')
    # myMat2=mat(myDat2)
    # print(createTree(myMat2))
    # print(createTree(myMat2,ops=(10000,4)))

    # myDatTest=loadDataSet('dataset/ex2test.txt')
    # myDat2=loadDataSet('dataset/ex2.txt')
    # myMat2=mat(myDat2)
    # myTree=createTree(myMat2,ops=(0,1))
    # myMat2Test=mat(myDatTest)
    # print(myTree)
    # print(prune(myTree,myMat2Test))

    # myMat2=mat(loadDataSet('dataset/exp2.txt'))
    # print(createTree(myMat2,modelLeaf,modelErr,(1,10)))

    trainMat=mat(loadDataSet('dataset/bikeSpeedVsIq_train.txt'))
    testMat=mat(loadDataSet('dataset/bikeSpeedVsIq_test.txt'))
    myTree=createTree(trainMat,ops=(1,20))
    yHat=createForeCast(myTree,testMat[:,0])
    print(corrcoef(yHat,testMat[:,1],rowvar=0)[0,1])
    myTree=createTree(trainMat,modelLeaf,modelErr,(1,20))
    yHat=createForeCast(myTree,testMat[:,0],modelTreeEval)
    print(corrcoef(yHat,testMat[:,1],rowvar=0)[0,1])
    ws,X,Y=linearSolve(trainMat)
    print(ws)
    for i in range(shape(testMat)[0]):
        yHat[i]=testMat[i,0]*ws[1,0]+ws[0,0]
    print(corrcoef(yHat,testMat[:,1],rowvar=0)[0,1])









