
#File just to test stuff, don't expect anything to make sense here

from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np

raw_data = macro_data


def select_time_window(input, datecol='timestamp', lookback=48, max_date='2016-05-30'):

    date = list(input[datecol])

    latest = datetime.strptime(max_date, '%Y-%m-%d')
    earliest = latest - relativedelta(months=lookback)
    subset = np.zeros(len(date))

    for d in range(0, len(date)):
        try:
            if 'Timestamp' not in str(type(date[d])):
                date[d] = datetime.strptime(date[d], '%Y-%m-%d')

            if earliest < date[d] <= latest:
                subset[d] = 1

        except:
            print('Did not process line {}..'.format(d))
            continue

    input[datecol] = date
    input['in_range'] = subset.astype(bool)

    output = input[input['in_range']]
    output.drop('in_range', axis=1, inplace=True)

    return output

raw_data.shape # (2484, 100)

max_date='2016-05-30'

raw_data_trimmed = select_time_window(input=raw_data)

latest = datetime.strptime(max_date, '%Y-%m-%d')
earliest = latest - relativedelta(months=48)

datecol = 'timestamp'

date = list(raw_data[datecol])