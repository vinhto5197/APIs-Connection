import pandas as pd 
import numpy as np

x = pd.read_csv("Dummy_Data.csv") # reading in sample data
df = x.iloc[:, 1:] # time series, sparing the dates column

# backend data engineering function to feed to cloud model
def features_Azure(df):
    ### BACKEND CODE ###
    return df

def features_GCP(df):
    ### BACKEND CODE ###
    return df