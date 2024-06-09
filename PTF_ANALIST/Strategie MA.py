import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import pandas_datareader as data
import openpyxl
from datetime import datetime
#plt.style.use('fivethirtyeight')


aapl = yf.download(['AAPL'], start ="2010-01-01", end ="2021-01-01")

#MA 30 day
aapl['MA10']= aapl['Close'].rolling(10).mean()
#print(aapl['MA30'])

#MA  day
aapl['MA60']= aapl['Close'].rolling(60).mean()
#print(aapl['MA100'])

#plt.show()

#New data frame

df = yf.download(['AAPL'], start ="2010-01-01", end ="2021-01-01")
df['AAPL']= df['Close']
df['MA10']= df['Close'].rolling(10).mean()
df['MA60']= df['Close'].rolling(60).mean()

#Create signal buy and sell

def buy_sell(df):
    sigPriceBuy=[]
    sigPriceSell=[]
    flag = -1
    for i in range(len(df)):
        if df['MA10'][i]>df['MA60'][i]:
            if flag != 1:
                sigPriceBuy.append(df['AAPL'][i])
                sigPriceSell.append(np.nan)
                flag = 1
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
        elif df['MA10'][i]<df['MA60'][i]:
            if flag != 0:
             sigPriceBuy.append(np.nan)
             sigPriceSell.append(df['AAPL'][i])
             flag = 0
            else :
             sigPriceBuy.append(np.nan)
             sigPriceSell.append(np.nan)
        else :
            sigPriceBuy.append(np.nan)
            sigPriceSell.append(np.nan)

    return(sigPriceBuy, sigPriceSell)

buy_sell= buy_sell(df)
df['Buy_Signal']= buy_sell[0]
df['Sell_Signal']= buy_sell[1]
df.to_excel('Test.xlsx')

#Strategy plot
plt.figure(figsize=(12.6, 4.6))
plt.plot(aapl['Close'], label = 'AAPL', alpha=0.35)
plt.plot(aapl['MA10'], label = 'MA10')
plt.plot(aapl['MA60'], label = 'MA60')
plt.scatter(df.index, df['Buy_Signal'], label = 'Buy', marker = '^', color ='green')
plt.scatter(df.index, df['Sell_Signal'], label = 'Sell', marker = 'v', color ='red')
plt.title('Apple Close Price History')
plt.xlabel('Jan. 01 2010 - Jan 01 2021')
plt.ylabel('Close price USD')
plt.legend(loc='upper left')
plt.show()



