import pandas as pd
import openpyxl
import numpy as np
import matplotlib.pyplot as plt
from pandas_datareader import data
import matplotlib.colors as colors
from math import sqrt


import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import self as self
from matplotlib import cm as cm
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import wx.lib.pubsub

#stock_1 = input("Enter a stock name : ")
#stock_2 = input("Entaer a stock name : ")
#stock_3 = input("Enter a stock name : ")
#stock_4 = input("Enter a stock name : ")
#stock_5 = input("Enter a stock name : ")
action = ['QQQ','META','IXJ','XLP','KBWR','PDBC','DJP','XLF']
#action = ['QQQ','META','IXJ','XLI','EXI','XLP','IAK','KBWR','PDBC','DJP','XLF']
dat = data.DataReader (action, 'yahoo', start ="2018/12/01", end ="2022/09/27")

#pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', None)
table = dat["Close"]
print(table)

returns_daily = table.pct_change()
returns_annual = returns_daily.mean() * 250

cov_daily = returns_daily.cov()
cov_annual = cov_daily * 250

port_returns = []
port_volatility = []
stock_weights = []
sharpe_ratio = []


num_assets = len(action)
num_portfolios = 50000

np.random.seed(101)

for single_portfolio in range(num_portfolios):
    weights = np.random.random(num_assets)
    weights /= np.sum(weights)
    returns = np.dot(weights, returns_annual)
    volatility = np.sqrt(np.dot(weights.T, np.dot(cov_annual, weights)))
    sharpe = returns / volatility
    sharpe_ratio.append(sharpe)
    port_returns.append(returns)
    port_volatility.append(volatility)
    stock_weights.append(weights)

portfolio = {'Returns': port_returns,
             'Volatility': port_volatility,
             'Sharpe Ratio': sharpe_ratio}

for counter,symbol in enumerate(action):
    portfolio[symbol+' weight'] = [weight[counter] for weight in stock_weights]

df = pd.DataFrame(portfolio)
column_order = ['Returns', 'Volatility', 'Sharpe Ratio'] + [stock+' weight' for stock in action]
df = df[column_order]
df.to_excel('Test.xlsx')
print(df)

min_volatility = df['Volatility'].min()
max_sharpe = df['Sharpe Ratio'].max()
sharpe_portfolio = df.loc[df['Sharpe Ratio'] == max_sharpe]
min_variance_port = df.loc[df['Volatility'] == min_volatility]


plt.style.use('seaborn-dark')
df.plot.scatter(x='Volatility', y='Returns', c='Sharpe Ratio', cmap='RdYlGn', edgecolors='black', figsize=(10, 8), grid=True)
plt.scatter(x=sharpe_portfolio['Volatility'], y=sharpe_portfolio['Returns'], c='red', marker='D', s=200)
plt.scatter(x=min_variance_port['Volatility'], y=min_variance_port['Returns'], c='blue', marker='D', s=200 )
plt.xlabel('Volatility (Std. Deviation)')
plt.ylabel('Expected Returns')
plt.title('Efficient Frontier')
print(plt.show())