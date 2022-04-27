"""
Notes:
 make sure to rename variables to be more descriptive of what they are and add some comments so future us doesnt get lost
 finish subcyclegenerator  
 
 """


import math
import numpy as np
import pandas as pd
from scipy import stats
#Constants
N = 100

def distance(y1,y2):
    d = np.sqrt((y2-y1)**2)
    return d

def handler(reference,window): #finds the euclidian distance between points at corresponding indexes and returns a list of the lowest distances
    holdvals = np.empty(0,int)
    x = 0
    for i in range(0,len(window) - 1):
        temp = window[i]
        dist = float(distance(reference[0],temp[0]))
        for j in range(0,N-2):
            if (float(distance(reference[j],float(temp[j]))) < dist):
                dist = float(distance(reference[j],temp[j]))
                x = j
        holdvals = np.append(holdvals,x)
    return holdvals

def minfinder(arr): #finds the mode of data from handler
    minvals = np.empty(0,int)
    for i in range(0, len(arr) - 2):
        minvals = np.append(minvals,(N - 1 -(arr[i] - arr[i + 1])))
    temp = stats.mode(minvals)
    if pd.isna(temp[0]):
        return int(sum(minvals)/len(minvals))
    else:
        return int(temp[0])

def segmentation(df,clen): #returns segmented data
    holder = pd.DataFrame(df,columns = ['Xvalue','Yvalue','Zvalue']).to_numpy()
    total = int(len(holder)/clen)
    na = np.array_split(holder,total)
    return na

def dynamcyclegenerator(file): #runs entire process
    df = pd.read_csv(rf'raw-data/{file}.csv')
    dfy = pd.DataFrame(df,columns = ['Yvalue']).to_numpy()
    dfy = np.square(dfy)
    dfy = np.sqrt(dfy)
    L = len(df.index)
    C = int(L/2)
    Start = C - int(N/2)
    End = C + int(N/2) - 1
    reference = dfy[Start:End]
    x = dfy[0:Start - 1]
    Lh = np.array_split(x,int(len(x)/(N-1)))
    x = dfy[End+1: L]
    Rh = np.array_split(x,int(len(x)/(N-1)))
    z = (handler(reference,Lh))
    z = np.append(z,handler(reference,Rh))
    z = minfinder(z)
    return segmentation(df,z)

def manualcyclegenerator(file,len):
    df = pd.read_csv(rf'raw-data{file}.csv')
    return segmentation(df,len)


def subclegenerator(file,timestamps):
    df = pd.read_csv(rf'raw-data/{file}.csv')
    times = pd.read_csv(rf'raw-data/{timestamps}.csv')
    calls = len(times)
    for i in range(calls -1):
        start = times.iat[i,0]
        end = times.iat[i+1,0]
        segment = 
        #need to find where the time section is equal to start and equal to end then submit just that section to dynamic cyclegenerastor


