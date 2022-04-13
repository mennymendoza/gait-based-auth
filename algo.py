import math
import numpy as np
import pandas as pd
from scipy.signal import argrelextrema
from operator import itemgetter
import itertools

"""
current issues - iterator in likecheck is messed up
indexing in minpull is messed up
need to figure out where to go next
its really slow
"""


df = pd.read_csv(r'C:\Users\drpra\OneDrive\Desktop\RAstuffs\user2handacc.csv')
dfy = pd.DataFrame(df,columns = ['Yvalue'])
dfy = dfy.apply(np.square)
dfy = dfy.apply(np.sqrt)
l = len(df.index)
c = int(l/2)
N = 100
start = int(c - N/2)
end = int(c + N/2 - 1)
nlist1 = dfy[start:end]

def distance(x1,x2,y1,y2):
    foo1 = np.square(x2-x1)
    foo2 = np.square(y2-y1)
    return np.sqrt(foo1+foo2)
def indexgetter(listname,val):
    temp = listname.index.values[(listname['Yvalue'] >= val - 0.0000000001) & (listname['Yvalue'] <= val + 0.0000000001)]
    return temp[0]
def likecheck(df2):
    vals = []
    indexes = []
    for index, row1 in nlist1.iterrows():
        vals.append(1000000000)
        indexes.append(1)
        for j, row2 in df2.iterrows():
            if (distance(indexgetter(nlist1,row1['Yvalue']),row1['Yvalue'],indexgetter(df2,row2['Yvalue']),row2['Yvalue'])) < vals[len(vals) - 1]:
                vals[len(vals) - 1] =  distance(indexgetter(nlist1,row1['Yvalue']),row1['Yvalue'],indexgetter(df2,row2['Yvalue']),row2['Yvalue'])
                indexes[len(indexes) - 1] = indexgetter(df2,row2['Yvalue'])
    return vals,indexes
def minpull(outvals):
    for i in range(1,20):
        if i % 2 != 0:
            looker = outvals[i]
            val, idx = min((val, idx) for (idx, val) in enumerate(looker))
            print(idx)
"""
take the indexes and values check if similar then build cycledetector
"""

def runprocess():
    scndstart = 0
    otuple = (0,)
    for i in range (1,6):
        scndstart = (start - (100*i))
        nlist2 = dfy[scndstart : int(scndstart + N - 1)]
        otuple = otuple + likecheck(nlist2)
    for i in range(1,6):
        print('we made it once!')
        scndstart = (end + (100*i)) + 1
        nlist2 = dfy[scndstart : int(scndstart + N - 1)]
        otuple = otuple + likecheck(nlist2)
    print(otuple[1])
    minpull(otuple)
    


runprocess()

