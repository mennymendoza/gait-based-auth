import feature
import numpy as np
import pandas as pd
import random
import cycledetection
import sys

def showcasetest():
    traininguser1 = rf"./data-folders/training-data/1_PocketPhone_Accelerometer_(Samsung_S6) -training-data.csv"
    traininguser47 = rf"./data-folders/training-data/47_PocketPhone_Accelerometer_(Samsung_S6)-training-data.csv"
    traininguser52 = rf"./data-folders/training-data/52_PocketPhone_Accelerometer_(Samsung_S6)-training-data.csv"
    testinguser1 = rf"./data-folders/testing-data/1_PocketPhone_Accelerometer_(Samsung_S6) -testing-data.csv"
    testinguser47 = rf"./data-folders/testing-data/47_PocketPhone_Accelerometer_(Samsung_S6)-testing-data.csv"
    testinguser52 = rf"./data-folders/testing-data/52_PocketPhone_Accelerometer_(Samsung_S6)-testing-data.csv"
    print("Results for user 1 compared to user 1 = " + str(feature.authenticator(traininguser1,testinguser1,testinguser1)))
    print("Results for user 1 compared to user 47 = " + str(feature.authenticator(traininguser1,testinguser1,testinguser47)))
    print("Results for user 1 compared to user 52 = " + str(feature.authenticator(traininguser1,testinguser1,testinguser52)))
    print("Results for user 47 compared to user 47 = " + str(feature.authenticator(traininguser47,testinguser47,testinguser47)))
    print("Results for user 47 compared to user 1 = " + str(feature.authenticator(traininguser47,testinguser47,testinguser1)))
    print("Results for user 47 compared to user 52 = " + str(feature.authenticator(traininguser47,testinguser47,testinguser52)))
    print("Results for user 52 compared to user 52 = " + str(feature.authenticator(traininguser52,testinguser52,testinguser52)))
    print("Results for user 52 compared to user 1 = " + str(feature.authenticator(traininguser52,testinguser52,testinguser1)))
    print("Results for user 47 compared to user 47 = " + str(feature.authenticator(traininguser52,testinguser52,testinguser47)))

showcasetest() 



