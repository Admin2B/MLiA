from numpy import  *
import operator

def createDataSet():
    group=array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels=['A','A','B','B']
    return group,labels

def classify0(inX,dataSet,labels,k):
    dataSetSize=dataSet.shape[0]  #训练数目
    diffMat=tile(inX,(dataSetSize,1))-dataSet  #对应距离相减
    sqDiffMat=diffMat**2  #平方和
    sqDistances=sqDiffMat.sum(axis=1) #行求和
    distances=sqDistances**0.5 #开方
    sortedDistIndicies=distances.argsort()  #数据按照从小到大的顺序进行排序，排的是下标
    classCount={}
    for i in range (k):  #前K个近邻循环
        voteIlabel=labels[sortedDistIndicies[i]]  #K近邻标签
        classCount[voteIlabel]=classCount.get(voteIlabel,0)+1 #统计标签数目
    sortedClassCount=sorted(classCount.items(),key=operator.itemgetter(1),reverse=True) #排序
    return sortedClassCount[0][0]

def file2matrix(filename):
    fr=open(filename)
    arrayOLines=fr.readlines()
    numberOfLines=len(arrayOLines)
    returnMat=zeros((numberOfLines,3))
    classLabelVector=[]
    index=0
    for line in arrayOLines:
        line=line.strip()
        listFromLine=line.split('\t')
        returnMat[index,:]=listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index += 1
    return returnMat,classLabelVector

def autoNorm(dataSet):
    minValue=dataSet.min(0)
    maxValue=dataSet.max(0)
    ranges=maxValue-minValue
    normDataSet=zeros(shape(dataSet))
    m=dataSet.shape[0]
    normDataSet=dataSet-tile(minValue,(m,1))
    normDataSet=normDataSet/tile(ranges,(m,1))
    return normDataSet,ranges,minValue

def datingClassTest():
    hoRatio=0.10
    datingDataMat,datingLabels=file2matrix('datingTestSet2.txt')
    normMat,ranges,minValue=autoNorm(datingDataMat)
    m=normMat.shape[0]
    numTestVecs=int(m*hoRatio)
    errCount=0.0
    for i in range (numTestVecs):
        classifierResult=classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)
        print("the classifier came back with %d, the real answer is: %d" %(classifierResult,datingLabels[i]))
        if (classifierResult!=datingLabels[i]):
            errCount +=1.0
    print("the total error rate is: %f"%(errCount/float(numTestVecs)))

def classifyPerson():
    resultList=['not at all','in small does','in large does']
    percentTats=float(input("Percentage of time spent playing videos games ?\n"))
    ffMiles=float(input("frequent flier miles earned per years ?\n"))
    iceCream=float(input("liters of ice cream consumed per year ?\n"))
    datingDataMat,datingLabels=file2matrix('datingTestSet2.txt')
    normMat,ranges,minValues=autoNorm(datingDataMat)
    inArr=array([ffMiles,percentTats,iceCream])
    classifierResult=classify0((inArr-minValues)/ranges,normMat,datingLabels,3)
    print ("You will probably like this person: ",resultList[classifierResult-1])

def img2vector(filename):
    returnVect=zeros((1,1024))
    fr=open(filename)
    for i in range(32):
        lineStr=fr.readline()
        for j in range(32):
            returnVect[0,32*i+j]=int(lineStr[j])
    return returnVect


def handwritingClassTest():
    from os import listdir
    hwLabels=[]
    trainingFileList=listdir('trainingDigits')
    m=len(trainingFileList)
    trainingMat=zeros((m,1024))
    for i in range (m):
        fileNameStr=trainingFileList[i]
        fileStr=fileNameStr.split('.')[0]
        classNumStr=int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i,:]=img2vector('trainingDigits/%s'%fileNameStr)
    testFileList=listdir('testDigits')
    errorCount=0.0
    mTest=len(testFileList)
    for i in range(mTest):
        fileNameStr=testFileList[i]
        fileStr=fileNameStr.split('.')[0]
        classNumStr=int(fileStr.split('_')[0])
        vectorUnderTest=img2vector('testDigits/%s'%fileNameStr)
        classifierResult=classify0(vectorUnderTest,trainingMat,hwLabels,3)
        print("the classifier came back with:%d, the real answer is:%d"%(classifierResult,classNumStr))
        if (classifierResult!=classNumStr):
            errorCount +=1
    print("\nthe total number of errors is:%d"%errorCount)
    print("\nthe total errir rate is:%f"%(errorCount/float(mTest)))





if __name__=='__main__':

    # group, labels = createDataSet()
    # print(classify0([0.1,0.05],group,labels,3))


    datingDataMat,datingLabels=file2matrix('datingTestSet2.txt')
    # import matplotlib
    # import matplotlib.pyplot as plt
    # fig=plt.figure()
    # ax=fig.add_subplot(111)
    # ax.scatter(datingDataMat[:,1],datingDataMat[:,2],10.0*array(datingLabels),10.0*array(datingLabels))
    # plt.xlabel("游戏占比百分数")
    # plt.ylabel("每周冰激凌消耗升数")
    # ax.scatter(datingDataMat[:,0],datingDataMat[:,1],10.0*array(datingLabels),10.0*array(datingLabels))
    # plt.xlabel("飞行里程")
    # plt.ylabel("游戏占比百分数")
    # plt.show()

    # datingClassTest()

    # classifyPerson()

    handwritingClassTest()

