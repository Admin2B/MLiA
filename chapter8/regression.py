# -*- encoding: utf-8 -*-
"""
@File    : regression.py
@Time    : 2019/10/8 0008 19:17
@Author  : xxx
@Email   : no email
@Software: PyCharm
"""
from numpy import *

def loadDataSet(filename):
    numFeat=len(open(filename).readline().split('\t'))-1
    dataMat=[]
    labelMat=[]
    fr=open(filename)
    for line in fr.readlines():
        lineArr=[]
        curLine=line.strip().split('\t')
        for i in range(numFeat):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        labelMat.append(float(curLine[-1]))
    return dataMat,labelMat

def standRegres(xArr,yArr):
    xMat=mat(xArr)
    yMat=mat(yArr).T
    xTx=xMat.T*xMat
    if linalg.det(xTx)==0.0:
        print("This matrix is singular, cannot do inverse")
        return
    ws=xTx.I*(xMat.T*yMat)
    return ws

def lwlr(testPoint,xArr,yArr,k=1.0):
    xMat=mat(xArr)
    yMat=mat(yArr).T
    m=shape(xMat)[0]
    weights=mat(eye(m))
    for j in range(m):
        diffMat=testPoint-xMat[j,:]
        weights[j,j]=exp(diffMat*diffMat.T/(-2.0*k**2))
    xTx=xMat.T*(weights*xMat)
    if linalg.det(xTx)==0.0:
        print("This matrix is singular, cannot do inverse")
        return
    ws=xTx.I*(xMat.T*(weights*yMat))
    return testPoint*ws

def lwlrTest(testArr,xArr,yArr,k=1.0):
    m=shape(testArr)[0]
    yHat=zeros(m)
    for i in range(m):
        yHat[i]=lwlr(testArr[i],xArr,yArr,k)
    return yHat

def rssError(yArr,yHatArr):
    return ((yArr-yHatArr)**2).sum()

def ridgeRegres(xMat,yMat,lam=0.2):
    xTx=xMat.T*xMat
    denom=xTx+eye(shape(xMat)[1])*lam
    if linalg.det(denom)==0.0:
        print("This matrix is singular, cannot inverse.")
        return
    ws = denom.I * (xMat.T * yMat)
    return ws

def ridgeTest(xArr,yArr):
    xMat=mat(xArr)
    yMat=mat(yArr).T
    yMean=mean(yMat,0)
    yMat=yMat-yMean
    xMeans=mean(xMat,0)
    xVar=var(xMat,0)
    xMat=(xMat-xMeans)/xVar
    numTestPts=30
    wMat=zeros((numTestPts,shape(xMat)[1]))
    for i in range(numTestPts):
        ws=ridgeRegres(xMat,yMat,exp(i-10))
        wMat[i,:]=ws.T
    return wMat

def regularize(xMat):
    inMat = xMat.copy()
    inMeans = mean(inMat,0)
    inVar = var(inMat,0)
    inMat = (inMat - inMeans)/inVar
    return inMat

def stageWise(xArr,yArr,eps=0.01,numIt=100):
    xMat=mat(xArr)
    yMat=mat(yArr).T
    yMean=mean(yMat,0)
    yMat=yMat-yMean
    xMat=regularize(xMat)
    m,n=shape(xMat)
    returnMat=zeros((numIt,n))
    ws=zeros((m,1))
    wsTest=ws.copy()
    wsMax=ws.copy()
    for i in range(numIt):
        print(ws.T)
        lowestError=inf
        for j in range(n):
            for sign in [-1,1]:
                wsTest=ws.copy()
                wsTest[j] += eps*sign
                yTest=xMat*wsTest
                rssE=rssError(yMat.A,yTest.A)
                if rssE<lowestError:
                    lowestError=rssE
                    wsMax=wsTest
        ws=wsMax.copy()
        returnMat[i,:]=ws.T
    return returnMat






if __name__=="__main__":
    # xArr,yArr=loadDataSet('ex0.txt')
    #xMat=mat(xArr)
    # yMat=mat(yArr)
    # yHat=xMat*ws
    # import matplotlib.pyplot as plt
    # fig=plt.figure()
    # ax=fig.add_subplot(111)
    # ax.scatter(xMat[:,1].flatten().A[0],yMat.T[:,0].flatten().A[0]) ## .flatten().A[0] 矩阵展开变一维numpy.ndarray
    # xCopy=xMat.copy()
    # xCopy.sort(0)
    # yHat=xCopy*ws
    # ax.plot(xCopy[:,1],yHat)
    # plt.show()

    # yHat=xMat*ws
    # a=corrcoef(yHat.T,yMat)
    # print(a)
    #


    # yHat=lwlrTest(xArr,xArr,yArr,0.02)
    # xMat=mat(xArr)
    # srtInd=xMat[:,1].argsort(0)
    # xSort=xMat[srtInd][:,0,:]
    # import matplotlib.pyplot as plt
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax.plot(xSort[:,1],yHat[srtInd])
    # ax.scatter(xMat[:,1].flatten().A[0],mat(yArr).T.flatten().A[0],s=2,c='red')
    # plt.show()

    # abX,abY=loadDataSet('abalone.txt')
    # abX=mat(abX)
    # abY=mat(abY)
    # ridgeWeights=ridgeTest(abX,abY)
    # import matplotlib.pyplot as plt
    # fig=plt.figure()
    # ax=fig.add_subplot(111)
    # ax.plot(ridgeWeights)
    # plt.show()

    print("hello")














