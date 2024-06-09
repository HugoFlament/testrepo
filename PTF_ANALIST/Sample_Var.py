import pandas as pd
import numpy as np
import pandas_datareader as data
from scipy.stats import norm
import matplotlib.pyplot as plt
import pylab

Fstsample = pd.DataFrame(np.random.normal(10, 5, size=30),dtype='float')
#print(Fstsample)
print("Mean sample is", Fstsample[0].mean())
print("Standard deviation is",Fstsample[0].std(ddof=1))

meanlist = []
for t in range(10000):
    sample = pd.DataFrame(np.random.normal(10, 5, size=30))
    meanlist.append(sample[0].mean())

collection = pd.DataFrame()
collection['meanlist'] = meanlist
collection['meanlist'].hist(bins=100, density=True,figsize=(15,8))

plt.show()
