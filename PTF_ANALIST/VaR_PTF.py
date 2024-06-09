import numpy as np
import pandas as pd
import datetime as dt
import pandas_datareader as data
import matplotlib.pylab as plt
import openpyxl
import seaborn as sns
import statistics as sta
from scipy.stats import norm


def getData(stocks, start, end):
    stockData = data.DataReader(stocks, 'yahoo',  start='2019/03/14', end='2021/03/14')
    stockData = stockData['Close']
    returns = stockData.pct_change().apply(lambda x : np.log(1+x))
    meanReturns = returns.mean()
    covMatrix = returns.cov()
    return returns, meanReturns, covMatrix

def portfolioPerformance(weights, meanReturns, covMatrix, Time):
    returns = np.sum(meanReturns*weights)*Time
    std = np.sqrt(np.dot(weights, np.dot(covMatrix, weights)))*np.sqrt(Time)
    return returns, std

stocklist = ['QQQ','XLF','KRE','IXJ','XLI','DBC','MC.PA']
#stocks = [stock+'.AX'for stock in stocklist]
#startDate = endDate - dt.timedelta(days=1000)

returns, meanReturns, covMatrix = getData(stocklist, start='2020/01/01', end='2022/11/12')
#returns = returns.dropna()
returns = returns.fillna(0)

#weights = np.random.random(len(returns.columns))
weights = [0.259,0.089,0.059,0.148,0.074,0.111,0.259]
#weights /= np.sum(weights)

returns['Portfolio'] = returns.dot(weights)

#returns.to_excel('Test.xlsx')

def historicalVaR(returns, alpha = 1):
    if isinstance(returns, pd.Series):
        return np.percentile(returns, alpha)

    elif isinstance(returns, pd.DataFrame):
        return returns.aggregate(historicalVaR, alpha=alpha)

    else:
        raise TypeError("Expected returns to be dataframe or series")

print(historicalVaR(returns,alpha=1))

def historicalCVaR(returns, alpha=1):

    if isinstance(returns, pd.Series):
        belowVaR = returns <= historicalVaR(returns, alpha=alpha)
        return returns[belowVaR].mean()

    elif isinstance(returns, pd.DataFrame):
        return returns.aggregate(historicalCVaR, alpha=alpha)

    else:
        raise TypeError("Expected returns to be dataframe or series")

# 1 day
Time = 1

VaR = -historicalVaR(returns['Portfolio'], alpha=1)*np.sqrt(Time)
CVaR = -historicalCVaR(returns['Portfolio'], alpha=1)*np.sqrt(Time)
pRet, pStd = portfolioPerformance(weights, meanReturns, covMatrix, Time)
mu = returns['Portfolio'].mean()
#sigma = sta.variance(returns['Portfolio'])
sigma = returns['Portfolio'].std(ddof=1)


InitialInvestment = 5400
print('Expected Portfolio Return :     ', round(InitialInvestment*pRet,2))
print('Value at Risk 95th CI :    ', round(InitialInvestment*VaR,2))
print('% of portfolio:   ',(round(InitialInvestment*VaR,2))/InitialInvestment)
print('Conditional Var 95th CI :    ', round(InitialInvestment*CVaR,2))

#CI 95%

CI = norm.ppf(0.01, mu, sigma)
#print(CI)

#returns['Portfolio'].hist(bins = 100,density=True,figsize=(15,8)) #alpha=0.95)
#plt.axvline(CI, color='red')
sns.displot(returns['Portfolio'], kde=True)
plt.title('Daily Return')
plt.ylabel('Number of Observation')
plt.axvline(CI, color='red')
plt.show()
