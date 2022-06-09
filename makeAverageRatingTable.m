% Get average scale ratings.
%
% Author: Max Henry
% June 2022.
clc; clear;

DATA_DIR = "./data";

dirInfo = dir(fullfile(DATA_DIR, "*.csv"));

df = table;

for f = 1:length(dirInfo)

    fname = dirInfo(f).name;
    fpath = fullfile(DATA_DIR, fname);

    T = readtable(fpath);

    df = [df; T];

end

stats = grpstats(df, "stim", "mean", "DataVars", ["Fused", "Busy", "Kaleidoscopic"]);
stats = removevars(stats, {'GroupCount'});

writetable(stats, "meanScaleRatingsByStimulus.csv");