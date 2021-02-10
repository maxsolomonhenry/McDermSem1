import pandas as pd
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
    method = 'spearman'

    orig, stat, spec = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    for file in filenames:
        df = pd.read_csv(file)

        orig = orig.append(df[df['type'] == 'O'])
        stat = stat.append(df[df['type'] == '32R'])
        spec = spec.append(df[df['type'] == 'S'])

    orig = orig.reset_index(drop=True)
    stat = stat.reset_index(drop=True)
    spec = spec.reset_index(drop=True)

    print('\nOriginal excerpts...')
    print(orig[scales].corr(method=method))

    print('\nStatistical resynth...')
    print(stat[scales].corr(method=method))

    print('\nSpectral resynth...')
    print(spec[scales].corr(method=method))

    print('\nOriginal corr. Statistics')
    print(orig[scales].corrwith(stat[scales], method=method))

    print('\nOriginal corr. Spectral')
    print(orig[scales].corrwith(spec[scales], method=method))

    print('\nSpectral corr. Statistics')
    print(stat[scales].corrwith(spec[scales], method=method))
