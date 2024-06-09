from pandas_datareader import data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean

stock = input("Enter a stock name : ")

df = data.DataReader ([stock], 'yahoo', start ="2018/05/21", end ="2021/05/21")

sto = df["Close"]
expt = sto.resample('Y').last().pct_change()

expected = expt.mean()

sd = df["Close"].pct_change().apply(lambda x : np.log(1+x))
sd_mean = sd.mean()
sqd_sd = sd.apply(lambda x : ((x-sd_mean)**2), axis=1)
sum_sd = sqd_sd.sum()
var = sum_sd/sd.count()
daily_std = np.sqrt(var)
annual_std = daily_std*np.sqrt(250)

sharpe_ration = ((expected-0.01)/annual_std)
print(sharpe_ration)

