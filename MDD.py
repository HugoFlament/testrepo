import pandas
import pandas as pd
from pandas import  *
import numpy as np
from datetime import datetime
from dateutil.relativedelta import  relativedelta
import monthly_returns_heatmap as mrh

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import gridspec

import_data_bloom = pandas.read_excel('DataMarta.xlsx' ,sheet_name ='Sheet1' )
import_data_pond = pandas.read_excel('DataMarta.xlsx', sheet_name='Sheet2')

import_data_bloom.set_index('Date', inplace = True)
import_data_pond.set_index('Date', inplace =True)

import_data_bloomM = import_data_bloom.asfreq('D')
import_data_pondM = import_data_pond.asfreq('D')

monthly_return = import_data_bloomM.pct_change(1)

import_data_pondM.reset_index(inplace=True)
monthly_return.reset_index(inplace = True)

column_name = import_data_pondM.keys()
import_data_pondM['Total']= np.nan

for index, row in import_data_pondM.iterrows():
    if isna(row[column_name[1]]):
        for x in column_name:
            if x !='Date' and x != 'Total':
                test2 = monthly_return.shape[0]
                if monthly_return.shape[0]-1 >= index:
                    import_data_pondM.at[index,x] = import_data_pondM.loc[index-1][x]*(1 + monthly_return.loc[index][x])
                    test3 = import_data_pondM.loc[index - 1][x] * (1 + monthly_return.loc[index][x])
                else :
                    break


for index, row in import_data_pondM.iterrows():
    if index == 0 :
        continue
    else :
        sum_tot = 0
        sum_pond = 0
        for x in column_name:
            if x != 'Date' and x != 'Total':
                if monthly_return.shape[0]-1 >= index:
                    if isna(monthly_return.loc[index][x]) or isna(import_data_pondM.loc[index-1][x]):
                        continue
                    else :
                        test1 = import_data_pondM.loc[index-1][x]
                        test2 = monthly_return.loc[index][x]
                        sum_tot = sum_tot + (import_data_pondM.loc[index -1][x]* monthly_return.loc[index][x])
                        sum_pond = sum_pond + import_data_pondM.loc[index -1][x]
                else:
                    break
        if sum_pond != 0:
            import_data_pondM.at[index, 'Total']=sum_tot / sum_pond

df10 = import_data_pondM#[(import_data_pondM['Date']<"2021-12-03")]
df11 = df10[df10['Total']!=0]
df12 = df11.set_index('Date')
table = df12['Total']
df13 = table.fillna(0)
cumulative_ret = (df13+1).cumprod()

r = cumulative_ret.reset_index()
ret = r['Total']

#--------------------------------------------------------MDD-----------------------------------------------------------
df = cumulative_ret
df.index=pd.to_datetime(df.index)

window = 252

# Calculate the max drawdown in the past window days for each day in the series.
Roll_Max = df.rolling(window, min_periods=1).max()
Daily_Drawdown =  df/Roll_Max - 1.0
Max_Daily_Drawdown = Daily_Drawdown.rolling(window, min_periods=1).min()

# Plot the results
Daily_Drawdown.plot()
Max_Daily_Drawdown.plot()
plt.show()

def calc_MDD(networth):
  df = pd.Series(networth, name="nw").to_frame()
  max_peaks_idx = df.nw.expanding(min_periods=1).apply(lambda x: x.argmax()).fillna(0).astype(int)
  df['max_peaks_idx'] = pd.Series(max_peaks_idx).to_frame()
  nw_peaks = pd.Series(df.nw.iloc[max_peaks_idx.values].values, index=df.nw.index)
  df['dd'] = ((df.nw-nw_peaks)/nw_peaks)
  df['mdd'] = df.groupby('max_peaks_idx')['dd'].transform(lambda x: x.expanding(min_periods=1).min()).fillna(0)
  return df

MDD = calc_MDD(df)

df8 = MDD.reset_index()
minvalue = df8.groupby(['max_peaks_idx'], sort=False)['mdd'].min().nsmallest(n=10)
mindate = df8.groupby(['max_peaks_idx'], sort=False)['Date'].min()
maxdate = df8.groupby(['max_peaks_idx'], sort=False)['Date'].max()
df9 = pd.DataFrame(minvalue).reset_index()
df10 = pd.DataFrame(mindate).reset_index()
df11 = pd.DataFrame(maxdate).reset_index()
df6 = df9.merge(df10, on ='max_peaks_idx')
df7 = df6.merge(df11, on ='max_peaks_idx')
df7['Période']=df7['Date_y']-df7['Date_x']

df12 = df7.set_axis(['IDX', 'MDD', 'Drop Date', 'Recovery Date', 'Nb days MDD'], axis=1, copy=False)
pd.options.display.float_format = '{:.2%}'.format
print(df12)