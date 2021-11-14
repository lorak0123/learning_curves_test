import math

import numpy as np, pandas as pd, random
from matplotlib import pyplot as plt
from sklearn.datasets import load_diabetes
from sklearn.metrics import mean_squared_error
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression
from sklearn.model_selection import RepeatedKFold
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from numpy import mean
from numpy import std
from scipy.stats import sem

plt.style.use('seaborn-whitegrid')

df = pd.DataFrame()
df['x'] = np.arange(-10, 10, 0.001)
df['y'] = df['x'].apply(lambda x: 2*x**3 - x**2 + x)/200

df2 = df.copy()
df2['y'] = df2['y'].apply(lambda x: x + x * (0.2 - random.random()*0.4))

df3 = pd.DataFrame()
df3['x'] = np.arange(-50000, 50000, 1)
df3['y'] = df3['x'].apply(lambda x: math.sin(x/100))

df4 = df3.copy()
df4['y'] = df4['y'].apply(lambda x: x + x * (0.1 - random.random()*0.05))


def my_cross_val_score(Model, data, n_samples=100, n_repeats=10):
    test_scores = []
    train_scores = []

    for x in range(0, n_repeats):
        model = Model(max_depth=400)

        shuffled = data.sample(n_samples)
        splited = np.array_split(shuffled, 2)

        train_X = splited[0][['x']]
        train_y = splited[0]['y']

        test_X = splited[1][['x']]
        test_y = splited[1]['y']

        model.fit(train_X, train_y)

        test = model.predict(test_X)
        train = model.predict(train_X)

        test_scores.append(mean_squared_error(test_y, test))
        train_scores.append(mean_squared_error(train_y, train))

    return {
        "test": mean(test_scores),
        "train": mean(train_scores)
    }


def test_model(X, y):
    regressor = KNeighborsRegressor()

    cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
    # cv = KFold(n_splits=10, random_state=1, shuffle=True)
    scores = cross_val_score(regressor, X, y, cv=cv)

    print('Accuracy: %.3f (%.3f)' % (mean(scores), std(scores)))


scores = pd.DataFrame()

# for samples in [10, 14, 16, 20, 30, 50, 100, 200, 300, 400, 500, 600, 800, 1000, 1500, 2000, 5000, 10000]:
for samples in [50, 100, 200, 300, 400, 500, 600, 800, 1000, 1500, 2000, 5000, 10000, 20000]:
    cross_val = my_cross_val_score(DecisionTreeRegressor, df3, n_samples=samples, n_repeats=50)

    cross_val['n_samples'] = samples

    scores = scores.append(cross_val, ignore_index=True)
    print("done", samples)


print(scores)
ax = scores.plot(x='n_samples', y=['test', 'train'])
ax.set_ylabel("RMSE")
plt.show()
