# MODULES
import numpy as np
import pandas as pd
import os
import glob
import sys

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

    print('Finished importing {} files..'.format(len(files)))

    return train, test, macro



