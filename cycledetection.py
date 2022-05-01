"""
Dynamic cycle generation for gait based auth functions via selecting the midpoint of the data range then creating a range "N" around it. The data is then compared in equal length segments, finding the points with 
the lowest distances between them at any 2 corresponding indexes. Those distances and indexes are then logged accordingly and the mode is found in order to produce a most common cycle length
Should the mode produce a NAN the average is instead used

"""
import math
import numpy as np
import pandas as pd
from scipy import stats
#Constants
N = 100 #defines cycle range to search during dynamic cycle detection

def distance(y1,y2):
    d = np.sqrt((y2-y1)**2)
    return d

def handler(reference,window): #finds the euclidian distance between points at corresponding indexes and returns a list of the lowest distances
    holdvals = np.empty(0,int)
    mindistance = 0
    for i in range(0,len(window) - 1):
        temp = window[i]
        dist = float(distance(reference[0],temp[0]))
        for j in range(0,N-2):
            if (float(distance(reference[j],float(temp[j]))) < dist):
                dist = float(distance(reference[j],temp[j]))
                mindistance = j
        holdvals = np.append(holdvals,mindistance)
    return holdvals

def minfinder(arr): #finds the mode of data from handler function ie the index that which appears the most often
    minvals = np.empty(0,int)
    for i in range(0, len(arr) - 2):
        minvals = np.append(minvals,(N - 1 -(arr[i] - arr[i + 1])))
    mode = stats.mode(minvals)
    if pd.isna(mode[0]):
        return int(sum(minvals)/len(minvals))
    else:
        return int(mode[0])

def segmentation(df,clen): #segments entire dataframe into parts based on length given either via dynamic or user input 
    holder = pd.DataFrame(df,columns = ['Xvalue','Yvalue','Zvalue']).to_numpy()
    total = int(len(holder)/clen)
    na = np.array_split(holder,total)
    return na

def dynamcyclegenerator(file): #finds magnitude of y value in order for best accuracy then runs enttire segmentation pipeline 
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
def dynamcyclegenerator(dataframe): #runs entire process - only exists for polymorphism to be used with timecyclegenerator
    df = dataframe
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

def manualcyclegenerator(file,len): #generates cycle manually ignoring n value based on a predetermined user given cycle length
    df = pd.read_csv(rf'raw-data{file}.csv')
    return segmentation(df,len)


def timecyclegenerator(file,timestamps): #generates cycles given specific intervals that which to view, ie to correlate with events - accepts a .csv file of timestamps
    df = pd.read_csv(rf'raw-data/{file}.csv')
    times = pd.read_csv(rf'raw-data/{timestamps}.csv')
    frames = []
    for i in range(0,len(times) - 1):
        start_row = df.loc[df['time'] == times[i]]
        end_row = df.loc[df['time'] == times[i+1]]
        startEID = int(start_row['EID'])
        endEID = int(end_row['EID'])+1
        timeperiod = df[startEID:endEID]
        frames = frames.append(timeperiod)
        i = i + 1
    df = pd.concat(frames)
    dynamcyclegenerator(df)




