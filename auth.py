import feature
import numpy as np
import pandas as pd
import random
import cycledetection
import sys

feature.build_feature_dataset(300)
test_path = "./testing-data/1_HandPhone_Accelerometer_(Samsung_S6)-testing-data.csv"
df = pd.read_csv(test_path)
first_row = df.iloc[0].to_numpy()
training_path = "./training-data/1_HandPhone_Accelerometer_(Samsung_S6)-training-data.csv"
print(feature.get_anomaly_score(first_row, training_path))
