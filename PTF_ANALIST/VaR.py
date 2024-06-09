import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import pandas_datareader as data
from scipy.stats import norm

action = ['BYND','DPW.DE','GLD','ICLN','JJC', 'MCO', 'NOVN.SW', 'PLTR','QQQ', 'SLHN.SW', 'TPAY', 'VDC']
weight = [0.0597,0.0832,0.0675,0.0805,0.0739,0.0825,0.0585,0.1150,0.1152,0.0947,0.0849,0.0852]
df = data.DataReader(action, 'yahoo',  start ="2018/01/01", end ="2021/01/01")
ptf = df["Close"].pct_change().apply(lambda x : np.log(1+x))*weight
print(ptf)
ptf['Daily_return']=ptf.sum(axis=1)
mu = ptf['Daily_return'].mean()
sigma = ptf['Daily_return'].std(ddof=1)

mu220 = 220*mu
sigma220 = (220**0.5) * sigma
print('The probability of dropping over 40% in 220 days is ', norm.cdf(-0.4, mu220, sigma220))

drop20 = norm.cdf(-0.2, mu220,sigma220)
print('The probability of dropping over 20% in 220 days is ', drop20)

VaR = norm.ppf(0.05, mu, sigma)
print('Single day value at risk',VaR)

print('5% quantile', norm.ppf(0.05, mu, sigma))
print('95% quantile', norm.ppf(0.95, mu, sigma))