import pandas as pd

df = pd.read_csv('mergedata.csv')
print(df.head())

x = df.drop(['Unnamed: 0','pokemonid1', 'pokemonid2', 'winner'], axis=1)
y = df['winner']
print(x.head())
print(y.head())

from sklearn.model_selection import train_test_split
xtrain, xtest, ytrain, ytest = train_test_split(
    x, y,
    test_size = .1
)

from sklearn.linear_model import LogisticRegression
modelLogR = LogisticRegression(solver= 'liblinear', multi_class='auto')
modelLogR.fit(x, y)

print(modelLogR.score(xtest,ytest))

import joblib
joblib.dump(modelLogR, 'modelpokemon')
