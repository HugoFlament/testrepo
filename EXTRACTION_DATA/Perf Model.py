import pandas
from pandas import  *
import numpy as np
from datetime import datetime
from dateutil.relativedelta import  relativedelta
import monthly_returns_heatmap as mrh
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import gridspec

#%%


import_data_bloom = pandas.read_excel('DataMarta.xlsx' ,sheet_name ='Sheet1' )
import_data_pond = pandas.read_excel('DataMarta.xlsx', sheet_name='Sheet2')

import_data_bloom.set_index('Date', inplace = True)
import_data_pond.set_index('Date', inplace =True)

import_data_bloomM = import_data_bloom.asfreq('M')
import_data_pondM = import_data_pond.asfreq('M')

monthly_return = import_data_bloomM.pct_change(1)

import_data_pondM.reset_index(inplace=True)
monthly_return.reset_index(inplace = True)

column_name = import_data_pondM.keys()
import_data_pondM['Total']= np.nan

print(monthly_return)
print(import_data_pondM)


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

print(import_data_pondM)

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


df1 = import_data_pondM#[(import_data_pondM['Date'] < '2022-01-01')]
df1.set_index('Date',inplace = True)
table = df1['Total']
table.drop(table.index[0:1], inplace = True)
df2 = table.iloc[::-1]

with pandas.option_context('display.max_rows',None,'display.max_columns', None):
    print(df2)

df5 = mrh.get(df2, eoy=True)
print(df5)
df3 = df5.iloc[::-1]
df10 = df3.reset_index()
df11 = df10[['Year','eoy']]
year = df11.set_index('Year')
mounth = df3.drop(columns=['eoy'])

fig = plt.figure(figsize=(18,14))
gs = gridspec.GridSpec(1, 2, width_ratios=[5, 1])
ax0 = plt.subplot(gs[0])
g1 = sns.heatmap(mounth, annot = True, cbar = False, cmap = 'RdYlGn', ax = ax0, fmt = '.2%', linecolor = 'black', linewidths=1.5, center = 0.00, vmin=-0.1, vmax=0.05, annot_kws =({'fontsize':12}))
g1.set(xlabel=None, ylabel=None)
g1.set_yticklabels(df10['Year'], rotation=0)

ax1 = plt.subplot(gs[1])
g2 = sns.heatmap(year, cbar = False, annot=True, cmap='RdYlGn', ax=ax1, fmt='.1%',vmax=0.2, linecolor = 'black', linewidths=1.5, center = 0.00, vmin=-0.1, annot_kws =({'fontsize':12}))
g2.set(xlabel=None, ylabel=None, yticklabels=[])
plt.tick_params(left=False)
plt.show()

