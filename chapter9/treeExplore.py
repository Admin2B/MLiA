# -*- encoding: utf-8 -*-
"""
@File    : treeExplore.py
@Time    : 2019/10/16 0016 22:02
@Author  : xxx
@Email   : no email
@Software: PyCharm
"""
from tkinter import *
import regTrees
from numpy import *
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def reDraw(tolS,tolN):
    reDraw.f.clf()
    reDraw.a=reDraw.f.add_subplot(111)
    if chkBtnVar.get():
        if tolN<2:
            tolN=2
        myTree=regTrees.createTree(reDraw.rawDat,regTrees.modelLeaf,regTrees.modelErr,(tolS,tolN))
        yHat=regTrees.createForeCast(myTree,reDraw.testDat,regTrees.modelTreeEval)
    else:
        myTree=regTrees.createTree(reDraw.rawDat,ops=(tolS,tolN))
        yHat=regTrees.createForeCast(myTree,reDraw.testDat)
    reDraw.a.scatter(array(reDraw.rawDat[:,0]),array(reDraw.rawDat[:,1]),s=5)
    reDraw.a.plot(reDraw.testDat,yHat,linewidth=2.0)
    reDraw.canvas.draw()

def getInputs():
    try:
        tolN=int(tolNentry.get())
    except:
        tolN=10
        print("Enter Integer for tolN")
        tolNentry.delete(0,END)
        tolNentry.insert(0,'10')
    try:
        tolS=float(tolSentry.get())
    except:
        tolS=1.0
        print("Enter float for tolS")
        tolSentry.delete(0,END)
        tolSentry.insert(0,'1.0')
    return tolN,tolS

def drawNewTree():
    tolN,tolS=getInputs()
    reDraw(tolS,tolN)


if __name__=='__main__':
    print("hello world")
    root=Tk()
    reDraw.f=Figure(figsize=(5,4),dpi=100)
    #reDraw.canvas=FigureCanvasAgg(reDraw.f,master=root)
    reDraw.canvas = FigureCanvasTkAgg(reDraw.f, master=root)
    reDraw.canvas.draw()
    reDraw.canvas.get_tk_widget().grid(row=0,columnspan=3)

    #Label(root,text="Plot Place Holder").grid(row=0,columnspan=3)

    Label(root,text="tolN").grid(row=1,column=0)
    tolNentry=Entry(root)
    tolNentry.grid(row=1,column=1)
    tolNentry.insert(0,'10')
    Label(root,text="tolS").grid(row=2,column=0)
    tolSentry=Entry(root)
    tolSentry.grid(row=2,column=1)
    tolSentry.insert(0,'1.0')
    Button(root,text="ReDraw",command=drawNewTree).grid(row=1,column=2,rowspan=3)
    chkBtnVar=IntVar()
    chkBtn=Checkbutton(root,text="Model Tree",variable=chkBtnVar)
    chkBtn.grid(row=3,column=0,columnspan=2)
    reDraw.rawDat=mat(regTrees.loadDataSet('dataset/sine.txt'))
    reDraw.testDat=arange(min(reDraw.rawDat[:,0]),max(reDraw.rawDat[:,0]),0.01)
    reDraw(1.0,10)
    root.mainloop()


