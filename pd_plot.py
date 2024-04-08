import glob
import pandas as pd
#import numpy as np

#import matplotlib.pyplot as plt

filenames = sorted(glob.glob('test*.gdat'))
filenames = filenames[0:3]


for filename in filenames:
    data = pd.read_csv(filename,sep='\s+')
    data = data.drop(columns = 'C')
    newnames = data.columns[1:4]
    data.columns = newnames
    print(data)