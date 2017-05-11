from sklearn import decomposition
import numpy as np
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta





def pca(raw_data, auto_opt=True):

    stripped, preserved = preserve(full_data=raw_data)
    n_variables = stripped.shape[1]
    pca_temp = decomposition.PCA(n_components=n_variables)
    pca_temp.fit(stripped)