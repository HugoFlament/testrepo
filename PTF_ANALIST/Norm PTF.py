import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import pandas_datareader as data
from scipy.stats import norm

action = ['QQQ','XLF','KRE','IXJ','XLI','DBC','MC.PA']
weight = [0.259,0.089,0.059,0.148,0.074,0.111,0.259]
df = data.DataReader(action, 'yahoo',  start ='2020/01/01', end ="2022/11/14")
#ptf = df["Close"].pct_change().apply(lambda x : np.log(1+x))
ptf = df["Close"].pct_change().apply(lambda x : np.log(1+x))*weight
ptf = ptf.fillna(0)
ptf['Daily_return']=ptf.sum(axis=1)
print(ptf)
mu = ptf['Daily_return'].mean()
sigma = ptf['Daily_return'].std(ddof=1)
ptf['Daily_return'].hist(bins=100, density=True, figsize=(15,8))
plt.title('Daily Return')
plt.ylabel('Number of Observation')
plt.xlabel('Return')
plt.savefig('Daily Return.png')
plt.show()

print('Perf daily is ', mu)
print('Standard deviation is',sigma)

prob_retunr1 = norm.cdf(-0.05, mu, sigma)
print('Tre Probability that the stock price will drop over 5% in a day', prob_retunr1)

