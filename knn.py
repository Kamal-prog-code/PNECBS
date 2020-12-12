import pickle
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn import neighbors

df = pd.read_csv('media/demo.csv')
df = df.replace("Not_found",np.NaN)
nu_F = df.iloc[:,3:].columns
for i in nu_F:
    df[i] = df[i].astype(str).astype(float)

ls = []
ls_min = []
for i in df['S.no']:
    req_q = df[df['S.no']==i].drop(df.columns[df.apply(lambda col: col.isnull().sum()>=1)], axis=1)
    req_q = req_q.drop(['S.no','item','Description'],axis=1)
    mode_req = req_q.mode(axis=1)
    min_req = req_q.min(axis=1)

    ls_min.append(min_req)
    ls.append(mode_req[0].values[0])
df['Mode'] = ls
df['Min'] = ls_min
df.sort_values(by=['Mode'])
df = df.drop(['S.no'],axis=1)
df['item_copy'] = df['item']
df['Description_copy'] = df['Description']

labels_ordered=df.groupby(['Description'])['Mode'].mean().sort_values().index
labels_ordered={k:i for i,k in enumerate(labels_ordered,0)}
df['Description']=df['Description'].map(labels_ordered)
temp = {}
for i,j in enumerate(df['item']):
    temp.setdefault(j,i)
L = []
for i,j in temp.items():
    L.append(i)

dic = {}
for i in range(0,len(L)):
    dic.setdefault(L[i],i)
df['item']=df['item'].map(dic)

dataset = df.drop(['Cost_Amazon','Cost_MI','Cost_flipkart','Cost_RelianceDigital','Cost_Apple'],axis=1)
req_df = dataset.iloc[:,0:3]
X_col = req_df.iloc[:,0:2].columns
X = req_df[X_col].values
Y = req_df['Mode'].values
X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.25)

scaler = MinMaxScaler(feature_range=(0, 1))
x_train_scaled = scaler.fit_transform(X_train)
X_train = pd.DataFrame(x_train_scaled)
x_test_scaled = scaler.fit_transform(X_test)
X_test = pd.DataFrame(x_test_scaled)

params = {'n_neighbors':[1,2]}
knn = neighbors.KNeighborsRegressor()
model = GridSearchCV(knn, params, cv=3)
model.fit(X_train,Y_train)
req_K = model.best_params_['n_neighbors']

model = neighbors.KNeighborsRegressor(n_neighbors = req_K)
model.fit(X_train, Y_train) 

dlist = [model,df]

save_path = 'prediction/'
completeName = os.path.join(save_path, "costknn.pkl")         
pickle.dump(dlist, open(completeName, 'wb'))