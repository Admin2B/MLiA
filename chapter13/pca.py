# -*- encoding: utf-8 -*-
"""
@File    : pca.py
@Time    : 2019/10/25 0025 16:38
@Author  : xxx
@Email   : no email
@Software: PyCharm
"""
from numpy import *

def loadDataSet(fileName,delim='\t'):
    fr=open(fileName)
    stringArr=[line.strip().split(delim) for line in fr.readlines()]
    datArr=[list(map (float,line)) for line in stringArr]
    return mat(datArr)

def pac(dataMat,topNfeat=9999999):
    meanVals=mean(dataMat,axis=0)
    meanRemoved=dataMat-meanVals
    conMat=cov(meanRemoved,rowvar=0)
    eigVals,eigVects=linalg.eig(mat(conMat))
    eigValInd=argsort(eigVals)
    eigValInd=eigValInd[:-(topNfeat+1):-1]
    redEigVects=eigVects[:,eigValInd]
    lowDDataMat=meanRemoved*redEigVects
    reconMat=(lowDDataMat*redEigVects.T)+meanVals
    return lowDDataMat,reconMat

def replaceNanWithMean():
    datMat=loadDataSet('dataset/secom.data',' ')
    numFeat=shape(datMat)[1]
    for i in range(numFeat):
        meanVal=mean(datMat[nonzero(~isnan(datMat[:,i].A))[0],i])
        datMat[nonzero(isnan(datMat[:,i].A))[0],i]=meanVal
    return datMat


if __name__=='__main__':
    print("hello world")
    # dataMat=loadDataSet('dataset/testSet.txt')
    # lowDMat,reconMat=pac(dataMat,1)
    # print(shape(lowDMat))
    # import matplotlib
    # import matplotlib.pyplot as plt
    # fig=plt.figure()
    # ax=fig.add_subplot(111)
    # ax.scatter(dataMat[:,0].flatten().A[0],dataMat[:,1].flatten().A[0],marker='^',s=90)
    # ax.scatter(reconMat[:,0].flatten().A[0],reconMat[:,1].flatten().A[0],marker='o',s=50,c='red')
    # plt.show()

    dataMat=replaceNanWithMean()
    meanVals=mean(dataMat,axis=0)
    meanRemoved=dataMat-meanVals
    covMat=cov(meanRemoved,rowvar=0)
    eigVals,eigVects=linalg.eig(mat(covMat))
    print(eigVals)

