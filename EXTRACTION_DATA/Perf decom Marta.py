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


df10 = import_data_pondM#[(im
# port_data_pondM['Date']<"2021-12-03")]
df11 = df10[df10['Total']!=0]
df12 = df11.set_index('Date')
table = df12['Total']
df13 = table.fillna(0)
cumulative_ret = (df13+1).cumprod()

set = monthly_return.set_index('Date')
cumulative_plot = (set + 1).cumprod()
cumulative_plot.plot(linestyle = ':')
cumulative_ret.plot(label = 'Total',linestyle = '-', linewidth = 2.0)
plt.legend()
plt.show()