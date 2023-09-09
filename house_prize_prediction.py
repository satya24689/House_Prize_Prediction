# -*- coding: utf-8 -*-
"""House Prize prediction

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dg6B4S1rO8Wh55CoW8L-Zpe1IzRGrdqt
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('housing.csv')

print(data)

data

data.info()

data.dropna(inplace=True)

data.info()

import sklearn.datasets
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn import metrics

X = data.drop(['median_house_value'],axis=1)
Y = data['median_house_value']

X_train ,X_test , Y_train , Y_test  = train_test_split(X,Y,test_size=0.2)

train_data = X_train.join(Y_train)

train_data

train_data.hist(figsize=(10,10))

train_data.corr()

plt.figure(figsize=(15,6))
sns.heatmap(train_data.corr(),annot=True,cmap='YlGnBu')

train_data['total_rooms'] =np.log(train_data['total_rooms'] + 1)
train_data['total_bedrooms'] =np.log(train_data['total_rooms'] + 1)
train_data['population'] =np.log(train_data['total_rooms'] + 1)
train_data['households'] =np.log(train_data['total_rooms'] + 1)

train_data.hist(figsize=(15,8))

train_data.ocean_proximity.value_counts()

train_data.join(pd.get_dummies(train_data.ocean_proximity)).drop(['ocean_proximity'], axis=1)

train_data

plt.figure(figsize=(15,10))
sns.heatmap(train_data.corr(),annot=True,cmap='YlGnBu')

plt.figure(figsize=(15,8))
sns.scatterplot(x='latitude',y ='longitude',data=train_data, hue="median_house_value",palette = "coolwarm")

train_data['bedroom_ratio'] = train_data['total_bedrooms'] / train_data['total_rooms']
train_data['household_rooms'] = train_data['total_rooms'] / train_data['households']

train_data = train_data.join(pd.get_dummies(train_data['ocean_proximity'])).drop(['ocean_proximity'], axis=1)

plt.figure(figsize=(15,8))
sns.heatmap(train_data.corr(),annot=True,cmap='YlGnBu')

from sklearn.linear_model import LinearRegression
X_train , Y_train = train_data.drop(['median_house_value'],axis=1), train_data['median_house_value']

reg = LinearRegression()

reg.fit(X_train,Y_train)

test_data = X_test.join(Y_test)
test_data['total_rooms'] =np.log(test_data['total_rooms'] + 1)
test_data['total_bedrooms'] =np.log(test_data['total_rooms'] + 1)
test_data['population'] =np.log(test_data['total_rooms'] + 1)
test_data['households'] =np.log(test_data['total_rooms'] + 1)
test_data = test_data.join(pd.get_dummies(test_data['ocean_proximity'])).drop(['ocean_proximity'], axis=1)
test_data['bedroom_ratio'] = test_data['total_bedrooms'] / test_data['total_rooms']
test_data['household_rooms'] = test_data['total_rooms'] / test_data['households']

X_test , Y_test = test_data.drop(['median_house_value'],axis=1), test_data['median_house_value']


reg.fit(X_test,Y_test)

reg.score(X_test,Y_test)

from sklearn.ensemble import RandomForestRegressor

forest = RandomForestRegressor()

forest.fit(X_train,Y_train)

forest.score(X_train,Y_train)

from sklearn.model_selection import GridSearchCV
forest = RandomForestRegressor()
param_grid = {
    "n_estimators":[3,10,30],
    "max_features":[2,4,6,8]
}

grid_search = GridSearchCV(forest , param_grid , cv=5, scoring="neg_mean_squared_error",
                           return_train_score=True)

grid_search.fit(X_train,Y_train)

best_forest = grid_search.best_estimator_

best_forest.score(X_train , Y_train)