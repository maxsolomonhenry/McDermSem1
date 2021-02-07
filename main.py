import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from glob import glob
import os

if __name__ == '__main__':
    DATA_PATH = './data'
    data_ext = '*.csv'

    search_path = os.path.join(DATA_PATH, data_ext)
    filenames = glob(search_path)
    assert filenames, 'No files found matching pattern {}.'.format(
        os.path.abspath(search_path)
    )

    scales = ['Fused', 'Busy', 'Kaleidoscopic']

    for file in filenames:
        df = pd.read_csv(file)

        orig = df[df['type'] == 'O']
        stat = df[df['type'] == '32R']
        spec = df[df['type'] == 'S']

        print('\nOriginal excerpts...')
        print(orig[scales].corr())

        print('\nStatistical resynth...')
        print(stat[scales].corr())

        print('\nSpectral resynth...')
        print(spec[scales].corr())
