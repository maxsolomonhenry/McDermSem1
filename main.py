"""
Data analysis TODO:

√   (1) Calculate correlations per subject, then average correlations.
√   (2) ALSO, average ratings across subjects, then computer correlations.
    e.g. AVERAGE ALL RATINGS between subjects, then computer one correlation.

√   (3) Do both spearman and pearson. In both cases, also do r**2.

    (4) Correlations between synthesis types (Orig <-> Spec, Orig <-> Stat, etc)

(5) how does this break down per stimulus?
       -   groups: orig, resynth, spectral (20 * 3 = 60 stimuli)
       -   for each stimulus, calculate correlation between resyntheses.
           (analysis level, statistical power not important at this juncture).
"""

import pandas as pd
from glob import glob
import os
import warnings


def average(tmp: pd.DataFrame) -> pd.DataFrame:
    """Average by index."""
    return tmp.groupby(tmp.index).mean()


if __name__ == '__main__':
    DATA_PATH = './data'
    data_ext = '*.csv'

    search_path = os.path.join(DATA_PATH, data_ext)
    filenames = glob(search_path)
    assert filenames, 'No files found matching pattern {}.'.format(
        os.path.abspath(search_path)
    )

    num_subjects = len(filenames)
    scales = ['Busy', 'Fused', 'Kaleidoscopic']
    correlation_type = ['pearson', 'spearman']

    # For correlations within participants (to be averaged later).
    orig_corr = {
        'pearson': pd.DataFrame(),
        'spearman': pd.DataFrame(),

    }
    stat_corr = {
        'pearson': pd.DataFrame(),
        'spearman': pd.DataFrame(),

    }
    spec_corr = {
        'pearson': pd.DataFrame(),
        'spearman': pd.DataFrame(),

    }

    # For average ratings across each stimulus (to be correlated later).
    orig_av, stat_av, spec_av = pd.DataFrame, pd.DataFrame, pd.DataFrame

    for i, file in enumerate(filenames):
        df = pd.read_csv(file)

        # Parse data with a warning message in first row.
        if df.columns.size == 1:
            warnings.warn(
                'File {} is flagged. Skipping first row...'.format(
                    os.path.basename(file)
                )
            )
            df = pd.read_csv(file, skiprows=1)

        orig = df[df['type'] == 'O'].reset_index(drop=True)
        stat = df[df['type'] == '32R'].reset_index(drop=True)
        spec = df[df['type'] == 'S'].reset_index(drop=True)

        if i == 0:
            orig_av = orig[scales]
            stat_av = stat[scales]
            spec_av = spec[scales]
        else:
            orig_av += orig
            stat_av += stat
            spec_av += spec

        for method in correlation_type:
            orig_corr[method] = orig_corr[method].append(
                orig[scales].corr(method=method)
            )
            stat_corr[method] = stat_corr[method].append(
                stat[scales].corr(method=method)
            )
            spec_corr[method] = spec_corr[method].append(
                spec[scales].corr(method=method)
            )

    # Calculate average.
    orig_av = orig_av / num_subjects
    stat_av = stat_av / num_subjects
    spec_av = spec_av / num_subjects

    orig_r, orig_r2, stat_r, stat_r2, spec_r, spec_r2 = (
        {}, {}, {}, {}, {}, {}
    )
    orig_av_r, orig_av_r2, stat_av_r, stat_av_r2, spec_av_r, spec_av_r2 = (
        {}, {}, {}, {}, {}, {}
    )

    for method in correlation_type:
        # Calculate correlation of average stimulus ratings across all subjects.
        orig_av_r[method] = orig_av[scales].corr(method=method)
        orig_av_r2[method] = orig_av_r[method]**2

        stat_av_r[method] = stat_av[scales].corr(method=method)
        stat_av_r2[method] = stat_av_r[method]**2

        spec_av_r[method] = spec_av[scales].corr(method=method)
        spec_av_r2[method] = spec_av_r[method]**2

        # Average the correlations calculated within subjects.
        orig_r[method] = average(orig_corr[method])
        orig_r2[method] = average(orig_corr[method]**2)

        stat_r[method] = average(stat_corr[method])
        stat_r2[method] = average(stat_corr[method]**2)

        spec_r[method] = average(spec_corr[method])
        spec_r2[method] = average(spec_corr[method]**2)

    print('\n\n======== Corr. within subject, then averaged ========')

    for method in correlation_type:
        print(f"\n------\nMethod:\t{method}\n------")

        print("\nOriginal excerpts")
        print("\nr:")
        print(orig_r[method])
        print("\nr2:")
        print(orig_r2[method])

        print("\nStatistical resynth")
        print("\nr:")
        print(stat_r[method])
        print("\nr2:")
        print(stat_r2[method])

        print("\nSpectrally matched noise")
        print("\nr:")
        print(spec_r[method])
        print("\nr2:")
        print(spec_r2[method])

    print('\n\n======== Average all ratings across subjects ========')

    for method in correlation_type:
        print(f"\n------\nMethod:\t{method}\n------")

        print("\nOriginal excerpts")
        print("\nr:")
        print(orig_av_r[method])
        print("\nr2:")
        print(orig_av_r2[method])

        print("\nStatistical resynth")
        print("\nr:")
        print(stat_av_r[method])
        print("\nr2:")
        print(stat_av_r2[method])

        print("\nSpectrally matched noise")
        print("\nr:")
        print(spec_av_r[method])
        print("\nr2:")
        print(spec_av_r2[method])

    # print('\nOriginal corr. Statistics')
    # print(orig[scales].corrwith(stat[scales], method=method))

    # print('\nOriginal corr. Spectral')
    # print(orig[scales].corrwith(spec[scales], method=method))

    # print('\nSpectral corr. Statistics')
    # print(stat[scales].corrwith(spec[scales], method=method))
