from pandas_datareader import data
import pandas as pd
import random


stock_1 = input("Enter a stock name : ")
stock_2 = input("Enter a stock name : ")
stock_3 = input("Enter a stock name : ")
stock = stock_1, stock_2, stock_3

df = data.DataReader ([stock_1, stock_2, stock_3], 'yahoo', start ="2017/01/01", end ="2020/03/21")

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
table = df["Close"]

expt = table.resample('Y').last().pct_change()
return_mean = expt.mean()



