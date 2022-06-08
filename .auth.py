import feature
import numpy as np
import pandas as pd
import random
import cycledetection
import sys


training = rf"./analysis-data/training-data/1_PocketPhone_Accelerometer_(Samsung_S6) -training-data.csv"
dittotest = rf"./analysis-data/testing-data/1_PocketPhone_Accelerometer_(Samsung_S6) -testing-data.csv"
test = rf"./analysis-data/testing-data/1_PocketPhone_Accelerometer_(Samsung_S6) -testing-data.csv"
print(feature.authenticator(training,dittotest,test))


def belmantest():
    traininguser1 = rf"./analysis-data/training-data/1_PocketPhone_Accelerometer_(Samsung_S6) -training-data.csv"
    dittotestuser1 = rf"./analysis-data/testing-data/1_PocketPhone_Accelerometer_(Samsung_S6) -testing-data.csv"
    selftest = rf"./analysis-data/testing-data/1_PocketPhone_Accelerometer_(Samsung_S6) -testing-data.csv"
    