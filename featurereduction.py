import numpy as np
import pandas as pd
from scipy import stats


def reduction(fts,rts):
    features = pd.read_csv(rf'raw-data/{fts}.csv')
    results = pd.read_csv(rf'raw-data/{rts}.csv')
    #compare each feature column to the results rows and pull a correlational r value, then return sorted numpy list of values highest at top
