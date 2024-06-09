import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import pandas_datareader as data
from scipy.stats import norm
from datetime import date
from dateutil.relativedelta import relativedelta

action = [input("Stock name : ")]
predict_day = float(input("Number of day to predict : "))
today_date = date.today()
three_year_date = date.today()-relativedelta(years=3)
df = data.DataReader(action, 'yahoo',  start =three_year_date, end =today_date)
#ptf = df["Close"].pct_change().apply(lambda x : np.log(1+x))
ptf = df["Close"].pct_change().apply(lambda x : np.log(1+x))
ptf = ptf.fillna(0)
ptf['Daily_return']=ptf.sum(axis=1)
#print(ptf)

mu = ptf['Daily_return'].mean()
sigma = ptf['Daily_return'].std(ddof=1)
ptf['Daily_return'].hist(bins=100, density=True, figsize=(15,8))
plt.title('Daily Return')
plt.ylabel('Number of Observation')
plt.xlabel('Return')
#plt.savefig('Daily Return.png')
#plt.show()

print('Perf daily is', mu)
print('Standard deviation is',sigma)

prob_retunr1 = norm.cdf(-0.05, mu, sigma)
print('Tre Probability that the stock price will drop over 5% in a day', prob_retunr1)

last_price = data.DataReader(action, 'yahoo',  start =today_date, end =today_date)
lp=last_price["Close"]
predict = (mu*predict_day*lp)+lp
print('Your prediction is')
print(predict)