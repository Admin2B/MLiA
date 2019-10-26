# -*- encoding: utf-8 -*-
"""
@File    : mrMeanMapper.py
@Time    : 2019/10/26 0026 18:24
@Author  : xxx
@Email   : no email
@Software: PyCharm
"""
import sys
from numpy import mat,mean,power

def read_input(file):
    for line in file:
        yield line.rstrip()

if __name__=='__main__':
    input=read_input(sys.stdin)
    input=[float(line) for line in input]
    numInputs=len(input)
    input=mat(input)
    sqInput=power(input,2)
    print("%d\t%f\t%f"%(numInputs,mean(input),mean(sqInput)))
    # print >> sys.stderr,"report:still alive"
