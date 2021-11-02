import os
import pandas as pd

def get_tic_list():
    for file in os.listdir():
        if 'tic_list' in file:
            tic_file = file
    df = pd.read_csv(tic_file, index_col=0)
    tic_list = df['0'].tolist()
    return tic_list

