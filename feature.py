import numpy as np
import pandas as pd
import os
import re
import cycledetection
import sys

# Constants

FEATURE_NAMES = ["iqr",
        "duration",
        "median",
        "mad",
        "max",
        "mean",
        "min",
        "rms",
        "std"]
VECTOR_DIMS = [
    "x",
    "y",
    "z",
    "m"
]
USERS = ["1", "47", "48", "49", "50", "51", "52", "83", "84", "85"]

# Functions

def extract_features(data: np.ndarray):

    ''' Takes as input a 2D numpy array. Extracts the features of the data and outputs a gait instance.'''

    data = data.transpose()

    # Calculates magnitude vectors
    m = np.sqrt(np.sum(np.power(data, 2), axis=0, keepdims=True))
    data = np.append(data, m, axis=0)

    # Gets final dimensions of data
    vector_size, duration = data.shape

    # Extracts features from transposed vectors
    # AAV, AC_C1, AC_C2, AC_DP1, AC_DP2
    q3, q1 = np.percentile(data, [75, 25], axis=1, keepdims=True) # Quartile calculation for IQR
    iqr_feature = q3 - q1
    duration_feature = np.ones((vector_size, 1)) * duration
    # kurtosis:
    median_feature = np.median(data, axis=1, keepdims=True)
    mad_feature = np.median(np.absolute(data - median_feature), axis=1, keepdims=True)
    max_feature = np.max(data, axis=1, keepdims=True)
    # MCR: https://stackoverflow.com/questions/57501852/how-to-calculating-zero-crossing-rate-zcr-mean-crossing-rate-mcr-in-an-arr
    mean_feature = np.mean(data, axis=1, keepdims=True)
    min_feature = np.min(data, axis=1, keepdims=True)
    # P2P:
    rms_feature = np.sqrt(np.mean(np.power(data, 2), axis=1, keepdims=True))
    std_feature = np.std(data, axis=1, keepdims=True)
    # skewness:


    features = np.concatenate((
        iqr_feature,
        duration_feature,
        median_feature,
        mad_feature,
        max_feature,
        mean_feature,
        min_feature,
        rms_feature,
        std_feature
    ), axis=1).flatten()

    return features

def build_training_data(user: str, data: np.ndarray) -> None:
    gait_instances = np.array(list(map(extract_features, data)))
    column_names = [f"{name}_{dim}" for dim in VECTOR_DIMS for name in FEATURE_NAMES]
    df = pd.DataFrame(gait_instances, columns=column_names)
    df.to_csv(f"training-data/{user}-training-data.csv", index=False)

def build_feature_batch() -> None:

    # Grabbing the file names of every file in raw-data
    all_paths = []
    for _, _, files in os.walk("./raw-data"):
        for file in files:
            all_paths.append(file)
    
    # Building training data for each user.
    for u in USERS:
        user_data = [path for path in all_paths if re.search(f'^{u}.*\.csv$', path)]
        for f in user_data:
            f = f[:-4] # removes the .csv part of the file
            print(f)
            # build_training_data(f"{f}", cycledetection.cyclegenerator(f)) 
            segments = cycledetection.manualcyclegenerator(f, 300)
            gait_instances = np.array(list(map(extract_features, segments)))
            split_index = int(len(gait_instances) * 0.80)
            training_data = gait_instances[:split_index]
            column_names = [f"{name}_{dim}" for dim in VECTOR_DIMS for name in FEATURE_NAMES]
            df_train = pd.DataFrame(training_data, columns=column_names)
            df_train.to_csv(f"training-data/{f}-training-data.csv", index=False)
            testing_data = gait_instances[split_index:]
            df_test = pd.DataFrame(testing_data, columns=column_names)
            df_test.to_csv(f"testing-data/{f}-testing-data.csv", index=False)
    
    # Go into the testing directory and take all acceleration/gyroscopic data.
    # Mix all testing data into a big dataframe (along with the name of the user)
    # For each user, build a new data frame where THAT user is labeled true and any other user is labelled false.

def df_build(path: str, user: str) -> None:
    df = pd.read_csv(f"./testing-data/{path}", header=0)
    user_df = re.search("^[0-9]*_", path).group().replace("_", "")
    df["user"] = [user_df for _ in range(df.shape[0])]
    if user_df == user:
        df["label"] = np.ones(df.shape[0])
    else:
        df["label"] = np.zeros(df.shape[0])
    return df

def build_testing_file(users: list) -> None:
    
    if len(users) < 2:
        print("Not enough users to create a testing dataset.")
        return

    # Grabbing the file names of every file in raw-data
    all_paths = []
    for _, _, files in os.walk("./testing-data"):
        for file in files:
            all_paths.append(file)

    first_user = users[0]

    # Grabs only the paths with the word Gyroscope in them
    gyro_data = [path for path in all_paths if re.search('Gyroscope', path)]
    
    # Turns all gyro paths into a list of DataFrames
    all_gyro_dfs = list(map(lambda p: df_build(p, first_user), gyro_data))
    gyro_df = pd.concat(all_gyro_dfs, axis=0) # Combines them into a single df
    gyro_df.to_csv("./testing-data/all_gyro.csv") # Saves to csv

    # Grabs only the paths with the word Accelerometer in them
    accel_data = [path for path in all_paths if re.search('Accelerometer', path)]
    
    # Turns all accel paths into a list of DataFrames
    all_accel_dfs = list(map(lambda p: df_build(p, first_user), accel_data))
    accel_df = pd.concat(all_accel_dfs, axis=0) # Combines them into a single df
    accel_df.to_csv("./testing-data/all_accel.csv") # Saves to csv

# Testing

build_testing_file(USERS)