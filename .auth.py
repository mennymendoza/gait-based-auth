import feature
import numpy as np
import pandas as pd
import random
import cycledetection
import sys


def setup():
    feature.build_feature_dataset(300)
    test_path = rf"./testing-data/1_PocketPhone_Accelerometer_(Samsung_S6) -testing-data.csv"
    df = pd.read_csv(test_path)
    first_row = df.iloc[0].to_numpy()
    training_path = rf"./training-data/1_PocketPhone_Accelerometer_(Samsung_S6) -training-data.csv"
    print(feature.get_anomaly_score(first_row, training_path))

def stdevgetter(training_path,test_path) -> float:
    feature.build_feature_dataset(300)
    df = pd.read_csv(test_path)
    values = np.empty([len(df)],dtype = float)
    for which_row in range(len(df)):
        row = df.iloc[which_row].to_numpy()
        values[which_row] = (feature.get_anomaly_score(row,training_path))
    stdev = np.std(values)
    return stdev

def authenticator(training_path,ditto_path,test_path) -> bool: 
    feature.build_feature_dataset(300)
    df = pd.read_csv(test_path)
    anomscores = np.empty([len(df)],dtype = float)
    for which_row in range(len(df)):
        row = df.iloc[which_row].to_numpy()
        anomscores[which_row] = feature.get_anomaly_score(row,training_path)
    average_score = np.average(anomscores)
    stdev = stdevgetter(training_path,ditto_path)
    stdev = stdev * 2.0
    if (average_score > stdev) or (average_score < (stdev*-1.0)): return 0
    else: return 1

    


training = rf"./analysis-data/training-data/1_PocketPhone_Accelerometer_(Samsung_S6) -training-data.csv"
dittotest = rf"./analysis-data/testing-data/1_PocketPhone_Accelerometer_(Samsung_S6) -testing-data.csv"
test = rf"./analysis-data/testing-data/1_PocketPhone_Accelerometer_(Samsung_S6) -testing-data.csv"
print(authenticator(training,dittotest,test))
