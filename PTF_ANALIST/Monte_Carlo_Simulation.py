from pandas_datareader import data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean
import statistics as st
import scipy.stats as ss
import math as mt
from matplotlib.pyplot import figure
import pylab

stock_1 = input("Enter a stock name : ")
date_begin = input("Enter a begin date : ")
date_end = input("Enter a end date : ")

df = data.DataReader (stock_1, 'yahoo', start = date_begin, end = date_end)
price = df["Close"]
pylab.rcParams['figure.figsize'] = (10, 6)
df["Close"].plot(grid = True)
plt.show()

t_intervals = 15
iteraction = 10

ln = df["Close"].pct_change().apply(lambda x : np.log(1+x))
pylab.rcParams['figure.figsize'] = (10, 6)
ln.plot(grid=True)
plt.show()

u = ln.mean()
var = ln.var()
drift = u - (0.5 * var)
stdev = ln.std()
rdm = float(stdev) * ss.norm.ppf(np.random.rand(t_intervals,iteraction))

#Next_Price = price[date_end] + mt.exp(float(Random_value) + float(Drift))
#print("Next price: " + str(Next_Price))

#a = Next_Price + mt.exp(float(Random_value)+ float(Drift))
#exp = mt.exp(float(Random_value)+ float(Drift))

Daily_return = np.exp(drift + rdm)

S0 = price.iloc[-1]
price_list = np.zeros_like(Daily_return)
price_list[0] = S0

for t in range(1, t_intervals):
    price_list[t] = price_list[t - 1] * Daily_return[t]

pylab.rcParams['figure.figsize'] = (10, 6)
plt.figure()
plt.plot(price_list)
plt.show()
print(price_list)
