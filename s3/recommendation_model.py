import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle

df=pd.read_csv('training_data.csv')
X=df[["age","gender"]]
y=df['genre']

model = LogisticRegression(max_iter=10000).fit(X, y)

pickle.dump (model,open('model.pkl','wb'))