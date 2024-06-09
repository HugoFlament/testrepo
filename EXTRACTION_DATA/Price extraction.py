import numpy as np
import pandas as pd
import pandas_datareader as data
import matplotlib.pyplot as plt
import scipy.stats as ss
import openpyxl
import yfinance as yf
import pyodbc
from datetime import datetime

conn_str = ("Driver={SQL Server};"
                "Server=HAL9000;"
                "DATABASE=Finance_DEV;"
                "Trusted_Connection=yes;")

Date_D = "2024-01-01"
Date_A = datetime.today().strftime('%Y-%m-%d')

range_2020 = pd.date_range(Date_D,Date_A, freq="D")

# action = ['XLF','KRE','IXJ','QQQ','GLD', 'XLI', 'QCOM', 'CAP.PA', 'ZURN.SW']
action = ['KRE', 'GLD']
df = yf.download(action, Date_D, Date_A)
close_price = df["Adj Close"]
df2 = pd.DataFrame(close_price, index=range_2020)
df2 = df2.ffill().reset_index()
df2 = df2.fillna(0)
df2.to_excel("PRICE.xlsx", index=False)

df3 = pd.read_excel("PRICE.xlsx")
df3 = df3.rename(columns={'index':'date'})
df3['date'] = df3['date'].dt.strftime('%Y-%m-%d')
#df2 = df2.index.name = 'index'
#df2 = df2.reset_index(inplace=True, level=['DATE'])
#df2 = df2[['KRE', 'GLD']]


cnxn = pyodbc.connect(conn_str)
cursor = cnxn.cursor()
cols = ",".join([str(i) for i in df3.columns.tolist()])
sql = "DELETE FROM PRICE_LIST"
cursor.execute(sql)
cursor.commit()
sql = "INSERT INTO PRICE_LIST (" + cols + ") VALUES (?,?,?)"
cursor.executemany(sql, df3.values.tolist())
cursor.commit()

cursor.close()
del cursor
#print(len(df2))
#df2.to_excel('extraction.xlsx')

