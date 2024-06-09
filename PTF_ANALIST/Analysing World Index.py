import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import date

# https://towardsdatascience.com/analyzing-world-stock-indices-performance-in-python-610df6a578f

df_list = pd.read_html('https://finance.yahoo.com/world-indices/')
majorStockIdx = df_list[0]
majorStockIdx.head()

stock_list = []
for s in majorStockIdx.Symbol:
    tickerData = yf.Ticker(s)
    tickerDf1 = tickerData.history(period='1d', start='2010-1-1', end='2020-9-30')
    tickerDf1['ticker'] = s
    stock_list.append(tickerDf1)
msi = pd.concat(stock_list, axis=0)

region_idx = {'US & Canada': ['^GSPC', '^DJI', '^IXIC', '^RUT', '^GSPTSE'],
              'Latin America': ['^BVSP', '^MXX', '^IPSA'],
              'East Asia': ['^N225', '^HSI', '000001.SS', '399001.SZ', '^TWII', '^KS11'],
              'ASEAN & Oceania': ['^STI', '^JKSE', '^KLSE', '^AXJO', '^NZ50'],
              'South & West Asia': ['^BSESN', '^TA125.TA'],
              'Europe': ['^FTSE', '^GDAXI', '^FCHI', '^STOXX50E', '^N100', '^BFX']
              }


def getRegion(ticker):
    for k in region_idx.keys():
        if ticker in region_idx[k]:
            return k

msi['region'] = msi.ticker.apply(lambda x: getRegion(x))

ms2 = msi.reset_index()
begRef = ms2.loc[ms2['Date'] == '2010-01-04']
begRef.set_index('Date', inplace=True)


def retBegin(ticker, val):
    start_val = begRef.loc[begRef['ticker'] == ticker, 'Close']
    return (val / start_val - 1) * 100


msi['chBegin'] = msi.apply(lambda x: retBegin(x.ticker, x.Close), axis=1)

chBegin = msi.groupby(['Date', 'ticker'])['chBegin'].first().unstack()
chBegin = chBegin.fillna(method='bfill')


fig, axes = plt.subplots(3, 2, figsize=(12, 8), sharex=True)
pagoda = ["#965757", "#D67469", "#4E5A44", "#A1B482", '#EFE482', "#99BFCF"]  # for coloring
for i, k in enumerate(region_idx.keys()):
    ax = axes[int(i / 2), int(i % 2)]
    for j, t in enumerate(region_idx[k]):
        print(region_idx[k])
        ax.plot(chBegin.index, chBegin[t], marker='', linewidth=1, color=pagoda[j])
        ax.legend([t for t in region_idx[k]], loc='upper left', fontsize=7)
        ax.set_title(k, fontweight='bold')
fig.text(0.5, 0, "Year", ha="center", va="center", fontweight="bold")
fig.text(0, 0.5, "Price Change/Return (%)", ha="center", va="center", rotation=90, fontweight="bold")
fig.suptitle("Price Change/Return for Major Stock Indices based on 2010", fontweight="bold", y=1.05, fontsize=14)
fig.tight_layout()
plt.show()

lastDate = ms2.loc[ms2['Date'] == '2020-09-30'].reset_index().drop(['index'],axis=1)

def nearest(dates, dateRef):
    # Get the previous days before the reference date (dateRef)
    prevDate = dates[dates < dateRef]
    return prevDate[-1]  # return the last date


def getReturn(period, number, ticker, dt, val):
    # Subset the dataset by stock index
    df = msi.loc[msi.ticker == ticker].reset_index()
    # Get all business days
    existingDates = df['Date'].unique()

    # Get the past date on months or some periods before
    if period == 'Y':
        dtp = (pd.Timestamp(dt) - pd.DateOffset(years=number)).to_numpy()
    elif period == 'M':
        dtp = (pd.Timestamp(dt) - pd.DateOffset(months=number)).to_numpy()
    elif period == 'W':
        dtp = (pd.Timestamp(dt) - pd.DateOffset(weeks=number)).to_numpy()
    elif period == 'D':
        dtp = (pd.Timestamp(dt) - pd.DateOffset(days=number)).to_numpy()

    # check if the past Date was business day
    # if not, get the closest business day
    # then, return the price change

    if dtp in existingDates:
        return (val / df.loc[df.Date == dtp, "Close"].values[0] - 1) * 100
    else:
        closestDate = nearest(existingDates, dtp)
        return (val / df.loc[df.Date == closestDate, "Close"].values[0] - 1) * 100

lastDate['6MR'] = lastDate.apply(lambda r: getReturn('M', 6, r.ticker, r.Date, r.Close), axis =1)
lastDate['1YR'] = lastDate.apply(lambda r: getReturn('Y', 1, r.ticker, r.Date, r.Close), axis =1)
lastDate['3YR'] = lastDate.apply(lambda r: getReturn('Y', 3, r.ticker, r.Date, r.Close), axis =1)
lastDate['5YR'] = lastDate.apply(lambda r: getReturn('Y', 5, r.ticker, r.Date, r.Close), axis =1)
lastDate['10YR'] = lastDate.apply(lambda r: getReturn('Y', 10, r.ticker, r.Date, r.Close), axis =1)

fig, axes = plt.subplots(1,5, figsize=(20, 10),sharey=True)
width = 0.75
cols = ['6MR','1YR','3YR', '5YR', '10YR']
for i, j in enumerate(cols):
    ax = axes[i]
    tick = lastDate.ticker.apply(lambda t : ticker[t])
    ax.barh(tick,lastDate[j], width, color = pagoda[i])
    ax.set_title(j, fontweight ="bold")
    ax.invert_yaxis()
fig.text(0.5,0, "Return (%)", ha="center", va="center", fontweight ="bold")
fig.text(0,0.5, "Stock Indices", ha="center", va="center", rotation=90, fontweight ="bold")
fig.suptitle("Returns for Major Stock Indices based on 30 September", fontweight ="bold",y=1.03, fontsize=14)
fig.tight_layout()
plt.show()