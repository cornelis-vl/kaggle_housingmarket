# MODULES
import pandas as pd
import numpy as np
import os
import glob


__version__ = '0.1'
__author__ = 'CV'


# CLASSES AND FUNCTIONS
def import_data():
    folder_location = input('> Where have you located the housingmarket folder?')
    MAIN_FOLDER = 'housingmarket'
    DESTINATION_FOLDER = 'data'
    data_folder = os.path.join(folder_location, MAIN_FOLDER, DESTINATION_FOLDER)

    os.chdir(data_folder)

    files = glob.glob1(data_folder, '*.csv')

    for f in files:
        if 'train' in f:
            train = pd.read_csv(f, sep=",", na_values='NA')
            print('Imported train file [{}]..'.format(train.shape))
        elif 'test' in f:
            test = pd.read_csv(f, sep=",", na_values='NA')
            print('Imported test file [{}]..'.format(test.shape))
        else:
            macro = pd.read_csv(f, sep=",", na_values='NA')
            print('Imported macro file [{}]..'.format(macro.shape))

    print('Finished importing {} files.'.format(len(files)))

    os.chdir(folder_location)

    return train, test, macro


def structure_data(train, test, index='id'):

    if index in train.columns and index in test.columns:
        train_temp = train.set_index(index, drop=True)
        test_features = test.set_index(index, drop=True)
    else:
        raise ValueError('ID variable not found in both train and test set.')

    target_variable = list(set(train.columns) - set(test.columns))

    if len(target_variable) > 1:
        raise ValueError('The train and test set are not aligned.')

    train_target = train_temp[target_variable]
    train_features = train_temp.drop(labels=target_variable, axis=1)

    return train_target, train_features, test_features


def train_test_split(target, features, prop=0.7):
    rows = np.arange(0, target.shape[0])
    np.random.shuffle(rows)

    threshold = int(prop * len(rows))
    train_rows = rows[0:threshold]
    test_rows = rows[threshold:len(rows)]

    train_features = features[train_rows]
    test_features = features[test_rows]

    train_target = target[train_rows]
    test_target = target[test_rows]

    return train_features, test_features, train_target, test_target


def append_data(raw_data, to_append, match_key):
    appended_data = raw_data.merge(
        to_append,
        how='left',
        left_on=match_key,
        right_on=match_key,
        left_index=True,
        right_index=False,
        sort=True,
        suffixes=('_x', '_y'),
        copy=True,
        indicator=True)

    matched = len(appended_data[appended_data["_merge"] == "both"])
    size_full = raw_data.shape[0]

    match_rate = np.round(100 * float(matched) / size_full, 1)

    print("Achieved matching rate: {} pct.".format(match_rate))

    return appended_data