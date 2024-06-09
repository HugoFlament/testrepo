import numpy as np
#import pandas
from scikit import DecisionTreeRegressor
from scikit import LinearRegression
from scikit import train_test_split
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
import yfinance as yfin
#import openpyxl

yfin.pdr_override()
df = pdr.get_data_yahoo('SPY', start ="2015-09-09", end ="2022-04-23")
# df.shape => ligne et colonne

plt.figure(figsize=(16,8))
plt.title('SPY')
plt.xlabel('Days')
plt.ylabel('Close Price USD')
plt.plot(df['Close'])
plt.show()

df = df[['Close']]

#create a variable to predict 'x' days into the future

future_days = 15

#Create a new column => remonter de 25 tous les closes prices

df['Predict']=df[['Close']].shift(-future_days)
X = np.array(df.drop(['Predict'],1))[:-future_days]
#print(X)
y = np.array(df['Predict'])[:-future_days]
#print(y)

#Split the data into 75% training and 25 % testing

x_train, x_test, y_train , y_test = train_test_split(X,y,test_size=0.25)

tree = DecisionTreeRegressor().fit(x_train, y_train)
lr = LinearRegression().fit(x_train,y_train)

x_future = df.drop(['Predict'],1)[:-future_days]
x_future = x_future.tail(future_days)
x_future = np.array(x_future)
#print(x_future)

tree_predict = tree.predict(x_future)
print(tree_predict)

lr_predict = lr.predict(x_future)
print(lr_predict)

predictions = tree_predict
valid = df[X.shape[0]:]
valid['Predict']= predictions
plt.figure(figsize=(16,8))
plt.title('Model')
plt.xlabel('Days')
plt.ylabel('Close price USD')
plt.plot(df['Close'])
plt.plot(valid[['Close','Predict']])
plt.legend(['Orig', 'Val','Pred'])
plt.show()

predictionslr = lr_predict
valid = df[X.shape[0]:]
valid['Predict']= predictionslr
plt.figure(figsize=(16,8))
plt.title('Model')
plt.xlabel('Days')
plt.ylabel('Close price USD')
plt.plot(df['Close'])
plt.plot(valid[['Close','Predict']])
plt.legend(['Orig', 'Val','Pred'])
plt.show()