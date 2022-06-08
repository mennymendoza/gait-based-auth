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
COLUMN_NAMES = [f"{name}_{dim}" for dim in VECTOR_DIMS for name in FEATURE_NAMES]

# Functions

def get_anomaly_score(new_entry: np.ndarray, filepath: str, verbose=False) -> float:
    
    ''' Gets the anomaly score (AS) of the features of a single gait instance. '''

    # Unpack data from csv to numpy array
    df = pd.read_csv(filepath)
    training_examples = df.to_numpy()
    num_examples, num_features = training_examples.shape
    
    # Dump some data and do some input vetting.
    if len(new_entry) != num_features:
        print("Error: Entry length should match the number of features.")
        sys.exit()
    
    # Find the smallest euclidean between our entry and a training example.
    min_dist = np.amin(np.sqrt(np.sum((training_examples - new_entry)**2, axis=1)))

    # Calculate the mean and standard deviation of the training data
    all_nn_distances = np.zeros(num_examples)
    for index in range(num_examples):
        diff_matrix = np.sqrt(np.sum((training_examples - training_examples[index])**2, axis=1))
        diff_matrix = diff_matrix[diff_matrix != diff_matrix[index]]
        if (len(diff_matrix) != num_examples - 1):
            print("Simple fix failed. Issue with mean and standard deviation calculations.")
            sys.exit()
        all_nn_distances[index] = np.amin(diff_matrix)
    mean = all_nn_distances.mean()
    std_dev = all_nn_distances.std()

    # Take that smallest distance and find its z-score
    anomaly_score = (min_dist - mean) / std_dev
    
    # Dump data
    if verbose:
        print(f"min-dist {min_dist} M: {mean} SD: {std_dev} AS: {anomaly_score}")

    return anomaly_score

def get_filenames(target_directory: str):
    all_paths = []
    for _, _, files in os.walk(target_directory):
        for file in files:
            all_paths.append(file)
    return all_paths

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

# Builds feature datasets for all users in users list
def build_feature_dataset(segment_size: int, training_split: float=0.8) -> None:

    if not (0 < training_split < 1):
        print("Error: training_split not between 0 and 1.")
        return

    # Grabbing the file names of every file in raw-data
    all_paths = [path for path in get_filenames("./raw-data") if re.search("^[0-9]*_", path)]
    for path in all_paths:
        path = path[:-4] # removes the .csv part of the file
        print(path)
        segments = cycledetection.manualcyclegenerator(path, segment_size)
        gait_instances = np.array(list(map(extract_features, segments)))
        split_index = int(len(gait_instances) * training_split)
        training_data = gait_instances[:split_index]
        df_train = pd.DataFrame(training_data, columns=COLUMN_NAMES)
        df_train.to_csv(f"training-data/{path}-training-data.csv", index=False)
        testing_data = gait_instances[split_index:]
        df_test = pd.DataFrame(testing_data, columns=COLUMN_NAMES)
        df_test.to_csv(f"testing-data/{path}-testing-data.csv", index=False)

def df_build(path: str, user: str) -> pd.DataFrame:
    df = pd.read_csv(f"./testing-data/{path}", header=0)
    user_df = re.search("^[0-9]*_", path).group().replace("_", "")
    df["user"] = [user_df for _ in range(df.shape[0])]
    if user_df == user:
        df["label"] = np.ones(df.shape[0])
    else:
        df["label"] = np.zeros(df.shape[0])
    return df

# Wraps all data in testing labelled 1 for target user and 0 for not target user.
def build_label_file(target_user: str) -> None:
    
    if not isinstance(target_user, str):
        print("Target user should be string.")
        return

    # Grabbing the file names of every file in testing-data
    all_paths = get_filenames("./testing-data")

    # Grabs only the paths with the word Gyroscope in them
    gyro_data = [path for path in all_paths if re.search('Gyroscope', path)]
    
    # Turns all gyro paths into a list of DataFrames
    all_gyro_dfs = list(map(lambda p: df_build(p, target_user), gyro_data))
    gyro_df = pd.concat(all_gyro_dfs, axis=0) # Combines them into a single df
    gyro_df.to_csv(f"./labeled-data/{target_user}-gyro-labeled-data.csv") # Saves to csv

    # Grabs only the paths with the word Accelerometer in them
    accel_data = [path for path in all_paths if re.search('Accelerometer', path)]
    
    # Turns all accel paths into a list of DataFrames
    all_accel_dfs = list(map(lambda p: df_build(p, target_user), accel_data))
    accel_df = pd.concat(all_accel_dfs, axis=0) # Combines them into a single df
    accel_df.to_csv(f"./labeled-data/{target_user}-accel-labeled-data.csv") # Saves to csv

# Gets all csvs in labelled-data directory and saves corresponding correlation data into analysis-data
def build_corr_dataset() -> None:
    all_paths = [path for path in get_filenames("./labeled-data") if re.search("^[0-9]*-", path)]

    for path in all_paths:
        print(path)
        df = pd.read_csv(f"./labeled-data/{path}", header=0)
        path = path[:-4]
        corr_stats = []
        for feat in COLUMN_NAMES:
            paired_df = df[[feat, "label"]]
            corr_coef = paired_df.corr().to_numpy()[0][1]
            percentage = abs(corr_coef) * 100
            corr_stats.append((feat, corr_coef, percentage))
        df_corr = pd.DataFrame(corr_stats, columns=["feature", "correlation", "%"])
        df_corr.to_csv(f"./analysis-data/{path}-correlation.csv")

def setup():
    build_feature_dataset(300)
    test_path = rf"./testing-data/1_PocketPhone_Accelerometer_(Samsung_S6) -testing-data.csv"
    df = pd.read_csv(test_path)
    first_row = df.iloc[0].to_numpy()
    training_path = rf"./training-data/1_PocketPhone_Accelerometer_(Samsung_S6) -training-data.csv"
    print(get_anomaly_score(first_row, training_path))

def stdevgetter(training_path,test_path) -> float:
    build_feature_dataset(300)
    df = pd.read_csv(test_path)
    values = np.empty([len(df)],dtype = float)
    for which_row in range(len(df)):
        row = df.iloc[which_row].to_numpy()
        values[which_row] = (get_anomaly_score(row,training_path))
    stdev = np.std(values)
    return stdev

def authenticator(training_path,ditto_path,test_path) -> bool: 
    build_feature_dataset(300)
    df = pd.read_csv(test_path)
    anomscores = np.empty([len(df)],dtype = float)
    for which_row in range(len(df)):
        row = df.iloc[which_row].to_numpy()
        anomscores[which_row] = get_anomaly_score(row,training_path)
    average_score = np.average(anomscores)
    stdev = stdevgetter(training_path,ditto_path)
    stdev = stdev * 2.0
    if (average_score > stdev) or (average_score < (stdev*-1.0)): return 0
    else: return 1