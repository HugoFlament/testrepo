
import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from pandas_datareader import data

#stock_1 = input("Enter a stock name : ")
#stock_2 = input("Enter a stock name : ")
#stock_3 = input("Enter a stock name : ")
#stock_4 = input("Enter a stock name : ")
#stock_5 = input("Enter a stock name : ")
action = ['TLT','IEI','GLD','HDG','SPY']


dat = yf.download(action, start ="2020-01-01", end ="2023-10-15")

table = dat["Adj Close"]
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
my_portfolios = 1

np.random.seed(101)

for multiple_portfolio in range(num_portfolios):
    weights = np.random.random(num_assets)
    weights /= np.sum(weights)
    returns = np.dot(weights, returns_annual)
    volatility = np.sqrt(np.dot(weights.T, np.dot(cov_annual, weights)))
    sharpe = returns / volatility
    sharpe_ratio.append(sharpe)
    port_returns.append(returns)
    port_volatility.append(volatility)
    stock_weights.append(weights)

for single_portfolio in range(my_portfolios):
    my_weights = [0.2,0.2,0.2,0.2,0.2]
    returns1 = np.dot(my_weights, returns_annual)
    vol = np.sqrt(np.dot(my_weights, np.dot(cov_annual, my_weights)))
    sharpe1 = returns1/vol
    sharpe_ratio.append(sharpe1)
    port_returns.append(returns1)
    port_volatility.append((vol))
    stock_weights.append(my_weights)

portfolio = {'Returns': port_returns,
             'Volatility': port_volatility,
             'Sharpe Ratio': sharpe_ratio}

for counter,symbol in enumerate(action):
    portfolio[symbol +' weight'] = [weight[counter] for weight in stock_weights]

df = pd.DataFrame(portfolio)
column_order = ['Returns', 'Volatility', 'Sharpe Ratio'] + [stock+' weight' for stock in action]
df = df[column_order]
df.to_excel('Test.xlsx')
print(df)

min_volatility = df['Volatility'].min()
max_sharpe = df['Sharpe Ratio'].max()
sharpe_portfolio = df.loc[df['Sharpe Ratio'] == max_sharpe]
min_variance_port = df.loc[df['Volatility'] == min_volatility]

plt.style.use('seaborn-deep')
df.plot.scatter(x='Volatility', y='Returns', c='Sharpe Ratio',
                cmap='RdYlGn', edgecolors='black', figsize=(10, 8), grid=True)
plt.scatter(x=sharpe_portfolio['Volatility'], y=sharpe_portfolio['Returns'], c='red', marker='D', s=200)
plt.scatter(x=min_variance_port['Volatility'], y=min_variance_port['Returns'], c='blue', marker='D', s=200)
plt.scatter(x=vol, y=returns1, c='yellow', marker='D', s=200)
plt.xlabel('Volatility (Std. Deviation)')
plt.ylabel('Expected Returns')
plt.title('Efficient Frontier')
print(plt.show())
