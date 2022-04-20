import random
import pandas as pd
import numpy as np
import sys

def extract_features(data: np.ndarray) -> np.ndarray:

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
    ), axis=1)

    return features

# Testing

DATA_POINTS = 200
VECTOR_FEATURES = 3
NUM_SEGMENTS = 4

# Generate new random entry and tests AS function
sample_data = np.array([[[
    random.randrange(-10, 10)
    for _ in range(VECTOR_FEATURES)]
    for _ in range(DATA_POINTS)]
    for _ in range(NUM_SEGMENTS)]
)

print(extract_features(sample_data[0]))
