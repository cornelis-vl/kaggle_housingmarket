import process_data
import numpy as np
import pandas as pd
import os
from collections import Counter

train_full, submit_full, macro_data = process_data.import_data()

Ytrain, Xtrain, Xsubmit = process_data.structure_data(train=train_full, test=submit_full, index='id')
Xtrain_macro = process_data.append_data(raw_data=Xtrain, to_append=macro_data, match_key="timestamp")