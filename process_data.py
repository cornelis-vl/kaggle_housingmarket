# MODULES
import pandas as pd
import numpy as np
import os
import glob
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta


__version__ = '0.2'
__author__ = 'CV'


# CLASSES AND FUNCTIONS
def import_data(location=False):
    if not location:
        location = input('> Where have you located the housingmarket folder?')
    MAIN_FOLDER = 'housingmarket'
    DESTINATION_FOLDER = 'data'
    data_folder = os.path.join(location, MAIN_FOLDER, DESTINATION_FOLDER)

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

    os.chdir(location)

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


def select_time_window(input, datecol='timestamp', lookback=48, max_date='2016-05-30'):

    date = list(input[datecol])

    for d in range(0, len(date)):
        try:
            date[d] = datetime.strptime(date[d], '%Y-%m-%d')
        except:
            continue

    input[datecol] = date

    latest = datetime.strptime(max_date, '%Y-%m-%d')
    earliest = latest - relativedelta(months=lookback)

    output = input[(input[datecol] <= latest) and input[datecol] > earliest]

    return output


def drop_nan_cols(raw_data, nan_rate=100):
    n_rows = raw_data.shape[0]
    cols_to_drop = []

    nan_threshold = int(float(nan_rate)/100 * n_rows)

    for col in raw_data.columns:
        if raw_data[col].isnull().values.sum() >= nan_threshold:
            cols_to_drop += [col]
            print('Dropping {}..'.format(col))

    print("Dropped {} columns in total that have more than {} NaN-values.".format(len(cols_to_drop), nan_threshold))

    output_data = raw_data.drop(cols_to_drop, axis=1, inplace=False)

    return output_data


def preserve(full_data, date_col='timestamp', additional=[]):
    if 'pandas.core.frame.DataFrame' not in str(type(full_data)):
        raw_data = pd.DataFrame(full_data)

    raw_data.set_index('timestamp', drop=False, inplace=True, verify_integrity=True)

    preserved_cols = [date_col]
    preserved_cols += additional

    preserved_data = raw_data[preserved_cols]
    stripped_data = raw_data.drop(preserved_cols, axis=1, inplace=False)

    return stripped_data, preserved_data