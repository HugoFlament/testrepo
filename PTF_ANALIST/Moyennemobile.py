from pandas_datareader import data as df
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

# Define the instruments to download. We would like to see Apple, Microsoft and the S&P500 index.
tickers = ['AAPL', 'MSFT', '^GSPC']

# We would like all available data from 01/01/2000 until 12/31/2016.
start_date = '2015-01-01'
end_date = '2022-09-15'

# User pandas_reader.data.DataReader to load the desired data. As simple as that.
panel_data = yf.download(tickers, start_date, end_date)

#print(panel_data.to_frame().head(9))

close = panel_data['Close'].iloc[3:]

all_weekdays = pd.date_range(start=start_date, end=end_date, freq='B')
close = close.reindex(all_weekdays)
close = close.fillna(method='ffill')
print(all_weekdays)
print(close.head(10))
print(close.describe())


msft = close.loc[:, 'MSFT']

short_rolling_msft = msft.rolling(window=20).mean()
long_rolling_msft = msft.rolling(window=100).mean()

fig, ax = plt.subplots(figsize=(16,9))

ax.plot(msft.index, msft, label='MSFT')
ax.plot(short_rolling_msft.index, short_rolling_msft, label='20 days rolling')
ax.plot(long_rolling_msft.index, long_rolling_msft, label='100 days rolling')
ax.set_xlabel('Date')
ax.set_ylabel('Adjusted closing price ($)')
ax.legend()
print(plt.show())


