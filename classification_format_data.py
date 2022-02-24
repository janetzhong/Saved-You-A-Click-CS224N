# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 11:08:35 2022

@author: Janet
"""

"""
This script converts the manually labelled excel sheet to numpy/ pandas array
"""
from os.path import exists
import numpy as np
import pandas as pd

#convert labelled excel data to array
df = pd.read_excel('data/title_classification/data_label_qs.xlsx')
df=df[0:400]
dnp = df.to_numpy()
ind=0
#some minor errors in labelling, either'L' for list or nan, let these be summary questions
for entry in dnp[:,2]:
    if entry == 'Q':
        pass
    else:
        dnp[:,2][ind] = 'S'
    ind+=1
np.save('data/title_classification/datalabel_for_classification_numpy.npy', dnp)
pd.DataFrame(dnp, columns = ['titles','answer','QorS'])
df.to_pickle("data/title_classification/datalabel_for_classification_pandas.pkl")