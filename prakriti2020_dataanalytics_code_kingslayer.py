# -*- coding: utf-8 -*-
"""Prakriti2020_DataAnalytics_Code_KingSlayer.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ar6zrLuKtHmtzjH6r6yG16ghGjtb2stN
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import norm, skew, kurtosis
from scipy.special import boxcox1p

train = pd.read_excel("Data_set.xlsx")

train.head()

train = train.drop(columns=['Sample '])
train = train.drop([81]).reset_index(drop=True)

train.head()

y_C = train['TC (%)']
y_N = train['TN (%)']

y_C = y_C.values.tolist()
y_N = y_N.values.tolist()

sns.distplot(y_C , fit=norm);

(mu_C, sigma_C) = norm.fit(y_C)
print( '\n mu = {:.2f} and sigma = {:.2f}\n'.format(mu_C, sigma_C))

plt.legend(['Normal dist. ($\mu=$ {:.2f} and $\sigma=$ {:.2f} )'.format(mu_C, sigma_C)],
            loc='best')
plt.ylabel('Frequency')
plt.title('Carbon %')

fig = plt.figure()
res = stats.probplot(y_C, plot=plt)
plt.show()

sns.distplot(y_N , fit=norm);

(mu_N, sigma_N) = norm.fit(y_N)
print( '\n mu = {:.2f} and sigma = {:.2f}\n'.format(mu_N, sigma_N))

plt.legend(['Normal dist. ($\mu=$ {:.2f} and $\sigma=$ {:.2f} )'.format(mu_N, sigma_N)],
            loc='best')
plt.ylabel('Frequency')
plt.title('Nitrogen %')

fig = plt.figure()
res = stats.probplot(y_N, plot=plt)
plt.show()

y_cl = np.multiply(y_C,y_C)

y_nl = y_N

sns.distplot(y_cl , fit=norm);

(mu_cl, sigma_cl) = norm.fit(y_cl)
print( '\n mu = {:.2f} and sigma = {:.2f}\n'.format(mu_cl, sigma_cl))

plt.legend(['Normal dist. ($\mu=$ {:.2f} and $\sigma=$ {:.2f} )'.format(mu_cl, sigma_cl)],
            loc='best')
plt.ylabel('Frequency')
plt.title('Carbon %')

fig = plt.figure()
res = stats.probplot(y_cl, plot=plt)
plt.show()

print(skew(y_cl))
print(kurtosis(y_cl))

print(skew(y_nl))
print(kurtosis(y_nl))

train.drop(['TN (%)','TC (%)'],axis=1,inplace=True)

train.head()

numeric_feats = train.dtypes[train.dtypes != "object"].index

# Check the skew of all numerical features
skewed_feats = train[numeric_feats].apply(lambda x: skew(x.dropna())).sort_values(ascending=False)
print("\nSkew in numerical features: \n")
skewness = pd.DataFrame({'Skew' :skewed_feats})
skewness.head(10)

skewness.shape

skewness = skewness[abs(skewness) > 0.75]
print("There are {} skewed numerical features to Box Cox transform".format(skewness.shape[0]))
skewed_features = skewness.index
lam = 0.15
for feat in skewed_features:
    #all_data[feat] += 1
    train[feat] = boxcox1p(train[feat], lam)

train.head()

X_1 = train[['Zn','S','K','Ca','Ti','Mn','Fe','Rb','Sr','Al','Si']]
X_2 = train.drop(columns=['Zn','S','K','Ca','Ti','Mn','Fe','Rb','Sr','Al','Si'])

from sklearn.linear_model import ElasticNet, Lasso,  BayesianRidge, LassoLarsIC
from sklearn.ensemble import RandomForestRegressor,  GradientBoostingRegressor
from sklearn.kernel_ridge import KernelRidge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import RobustScaler
from sklearn.base import BaseEstimator, TransformerMixin, RegressorMixin, clone
from sklearn.model_selection import KFold, cross_val_score, train_test_split,cross_validate
from sklearn.metrics import mean_squared_error
import xgboost as xgb
import lightgbm as lgb
from sklearn.model_selection import train_test_split

n_folds = 3

def rmsle_cv(model,X,y):
    kf = KFold(n_folds, shuffle=True, random_state=42).get_n_splits(X.values)
    rmse= cross_validate(model, X.values, y, scoring="neg_mean_squared_error", cv = kf,return_train_score=True)
    return(rmse)

model_xgb_x1_cl = xgb.XGBRegressor(colsample_bytree=1, 
                             learning_rate=0.1, max_depth=3, 
                             n_estimators=10000,
                             objective='reg:squarederror',
                             subsample=0.0125, 
                             random_state =7)

score = rmsle_cv(model_xgb_x1_cl,X_1,y_cl)
print(np.sqrt(-score['train_score']))
print(np.sqrt(-score['test_score']))

model_xgb_x1_nl = xgb.XGBRegressor(colsample_bytree=0.1, 
                             learning_rate=0.1, max_depth=3, 
                             n_estimators=1000,
                             objective='reg:squarederror',
                             subsample=0.0085, 
                             random_state =7)

score = rmsle_cv(model_xgb_x1_nl,X_1,y_nl)
print(np.sqrt(-score['train_score']))
print(np.sqrt(-score['test_score']))

model_xgb_x2_cl = xgb.XGBRegressor(colsample_bytree=1, 
                             learning_rate=0.01, max_depth=3, 
                             n_estimators=500,
                             objective='reg:squarederror',
                             subsample=0.1, 
                             random_state =7)

score = rmsle_cv(model_xgb_x2_cl,X_2,y_cl)
print(np.sqrt(-score['train_score']))
print(np.sqrt(-score['test_score']))

model_xgb_x2_nl = xgb.XGBRegressor(colsample_bytree=1, 
                             learning_rate=0.02, max_depth=3, 
                             n_estimators=1000,
                             objective='reg:squarederror',
                             subsample=0.02, 
                             random_state =7)

score = rmsle_cv(model_xgb_x2_nl,X_2,y_nl)
print(np.sqrt(-score['train_score']))
print(np.sqrt(-score['test_score']))

model_xgb_train_cl = xgb.XGBRegressor(colsample_bytree=1, 
                             learning_rate=0.01, max_depth=3, 
                             n_estimators=500,
                             objective='reg:squarederror',
                             subsample=0.1, 
                             random_state =7)

score = rmsle_cv(model_xgb_train_cl,train,y_cl)
print(np.sqrt(-score['train_score']))
print(np.sqrt(-score['test_score']))

model_xgb_train_nl = xgb.XGBRegressor(colsample_bytree=1, 
                             learning_rate=0.01, max_depth=3, 
                             n_estimators=1000,
                             objective='reg:squarederror',
                             subsample=0.02, 
                             random_state =7)

score = rmsle_cv(model_xgb_train_nl,train,y_nl)
print(np.sqrt(-score['train_score']))
print(np.sqrt(-score['test_score']))

def rmsle(y, y_pred):
    return np.sqrt(mean_squared_error(y, y_pred))

model_xgb_x1_cl.fit(X_1, y_cl)
xgb_pred = model_xgb_x1_cl.predict(X_1)
print(rmsle(y_cl, xgb_pred))
print(rmsle(y_C,np.sqrt(xgb_pred)))

model_xgb_x2_cl.fit(X_2, y_cl)
xgb_pred = model_xgb_x2_cl.predict(X_2)
print(rmsle(y_cl, xgb_pred))
print(rmsle(y_C,np.sqrt(xgb_pred)))

model_xgb_train_cl.fit(train, y_cl)
xgb_pred = model_xgb_train_cl.predict(train)
print(rmsle(y_cl, xgb_pred))
print(rmsle(y_C,np.sqrt(xgb_pred)))

model_xgb_x1_nl.fit(X_1, y_nl)
xgb_pred = model_xgb_x1_nl.predict(X_1)
print(rmsle(y_nl, xgb_pred))

model_xgb_x2_nl.fit(X_2, y_nl)
xgb_pred = model_xgb_x2_nl.predict(X_2)
print(rmsle(y_nl, xgb_pred))

model_xgb_train_nl.fit(train, y_nl)
xgb_pred = model_xgb_train_nl.predict(train)
print(rmsle(y_nl, xgb_pred))

